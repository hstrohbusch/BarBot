import sqlite3

# relative filepath to database
drinks_fp = 'drinks_database.db'

# connect to sqlite
connection = sqlite3.connect(drinks_fp)

# cursor for moving through the database with sql
cursor = connection.cursor()

# SQL statements for creating the ingredients table
create_ingredients_table = '''
    CREATE TABLE ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT CHECK(type IN ('liquor', 'mixer', 'other')),
        pantry INTEGER NOT NULL
    )
'''

# SQL statements for creating the drinks table
create_drinks_table = '''
    CREATE TABLE drinks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        ingredient_id INTEGER,
        measure REAL,
        FOREIGN KEY (ingredient_id) REFERENCES ingredients (id)
    )
'''

# Execute the CREATE TABLE statements separately
cursor.execute(create_ingredients_table)
cursor.execute(create_drinks_table)

# commit and close the changes
connection.commit()
connection.close()