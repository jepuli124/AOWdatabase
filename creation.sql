CREATE TABLE Organism
(
    OrgID INT NOT NULL,
    Name CHAR(40) NOT NULL,
    Description VARCHAR(65535),
    OrgTypeID INT NOT NULL,
    LivingStyleID INT NOT NULL,
    SoulID INT NOT NULL,
    PRIMARY KEY (OrgID),
    FOREIGN KEY (OrgTypeID) REFERENCES OrganismType (OrgTypeID),
    FOREIGN KEY (LivingStyleID) REFERENCES LivingStyle (LivingStyleID),
    FOREIGN KEY (SoulID) REFERENCES Soul (SoulID)
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
    FOREIGN KEY (OrgID) REFERENCES Organism (OrgID)
);

CREATE TABLE OrgToLA(
    OrgID INT NOT NULL,
    LivingAreaID INT NOT NULL,
    FOREIGN KEY (OrgID) REFERENCES Organism (OrgID),
    FOREIGN KEY (LivingAreaID) REFERENCES LivingArea (LivingAreaID)
);

CREATE TABLE Infection(
    OrgID INT NOT NULL,
    MorbusID INT NOT NULL,
    FOREIGN KEY (OrgID) REFERENCES Organism (OrgID),
    FOREIGN KEY (MorbusID) REFERENCES Morbus (MorbusID)
);


INSERT INTO OrganismType (OrgTypeID, Name, Description) VALUES (1, "Hello", "World");

INSERT INTO LivingStyle (LivingStyleID, Name, Description) VALUES (1, "Carnivore", "Eats meat");
INSERT INTO Soul (SoulID) VALUES (1);


INSERT INTO Organism (OrgID, Name, Description, OrgTypeID, LivingStyleID, SoulID) VALUES (1, "Beast", "Aggressive", 1, 1, 1);
--CREATE TABLE Likes 
--(
--    LikeID	INT NOT NULL,
--    UserID	INT NOT NULL,
--    TweetID	INT,
--    CommentID	INT,
--    PRIMARY KEY (LikeID),
--    FOREIGN KEY (UserID) REFERENCES User (UserID),
--    FOREIGN KEY (TweetID) REFERENCES Tweet (TweetID),
--    FOREIGN KEY (CommentID) REFERENCES Comments (CommentID)
--);