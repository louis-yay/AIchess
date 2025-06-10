from Node import Node
from saving import save
from constructor import constructTree

for i in range(10, 201, 10):
    print(f"Tree N°{i}")
    tree = constructTree("data", max=i)
    save(tree, f"models/{i}PlayerTree.pkl")
    del tree
