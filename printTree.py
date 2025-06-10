from saving import load
from Node import Node
from constructor import constructTree

tree = constructTree("data", max=100)

def display(tree, depth):
    if depth > 0:
        for elt in tree.getChilds().keys():
            print(depth*"    " + elt)
            display(tree.getChilds()[elt], depth-1)

display(tree, 2)