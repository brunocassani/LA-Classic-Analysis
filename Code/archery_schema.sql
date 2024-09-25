-- Create the Mens_Barebow table
CREATE TABLE IF NOT EXISTS Mens_Barebow (
    Match_ID INTEGER PRIMARY KEY,          -- Unique identifier for each match
    Archer_1_Name TEXT NOT NULL,          -- Name of the first archer
    Archer_2_Name TEXT NOT NULL,          -- Name of the second archer
    Archer_1_Score INTEGER NOT NULL,      -- Score of the first archer
    Archer_2_Score INTEGER NOT NULL,      -- Score of the second archer
    Archer_1_Xs INTEGER NOT NULL,         -- Number of Xs hit by the first archer
    Archer_2_Xs INTEGER NOT NULL,         -- Number of Xs hit by the second archer
    Archer_1_Target TEXT NOT NULL,        -- Target of the first archer
    Archer_2_Target TEXT NOT NULL,        -- Target of the second archer
    Archer_1_Riser TEXT NOT NULL,         -- Riser brand of the first archer
    Archer_2_Riser TEXT NOT NULL,         -- Riser brand of the second archer
    Winner TEXT NOT NULL,                 -- Name of the winning archer
    Year INTEGER NOT NULL,                -- Year of the match
    Notes TEXT                            -- Additional notes about the match
);
