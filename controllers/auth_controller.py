'''
    Handlers for user authentication
'''
import hashlib
import maskpass

from database.database_access import DatabaseAccess as DAO
from database.queries import Queries
from models.users import User

class Authenticate:
    '''Authenticates user'''

    @staticmethod
    def login():
        '''Method for user login'''
        username = input("Enter username: ")
        user_data = DAO.read_from_database(Queries.GET_CREDENTIALS, (username, ))

        if not user_data:
            print("Account not found! Please signup...")
            return

        password = maskpass.askpass(mask="*")
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        user_password, role, is_password_changed = user_data[0]

        if user_password != hashed_password:
            print("Invalid Credentials!")
            return

        print("Successfully Logged In!")
        return role, is_password_changed

    @staticmethod
    def signup():
        '''Method for signup, only for user'''

        user_data = {}
        user_data['name'] = input("Enter your name: ")
        user_data['email'] = input("Enter your email: ")
        user_data['username'] = input("Enter your username: ")
        password = maskpass.askpass(mask="*")
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        user_data['password'] = hashed_password

        user = User(user_data)
        user.save_user_to_database()
        print("Account created successfully! Please login...\n")
