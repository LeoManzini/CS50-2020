from cs50 import get_int

while True:
    height = get_int("Height: ")
    if height > 0 and height <= 8:
        break

blank = height - 1

for i in range(height):
    print(" " * blank + "#" * (i+1))
    blank -= 1