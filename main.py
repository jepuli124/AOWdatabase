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
    cursor.close()
    db.close()
    return 0

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
    organismTypeID = input("Organism type (0,1,2): ")
    livingStyleID = input("Living style (0,1,2): ") 
    livingAreaID = input("Living area (0,1,2): ") 
    cursor.execute("SELECT OrgID FROM Organism ORDER BY OrgID DESC LIMIT 1")
    data = cursor.fetchone()
    if data != None:
        newOrgID = str(data[0]+1)
    else:
        newOrgID = "0"
    
    soulID = insertSoul(newOrgID)

    try:
        cursor.execute('INSERT INTO Organism (OrgID, Name, Description, OrgTypeID, LivingStyleID, SoulID) VALUES ('+newOrgID+', "'+name+'", "'+description+'", '+organismTypeID+', '+livingStyleID+', '+soulID+');')
        cursor.execute('UPDATE Soul SET OrgID = '+newOrgID+' WHERE SoulID == '+soulID+';')
        cursor.execute('INSERT INTO OrgToLA (LivingAreaID, OrgID) VALUES ('+livingAreaID+', '+newOrgID+')')
        db.commit()
    except:
        db.rollback()
        print("\nWrong input, try again!")
    

def insertSoul(OrgID):
    print("\nGive the details of the new soul")
    naturalSkills = input("Natural skills: ")
    skillsLimits = input("Skills limits: ")
    stats = input("Stats: ") 
    cursor.execute("SELECT SoulID FROM Soul ORDER BY SoulID DESC LIMIT 1")
    data = cursor.fetchone()
    if data != None:
        newSoulID = str(data[0]+1)
    else: 
        newSoulID = "0"

    cursor.execute('INSERT INTO Soul (SoulID, OrgID, NaturalSkills, SkillsLimits, Stats) VALUES ('+newSoulID+', NULL, "'+naturalSkills+'", "'+skillsLimits+'", "'+stats+'");')
    return newSoulID

initDatabase()
main()