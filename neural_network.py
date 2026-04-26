from torch import nn
import torch

class CarModel(nn.Module):
    """
    A simple neural network model used to drive a car, where the inputs
    come from distance sensors mounted to the car that detect how close
    objects are.
    """
    def __init__(self, input_features, output_features, hidden_units):
        super().__init__()
        self.layer_stack = nn.Sequential(
            nn.Linear(input_features, hidden_units),
            nn.ReLU(),
            nn.Linear(hidden_units, hidden_units),
            nn.ReLU(),
            nn.Linear(hidden_units, output_features)
        )

        # Used to keep track of each generations
        # score throughout training
        self.historical_scores = []

    def forward(self, x):
        return self.layer_stack(x)


    def get_answer(self, inputs):
        """
        Retrieves the output of the model
        given a certain input
        """
        # Convert inputs to tensors
        x = torch.tensor(inputs, dtype=torch.float32).unsqueeze(dim=0)

        # Make prediction
        self.eval() # Remove this and just set model to eval at start of simulation?
        with torch.inference_mode():
            logits = self(x)
            prediction = torch.argmax(torch.softmax(logits, dim=1), dim=1)

        # Translate prediction
        if prediction == 0:
            return "left"
        elif prediction == 1:
            return "forward"
        else:
            return "right"


    def downsize_scores(self, points_to_keep, mode = "even"):
        """
        Used to reduce the number of historical scores kept,
        otherwise over many generations the length of the list
        gets too big and causes issues.
        3 modes of operation: even, latest, biased are
        used to determine which scores are kept.

        Even = An even distribution of all the scores are kept
        Latest = Only the latest points_to_keep scores are kept
        Biased = Half of points_to_keep of the latest scores are kept, and the
        remaining half of points_to_keep comes from an even distribution
        of the remaining scores.
        """
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



