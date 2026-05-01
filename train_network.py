import os.path
import pickle
import torch
from torch import nn
from sklearn.model_selection import train_test_split
from torchmetrics import Accuracy
import neural_network
import matplotlib.pyplot as plt
import utilities

# Device agnostics
device = "cuda" if torch.cuda.is_available() else "cpu"

# Process and retrieve data
inputs, answers = utilities.process_data("Data/SaveFiles/saved_data.pkl", 20, 10)

# Convert to tensors
inputs = torch.tensor(inputs, dtype=torch.float32)
answers = torch.tensor(answers, dtype=torch.long)

# Create test/train split
train_inputs, test_inputs, train_answers, test_answers = train_test_split(
    inputs,
    answers,
    test_size=0.2,
    random_state=73
)

# Load the model if a saved one exists,
# otherwise create a new one
if os.path.exists("Data/SaveFiles/saved_model.pkl"):
    with open("Data/SaveFiles/saved_model.pkl", "rb") as model_file:
        print("Loading saved model...")
        my_model = pickle.load(model_file)
        my_model.to(device)
else:
    print("Creating new model...")
    my_model = neural_network.CarModel(13, 3, 64)

# Loss function, optimizer and accuracy function

class_weights = torch.Tensor([4.0, 1.0, 4.0])
loss_fn = nn.CrossEntropyLoss(weight=class_weights)
optimizer = torch.optim.Adam(my_model.parameters(),
                            lr=0.001)
acc_fn = Accuracy("multiclass",
                  num_classes=3).to(device)

# Set seeds
torch.manual_seed(73)
torch.cuda.manual_seed(73)

# Set data and model to device
train_inputs = train_inputs.to(device)
train_answers = train_answers.to(device)
test_inputs = test_inputs.to(device)
test_answers = test_answers.to(device)
my_model.to(device)

# Store loss values
train_loss_list = []
test_loss_list = []

# Training loop
epochs = 3000
for epoch in range(epochs):
    my_model.train()

    # Make predictions
    train_logits = my_model(train_inputs)
    train_preds = torch.argmax(torch.softmax(train_logits, dim=1), dim=1)

    train_loss = loss_fn(train_logits, train_answers)
    train_acc = acc_fn(train_preds, train_answers)

    optimizer.zero_grad()

    train_loss.backward()

    optimizer.step()

    # Test loop
    my_model.eval()
    with torch.inference_mode():
        test_logits = my_model(test_inputs)
        test_preds = torch.argmax(torch.softmax(test_logits, dim=1), dim=1)

        test_loss = loss_fn(test_logits, test_answers)
        test_acc = acc_fn(test_preds, test_answers)

        # Keep record of the scores
        my_model.historical_scores.append(test_acc)
        if len(my_model.historical_scores) > 10000:
            print("Downsizing")
            my_model.downsize_scores(5000)


    train_loss_list.append(int(train_loss))
    test_loss_list.append(int(test_loss))

    # Print epoch info
    print(
        f"Epoch: {epoch} | Loss: {train_loss:.4f}, Acc: {train_acc*100:.2f}% | Test Loss: {test_loss:.4f}, Test Acc: {test_acc*100:.2f}%"
    )

# Save model
print("Saving model...")
with open("Data/SaveFiles/saved_model.pkl", "wb") as file:
    pickle.dump(my_model, file)


# Display score improvement graph
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.title("Test Accuracy")
plt.plot([i for i in range(len(my_model.historical_scores))], my_model.historical_scores)
plt.subplot(1, 2, 2)
plt.title("Train(red) and Test (blue) Losses (this training run)")
plt.plot([i for i in range(len(train_loss_list))], train_loss_list, "r--")
plt.plot([i for i in range(len(test_loss_list))], test_loss_list, "b--")
plt.show()
