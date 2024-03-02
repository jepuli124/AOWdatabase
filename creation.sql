CREATE TABLE Organism
(
    OrgID INT NOT NULL,
    Name CHAR(40) NOT NULL UNIQUE CHECK (LENGTH(Name) <= 40),
    Description VARCHAR(65535) DEFAULT 'No description given!',
    OrgTypeID INT NOT NULL,
    LivingStyleID INT,
    SoulID INT NOT NULL,
    PRIMARY KEY (OrgID),
    FOREIGN KEY (OrgTypeID) REFERENCES OrganismType (OrgTypeID) ON DELETE CASCADE,
    FOREIGN KEY (LivingStyleID) REFERENCES LivingStyle (LivingStyleID) ON DELETE SET NULL,
    FOREIGN KEY (SoulID) REFERENCES Soul (SoulID) ON DELETE CASCADE
);

CREATE TABLE Morbus
(
    MorbusID INT NOT NULL,
    Name CHAR(40) NOT NULL,
    Description VARCHAR(65535),
    Symptoms VARCHAR(65535),
    PRIMARY KEY (MorbusID)
);

CREATE TABLE OrganismType
(
    OrgTypeID INT NOT NULL,
    Name CHAR(60) NOT NULL,
    Description VARCHAR(65535),
    PRIMARY KEY (OrgTypeID)
);

CREATE TABLE LivingStyle
(
    LivingStyleID INT NOT NULL,
    Name CHAR(60) NOT NULL,
    Description VARCHAR(65535),
    PRIMARY KEY (LivingStyleID)
);

CREATE TABLE LivingAreas
(
    LivingAreaID INT NOT NULL,
    Name CHAR(60) NOT NULL,
    Description VARCHAR(65535),
    PRIMARY KEY (LivingAreaID)
    
);

CREATE TABLE Soul
(
    SoulID INT NOT NULL,
    NaturalSkills VARCHAR(65535),
    SkillsLimits VARCHAR(65535),
    Stats VARCHAR(65535),
    OrgID INT,
    PRIMARY KEY (SoulID),
    FOREIGN KEY (OrgID) REFERENCES Organism (OrgID) ON DELETE CASCADE
);

CREATE TABLE OrgToLA(
    OrgID INT NOT NULL,
    LivingAreaID INT NOT NULL,
    FOREIGN KEY (OrgID) REFERENCES Organism (OrgID) ON DELETE CASCADE,
    FOREIGN KEY (LivingAreaID) REFERENCES LivingAreas (LivingAreaID) ON DELETE CASCADE
);

CREATE TABLE Infection(
    OrgID INT NOT NULL,
    MorbusID INT NOT NULL,
    FOREIGN KEY (OrgID) REFERENCES Organism (OrgID) ON DELETE CASCADE,
    FOREIGN KEY (MorbusID) REFERENCES Morbus (MorbusID) ON DELETE CASCADE
);


INSERT INTO OrganismType (OrgTypeID, Name, Description) VALUES (0, "Bestia", "All animals that lives on land or air");
INSERT INTO OrganismType (OrgTypeID, Name, Description) VALUES (1, "Aqua", "All animals that lives by water");
INSERT INTO OrganismType (OrgTypeID, Name, Description) VALUES (2, "Herba", "All kinds of plants");
INSERT INTO OrganismType (OrgTypeID, Name, Description) VALUES (3, "Fungus", "All kinds of Mushrooms");
INSERT INTO OrganismType (OrgTypeID, Name, Description) VALUES (4, "Unknown", "Unknown");

INSERT INTO LivingStyle (LivingStyleID, Name, Description) VALUES (0, "Obligate Carnivore", "Eats only meat");
INSERT INTO LivingStyle (LivingStyleID, Name, Description) VALUES (1, "Carnivore", "Eats mainly meat");
INSERT INTO LivingStyle (LivingStyleID, Name, Description) VALUES (2, "omnivore", "Eats everything");
INSERT INTO LivingStyle (LivingStyleID, Name, Description) VALUES (3, "Vegetarian", "Eats mainly vegetables");
INSERT INTO LivingStyle (LivingStyleID, Name, Description) VALUES (4, "Obligate Vegetarian", "Eats only vegetables");
INSERT INTO LivingStyle (LivingStyleID, Name, Description) VALUES (5, "Light", "Plant that eats light");

INSERT INTO LivingAreas (LivingAreaID, Name, Description) VALUES (0, "Forest", "Dense forest");
INSERT INTO LivingAreas (LivingAreaID, Name, Description) VALUES (1, "Water", "sea");
INSERT INTO LivingAreas (LivingAreaID, Name, Description) VALUES (2, "Mountain", "big mountain");
INSERT INTO LivingAreas (LivingAreaID, Name, Description) VALUES (3, "Desert", "It's coarse, irritating and gets everywhere");
INSERT INTO LivingAreas (LivingAreaID, Name, Description) VALUES (4, "Savanna", "High tempetature, dry, suitable only those that evolved to that, not much life");
INSERT INTO LivingAreas (LivingAreaID, Name, Description) VALUES (5, "Rainforest", "High tempetature, wet, filled to the brim with living beings");


INSERT INTO Soul (SoulID, NaturalSkills, SkillsLimits, Stats) VALUES (0, "equip,learn,study", "str:20,sta:20,cha:5", "str:5,sta:4,cha:4");
INSERT INTO Soul (SoulID, NaturalSkills, SkillsLimits, Stats) VALUES (1, "Photosyntesis", "", "growth:12");
INSERT INTO Soul (SoulID, NaturalSkills, SkillsLimits, Stats) VALUES (2, "Vampyrism, weak regeneration", "str:4, sta:7", "str:2,sta:4,cha:0");
INSERT INTO Soul (SoulID, NaturalSkills, SkillsLimits, Stats) VALUES (3, "gills", "breath:0", "str:1,sta:1,cha:1");
INSERT INTO Soul (SoulID, NaturalSkills, SkillsLimits, Stats) VALUES (4, "Fear, Despair", "cha:1", "str:12,sta:17,cha:-5");

INSERT INTO Organism (OrgID, Name, Description, OrgTypeID, LivingStyleID, SoulID) VALUES(0, "Inginate", "Humanoid species with multiple cultures and found all around the world", 0, 2, 0);
INSERT INTO Organism (OrgID, Name, Description, OrgTypeID, LivingStyleID, SoulID) VALUES(1, "Frenklie", "fast spreading moss that likes corpses", 2, 2, 1);
INSERT INTO Organism (OrgID, Name, Description, OrgTypeID, LivingStyleID, SoulID) VALUES(2, "Buha", "Small black ball that goes with the wind, Drinks blood with small needles from anything it touches", 0, 0, 2);
INSERT INTO Organism (OrgID, Name, Description, OrgTypeID, LivingStyleID, SoulID) VALUES(3, "Nahvle", "A small fish with beautiful red and yellow fins", 1, 2, 3);
INSERT INTO Organism (OrgID, Name, Description, OrgTypeID, LivingStyleID, SoulID) VALUES(4, "Dentio", "Unknown", 4, NULL, 4);

UPDATE Soul SET OrgID = 0 WHERE SoulID == 0;
UPDATE Soul SET OrgID = 1 WHERE SoulID == 1;
UPDATE Soul SET OrgID = 2 WHERE SoulID == 2;
UPDATE Soul SET OrgID = 3 WHERE SoulID == 3;
UPDATE Soul SET OrgID = 4 WHERE SoulID == 4;

INSERT INTO Morbus (MorbusID, Name, Description, Symptoms) VALUES (0, "Thorn disease", "Bones start to malform such as spikes form and grow out of skin, spreads by water or contact", "Pain, death 100%, muscle loss, weakness, vomiting, diarrhea");
INSERT INTO Morbus (MorbusID, Name, Description, Symptoms) VALUES (1, "plants' armagedon", "fast killing diseases, spreads by air", "Dryness, death %70, imcapable to reproduce, imcapable to grow");
INSERT INTO Morbus (MorbusID, Name, Description, Symptoms) VALUES (2, "rock disease", "turns skin hard, spreads by contact", "Pain, wounds, blood loss");
INSERT INTO Morbus (MorbusID, Name, Description, Symptoms) VALUES (3, "sailors' bane", "Spreads in water", "weakness, tiredness, headache, hard to breath");
INSERT INTO Morbus (MorbusID, Name, Description, Symptoms) VALUES (4, "blood poisoning", "veins to turn black and spreads with blood contact", "weakness, vomiting, death %20");

INSERT INTO OrgToLA (OrgID, LivingAreaID) VALUES (0, 4);
INSERT INTO OrgToLA (OrgID, LivingAreaID) VALUES (0, 0);
INSERT INTO OrgToLA (OrgID, LivingAreaID) VALUES (1, 5);
INSERT INTO OrgToLA (OrgID, LivingAreaID) VALUES (2, 3);
INSERT INTO OrgToLA (OrgID, LivingAreaID) VALUES (3, 1);


INSERT INTO Infection (OrgID, MorbusID) VALUES (1, 1);
INSERT INTO Infection (OrgID, MorbusID) VALUES (0, 0);
INSERT INTO Infection (OrgID, MorbusID) VALUES (2, 4);
INSERT INTO Infection (OrgID, MorbusID) VALUES (0, 3);
INSERT INTO Infection (OrgID, MorbusID) VALUES (0, 4);
