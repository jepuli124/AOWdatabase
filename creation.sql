CREATE TABLE Organism
(
    OrgID INT NOT NULL,
    Name CHAR(40) NOT NULL UNIQUE CHECK (LENGTH(Name) <= 40),
    Description VARCHAR(65535) DEFAULT 'No description given!',
    OrgTypeID INT NOT NULL,
    LivingStyleID INT NOT NULL,
    SoulID INT NOT NULL,
    PRIMARY KEY (OrgID),
    FOREIGN KEY (OrgTypeID) REFERENCES OrganismType (OrgTypeID) ON DELETE CASCADE,
    FOREIGN KEY (LivingStyleID) REFERENCES LivingStyle (LivingStyleID) ON DELETE CASCADE,
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

INSERT INTO LivingStyle (LivingStyleID, Name, Description) VALUES (0, "Obligate Carnivore", "Eats only meat");
INSERT INTO LivingStyle (LivingStyleID, Name, Description) VALUES (1, "Carnivore", "Eats mainly meat");
INSERT INTO LivingStyle (LivingStyleID, Name, Description) VALUES (2, "omnivore", "Eats everything");
INSERT INTO LivingStyle (LivingStyleID, Name, Description) VALUES (3, "Vegetarian", "Eats mainly vegetables");
INSERT INTO LivingStyle (LivingStyleID, Name, Description) VALUES (4, "Obligate Vegetarian", "Eats only vegetables");

INSERT INTO LivingAreas (LivingAreaID, Name, Description) VALUES (0, "Forest", "Dense forest");
INSERT INTO LivingAreas (LivingAreaID, Name, Description) VALUES (1, "Water", "sea");
INSERT INTO LivingAreas (LivingAreaID, Name, Description) VALUES (2, "Mountain", "big mountain");
INSERT INTO LivingAreas (LivingAreaID, Name, Description) VALUES (3, "Desert", "It's coarse, irritating and gets everywhere");
INSERT INTO LivingAreas (LivingAreaID, Name, Description) VALUES (4, "Savanna", "High tempetature, dry, suitable only those that evolved to that, not much life");
INSERT INTO LivingAreas (LivingAreaID, Name, Description) VALUES (5, "Rainforest", "High tempetature, wet, filled to the brim with living beings");

