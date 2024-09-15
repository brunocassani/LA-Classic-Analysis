import pandas as pd
import sqlite3

# Load the CSV data into a pandas DataFrame
data = pd.read_csv('Mens_Barebow.csv')

# Connect to SQLite database
conn = sqlite3.connect('archery.db')
cursor = conn.cursor()

# Create Tables if they do not exist
cursor.execute('''CREATE TABLE IF NOT EXISTS Archers (
                    ArcherID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Name TEXT, Riser TEXT, AvgScore REAL, AvgXs REAL
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS Matches (
                    MatchID INTEGER, Archer1ID INTEGER, Archer2ID INTEGER,
                    Archer1Score INTEGER, Archer2Score INTEGER,
                    Archer1Xs INTEGER, Archer2Xs INTEGER, Year INTEGER, Winner TEXT, Notes TEXT,
                    FOREIGN KEY (Archer1ID) REFERENCES Archers(ArcherID),
                    FOREIGN KEY (Archer2ID) REFERENCES Archers(ArcherID)
                )''')

# Insert Archers
for _, row in data.iterrows():
    # Insert Archer 1
    cursor.execute('''INSERT OR IGNORE INTO Archers (Name, Riser) VALUES (?, ?)''',
                   (row['Archer 1 Name'], row['Archer 1 Riser']))
    # Insert Archer 2
    cursor.execute('''INSERT OR IGNORE INTO Archers (Name, Riser) VALUES (?, ?)''',
                   (row['Archer 2 Name'], row['Archer 2 Riser']))

# Insert Matches
for _, row in data.iterrows():
    # Retrieve Archer 1 ID
    archer1 = cursor.execute('''SELECT ArcherID FROM Archers WHERE Name = ?''', (row['Archer 1 Name'],)).fetchone()
    if archer1 is None:
        print(f"Error: Archer 1 '{row['Archer 1 Name']}' not found in database.")
        continue
    archer1_id = archer1[0]
    
    # Retrieve Archer 2 ID
    archer2 = cursor.execute('''SELECT ArcherID FROM Archers WHERE Name = ?''', (row['Archer 2 Name'],)).fetchone()
    if archer2 is None:
        print(f"Error: Archer 2 '{row['Archer 2 Name']}' not found in database.")
        continue
    archer2_id = archer2[0]

    # Insert match data
    cursor.execute('''INSERT INTO Matches (MatchID, Archer1ID, Archer2ID, Archer1Score, Archer2Score, Archer1Xs, Archer2Xs, Year, Winner, Notes)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (row['Match ID'], archer1_id, archer2_id, row['Archer 1 Score'], row['Archer 2 Score'],
                    row['Archer 1 Xs'], row['Archer 2 Xs'], row['Year'], row['Winner'], row['Notes']))

conn.commit()
conn.close()
