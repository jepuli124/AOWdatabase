import sqlite3 as sql

cursor = None


def initDatabase():
    global cursor
    global db
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
    while True:
        options()
        choise = int(input("Your choise: "))
        print("")
        if choise == 1:
            printOrganisms()
        elif choise == 2:
            printSouls()
        elif choise == 3:
            insertOrganism()
        elif choise == 0:
            break
        else:
            print("No such option!")
    pass


def options():
    print("")
    print("Choose option")
    print("1) Print Organisms")
    print("2) Print Souls")
    print("3) Add new Organism")
    print("0) End")
    pass


def printOrganisms():
    data = cursor.execute("SELECT * FROM Organism")
    print(data.fetchall())

def printSouls():
    data = cursor.execute("SELECT * FROM Soul")
    print(data.fetchall())

def insertOrganism():
    print("Give the details of the new Organism")
    name = input("Name: ")
    description = input("Description: ")
    livingStyle = input("Living style: ") 
    livingArea = input("Living area: ") 
    cursor.execute("SELECT OrgID FROM Organism ORDER BY OrgID DESC LIMIT 1")
    newOrgID = str(cursor.fetchone()[0]+1)
    
    soulID = insertSoul(newOrgID)

    cursor.execute('INSERT INTO Organism (OrgID, Name, Description, OrgTypeID, LivingStyleID, SoulID) VALUES ('+newOrgID+', "'+name+'", "'+description+'", 1, 1, '+soulID+');')
    cursor.execute('UPDATE Soul SET OrgID = '+newOrgID+' WHERE SoulID == '+soulID+';')
    db.commit()

def insertSoul(OrgID):
    print("\nGive the details of the new soul")
    naturalSkills = input("Natural skills: ")
    skillsLimits = input("Skills limits: ")
    stats = input("Stats: ") 
    cursor.execute("SELECT SoulID FROM Soul ORDER BY SoulID DESC LIMIT 1")
    newSoulID = str(cursor.fetchone()[0]+1)

    cursor.execute('INSERT INTO Soul (SoulID, OrgID, NaturalSkills, SkillsLimits, Stats) VALUES ('+newSoulID+', NULL, "'+str(naturalSkills)+'", "'+str(skillsLimits)+'", "'+str(stats)+'")')
    db.commit()
    return newSoulID

initDatabase()
main()