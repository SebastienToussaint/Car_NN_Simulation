from torch import nn
import torch

# Construct model
class CarModel(nn.Module):
    def __init__(self, input_features, output_features, hidden_units):
        super().__init__()
        self.layer_stack = nn.Sequential(
            nn.Linear(input_features, hidden_units),
            nn.ReLU(),
            nn.Linear(hidden_units, hidden_units),
            nn.ReLU(),
            nn.Linear(hidden_units, output_features)
        )

        self.historical_scores = []

    def forward(self, x):
        return self.layer_stack(x)


    def get_answer(self, inputs):
        x = torch.tensor(inputs, dtype=torch.float32).unsqueeze(dim=0)

        self.eval()
        with torch.inference_mode():
            logits = self(x)
            prediction = torch.argmax(torch.softmax(logits, dim=1), dim=1)

        if prediction == 0:
            return "left"
        elif prediction == 1:
            return "forward"
        else:
            return "right"


    def downsize_scores(self, points_to_keep, mode = "even"):
        new_scores = []
        match mode:
            case "even":
                interval = int(len(self.historical_scores) / points_to_keep)

                for i in range(0, len(self.historical_scores), interval):
                    new_scores.append(self.historical_scores[i])

                self.historical_scores = new_scores

            case "latest":
                self.historical_scores = self.historical_scores[-points_to_keep:-1]

            case "biased":
                interval_end = int(len(self.historical_scores) - 0.5*points_to_keep)
                interval = int(interval_end / (0.5 * points_to_keep))

                for i in range(0, interval_end, interval):
                    new_scores.append(self.historical_scores[i])

                for i in range(interval_end, len(self.historical_scores)):
                    new_scores.append(self.historical_scores[i])

                self.historical_scores = new_scores

            case _:
                print("Error: Mode needs to be set to even, latest or biased\n"
                      "Using even as default")
                self.downsize_scores(points_to_keep)



