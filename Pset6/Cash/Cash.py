from cs50 import get_float

while True:
    change = get_float("Enter with the money value: ")
    if change >= 0:
        break

change *= 100
counter = 0

while change - 25 >= 0:
    change -= 25
    counter += 1

while change - 10 >= 0:
    change -= 10
    counter += 1

while change - 5 >= 0:
    change -= 5
    counter += 1

while change - 1 >= 0:
    change -= 1
    counter += 1

print(counter)