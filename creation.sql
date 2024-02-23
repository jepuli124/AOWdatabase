CREATE TABLE Organism
(
    OrgID INT NOT NULL,
    Name CHAR(40) NOT NULL,
    Description VARCHAR(65535),
    Type INT NOT NULL,
    PRIMARY KEY (OrgID)
);

INSERT INTO Organism (OrgID, Name, Description, Type) VALUES (1, "Hello", "World", 3);
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