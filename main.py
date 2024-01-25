import sqlite3
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
        print('5. Go back to bar management')

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
        action = input('Enter the number of the ingredient\'s type')

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

def display_pantry():
    pass

def add_recipe():
    pass


def management():
    """ 
    method for managing bar inventory

    This will lead to adding or removing ingredients from drinks_database.db's ingredients table
    """

    while(1):
        print('--------------------------------------------')
        print('What would you like to do to manage the bar?\n')

        print('1. Add an an ingredient to my bar')
        print('2. Remove an ingredient from my bar')
        print('3. Show me what is currently in my bar')
        print('4. Add a new recipe to my bar (note: if recipe uses a new ingredient, add it first)')
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
                add_recipe()
            case 5: 
                break
            case _:
                print('Oops, bad input detected, please try again')

def random_drink():
    """
    Method that returns a random drink based on current bar inventory

    Inventory is built up in the management() method

    Drinks are found in the drinks_database.db
    """

    print('I am making a drink with what I have')
    


# main runner
print('Welcome to the bar!')

while(1):
    # show the main options
    print('\n---------------\n')
    print('1. Manage my bar')
    print('2. Show me a drink with what I have in my bar right now')
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
            random_drink()
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
