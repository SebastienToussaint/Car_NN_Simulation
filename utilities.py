import pickle

class SaveDataStructure:
    def __init__(self):
        self.distances = []
        self.key_presses = []

    def write_to_file(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self, file)



def clean_data(filename, buffer):
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

    print(f"Reduced data down from {initial_length} entries to {len(inputs)}")
    return inputs, answers



