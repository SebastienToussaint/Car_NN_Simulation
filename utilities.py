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

def process_data(filename, straight_buffer, smoothing_buffer, smoothing_mode = "delete"):
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

    # Removal of short straight blocks
    i = 0
    counter = 0
    start_of_straight_block = 0
    while i < len(answers):
        # If turning
        if answers[i] != 1:
            # Delete the straight block if the inputs
            # haven't been going straight for long enough
            if 0 < counter < straight_buffer:
                del answers[start_of_straight_block:i]
                del inputs[start_of_straight_block:i]
                i = start_of_straight_block
            counter = 0
        else:
            # Increase the length of the block by 1
            # and set start position if needed
            if counter == 0:
                start_of_straight_block = i

            counter += 1
        i += 1

    # Smoothing of data
    i = 0
    while i < len(answers) - smoothing_buffer:
        # If more than one unique value in the sublist
        if len(set(answers[i:i + smoothing_buffer])) > 1:
            if smoothing_mode == "delete":
                # Remove the whole block (except edges that are part of previous or next blocks
                lower = i
                upper = i + smoothing_buffer
                if i > 0:
                    # Check if beginning of sublist is part of the previous sequence
                    while answers[lower] == answers[i - 1]:
                        lower += 1

                if i + smoothing_buffer + 1 < len(answers):
                    # Check if end of sublist is part of the next sequence
                    while answers[upper] == answers[i + smoothing_buffer + 1]:
                        upper -= 1

                del answers[lower:upper + 1]
                del inputs[lower:upper + 1]
                i = lower
            elif smoothing_mode == "common":
                # Keep the datapoints that are part of the majority and remove the rest
                # Check if we're at a block boundary and there's 2 values in the block with similar counts
                values = answers[i:i + smoothing_buffer]
                unique_values = list(set(values))
                value_counts = {}
                for val in unique_values:
                    value_counts[val] = values.count(val)

                # Get the 2 most common values
                if len(value_counts) == 3:
                    # noinspection PyTypeChecker
                    # Remove the value with the lowest count from the list and replace it with the value with the highest count
                    lowest_count_output = (min(value_counts, key=value_counts.get))
                    value_counts.pop(lowest_count_output)
                    # noinspection PyTypeChecker
                    highest_count_output = max(value_counts, key=value_counts.get)

                    while lowest_count_output in values:
                        values[values.index(lowest_count_output)] = highest_count_output

                # NOTE: CURRENTLY STILL USES INITIAL VALUE COUNTS, DOESN'T TAKE INTO ACCOUNT VALUES FROM THE LOWEST COUNT THAT WERE
                # REPLACED WITH THE HIGHEST COUNT. DOING THIS TO REDUCE BIAS, MIGHT CHANGE LATER.

                # If similar number of each output in the list, keep both, otherwise replace everything with the most common
                difference = abs(list(value_counts.values())[0] - list(value_counts.values())[1])
                if difference > max(int(0.3 * smoothing_buffer), 1):
                    # Keep only the most common number
                    # noinspection PyTypeChecker
                    highest_count_output = max(value_counts, key=value_counts.get)
                    values = [highest_count_output] * len(values)

                answers[i:i + smoothing_buffer] = values
            else:
                pass
        else:
            i += smoothing_buffer

    print(f"Reduced data down from {initial_length} entries to {len(inputs)}")
    return inputs, answers