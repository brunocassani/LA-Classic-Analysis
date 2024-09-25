import pandas as pd
import sqlite3

df = pd.read_csv('Mens_Barebow.csv')

conn = sqlite3.connect('mens_barebow.db')

# Create a cursor object
cursor = conn.cursor()

# Create a table if it doesn't exist already
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Mens_Barebow (
        Match_ID INTEGER PRIMARY KEY,
        Archer_1_Name TEXT,
        Archer_2_Name TEXT,
        Archer_1_Score INTEGER,
        Archer_2_Score INTEGER,
        Archer_1_Xs INTEGER,
        Archer_2_Xs INTEGER,
        Archer_1_Target TEXT,
        Archer_2_Target TEXT,
        Archer_1_Riser TEXT,
        Archer_2_Riser TEXT,
        Winner TEXT,
        Year INTEGER,
        Notes TEXT
    )
''')

# Insert data into the table
for _, row in df.iterrows():
    cursor.execute('''
        INSERT INTO Mens_Barebow (
            Match_ID, Archer_1_Name, Archer_2_Name, Archer_1_Score, Archer_2_Score, Archer_1_Xs, Archer_2_Xs,
            Archer_1_Target, Archer_2_Target, Archer_1_Riser, Archer_2_Riser, Winner, Year, Notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', tuple(row))

# Commit the changes
conn.commit()

# Close the connection
conn.close()

print('Database created and data inserted successfully.')
