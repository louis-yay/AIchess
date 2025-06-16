import os
import matplotlib.pyplot as plt
from saving import save
from constructor import constructTree

def depth(tree):
    if tree.getChilds() != {}:
        return 1 + max([depth(tree.getChilds()[elt]) for elt in tree.getChilds().keys()])
    return 0

treeDepth = {}

# analyse of size and nulber of combinaison found
for i in range(1, 50, 1):
    print(i)
    treeDepth[i] = depth(constructTree("data", max=i))
    

plt.plot(treeDepth.keys(), treeDepth.values(), label="TREE")
plt.ylabel('Taille')
plt.xlabel("Nombre de partie")
plt.legend()


plt.show()
