import sqlite3

# Define the database file
db_path = "salvatori_butchers.db"

# Connect to SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Read and execute the schema file
with open("schema.sql", "r") as f:
    schema = f.read()
cursor.executescript(schema)

# Commit and close
conn.commit()
conn.close()

print("Database schema has been applied successfully.")
