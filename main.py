import sqlite3 as sql
import os
import time
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
        time.sleep(0.1)
        print("New database has been created!")
        time.sleep(0.1)
        print("Welcome to Age Of Wonders' bestiary!")
        time.sleep(0.1)
    else:
        print("Database exist, hurray")
        time.sleep(0.1)
        choise = input("Do you want to create a new one?: [y/n]")
        if choise[0] == "y" or choise[0] == "Y": 
            time.sleep(0.1)
            choise = input("Are you sure, old one will be overwritten?: [y/n]")
            if choise[0] == "y" or choise[0] == "Y": 
                os.remove("database.db")
                initDatabase()
                return
        db = sql.connect("database.db")
        cursor = db.cursor()
        cursor.execute("PRAGMA foreign_keys = ON")
        time.sleep(0.1)
        print("Welcome to Age Of Wonders' bestiary!")
        time.sleep(0.1)
    

#############################################################################################################
# Option functions:
        
def main():
    while True:
        choise = mainOptions()
        print("")
        if choise == "1" or "add" in choise or "insert" in choise:
            if "mo" in input("Do you want to add a morbus or other organism? : ").lower():
                insertMorbus()
            else:
                insertOrganism()
        elif choise == "2" or "del" in choise:
            deleteOrganism()
        elif choise == "3"or "upda" in choise:
            updateOrganism()
        elif choise == "4" or "infect" in choise:
            insertInfection()
        elif choise == "5" or "view" in choise:
            dataViewFunction()
        elif choise == "0" or "end" in choise:
            break
        elif "any" in choise or "lua" in choise:
            lua()
        else:
            print("No such option!")
    cursor.close()
    db.close()
    return 0

def mainOptions():
    time.sleep(0.1)
    print("\nChoose option")
    time.sleep(0.1)
    print("1) Add new Organism or morbus")
    time.sleep(0.1)
    print("2) Delete Organism")
    time.sleep(0.1)
    print("3) Update Organism")
    time.sleep(0.1)
    print("4) Add infection (connection between morbus and organism)")
    time.sleep(0.1)
    print("5) Data view selection")
    time.sleep(0.1)
    print("0) End\n")
    time.sleep(0.1)
    print("lua) to enter LUA mode")
    time.sleep(0.1)
    choise = input("Your choise: ")
    return choise.lower()

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
            if choise == '1':
                newData = input("Give new Name: ")
                cursor.execute('UPDATE Organism SET Name = "'+newData+'" WHERE OrgID == '+orgID+';')
            elif choise == '2':
                newData = input("Give new Description: ")
                cursor.execute('UPDATE Organism SET Description = "'+newData+'" WHERE OrgID == '+orgID+';')
            elif choise == '3':
                cursor.execute("select count(*) from OrganismType")
                choises = choiseAmount()
                newData = input("Give new Organism type "+choises+": ")
                cursor.execute('UPDATE Organism SET OrgTypeID = '+newData+' WHERE OrgID == '+orgID+';')
            elif choise == '4':
                cursor.execute("select count(*) from LivingStyle")
                choises = choiseAmount()
                newData = input("Give new Living style "+choises+": ")
                cursor.execute('UPDATE Organism SET LivingStyleID = '+newData+' WHERE OrgID == '+orgID+';')
            elif choise == '5':
                cursor.execute("select count(*) from LivingAreas")
                choises = choiseAmount()
                newData = input("Give new Living area "+choises+": ")
                cursor.execute('UPDATE OrgToLA SET LivingAreaID = '+newData+' WHERE OrgID == '+orgID+';')
            elif choise == '0':
                db.commit()
                break
            else:
                print("\nNo such option!")
        except sql.Error as e:
            print("\nWrong input, try again! Error: ",e)

def updateOptions():
    print("\nWhat do you wnat to update:")
    print("1) Name")
    print("2) Description")
    print("3) Organism type")
    print("4) Living style")
    print("5) Living area")
    print("0) Save")
    choise = input("Your choise: ")
    return choise

def dataViewFunction():
    while True:
        choise = dataViewOptions()
        if choise == "1":
            printLivingAreasAndLivingStyle()
        elif choise == "2" or "print org" in choise:
            printOrganisms()
        elif choise == "3" or "print s" in choise:
            printSouls()
        elif choise == "4" or "find" in choise:
            userInput = input("Do you want to find by id, keyword, living area, or living style: ")
            if "id" in userInput or "key" in userInput:     
                findBySpecific()
            if "area" in userInput:
                findByArea()
            if "sty" in userInput:
                findByStyle()
        elif choise == "5":
            printInfections()
        elif choise == "0":
            break
        else:
            print("No such option!")
    return 0

def dataViewOptions():
    time.sleep(0.1)
    print("\nChoose a dataview that you want to see:")
    time.sleep(0.1)
    print("1) Print living areas and living style of a specific organism")
    time.sleep(0.1)
    print("2) Print Organisms")
    time.sleep(0.1)
    print("3) Print Souls")
    time.sleep(0.1)
    print("4) Find by id or keyword")
    time.sleep(0.1)
    print("5) Print Infections")
    time.sleep(0.1)
    print("0) Exit")
    time.sleep(0.1)
    choise = input("Your choise: ")
    return choise.lower()    

#############################################################################################################


#############################################################################################################
# Print functions:

def printOrganisms():
    print("Organisms:")
    data = cursor.execute("SELECT * FROM Organism")
    for cell in data:
        print("\nID:", cell[0], "Name:", cell[1], "\nDescription:", cell[2])
        time.sleep(0.1)
    print("")
    time.sleep(1)

def printInfections(): 
    print("Infections:")
    data = cursor.execute("Select OrgName, Name FROM (SELECT * FROM Infection INNER JOIN (SELECT OrgID as OrganismID, name as OrgName FROM Organism) ON OrganismID = Infection.OrgID INNER JOIN Morbus On Morbus.MorbusID = Infection.MorbusID) ORDER BY OrgName")
    for cell in data.fetchall():
        print("\nOrganism:", cell[0], "Morbus:", cell[1])
        time.sleep(0.1)
    print("")
    time.sleep(1)

def printSpecificOrganism(orgID):
    data = cursor.execute('SELECT * FROM Organism WHERE OrgID == '+orgID+';')
    print("")
    print(data.fetchall()[0])
    time.sleep(1)
    
def printStyles():
    print("Living Styles: ")
    data = cursor.execute("SELECT * FROM LivingStyle")
    for sty in data.fetchall():
        print(sty)
        time.sleep(0.1)
    print("")
    time.sleep(1)

def printAreas():
    print("Living Areas: ")
    data = cursor.execute("SELECT * FROM LivingAreas")
    for area in data.fetchall():
        print(area)
        time.sleep(0.1)
    print("")
    time.sleep(1)

def printSouls():
    print("Souls:")
    data = cursor.execute("SELECT name, NaturalSkills, SkillsLimits, Stats FROM Soul INNER JOIN Organism On Soul.OrgID = Organism.OrgID")
    for soul in data.fetchall():
        print("\nName:", soul[0])
        time.sleep(0.1)
        print("\nNaturalSkills:", soul[1])
        time.sleep(0.1)
        print("\nSkillsLimits:", soul[2])
        time.sleep(0.1)
        print("\nStats:", soul[3])
        time.sleep(0.1)
    print("")
    time.sleep(1)

def printMorbus():
    print("Morbus:")
    data = cursor.execute("SELECT * FROM Morbus")
    for cell in data:
        print("\nID:", cell[0], "Name:", cell[1], "\nDescription:", cell[2], "\nSymptoms:", cell[3])
        time.sleep(0.1)
    print("")
    time.sleep(1)

def printLivingAreasAndLivingStyle():
    print("")
    printOrganisms()
    choise = input("Choose Organism by ID: ")
    try:
        int(choise)
        cursor.execute('SELECT OrgID FROM Organism WHERE OrgID == '+choise+';')
        data = cursor.fetchone()
        if data == None:
            print("Organism not found.")
            return
        orgID = str(data[0])
    except ValueError or sql.Error as e:
        print("Wrong input, try again. Error: ", e)
        return
    try:
        cursor.execute('SELECT LivingStyleID FROM Organism WHERE OrgID == '+orgID+';')
        livingStyleID = str(cursor.fetchone()[0])
        cursor.execute('SELECT GROUP_CONCAT(LivingAreas.Name, ", "), LivingStyle.Name FROM LivingAreas INNER JOIN OrgToLA ON OrgToLA.OrgID == '+orgID+' AND OrgToLA.LivingAreaID == LivingAreas.LivingAreaID INNER JOIN LivingStyle ON LivingStyle.LivingStyleID == '+livingStyleID+';')
        fetchedData = cursor.fetchone()

        print("\n\nDATA:\n")
        print("Living areas:")
        print(fetchedData[0])
        print("\nLiving style:")
        print(fetchedData[1])
    except sql.Error as e:
        print("Something went wrong Error: ", e)
        return
    
#############################################################################################################


#############################################################################################################
# Database data cahange functions:

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
    count = str(cursor.fetchone()[0])
    while True:
        answer = input("How many living areas do you want to choose (1-"+count+"): ")
        try:
            amount = int(answer)
            if amount >= 1 and amount <= int(count):
                break
            print("Choise must be in the given range, try again.")
        except ValueError:
            print("Wrong input, try again.")
    cursor.execute("select count(*) from LivingAreas")
    choises = choiseAmount()
    livingAreaIDList = []
    i=1
    while i <= amount:
        answer = input(str(i)+". Living area "+choises+": ")
        try:
            number = int(answer)
            if number >= 0 and number < int(count):
                livingAreaIDList.append(str(number))
                i += 1
                continue
            print("Choise must be in the given range, try again.")
        except ValueError:
            print("Wrong input, try again.")

    cursor.execute("SELECT OrgID FROM Organism ORDER BY OrgID DESC LIMIT 1")
    data = cursor.fetchone()
    if data != None:
        newOrgID = str(data[0]+1)
    else:
        newOrgID = "0"
    
    soulID = insertSoul()

    try:
        cursor.execute('INSERT INTO Organism (OrgID, Name, Description, OrgTypeID, LivingStyleID, SoulID) VALUES ('+newOrgID+', "'+name+'", "'+description+'", '+organismTypeID+', '+livingStyleID+', '+soulID+');')
        cursor.execute('UPDATE Soul SET OrgID = '+newOrgID+' WHERE SoulID == '+soulID+';')
        for la in livingAreaIDList:
            cursor.execute('INSERT INTO OrgToLA (LivingAreaID, OrgID) VALUES ('+la+', '+newOrgID+')')
        db.commit()
    except sql.Error as e:
        db.rollback()
        print("\nWrong input, try again! Error: ", e)

def insertSoul():
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

def insertMorbus():
    print("Give the details of the new Morbus")
    name = input("Name: ")
    description = input("Description: ")
    symptoms = input("Symptoms: ")
    cursor.execute("SELECT MorbusID FROM Morbus ORDER BY MorbusID DESC LIMIT 1")
    data = cursor.fetchone()
    if data != None:
        newMorbusID = str(data[0]+1)
    else:
        newMorbusID = "0"
    try:
        cursor.execute('INSERT INTO Morbus (MorbusID, Name, Description, Symptoms) VALUES ('+newMorbusID+', "'+name+'", "'+description+'", "'+symptoms+'");')
        db.commit()
    except sql.Error as e:
        db.rollback()
        print("\nSomething hit the fan, try again! Error: ", e)

def insertInfection():
    print("Add a way that a morbus can infect a organism")
    printMorbus()
    morbus = input("Which morbus? you may insert id or name. 'E' exits: ")
    if morbus.lower() == "e":
        return
    try:
        int(morbus)
        cursor.execute("SELECT MorbusID FROM Morbus WHERE MorbusID = "+morbus)
    except ValueError:
        cursor.execute("SELECT MorbusID FROM Morbus WHERE Name LIKE '%"+morbus+"%'")
    morbusID = cursor.fetchall()
    if morbusID == None:
        print("invalid request")
        return
    morbusID = morbusID[0]
    while True:
        printOrganisms()
        organism = input("Which organism? you may insert id or name. 'E' exits: ")
        if organism.lower() == "e":
            break
        try:
            int(organism)
            cursor.execute("SELECT OrgID FROM Organism WHERE OrgID = "+organism)
        except ValueError:
            cursor.execute("SELECT OrgID FROM Organism WHERE Name LIKE '%"+organism+"%'")
        orgID = cursor.fetchall()
        if orgID == None:
            print("invalid request")
            continue
        orgID = orgID[0]
        print("\nTrying to add infection link between", str(morbusID[0]), "and", str(orgID[0]))
        try:
            cursor.execute('INSERT INTO Infection (MorbusID, OrgID) VALUES ('+str(morbusID[0])+', "'+str(orgID[0])+'");')
            print("Success")
            db.commit()
            time.sleep(0.5)
        except sql.Error as e:
            db.rollback()
            print("\nSomething hit the fan, try again! Error: ", e)
    if 'y' in input("do you want to choose another morbus) [y/n]").lower():
        insertInfection()
    return

def deleteOrganism():
    print("Which Organism you want to delete?\n")
    printOrganisms()
    orgID = input("\nGive Organism ID: ")
    try:
        cursor.execute('DELETE FROM Organism WHERE OrgID == '+orgID+';')
        db.commit()
    except sql.Error as e:
        print("\nWrong input, try again! Error: ",e)

def choiseAmount():
    choiseAmount = cursor.fetchone()
    choises = "(0"
    for x in range(1, choiseAmount[0]):
        choises += ", " + str(x) 
    choises += ")"
    return choises

#############################################################################################################


#############################################################################################################
# Find functions and lua function:

def findBySpecific():
    print("\nFind all organisms and morbus with a id, name or keyword")
    print("if input is number a ID search is performed,\nif input is not integer a keyword search is performed")

    rawChoise = input("Your choise: ")
    try:
        choise = int(rawChoise)
        cursor.execute("SELECT OrgID, Name, Description FROM Organism where OrgID = "+rawChoise+" UNION SELECT MorbusID, Name, Description FROM Morbus where MorbusID = "+rawChoise)
    except ValueError:
        cursor.execute("SELECT OrgID, Name, Description FROM Organism where Name LIKE '%"+rawChoise+"%' UNION SELECT MorbusID, Name, Description FROM Morbus where Name like '%"+rawChoise+"%' UNION SELECT OrgID, Name, Description FROM Organism where Description LIKE '%"+rawChoise+"%' UNION SELECT MorbusID, Name, Description FROM Morbus where Description like '%"+rawChoise+"%'")
    finally:
        print("")
        for data in cursor.fetchall():
            print("ID:", data[0], "\nName:", data[1], "\nDescription:", data[2],"\n")

def lua():
    while True:
        print("\nThis is LUA mode, you may make any querry as you wish, by inputing 0 you may exit to many\n")
        userInput = input("Please make your input: ")
        if userInput == "0":
            break
        else:
            try:
                cursor.execute(userInput)
            except sql.Error as e:
                print("Error in inserted querry, try again. Error: ", e)
                continue
            if "select" in userInput.lower():
                data = cursor.fetchall()
                for cell in data:
                    print(cell)
                    time.sleep(0.1)

            if "insert" in userInput.lower() or "delete" in userInput.lower() or "update" in userInput.lower():
                db.commit()

def findByStyle():
    printStyles()
    userInput = input("What living style you choose: ").lower()
    data = cursor.execute('SELECT OrgID, Name, Description FROM Organism where LivingStyleID == '+userInput+';')
    print("")
    for cell in data:
        print("ID:",cell[0],"Name:",cell[1],"Description:",cell[2])
    
def findByArea():
    printAreas()
    userInput = input("What living area you choose: ").lower()
    data = cursor.execute('SELECT OrgID, Name, Description FROM Organism where OrgID = (SELECT OrgID as ID FROM OrgToLA WHERE LivingAreaID == '+userInput+');')
    print("")
    for cell in data:
        print("ID:",cell[0],"Name:",cell[1],"Description:",cell[2])


print("Welcome")
initDatabase()
main()