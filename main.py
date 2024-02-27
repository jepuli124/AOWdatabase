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
        if choise == "1" or "print org" in choise:
            printOrganisms()
        elif choise == "2" or "print s" in choise:
            printSouls()
        elif choise == "3" or "add" in choise or "insert" in choise:
            if "mo" in input("Do you want to add a morbus or other organism? : ").lower():
                insertMorbus()
            else:
                insertOrganism()
        elif choise == "4" or "del" in choise:
            deleteOrganism()
        elif choise == "5"or "upda" in choise:
            updateOrganism()
        elif choise == "6" or "find" in choise:
            userInput = input("Do you want to find by id, keyword, living area, or living style: ")
            if "id" in userInput or "key" in userInput:     
                findBySpecific()
            if "area" in userInput:
                findByArea()
            if "sty" in userInput:
                findByStyle()
        elif choise == "7" or "infect" in choise:
            addInfection()
        elif choise == "8":
            printInfections()
        elif choise == "9" or "view" in choise:
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

def options():
    print("\nChoose option")
    print("1) Print Organisms")
    print("2) Print Souls")
    print("3) Add new Organism or morbus")
    print("4) Delete Organism")
    print("5) Update Organism")
    print("6) Find by id or keyword")
    print("7) Add infection (connection between morbus and organism)")
    print("8) Print Infections")
    print("9) Data view selection")
    print("0) End\n")
    print("lua) to enter LUA mode")
    choise = input("Your choise: ")
    return choise.lower()


def printOrganisms():
    print("Organisms:")
    data = cursor.execute("SELECT * FROM Organism")
    for cell in data:
        print("\nID:", cell[0], "Name:", cell[1], "\nDescription:", cell[2])
    print("")

def printInfections(): #!DOTO
    print("Infections:")
    #data = cursor.execute("Select Organism.Name as orgName where Organism.OrgID = (SELECT OrgID as ID FROM Infection)  , Morbus.Name as NM FROM Organism WHERE OrdID INNER JOIN Morbus ON Infection.MorbusID = Infection.OrgID)")
    #for cell in data:
    #    print("\nOrganism:", cell[0], "Morbus:", cell[1])
    print("")

def printSpecificOrganism(orgID):
    data = cursor.execute('SELECT * FROM Organism WHERE OrgID == '+orgID+';')
    print("")
    print(data.fetchall()[0])
    
def printStyles():
    print("Living Styles: ")
    data = cursor.execute("SELECT * FROM LivingStyle")
    for sty in data.fetchall():
        print(sty)

def printAreas():
    print("Living Areas: ")
    data = cursor.execute("SELECT * FROM LivingAreas")
    for area in data.fetchall():
        print(area)

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

def printMorbus():
    print("Morbus:")
    data = cursor.execute("SELECT * FROM Morbus")
    for cell in data:
        print("\nID:", cell[0], "Name:", cell[1], "\nDescription:", cell[2], "\nSymptoms:", cell[3])
    print("")


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

def addInfection():
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
    morbusID = cursor.fetchone()
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
        orgID = cursor.fetchone()
        if orgID == None:
            print("invalid request")
            continue
        orgID = orgID[0]
        try:
            cursor.execute('INSERT INTO Infection (MorbusID, OrgID) VALUES ('+str(morbusID)+', "'+str(orgID)+'");')
            db.commit()
        except sql.Error as e:
            db.rollback()
            print("\nSomething hit the fan, try again! Error: ", e)
    if 'y' in input("do you want to choose another morbus) [y/n]").lower():
        addInfection()
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
    choise = input("Your choise: ")
    return choise

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

            cursor.execute(userInput)
            if "select" in userInput.lower():
                data = cursor.fetchall()
                for cell in data:
                    print(cell)

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

def viewSelection():
    print("\nChoose a dataview that you want to see:")
    print("1) Print living areas and living style of a specific organism")
    print("0) Exit")
    choise = input("Your choise: ")
    return choise
    
def dataViewFunction():
    while True:
        choise = viewSelection()
        if choise == "1":
            printData1()
        elif choise == "0":
            break
        else:
            print("No such option!")
    return 0    

def printData1():
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
        print("Somethjing went wrong Error: ", e)
        return


print("Welcome")
initDatabase()
main()