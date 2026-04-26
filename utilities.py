import pickle

class SaveDataStructure:
    """
    Structure used to store the
    gathered data produced by the car
    """
    def __init__(self):
        self.distances = []
        self.key_presses = []

    def write_to_file(self, filename):
        """
        Save the object using the pickle module
        """
        with open(filename, "wb") as file:
            pickle.dump(self, file)



def process_data(filename, buffer):
    """
    A function used to process and reduce noise in the data.
    Goes through the given .pkl data file, extracts the inputs
    and their associated outputs and removes some
    noise. Noise is determined by areas of outputs where
    there's a lot of variation. The buffer is used as
    the number of values that need to be the same in a row
    to keep that segment of data. Also checks if a segment
    that is about to be removed has sections that are part
    of the surrounding block and keeps them.
    Also filters super close distance values and sets a floor,
    in case the training data contains inputs that lead to hitting
    a wall, which would bias the model and incorrectly make it think
    that getting too close to a wall is acceptable
    """
    with open(filename, "rb") as file:
        data_object = pickle.load(file)

    inputs = data_object.distances.copy()
    answers = []

    initial_length = len(inputs)

    # Answer key -> left = 0, forward = 1, right = 2
    for key_presses in data_object.key_presses:
        if key_presses["left"] and key_presses["right"]:
            answers.append(1)
        elif key_presses["left"]:
            answers.append(0)
        elif key_presses["right"]:
            answers.append(2)
        else:
            answers.append(1)

    i = 0
    while i < len(answers) - buffer:
        # If more than one unique value in the sublist
        if len(set(answers[i:i+buffer])) > 1:

            lower = i
            upper = i + buffer
            if i > 0:
                # Check if beginning of sublist is part of the previous sequence
                while answers[lower] == answers[i-1]:

                    lower += 1

            if i + buffer + 1 < len(answers):
                # Check if end of sublist is part of the next sequence
                while answers[upper] == answers[i +buffer + 1]:

                    upper -= 1

            del answers[lower:upper+1]
            del inputs[lower:upper+1]
            i = lower
        else:
            i += buffer

    while i < len(answers):
        for j, dist in enumerate(inputs[i]):
            if dist <= 40:
                inputs[i][j] = 40

        i += 1

    print(f"Reduced data down from {initial_length} entries to {len(inputs)}")
    return inputs, answers



