import pickle

def save(tree, path):
    print("Saving data...")
    with open(path, "wb") as output:
        pickle.dump(tree, output, pickle.HIGHEST_PROTOCOL)


def load(path):
    # TODO: Build 2 same tree, save and load one, check if there are the same.
    print("loading data...")
    with open(path, 'rb') as input:
        return pickle.load(input)

