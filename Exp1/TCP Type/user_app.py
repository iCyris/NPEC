"""

Login System (with sqlite3)

Author: Cyris

"""

import sqlite3
import os.path
import getpass
from argparse import ArgumentParser

DATABASE = 'user.sql'

def connect_db():
    """
    Connect to database
    """
    cd = sqlite3.connect(DATABASE)
    cd.row_factory = sqlite3.Row
    # It supports mapping access by column name and index, iteration, representation, equality testing and len().

    return cd

def init_db(filename):
    """
    Initalize the database.
    """
    db = connect_db()
    with open(filename, mode='r') as f:
        db.cursor().executescript(f.read())
    c_table = 'create table users (username text, password text)'
    cursor = db.cursor()
    cursor.execute(c_table)
    cursor.close()
    db.commit()
    print('Database initialized.')

def register(username, password):
    """
    Add new user to database.
    """
    #username, password = user_input()
    db = connect_db()
    cursor = db.execute('select username from users where username = (?) ', (username,))
    if (cursor.fetchone()):
        #print("The username already exits.")
        return False
    db.execute('INSERT INTO users'
                '(username, password) VALUES (?, ?)', [username, password])
    db.commit()
    #print('Register Success!')
    return True

def login():
    """
    Login function (for test).
    """
    username, password = user_input()
    return check_user(username, password)

def user_input():
    """
    Username turn to lowercase.
    Use getpass to make the entering password experience better.
    """
    username = input('User name: ')
    username = username.lower()
    password = getpass.getpass('Password: ')
    return username, password

def check_user(username, password):
    """
    Check if the user exits and the password is correct.
    """
    db = connect_db()
    cursor = db.cursor()
    try:         
        cursor = db.execute(
            'select username, password from users where username = (?)',
            (username,)
        )
        if password == cursor.fetchone()[1]:
            return True
        else:
            return False
    except Exception as e:
        #print("Password error or the User dosn't exit, Please try again.")
        return False

def user_list():
    """
    Show all the Users
    """
    db = connect_db()
    sql = 'select * from users'
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    print (result)

if __name__ == "__main__":
    parser = ArgumentParser(description="Login system test")
    parser.add_argument('--init',
                        help='initialize the database',
                        action='store_true')
    parser.add_argument('--register',
                        help='create a new user',
                        action='store_true')
    parser.add_argument('--login',
                        help='Login',
                        action='store_true')
    parser.add_argument('--show',
                        help='Show all the users',
                        action='store_true')
    args = parser.parse_args()

    if args.init:
        if os.path.isfile(DATABASE):
            print('A database already exists!')
        else:
            init_db('user.sql')

    if args.register:
        register()
    
    if args.login:
        if(login()):
            print("Success login!")
        else:
            print("Login False...")

    if args.show:
        user_list()


