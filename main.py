import sqlite3 as sql

cursor = None


def initDatabase():
    global cursor
    Exist = False
    try:
        open("database.db", "x")
    except FileExistsError:
        Exist = True
    db = sql.connect("database.db")
    cursor = db.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    if not Exist:
        with open("creation.sql", "r") as file:
            command = ""
            for line in file.readlines():
                command+=line
            cursor.executescript(command)
    else:
        print("Database exist, hurray")
    
        

def main():
    printOrganisms()
    pass


def options():
    pass


def printOrganisms():
    data = cursor.execute("SELECT * FROM Organism")
    print(data.fetchall())

initDatabase()
main()