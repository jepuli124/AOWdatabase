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
            data = file.readlines()
            for commandline in data:
                markedContinue = False
                markedExecute = False
                for char in commandline:
                    if char == '-':
                        markedContinue = True
                        continue
                    elif char == ';':
                        markedExecute = True
                        continue
                if markedContinue:
                    continue
                if markedExecute: 
                    command += commandline
                    cursor.execute(command)
                    command = ""
                else:
                    command += commandline
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