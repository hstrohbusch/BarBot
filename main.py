import sqlite3
import random

# relative filepath to database
drinks_fp = 'drinks_database.db'

# connect to sqlite
connection = sqlite3.connect(drinks_fp)

# cursor for moving through the database with sql
cursor = connection.cursor()

def new_ingredient():
    """
    method for adding an ingredient to the bar

    This handles both ingredients in the database that are not in the 'pantry' as well as 
    adding completely new ingredients
    """
    print("\n---------------------------------------------------------------------------------------------")
    print('Garnishes are not tracked as ingredients, they can be mentioned in a recipe but are not tracked')
    print('Furthermore, when entering an ingredient you should enter the general ingredient type, not a brand name\n')

    while(1):
        
        print('\nHere are some choices\n')
        print('1. Add a Liquor: anything with alcohol in it')
        print('2. Add a Mixer: any liquid that does not contain alcohol')
        print('3. Add Something Else: ingredients essential in a cocktail that does not fall into either category, but is not a garnish')
        print('4. Show me an example: not an ingredient, choose me if you want to see some examples of categorization')
        print('5. Go back to bar management\n')

        action = input('Please enter the Number of your choice:\t')
        
        # make sure it is a number
        try:
            action = int(action)
        except:
            action = -1

        ingredient_type = ''

        if action == 1: ingredient_type = 'Liquor'
        elif action == 2: ingredient_type = 'Mixer'
        elif action == 3: ingredient_type = 'Other'


        if action == 1 or action == 2 or action == 3:
            name = input('Please enter the ingredients generic name:\t')
            # string check not necessary, all inputs are strings
            # need to otherwise trust the user

            # try to insert new ingredient, fails if already present
            # if fail, it is already present just update it to be in the pantry

            try:
                cursor.execute('INSERT INTO ingredients (name, type, pantry) VALUES (?, ?, ?)', (name, ingredient_type, 1))
                print('New '+ingredient_type+' '+name+' added, time to make a new recipe with it!')

                connection.commit()
                print('Brand new ingredients are exciting!')
                
            except sqlite3.IntegrityError:
                try:
                    # Use a parameterized query to safely update data
                    cursor.execute('UPDATE ingredients SET pantry = 1 WHERE name = ? AND type = ?', (name, ingredient_type))
                    # Commit the changes
                    connection.commit()

                    print(name+' which is in the category '+ingredient_type+' was added to your pantry!')

                except sqlite3.Error as e:
                    print(f'Error updating pantry status: {e}')

            # try:
            #     # Use a parameterized query to safely insert data
            #     cursor.execute('INSERT INTO ingredients (name, type, pantry) VALUES (?, ?, ?)', (name, ingredient_type, 1))
            #     # Commit the changes
            #     connection.commit()
            #     print(f'Ingredient {name} added successfully.')
            # except sqlite3.Error as e:
            #     print(f'Error adding ingredient: {e}')

            
        elif action == 4:
            print()
            print('Angostora Bitters -> a liquor named bitters')
            print('Captain Morgan -> A liquor named Spiced Rum')
            print('Chambord -> A liquor called Raspberry Liqueur')
            print('Dole Pineapple Juice -> a mixer called Pineapple Juice')
            print('Monin Mango Syrup -> a mixer named Mango Syrup')
            print('Mint Leaf -> a garnish, should not be entered')
            print('Mint Sprig -> if it intended to be  used as an ingredient, such as for a mint juleep, other named mint')
        elif action == 5: 
            break
        else:
            print('Oops, bad input detected, please try again')

def remove_ingredient():
    """
    A method for removing ingredients from the user's pantry
    
    does not actually remove the ingredient from the database, just sets it to not be present

    This makes it easier for things like recipes to remain after an ingredient is temporarily removed

    It also makes re-adding an ingredient much simpler
    """
    print('\n----------------------------')
    print('Time to remove an ingredient from my pantry\n')
    
    while(1):
        print('1. Liquor')
        print('2. Mixer')
        print('3. Other')
        print('4. I am done removing ingredients from my pantry\n')
        action = input('Enter the number of the ingredient\'s type\t')

        try:
            action = int(action)
        except:
            action = -1

        ingredient_type = ''

        if action == 1: ingredient_type = 'Liquor'
        elif action == 2: ingredient_type = 'Mixer'
        elif action == 3: ingredient_type = 'Other'

        if action == 1 or action == 2 or action == 3:
            name = input('Please enter the ingredients generic name:\t')

            try:
                # Use a parameterized query to safely update data
                cursor.execute('UPDATE ingredients SET pantry = 0 WHERE name = ? AND type = ?', (name,ingredient_type))
                # Commit the changes
                connection.commit()

                print(name+' which is in the category '+ingredient_type+' was removed from pantry!')

            except sqlite3.Error as e:
                print(f'Error updating pantry status: {e}')
        elif action == 4:
            break
        else:
            print('Invalid ingredient type')

def get_ingredients_by_type(ingredient_type):
    """
    Retrieve ingredients of a specific type from the 'ingredients' table.\n
    Type must be 'Liquor' 'Mixer' or 'Other'\n
    Returns None in case of an error
    """

    if not (ingredient_type == 'Liquor' or ingredient_type == 'Mixer' or ingredient_type == 'Other'):
        print('Incorrect Ingredient type, tried to find: '+ingredient_type)
        return None

    try:
        # Use a parameterized query to safely retrieve data based on type
        cursor.execute("SELECT * FROM ingredients WHERE type = ?", (ingredient_type,))
        ingredients = cursor.fetchall()
        return ingredients
    except sqlite3.Error as e:
        print(f"Error retrieving "+ingredient_type+" type ingredients: {e}")
        return None

def display_pantry():
    """
    returns ingredients listed as being in the users pantry
    """
    print('-------------------------\n')
    print('Current ingredients in pantry\n')
    print('Liquors:')
    liquors = get_ingredients_by_type('Liquor')
    
    if liquors is not None:
        for l in liquors:
            if l[3]: print(l[1])
    else:
        print('No liquors currently in pantry')

    print('Mixers:')
    mixers = get_ingredients_by_type('Mixer')
    
    if mixers is not None:
        for m in mixers:
            if m[3]: print(m[1])
    else:
        print('No mixers currently in pantry')

    print('Others:')
    others = get_ingredients_by_type('Other')
    
    if others is not None:
        for o in others:
            if o[3]: print(o[1])
    else:
        print('No others currently in pantry')


def display_ingredients():
    """
    returns every ingredient in the ingredients table
    """
    # cursor.execute("SELECT * FROM ingredients")
    # temp = cursor.fetchall()
    # for i in temp:
    #     print(i)

    print('-------------------------\n')
    print('Current known ingredients\n')
    print('Liquors:')
    liquors = get_ingredients_by_type('Liquor')

    if liquors is not None:
        for l in liquors:
            print(l[1])
    else:
        print('No liquors currently known')

    print('\nMixers:')
    mixers = get_ingredients_by_type('Mixer')

    if mixers is not None:
        for m in mixers:
            print(m[1])
    else:
        print('No mixers currently known')

    print('\nOthers:')
    others = get_ingredients_by_type('Other')

    if others is not None:
        for o in others:
            print(o[1])
    else:
        print('No mixers currently known')


def management():
    """ 
    method for managing bar inventory

    This will lead to adding or removing ingredients from drinks_database.db's ingredients table
    """

    while(1):
        print('--------------------------------------------')
        print('What would you like to do to manage the bar?\n')

        print('1. Add an an ingredient to my pantry')
        print('2. Remove an ingredient from my pantry')
        print('3. Show me what is currently in my pantry')
        print('4. Show me all currently "known" ingredients')
        print('5. Nevermind, back to the main menu')

        action = input('Please enter your desired input as a number\t')
        print()

        # make sure it is a number
        try:
            action = int(action)
        except:
            action = -1

        # do appropriate action, expand as needed
        match action:
            case 1:
                new_ingredient()
            case 2: 
                remove_ingredient()
            case 3:
                display_pantry()
            case 4:
                display_ingredients()
            case 5: 
                break
            case _:
                print('Oops, bad input detected, please try again')

def add_drink():
    """
    Add a new drink to the 'drinks', 'ingredients', and 'drink_ingredients' tables.
    """
    # get user input
    print('---------------------------------------')
    name = input('What is the name of this new drink?\t')
    description = input('\nEnter a description of this drink\t')
    favorite = 0
    ingredients_list = [] # ingredient, ingredient type, measure

    print('\nNow we will enter ingredients')
    print('First enter the ingredients type: 1 for Liquor, 2 for Mixer, 3 for Other')
    print('Then enter the ingredient\'s generic name (korbel -> brandy) CASE SENSITIVE')
    print('Then enter the appropriate measurement (2 ounces, 10 ml, 2 sprigs, etc)\n')

    done = False
    while not done:
        action = input('Enter the ingredient type number\t')
        try:
            action = int(action)
        except:
            action = -1

        ingredient_type = ''

        if action == 1: ingredient_type = 'Liquor'
        elif action == 2: ingredient_type = 'Mixer'
        elif action == 3: ingredient_type = 'Other'
        else:
            print('incorrect ingredient type')
            continue
        
        ingredient = input('Enter the ingredient\'s generic name\t')
        measure = input('Enter the measurement of the ingredient\t')

        combined = (ingredient, ingredient_type, measure)
        ingredients_list.append(combined)
        print('Added '+str(combined)+' to recipe\n')

        action = input('Add another ingredient? y/n\t')

        if action == 'n' or action == 'N':
            done = True


    # Now do the actual insertion
    try:
        # Insert the drink details into the 'drinks' table
        cursor.execute('INSERT INTO drinks (name, description, favorite) VALUES (?, ?, ?)',
                       (name, description, favorite))
        # Get the last inserted row id (drink_id)
        drink_id = cursor.lastrowid

        for ingredient, ingredient_type, measure in ingredients_list:
            # Validate the ingredient and type
            cursor.execute("""
                SELECT id FROM ingredients 
                WHERE name = ? AND type = ?
            """, (ingredient, ingredient_type))
            result = cursor.fetchone()

            if not result:
                print(f"Error: Ingredient '{ingredient}' with type '{ingredient_type}' not found in the 'ingredients' table.")
                # Rollback the transaction and exit the method
                connection.rollback()
                return

            ingredient_id = result[0]

            # Insert the drink recipe into the 'drink_ingredients' table
            cursor.execute('INSERT INTO drink_ingredients (drink_id, ingredient_id, measure) VALUES (?, ?, ?)',
                           (drink_id, ingredient_id, measure))

        # Commit the changes
        connection.commit()
        print(f'Drink "{name}" added successfully.')
    except sqlite3.Error as e:
        print(f'Error adding drink: {e}')

def every_drink():
    """
    Print information about all known drinks.
    """
    try:
        # Fetch all drinks from the 'drinks' table
        cursor.execute('SELECT * FROM drinks')
        drinks = cursor.fetchall()

        if not drinks:
            print('No drinks found.')
            return

        print('All Known Drinks:')
        print('-' * 40)

        for drink in drinks:
            drink_id, name, description, favorite = drink
            # print(f'Drink ID: {drink_id}')
            print(f'Name: {name}')
            print(f'Description: {description}')
            # print(f'Favorite: {"Yes" if favorite else "No"}')

            # Fetch ingredients for the current drink
            cursor.execute('''
                SELECT i.name, di.measure
                FROM drink_ingredients di
                JOIN ingredients i ON di.ingredient_id = i.id
                WHERE di.drink_id = ?
            ''', (drink_id,))
            ingredients = cursor.fetchall()

            print('Ingredients:')
            for ingredient, measure in ingredients:
                print(f'  - {ingredient}: {measure}')

            print('-' * 40)

    except sqlite3.Error as e:
        print(f'Error fetching drinks: {e}')

def favorite_drinks():
    # TODO implement, shows all favorite drinks (field in drinks schema)
    pass

def random_drink():
    """
    Method that returns a random drink based on current bar inventory

    Inventory is built up in the management() method

    Drinks are found in the drinks_database.db
    """
    try:
        # Fetch drinks with ingredients from the 'drink_ingredients' and 'ingredients' tables
        cursor.execute('''
            SELECT d.id, d.name, d.description, i.name AS ingredient_name, di.measure
            FROM drinks d
            JOIN drink_ingredients di ON d.id = di.drink_id
            JOIN ingredients i ON di.ingredient_id = i.id
            WHERE d.id IN (
                SELECT di.drink_id
                FROM drink_ingredients di
                JOIN ingredients i ON di.ingredient_id = i.id
                GROUP BY di.drink_id
                HAVING COUNT(i.pantry) = SUM(i.pantry)
            )
        ''')
        drink_ingredients = cursor.fetchall()

        if not drink_ingredients:
            print('No drinks found with all ingredients in the pantry.')
            return None

        # Group drink ingredients by drink_id
        drinks_dict = {}
        for drink_id, drink_name, drink_description, ingredient_name, measure in drink_ingredients:
            if drink_id not in drinks_dict:
                drinks_dict[drink_id] = {
                    'name': drink_name,
                    'description': drink_description,
                    'ingredients': []
                }
            drinks_dict[drink_id]['ingredients'].append((ingredient_name, measure))

        # Randomly select a drink
        random_drink = random.choice(list(drinks_dict.values()))

        print('Random Drink from Pantry:')
        print('-' * 40)
        print(f'Name: {random_drink["name"]}')
        print(f'Description: {random_drink["description"]}')

        print('Ingredients:')
        for ingredient, measure in random_drink['ingredients']:
            print(f'  - {ingredient}: {measure} ounces')

        print('-' * 40)

        return random_drink

    except sqlite3.Error as e:
        print(f'Error fetching random drink: {e}')
        return None

def recipe():
    """
    method handler for things directly related to recipes
    """

    while(1):
        print('--------------------------------------------')
        print('What recipe would you like to see?\n')

        print('1. I want to add a new drink')
        print('2. Show me every drink recipe I have')
        print('3. Show me my favorite drinks')
        print('4. Show me a random drink I can make with what I have in my pantry')
        print('5. Nevermind, go back to the main menu')


        action = input('Please enter your desired input as a number\t')
        print()

        # make sure it is a number
        try:
            action = int(action)
        except:
            action = -1

        # do appropriate action, expand as needed
        match action:
            case 1:
                add_drink()
            case 2: 
                every_drink()
            case 3:
                favorite_drinks()
            case 4:
                random_drink()
            case 5:
                break
            case _:
                print('Oops, bad input detected, please try again')

# main runner
print('Welcome to the bar!')

while(1):
    # show the main options
    print('\n---------------\n')
    print('1. Manage my bar')
    print('2. Recipe Book')
    print('3. Exit\n')

    # take in input
    action = input('Please enter your desired input as a number\t')
    print()

    # make sure it is a number
    try:
        action = int(action)
    except:
        action = -1

    # do appropriate action, expand as needed
    match action:
        case 1:
            management()
        case 2: 
            recipe()
        case 3:
            print('Thank you, see you again later!')
            connection.close()
            exit(0)
        case _:
            print('Oops, bad input detected, please try again')

"""
Future expansion:
favorite drinks
adding/removing recipes
show drinks missing one ingredient
"""
