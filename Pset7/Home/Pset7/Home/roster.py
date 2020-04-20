from sys import argv
from cs50 import SQL
import csv

def main(argv):

    if len(argv) != 2:
        print("Usage: python roster.py homes")
        exit(1)

    open("students.db", "r").close()
    db = SQL("sqlite:///students.db")
    answer = []
    home = argv[1]
    answer = db.execute("SELECT first,middle,last,birth from students where house = ? order by last,first", home)
    print(answer)

    for row in answer:
        print(row["first"], end = ' ')
        if row["middle"] != None: print(row["middle"], end = ' ')
        print(row["last"], end = ',')
        print(f" born",row["birth"])

if __name__ == "__main__":
    main(argv)