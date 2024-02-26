import sqlite3 as sql
import os
cursor = None


def initDatabase():
    global cursor
    global db
    Exist = False
    try:
        database = open("database.db", "x")
        database.close()
    except FileExistsError:
        Exist = True

    if not Exist:
        db = sql.connect("database.db")
        cursor = db.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        with open("creation.sql", "r") as file:
            command = ""
            for line in file.readlines():
                command+=line
            cursor.executescript(command)
        
        print("New database has been created!")
        print("Welcome to Age Of Wonders' bestiary!")
    else:
        print("Database exist, hurray")
        choise = input("Do you want to create a new one?: [y/n]")
        if choise[0] == "y" or choise[0] == "Y": 
            choise = input("Are you sure, old one will be overwritten?: [y/n]")
            if choise[0] == "y" or choise[0] == "Y": 
                os.remove("database.db")
                initDatabase()
                return
        db = sql.connect("database.db")
        cursor = db.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        print("Welcome to Age Of Wonders' bestiary!")
    
        

def main():
    while True:
        choise = options()
        print("")
        if choise == 1:
            printOrganisms()
        elif choise == 2:
            printSouls()
        elif choise == 3:
            insertOrganism()
        elif choise == 4:
            deleteOrganism()
        elif choise == 5:
            updateOrganism()
        elif choise == 0:
            break
        else:
            print("No such option!")
    cursor.close()
    db.close()
    return 0

def options():
    print("\nChoose option")
    print("1) Print Organisms")
    print("2) Print Souls")
    print("3) Add new Organism")
    print("4) Delete Organism")
    print("5) Update Organism")
    print("0) End\n")
    try:
        choise = int(input("Your choise: "))
    except ValueError:
        print("please give your choise as a integer")
        choise = options()
    return choise


def printOrganisms():
    print("Organisms:")
    data = cursor.execute("SELECT * FROM Organism")
    for org in data.fetchall():
        print(org)

def printSpecificOrganism(orgID):
    data = cursor.execute('SELECT * FROM Organism WHERE OrgID == '+orgID+';')
    print("")
    print(data.fetchall()[0])
    

def printSouls():
    print("Souls:")
    data = cursor.execute("SELECT * FROM Soul")
    for soul in data.fetchall():
        print(soul)

def insertOrganism():
    print("Give the details of the new Organism")
    name = input("Name: ")
    description = input("Description: ")

    cursor.execute("select count(*) from OrganismType")
    choises = choiseAmount()
    organismTypeID = input("Organism type "+choises+": ")
    cursor.execute("select count(*) from LivingStyle")
    choises = choiseAmount()
    livingStyleID = input("Living style "+choises+": ") 
    cursor.execute("select count(*) from LivingAreas")
    choises = choiseAmount()
    livingAreaID = input("Living area "+choises+": ")

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
    except sql.Error as e:
        db.rollback()
        print("\nWrong input, try again! Error: ", e)
    

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

def deleteOrganism():
    print("Which Organism you want to delete?\n")
    printOrganisms()
    orgID = input("\nGive Organism ID: ")
    try:
        cursor.execute('DELETE FROM Organism WHERE OrgID == '+orgID+';')
        db.commit()
    except sql.Error as e:
        print("\nWrong input, try again! Error: ",e)

def updateOrganism():
    print("Which Organism you want to update?\n")
    printOrganisms()
    orgID = input("\nGive Organism ID: ")
    cursor.execute('SELECT COUNT(*) FROM Organism WHERE OrgID == "'+orgID+'";')

    if cursor.fetchone()[0] == 0:
        print("No such Organism!")
        return
    
    while True:
        printSpecificOrganism(orgID)
        choise = updateOptions()
        try:
            if choise == 1:
                newData = input("Give new Name: ")
                cursor.execute('UPDATE Organism SET Name = "'+newData+'" WHERE OrgID == '+orgID+';')
            elif choise == 2:
                newData = input("Give new Description: ")
                cursor.execute('UPDATE Organism SET Description = "'+newData+'" WHERE OrgID == '+orgID+';')
            elif choise == 3:
                cursor.execute("select count(*) from OrganismType")
                choises = choiseAmount()
                newData = input("Give new Organism type "+choises+": ")
                cursor.execute('UPDATE Organism SET OrgTypeID = '+newData+' WHERE OrgID == '+orgID+';')
            elif choise == 4:
                cursor.execute("select count(*) from LivingStyle")
                choises = choiseAmount()
                newData = input("Give new Living style "+choises+": ")
                cursor.execute('UPDATE Organism SET LivingStyleID = '+newData+' WHERE OrgID == '+orgID+';')
            elif choise == 5:
                cursor.execute("select count(*) from LivingAreas")
                choises = choiseAmount()
                newData = input("Give new Living area "+choises+": ")
                cursor.execute('UPDATE OrgToLA SET LivingAreaID = '+newData+' WHERE OrgID == '+orgID+';')
            elif choise == 0:
                db.commit()
                break
            else:
                print("\nNo such option!")
        except sql.Error as e:
            print("\nWrong input, try again! Error: ",e)

def choiseAmount():
    choiseAmount = cursor.fetchone()
    choises = "(0"
    for x in range(1, choiseAmount[0]):
        choises += ", " + str(x) 
    choises += ")"
    return choises

def updateOptions():
    print("\nWhat do you wnat to update:")
    print("1) Name")
    print("2) Description")
    print("3) Organism type")
    print("4) Living style")
    print("5) Living area")
    print("0) Save")
    try:
        choise = int(input("Your choise: "))
    except ValueError:
        print("please give your choise as a integer")
        choise = updateOptions()
    return choise

print("Welcome")
initDatabase()
main()