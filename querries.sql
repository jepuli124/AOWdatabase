-- All querries and SQL lines used in python frontend

SELECT COUNT(*) FROM Organism WHERE OrgID == "'+orgID+'";
select Name from Organism where OrgID == '+orgID+';
UPDATE Organism SET Name = "'+newData+'" WHERE OrgID == '+orgID+';
select Description from Organism where OrgID == '+orgID+';
UPDATE Organism SET Description = "'+newData+'" WHERE OrgID == '+orgID+';
select OrgTypeID from Organism where OrgID == '+orgID+';
UPDATE Organism SET OrgTypeID = '+newData+' WHERE OrgID == '+orgID+';
select LivingStyleID from Organism where OrgID == '+orgID+';
select count(*) from LivingStyle;
UPDATE Organism SET LivingStyleID = '+newData+' WHERE OrgID == '+orgID+';
select LivingAreaID from OrgToLA where OrgID == '+orgID+';
select LivingAreaID from OrgToLA where LivingAreaID == '+livingAreaID+' and OrgID == '+orgID+';
select count(*) from LivingAreas;
UPDATE OrgToLA SET LivingAreaID = '+newData+' WHERE OrgID == '+orgID+' and LivingAreaID == '+livingAreaID+';
SELECT * FROM Organism;
SELECT COUNT(*) FROM Organism;
Select OrgName, Name FROM (SELECT * FROM Infection INNER JOIN (SELECT OrgID as OrganismID, name as OrgName FROM Organism) ON OrganismID = Infection.OrgID INNER JOIN Morbus On Morbus.MorbusID = Infection.MorbusID) ORDER BY OrgName;
SELECT * FROM Organism WHERE OrgID == '+orgID+';
SELECT * FROM LivingStyle;
SELECT * FROM LivingAreas;
SELECT name, NaturalSkills, SkillsLimits, Stats FROM Soul INNER JOIN Organism On Soul.OrgID = Organism.OrgID;
SELECT * FROM Morbus;
SELECT OrgID FROM Organism WHERE OrgID == '+choise+';
SELECT LivingStyleID FROM Organism WHERE OrgID == '+orgID+';
SELECT GROUP_CONCAT(LivingAreas.Name, ", "), LivingStyle.Name FROM LivingAreas INNER JOIN OrgToLA ON OrgToLA.OrgID == '+orgID+' AND OrgToLA.LivingAreaID == LivingAreas.LivingAreaID INNER JOIN LivingStyle ON LivingStyle.LivingStyleID == '+livingStyleID+';
select COUNT(Name) from Organism where LOWER(Name) == "'+name.lower()+'";
select count(*) from OrganismType;
select count(*) from LivingStyle;
select count(*) from LivingAreas;
select count(*) from LivingAreas;
SELECT OrgID FROM Organism ORDER BY OrgID DESC LIMIT 1;
INSERT INTO Organism (OrgID, Name, Description, OrgTypeID, LivingStyleID, SoulID) VALUES ('+newOrgID+', "'+name+'", "'+description+'", '+organismTypeID+', '+livingStyleID+', '+soulID+');
UPDATE Soul SET OrgID = '+newOrgID+' WHERE SoulID == '+soulID+';
INSERT INTO OrgToLA (LivingAreaID, OrgID) VALUES ('+la+', '+newOrgID+');
SELECT SoulID FROM Soul ORDER BY SoulID DESC LIMIT 1;
INSERT INTO Soul (SoulID, OrgID, NaturalSkills, SkillsLimits, Stats) VALUES ('+newSoulID+', NULL, "'+naturalSkills+'", "'+skillsLimits+'", "'+stats+'");
SELECT MorbusID FROM Morbus ORDER BY MorbusID DESC LIMIT 1;
INSERT INTO Morbus (MorbusID, Name, Description, Symptoms) VALUES ('+newMorbusID+', "'+name+'", "'+description+'", "'+symptoms+'");
SELECT MorbusID FROM Morbus WHERE MorbusID = "+morbus+";
SELECT MorbusID FROM Morbus WHERE Name LIKE '%"+morbus+"%';
SELECT OrgID FROM Organism WHERE OrgID = "+organism+";
SELECT OrgID FROM Organism WHERE Name LIKE '%"+organism+"%';
INSERT INTO Infection (MorbusID, OrgID) VALUES ('+str(morbusID[0])+', "'+str(orgID[0])+'");
SELECT COUNT(*) FROM Organism WHERE OrgID == "'+orgID+'";
DELETE FROM Organism WHERE OrgID == '+orgID+';
SELECT OrgID, Name, Description FROM Organism where OrgID = "+rawChoise+" UNION SELECT MorbusID, Name, Description FROM Morbus where MorbusID = "+rawChoise+";
SELECT OrgID, Name, Description FROM Organism where Name LIKE '%"+rawChoise+"%' UNION SELECT MorbusID, Name, Description FROM Morbus where Name like '%"+rawChoise+"%' UNION SELECT OrgID, Name, Description FROM Organism where Description LIKE '%"+rawChoise+"%' UNION SELECT MorbusID, Name, Description FROM Morbus where Description like '%"+rawChoise+"%';
SELECT OrgID, Name, Description FROM Organism where LivingStyleID == '+userInput+';
SELECT OrgID, Name, Description FROM Organism where OrgID = (SELECT OrgID as ID FROM OrgToLA WHERE LivingAreaID == '+userInput+');
SELECT ID, name FROM (SELECT Organism.OrgID as ID, name, MorbusID FROM Organism INNER JOIN Infection ON Organism.OrgID = Infection.OrgID) where MorbusID = "+rawChoise+";
SELECT ID, oName FROM (SELECT Organism.OrgID as ID, Morbus.name as mName, Organism.name as oName, Symptoms, Morbus.Description as mDescription FROM Organism INNER JOIN Infection ON Organism.OrgID = Infection.OrgID INNER JOIN Morbus ON Infection.MorbusID = Morbus.MorbusID) where mName like '%"+rawChoise+"%' OR mDescription like '%"+rawChoise+"%' OR Symptoms like '%"+rawChoise+"%';
SELECT MorbusID, Name, Description, Symptoms FROM Morbus where MorbusID = "+rawChoise+";
SELECT MorbusID, Name, Description, Symptoms FROM Morbus where Name like '%"+rawChoise+"%' UNION SELECT MorbusID, Name, Description, Symptoms FROM Morbus where Description like '%"+rawChoise+"%' UNION SELECT MorbusID, Name, Description, Symptoms FROM Morbus where Symptoms like '%"+rawChoise+"%';
