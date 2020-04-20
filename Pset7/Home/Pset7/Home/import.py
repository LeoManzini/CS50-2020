import csv
from cs50 import SQL
from sys import argv

def main(argv):

    if len(argv)!=2:
        print("Usage: python import.py characters.csv")
        exit(1)

    open("students.db", "w").close()
    db = SQL("sqlite:///students.db")
    db.execute("CREATE TABLE students (first TEXT, middle TEXT, last TEXT, house TEXT, birth NUMBERIC)")

    with open(argv[1], "r") as file:
        reader = csv.DictReader(file)

        for row in reader:
            name = []
            name.append(row["name"].split())
            fullName = name[0]
            if len(fullName) == 2:
                db.execute("INSERT INTO students(first, last, house, birth) VALUES (?,?,?,?)",fullName[0], fullName[1], row["house"], int(row["birth"]))
            if len(fullName) == 3:
                db.execute("INSERT INTO students(first, middle, last, house, birth) VALUES (?,?,?,?,?)",fullName[0], fullName[1], fullName[2], row["house"], int(row["birth"]))

if __name__ == "__main__":
    main(argv)