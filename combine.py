from os import listdir

files = [x for x in listdir("txt") if ".txt" in x.lower() and 'P-3' not in x]

single = []

for file in files:
    with open("txt/" + file, "r", encoding="utf-8") as f:
        single.append(f.read())

with open("single.txt", "w", encoding="utf-8") as sf:
    sf.write("\n".join(single))


