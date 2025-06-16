import os
import matplotlib.pyplot as plt
from saving import save
from Nconstructor import constructNGRam
from treecontrustor import constructTree

def convert_bytes_to_MB(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    return round(num/(1024**2),2)


def file_size(file_path):
    """
    this function will return the file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes_to_MB(file_info.st_size)


gram1Size = {}
gram2Size = {}
gram3Size = {}
treeSize = {}

# analyse of size and nulber of combinaison found
for i in range(50, 5000, 100):
    print(i)

    # 1-Gram file size
    # Gram1 = constructNGRam("data", max=i, N=1)
    # save(Gram1, f"models/stat/gram{i}.pkl")
    gram1Size[i] = file_size(f"models/stat/gram{i}.pkl")

    # 2-Gram file size
    # Gram2 = constructNGRam("data", max=i, N=2)
    # save(Gram2, f"models/stat/2gram{i}.pkl")
    gram2Size[i] = file_size(f"models/stat/2gram{i}.pkl")

    # 3-Gram file size
    # Gram3 = constructNGRam("data", max=i, N=3)
    # save(Gram3, f"models/stat/3gram{i}.pkl")
    gram3Size[i] = file_size(f"models/stat/3gram{i}.pkl")

    # Tree file size
    # Tree = constructTree("data", max=i)
    # save(Tree, f"models/stat/tree{i}.pkl")
    treeSize[i] = file_size(f"models/stat/tree{i}.pkl")
    

plt.plot(gram1Size.keys(), gram1Size.values(), label="1-GRAM")
plt.plot(gram2Size.keys(), gram2Size.values(), label="2-GRAM")
plt.plot(gram3Size.keys(), gram3Size.values(), label="3-GRAM")
plt.plot(treeSize.keys(), treeSize.values(), label="TREE")
plt.ylabel('Taille en MB')
plt.xlabel("Nombre de partie")
plt.legend()


plt.show()
