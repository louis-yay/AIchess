import os
import matplotlib.pyplot as plt
from constructor import constructNGRam

DIR = "data"
data = []

# NUMBER OF GAME
for file in sorted(os.listdir(DIR)):
        with open(DIR + "/" + file, "r", errors='ignore') as file:
            reader = file.read().split("\n\n")
            for i in range(1, len(reader), 2):
                data.append(reader[i])
        del reader


print(f"{len(data)} games on {len(os.listdir(DIR))} files with an average of {len(data)/len(os.listdir(DIR))}")


# AVERAGE MOVE PER GAME
for i in range(len(data)):
        # print(f'Extraction des coups: {round(i/len(data)*100)}%')
        
        data[i] = data[i].replace("\n", " ")
        data[i] = data[i].replace("+", "")      # Don't keep the chess note
        data[i] = data[i].replace("x", "")      # Don't keep take info
        data[i] = data[i].split(" ")
        while "" in data[i]:
            data[i].remove("")

total = 0
for game in data:
    for move in game:
         total += 1

print(f"{total/len(data)} moves in average")
del data


# TREE SIZE

def size(tree):
    if tree.getChilds() != {}:
        return 1 + sum([size(tree.getChilds()[elt]) for elt in tree.getChilds().keys()])
    return 1

print("1")
size1 = {}
for i in range(1000, 20001, 1000):
     print(i)
     size1[i] = size(constructNGRam("data", max=i, N=1))  

print("2")
size2 = {}
for i in range(1000, 20001, 1000):
     print(i)
     size2[i] = size(constructNGRam("data", max=i, N=2))  

print("3")
size3 = {}
for i in range(1000, 20001, 1000):
     print(i)
     size3[i] = size(constructNGRam("data", max=i, N=3))  

print("4")
size4 = {}
for i in range(1000, 20001, 1000):
     print(i)
     size4[i] = size(constructNGRam("data", max=i, N=4))  

print("5")
size5 = {}
for i in range(1000, 20001, 1000):
     print(i)
     size5[i] = size(constructNGRam("data", max=i, N=5))  

print("6")
size6 = {}
for i in range(1000, 20001, 1000):
     print(i)
     size6[i] = size(constructNGRam("data", max=i, N=6))  

plt.plot(size1.keys(), size1.values(), label="N=1")
plt.plot(size2.keys(), size2.values(), label="N=2")
plt.plot(size3.keys(), size3.values(), label="N=3")
plt.plot(size4.keys(), size4.values(), label="N=4")
plt.plot(size5.keys(), size5.values(), label="N=5")
plt.plot(size6.keys(), size6.values(), label="N=6")

plt.xlabel("Nombre de partie")
plt.ylabel("Taille du N-Gram")
plt.legend()

plt.show()
