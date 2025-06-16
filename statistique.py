import matplotlib.pyplot as plt
from Nconstructor import constructNGRam

size1 = {}
# size2 = {}
# size3 = {}
# size4 = {}

# analyse of size and nulber of combinaison found
for i in range(50, 10000, 100):
    print(i)
    Gram1 = constructNGRam("data", max=i, N=1)
#     Gram2 = constructNGRam("data", max=i, N=2)
#     Gram3 = constructNGRam("data", max=i, N=3)
#     Gram4 = constructNGRam("data", max=i, N=4)
    size1[i] = len(Gram1)
#     size2[i] = len(Gram2)
#     size3[i] = len(Gram3)
#     size4[i] = len(Gram4)
#     for key in Gram1.keys():
#         size1[i] += len(Gram1[key])
#     
#     for key in Gram2.keys():
#         size2[i] += len(Gram2[tuple(key)])
# 
#     for key in Gram3.keys():
#         size3[i] += len(Gram3[tuple(key)])
# 
#     for key in Gram4.keys():
#         size4[i] += len(Gram4[tuple(key)])
# 
# 
# 
plt.plot(size1.keys(), size1.values(), label="1-GRAM")
# plt.plot(size2.keys(), size2.values(), label="2-GRAM")
# plt.plot(size3.keys(), size3.values(), label="3-GRAM")
# plt.plot(size4.keys(), size4.values(), label="4-GRAM")
plt.ylabel('Nombre de coup trouvé')
plt.xlabel("Nombre de partie")

# Analyse of the size of the N-Gram for 1000 games, by the size of N
# data = {}
# 
# for i in range(1, 21):
#     print(i)
#     gram = constructNGRam("data", max=2000, N=i)
#     total = len(gram)
#     for key in gram.keys():
#         total += len(gram[key])
#     data[i] = total
# 
# plt.plot(data.keys(), data.values())
# plt.ylabel("Taille du N-Gram pour 2000 parties")
# plt.xlabel("N")
# plt.legend()
# 
plt.show()
