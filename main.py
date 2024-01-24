import sqlite3
# relative filepath to database
drinks_fp = 'drinks_database.db'

# connect to sqlite
connection = sqlite3.connect(drinks_fp)

# cursor for moving through the database with sql
cursor = connection.cursor()


def management():
    """ 
    method for managing bar inventory

    This will lead to adding or removing ingredients from drinks_database.db's ingredients table
    """

    print('I am managing the bar')

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
    print('\n')

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
            exit(0)
        case _:
            print('Oops, bad input detected, please feel free to try again')

"""
Future expansion:
favorite drinks
adding/removing recipes
show drinks missing one ingredient
"""
