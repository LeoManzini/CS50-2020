from csv import reader, DictReader
from sys import argv, exit

if len(argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt")
    exit(1)

with open(argv[2]) as csv_file:
    csv_reader = reader(csv_file)
    for row in csv_reader:
        line_count = row

dna = line_count[0]
count = {}

with open(argv[1]) as test_file:
    people = reader(test_file)
    for row in people:
        sequence = row
        sequence.pop(0)
        break

for x in sequence:
    count[x] = 1

for y in count:
    size = len(y)
    major = 0
    compare = 0
    for i in range(len(dna)):
        while compare > 0:
            compare -= 1
            continue
        if dna[i: i + size] == y:
            while dna[i - size: i] == dna[i: i + size]:
                compare += 1
                i += size
            if compare > major:
                major = compare
    count[y] += major

with open(argv[1], newline='') as compair_file:
    compair = DictReader(compair_file)
    for people in compair:
        match = 0
        for dna in count:
            if count[dna] == int(people[dna]):
                match += 1
        if match == len(count):
            print(people['name'])
            exit(0)

print("No match")