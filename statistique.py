import matplotlib.pyplot as plt
from Nconstructor import constructNGRam

data = {}

for i in range(100, 5001, 100):
    print(i)
    Gram = constructNGRam("data", max=i, N=2)
    data[i] = len(Gram)
    # for key in Gram.keys():
    #     data[i] += len(Gram[key])

plt.close
plt.plot(data.keys(), data.values())
plt.ylabel('Nombre de combinaison')
plt.xlabel("Nombre de partie")

plt.show()
