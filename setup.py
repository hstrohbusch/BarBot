import sqlite3

# relative filepath to database
drinks_fp = 'drinks_database.db'

# connect to sqlite
connection = sqlite3.connect(drinks_fp)

# cursor for moving through the database with sql
cursor = connection.cursor()

# SQL statements for creating the ingredients table
create_ingredients_table = '''
    CREATE TABLE IF NOT EXISTS ingredients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT CHECK(type IN ('Liquor', 'Mixer', 'Other')),
        pantry INTEGER NOT NULL,
        UNIQUE(name, type)
    )
'''

# SQL statements for creating the drinks table
create_drinks_table = '''
    CREATE TABLE IF NOT EXISTS drinks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        description TEXT,
        favorite REAL
    )
'''

create_drink_ingredients_table = '''
    CREATE TABLE IF NOT EXISTS drink_ingredients (
        drink_id INTEGER,
        ingredient_id INTEGER,
        measure TEXT,
        PRIMARY KEY (drink_id, ingredient_id),
        FOREIGN KEY (drink_id) REFERENCES drinks (id),
        FOREIGN KEY (ingredient_id) REFERENCES ingredients (id)
)
'''

# Execute the CREATE TABLE statements separately
cursor.execute(create_ingredients_table)
cursor.execute(create_drinks_table)
cursor.execute(create_drink_ingredients_table)

# commit and close the changes
connection.commit()
connection.close()