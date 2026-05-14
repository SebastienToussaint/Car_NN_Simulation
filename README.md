A simple Neural Network Learning simulation.

Basic Concept:
- The user drives a car around a track while the car gathers data. The car contains a set of "distance sensors" (or lasers) which measure the distance to the nearest object in a given direction.
- While the user drives, the car keeps track of the distances being measured by each sensor, as well as the current keyboard of the driver. This way, the data essentially becomes an input set of distances with an output set of answers for the given inputs.
- This data is then passed on to a simple neural network for training via a supervised learning approach.
- The neural network will therefore learn the answers to a given input, and will be able to infer the answer to an input it hasn't seen yet based on it's training.
- Following training, the network will be able to automatically drive around the track in the style of the user (since the training was based on what the user would do in a given scenario).



Technical Details:
- Optimizer : Adam
- Loss function : Cross Entropy Loss
- Model size : 13 -> 64 -> 3 (with ReLU layers between each)
- Output weighting : [4, 0, 4]

