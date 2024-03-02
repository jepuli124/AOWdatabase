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
        printslow("New database has been created!")
        printslow("Welcome to Age Of Wonders' bestiary!")
    else:
        printslow("Database exist, hurray")
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
        printslow("Welcome to Age Of Wonders' bestiary!")


#############################################################################################################
# decoration functions:

def printslow(*string):
    for word in string:
        print(word, end=" ")
    print()
    time.sleep(0.1)

#############################################################################################################
# Option functions:
        
def main():
    while True:
        choise = mainOptions()
        printslow("")
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
            printslow("No such option!")
    cursor.close()
    db.close()
    return 0

def mainOptions():
    printslow("\nChoose option")
    printslow("1) Add new Organism or morbus")
    printslow("2) Delete Organism")
    printslow("3) Update Organism")
    printslow("4) Add infection (connection between morbus and organism)")
    printslow("5) Data view selection")
    printslow("0) End\n")
    printslow("lua) to enter LUA mode")
    choise = input("Your choise: ")
    return choise.lower()

def updateOrganism():
    printslow("Which Organism you want to update?\n")
    printOrganisms()
    orgID = input("\nGive Organism ID: ")
    cursor.execute('SELECT COUNT(*) FROM Organism WHERE OrgID == "'+orgID+'";')

    if cursor.fetchone()[0] == 0:
        printslow("No such Organism!")
        return
    
    while True:
        printSpecificOrganism(orgID)
        choise = updateOptions()
        print("\n")
        try:
            if choise == '1':
                cursor.execute('select Name from Organism where OrgID == '+orgID+';')
                print("Old Name: "+cursor.fetchone()[0]+"")
                newData = input("Give new Name: ")
                cursor.execute('UPDATE Organism SET Name = "'+newData+'" WHERE OrgID == '+orgID+';')
            elif choise == '2':
                cursor.execute('select Description from Organism where OrgID == '+orgID+';')
                print("Old Description: "+cursor.fetchone()[0]+"")
                newData = input("Give new Description: ")
                cursor.execute('UPDATE Organism SET Description = "'+newData+'" WHERE OrgID == '+orgID+';')
            elif choise == '3':
                cursor.execute('select OrgTypeID from Organism where OrgID == '+orgID+';')
                print("Old Organism type: "+cursor.fetchone()[0]+"")
                cursor.execute("select count(*) from OrganismType")
                choises = choiseAmount()
                newData = input("Give new Organism type "+choises+": ")
                cursor.execute('UPDATE Organism SET OrgTypeID = '+newData+' WHERE OrgID == '+orgID+';')
            elif choise == '4':
                cursor.execute('select LivingStyleID from Organism where OrgID == '+orgID+'')
                print("Old Living style: "+cursor.fetchone()[0]+"")
                cursor.execute("select count(*) from LivingStyle")
                choises = choiseAmount()
                newData = input("Give new Living style "+choises+": ")
                cursor.execute('UPDATE Organism SET LivingStyleID = '+newData+' WHERE OrgID == '+orgID+';')
            elif choise == '5':
                cursor.execute('select LivingAreaID from OrgToLA where OrgID == '+orgID+';')
                print("Old Living area(s): ", end="")
                for i in cursor.fetchall():
                    print(i[0], end=" ")
                print("\n")
                livingAreaID = input("Give the ID of the living area you want to update: ")
                try:
                    cursor.execute('select LivingAreaID from OrgToLA where LivingAreaID == '+livingAreaID+' and OrgID == '+orgID+';')
                    data = cursor.fetchone()[0]
                    print(data)
                except:
                    print("No such ID found!")
                    continue
                cursor.execute("select count(*) from LivingAreas")
                choises = choiseAmount()
                newData = input("Give new Living area "+choises+": ")
                cursor.execute('UPDATE OrgToLA SET LivingAreaID = '+newData+' WHERE OrgID == '+orgID+' and LivingAreaID == '+livingAreaID+';')
            elif choise == '0':
                db.commit()
                break
            else:
                printslow("\nNo such option!")
        except sql.Error as e:
            printslow("\nWrong input, try again! Error: ",e)

def updateOptions():
    printslow("\nWhat do you wnat to update:")
    printslow("1) Name")
    printslow("2) Description")
    printslow("3) Organism type")
    printslow("4) Living style")
    printslow("5) Living area")
    printslow("0) Save")
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
            userInput = input("Do you want to find by id, keyword, living area, living style, or by morbus: ")
            if "id" in userInput.lower() or "key" in userInput.lower():     
                findBySpecific()
            elif "area" in userInput.lower():
                findByArea()
            elif "sty" in userInput.lower():
                findByStyle()
            elif "morbus" in userInput.lower():
                findByMorbus()
            else:
                printslow("Invalid input")
        elif choise == "5":
            printInfections()
        elif choise == "0":
            break
        else:
            printslow("No such option!")
    return 0

def dataViewOptions():
    printslow("\nChoose a dataview that you want to see:")
    printslow("1) Print living areas and living style of a specific organism")
    printslow("2) Print Organisms")
    printslow("3) Print Souls")
    printslow("4) Find by id or keyword")
    printslow("5) Print Infections")
    printslow("0) Exit")
    choise = input("Your choise: ")
    return choise.lower()    

#############################################################################################################


#############################################################################################################
# Print functions:

def printOrganisms():
    printslow("Organisms:")
    cursor.execute("SELECT * FROM Organism")
    data = cursor.fetchall()
    cursor.execute("SELECT COUNT(*) FROM Organism")
    count = cursor.fetchone()
    for cell in data:
        printslow("\nID:", cell[0], "Name:", cell[1], "\nDescription:", cell[2])
    printslow("")
    time.sleep(1)
    return count[0]
    

def printInfections(): 
    printslow("Infections:")
    data = cursor.execute("Select OrgName, Name FROM (SELECT * FROM Infection INNER JOIN (SELECT OrgID as OrganismID, name as OrgName FROM Organism) ON OrganismID = Infection.OrgID INNER JOIN Morbus On Morbus.MorbusID = Infection.MorbusID) ORDER BY OrgName")
    for cell in data.fetchall():
        printslow("\nOrganism:", cell[0], "Morbus:", cell[1])
    printslow("")
    time.sleep(1)

def printSpecificOrganism(orgID):
    data = cursor.execute('SELECT * FROM Organism WHERE OrgID == '+orgID+';')
    printslow("")
    printslow(data.fetchall()[0])
    time.sleep(1)
    
def printStyles():
    printslow("Living Styles: ")
    data = cursor.execute("SELECT * FROM LivingStyle")
    for sty in data.fetchall():
        printslow(sty)
    printslow("")
    time.sleep(1)

def printAreas():
    printslow("Living Areas: ")
    data = cursor.execute("SELECT * FROM LivingAreas")
    for area in data.fetchall():
        printslow(area)
    printslow("")
    time.sleep(1)

def printSouls():
    printslow("Souls:")
    data = cursor.execute("SELECT name, NaturalSkills, SkillsLimits, Stats FROM Soul INNER JOIN Organism On Soul.OrgID = Organism.OrgID")
    for soul in data.fetchall():
        printslow("\nName:", soul[0])
        printslow("\nNaturalSkills:", soul[1])
        printslow("\nSkillsLimits:", soul[2])
        printslow("\nStats:", soul[3])
    printslow("")
    time.sleep(1)

def printMorbus():
    printslow("Morbus:")
    data = cursor.execute("SELECT * FROM Morbus")
    for cell in data:
        printslow("\nID:", cell[0], "Name:", cell[1], "\nDescription:", cell[2], "\nSymptoms:", cell[3])
    printslow("")
    time.sleep(1)

def printLivingAreasAndLivingStyle():
    printslow("")
    count = printOrganisms()
    if count == 0:
        print("No Organisms in the database!")
        return
    choise = input("Choose Organism by ID: ")
    try:
        int(choise)
        cursor.execute('SELECT OrgID FROM Organism WHERE OrgID == '+choise+';')
        data = cursor.fetchone()
        if data == None:
            printslow("Organism not found.")
            return
        orgID = str(data[0])
    except ValueError or sql.Error as e:
        printslow("Wrong input, try again. Error: ", e)
        return
    try:
        cursor.execute('SELECT LivingStyleID FROM Organism WHERE OrgID == '+orgID+';')
        livingStyleID = str(cursor.fetchone()[0])
        cursor.execute('SELECT GROUP_CONCAT(LivingAreas.Name, ", "), LivingStyle.Name FROM LivingAreas INNER JOIN OrgToLA ON OrgToLA.OrgID == '+orgID+' AND OrgToLA.LivingAreaID == LivingAreas.LivingAreaID INNER JOIN LivingStyle ON LivingStyle.LivingStyleID == '+livingStyleID+';')
        fetchedData = cursor.fetchone()

        printslow("\n\nDATA:\n")
        printslow("Living areas:")
        printslow(fetchedData[0])
        printslow("\nLiving style:")
        printslow(fetchedData[1])
    except sql.Error as e:
        printslow("Something went wrong Error: ", e)
        return
    
#############################################################################################################


#############################################################################################################
# Database data cahange functions:

def insertOrganism():
    printslow("Give the details of the new Organism")
    name = input("Name: ")
    cursor.execute('select COUNT(Name) from Organism where LOWER(Name) == "'+name.lower()+'";')
    if cursor.fetchone()[0] != 0:
        print("The name has been already taken!")
        return
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
            printslow("Choise must be in the given range, try again.")
        except ValueError:
            printslow("Wrong input, try again.")
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
            printslow("Choise must be in the given range, try again.")
        except ValueError:
            printslow("Wrong input, try again.")

    cursor.execute("SELECT OrgID FROM Organism ORDER BY OrgID DESC LIMIT 1")
    data = cursor.fetchone()
    if data != None:
        newOrgID = str(data[0]+1)
    else:
        newOrgID = "0"
    
    soulID = insertSoul()

    try:
        if description == "":
            cursor.execute('INSERT INTO Organism (OrgID, Name, OrgTypeID, LivingStyleID, SoulID) VALUES ('+newOrgID+', "'+name+'", '+organismTypeID+', '+livingStyleID+', '+soulID+');')
        else:
            cursor.execute('INSERT INTO Organism (OrgID, Name, Description, OrgTypeID, LivingStyleID, SoulID) VALUES ('+newOrgID+', "'+name+'", "'+description+'", '+organismTypeID+', '+livingStyleID+', '+soulID+');')
        cursor.execute('UPDATE Soul SET OrgID = '+newOrgID+' WHERE SoulID == '+soulID+';')
        for la in livingAreaIDList:
            cursor.execute('INSERT INTO OrgToLA (LivingAreaID, OrgID) VALUES ('+la+', '+newOrgID+')')
        db.commit()
    except sql.Error as e:
        db.rollback()
        printslow("\nWrong input, try again! Error: ", e)

def insertSoul():
    printslow("\nGive the details of the new soul")
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
    printslow("Give the details of the new Morbus")
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
        printslow("\nSomething hit the fan, try again! Error: ", e)

def insertInfection():
    printslow("Add a way that a morbus can infect a organism")
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
    try:
        morbusID = morbusID[0]
    except:
        printslow("No such Morbus!")
        return
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
            printslow("invalid request")
            continue
        orgID = orgID[0]
        printslow("\nTrying to add infection link between", str(morbusID[0]), "and", str(orgID[0]))
        try:
            cursor.execute('INSERT INTO Infection (MorbusID, OrgID) VALUES ('+str(morbusID[0])+', "'+str(orgID[0])+'");')
            printslow("Success")
            db.commit()
            time.sleep(0.5)
        except sql.Error as e:
            db.rollback()
            printslow("\nSomething hit the fan, try again! Error: ", e)
    if 'y' in input("do you want to choose another morbus) [y/n]").lower():
        insertInfection()
    return

def deleteOrganism():
    printslow("Which Organism you want to delete?\n")
    printOrganisms()
    orgID = input("\nGive Organism ID: ")
    cursor.execute('SELECT COUNT(*) FROM Organism WHERE OrgID == "'+orgID+'";')

    if cursor.fetchone()[0] == 0:
        print("No such Organism!")
        return
    try:
        cursor.execute('DELETE FROM Organism WHERE OrgID == '+orgID+';')
        db.commit()
    except sql.Error as e:
        printslow("\nWrong input, try again! Error: ",e)

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
    printslow("\nFind all organisms and morbus with a id, name or keyword")
    printslow("if input is number a ID search is performed,\nif input is not integer a keyword search is performed")

    rawChoise = input("Your choise: ")
    try:
        choise = int(rawChoise)
        cursor.execute("SELECT OrgID, Name, Description FROM Organism where OrgID = "+rawChoise+" UNION SELECT MorbusID, Name, Description FROM Morbus where MorbusID = "+rawChoise)
    except ValueError:
        cursor.execute("SELECT OrgID, Name, Description FROM Organism where Name LIKE '%"+rawChoise+"%' UNION SELECT MorbusID, Name, Description FROM Morbus where Name like '%"+rawChoise+"%' UNION SELECT OrgID, Name, Description FROM Organism where Description LIKE '%"+rawChoise+"%' UNION SELECT MorbusID, Name, Description FROM Morbus where Description like '%"+rawChoise+"%'")
    finally:
        printslow("")
        for data in cursor.fetchall():
            printslow("ID:", data[0], "\nName:", data[1], "\nDescription:", data[2],"\n")

def lua():
    while True:
        printslow("\nThis is LUA mode, you may make any querry as you wish, by inputing 0 you may exit to many\n")
        userInput = input("Please make your input: ")
        if userInput == "0":
            break
        else:
            try:
                cursor.execute(userInput)
            except sql.Error as e:
                printslow("Error in inserted querry, try again. Error: ", e)
                continue
            if "select" in userInput.lower():
                data = cursor.fetchall()
                for cell in data:
                    printslow(cell)

            if "insert" in userInput.lower() or "delete" in userInput.lower() or "update" in userInput.lower():
                db.commit()

def findByStyle():
    printStyles()
    userInput = input("What living style you choose: ").lower()
    data = cursor.execute('SELECT OrgID, Name, Description FROM Organism where LivingStyleID == '+userInput+';')
    printslow("")
    for cell in data:
        printslow("ID:",cell[0],"Name:",cell[1],"Description:",cell[2])
    
def findByArea():
    printAreas()
    userInput = input("What living area you choose: ").lower()
    data = cursor.execute('SELECT OrgID, Name, Description FROM Organism where OrgID = (SELECT OrgID as ID FROM OrgToLA WHERE LivingAreaID == '+userInput+');')
    printslow("")
    for cell in data:
        printslow("ID:",cell[0],"Name:",cell[1],"Description:",cell[2])

def findByMorbus():
    printslow("Insert a morbus name, id, keyword or symptom to find which organisms can suffer from it")
    rawChoise = input("Your choise: ")
    try:
        choise = int(rawChoise)
        data = cursor.execute("SELECT ID, name FROM (SELECT Organism.OrgID as ID, name, MorbusID FROM Organism INNER JOIN Infection ON Organism.OrgID = Infection.OrgID) where MorbusID = "+rawChoise+"")
        
        for cell in data.fetchall():
            printslow("ID:", cell[0], "\nName:", cell[1])
    except ValueError:
        data = cursor.execute("SELECT ID, oName FROM (SELECT Organism.OrgID as ID, Morbus.name as mName, Organism.name as oName, Symptoms, Morbus.Description as mDescription FROM Organism INNER JOIN Infection ON Organism.OrgID = Infection.OrgID INNER JOIN Morbus ON Infection.MorbusID = Morbus.MorbusID) where mName like '%"+rawChoise+"%' OR mDescription like '%"+rawChoise+"%' OR Symptoms like '%"+rawChoise+"%'")
        for cell in data.fetchall():
            printslow("ID:", cell[0], "\nName:", cell[1])
    printslow("")
        
    printslow("")
    time.sleep(1)

def findMorbus():
    printslow("Insert a morbus name, id, keyword or symptom to all morbus by that")
    rawChoise = input("Your choise: ")
    try:
        choise = int(rawChoise)
        cursor.execute("SELECT MorbusID, Name, Description, Symptoms FROM Morbus where MorbusID = "+rawChoise)
    except ValueError:
        cursor.execute("SELECT MorbusID, Name, Description, Symptoms FROM Morbus where Name like '%"+rawChoise+"%' UNION SELECT MorbusID, Name, Description, Symptoms FROM Morbus where Description like '%"+rawChoise+"%' UNION SELECT MorbusID, Name, Description, Symptoms FROM Morbus where Symptoms like '%"+rawChoise+"%'")
    finally:
        printslow("")
        for data in cursor.fetchall():
            printslow("ID:", data[0], "\nName:", data[1], "\nDescription:", data[2],"\nSymptoms:", data[3],"\n")
    printslow("")
    time.sleep(1)


printslow("Welcome")
initDatabase()
main()
printslow("Thank you for the usage of this program")
