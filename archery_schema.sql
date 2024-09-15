CREATE TABLE Archers (
    ArcherID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT,
    Riser TEXT,
    AvgScore REAL,
    AvgXs REAL
);

CREATE TABLE Matches (
    MatchID INTEGER,
    Archer1ID INTEGER,
    Archer2ID INTEGER,
    Archer1Score INTEGER,
    Archer2Score INTEGER,
    Archer1Xs INTEGER,
    Archer2Xs INTEGER,
    Year INTEGER,
    Winner TEXT,
    Notes TEXT,
    FOREIGN KEY (Archer1ID) REFERENCES Archers(ArcherID),
    FOREIGN KEY (Archer2ID) REFERENCES Archers(ArcherID)
);

