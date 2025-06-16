import os
import matplotlib.pyplot as plt
from saving import save
from treecontrustor import constructTree

def depth(tree):
    if tree.getChilds() != {}:
        return 1 + sum([depth(tree.getChilds()[elt]) for elt in tree.getChilds().keys()])
    return 0

treeDepth = {}

treeDepth["sample1"] = depth(constructTree("sample", max=1000000))
treeDepth["sample2"] = depth(constructTree("sample2", max=1000000))
    

plt.plot(treeDepth.keys(), treeDepth.values(), label="TREE")
plt.ylabel('Taille')
plt.xlabel("Nombre de partie")
plt.legend()


plt.show()