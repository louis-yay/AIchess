import pickle
import Node

def save(tree, path):
    print("Saving data...")
    with open(path, "wb") as output:
        pickle.dump(tree, output, pickle.HIGHEST_PROTOCOL)


def load(path):
    print("loading data...")
    with open(path, 'rb') as input:
        return pickle.load(input)

