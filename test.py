import os

DIR = "data"
data = []

for file in sorted(os.listdir(DIR)):
        with open(DIR + "/" + file, "r", errors='ignore') as file:
            reader = file.read().split("\n\n")
            for i in range(1, len(reader), 2):
                data.append(reader[i])
        del reader


print(f"{len(data)} games on {len(os.listdir(DIR))} files with an average of {len(data)/len(os.listdir(DIR))}")

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