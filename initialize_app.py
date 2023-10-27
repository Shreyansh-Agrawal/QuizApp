'''
    Runs at the start to create super admin and other tables in database
'''

from super_admin_credentials import SuperAdminCredentials
from models.users import SuperAdmin
from database.queries import InitializationQueries
from database.database_access import DatabaseAccess as DAO


class Initializer:
    '''Class containing methods to create super admin'''

    @staticmethod
    def create_super_admin():
        '''method to create a super admin '''

        name, email, username, password = SuperAdminCredentials.credentials.values()

        super_admin_obj = {}
        super_admin_obj['name'] = name
        super_admin_obj['email'] = email
        super_admin_obj['username'] = username
        super_admin_obj['password'] = password

        super_admin = SuperAdmin(super_admin_obj)
        super_admin.save_user_to_database()
        print("Super Admin created!")

    @staticmethod
    def initialize_app():
        '''method to initialize application'''

        InitializeDatabase.create_users_table()
        InitializeDatabase.create_credentials_table()
        InitializeDatabase.create_scores_table()
        InitializeDatabase.create_categories_table()
        InitializeDatabase.create_questions_table()
        InitializeDatabase.create_options_table()
        Initializer.create_super_admin()


class InitializeDatabase:
    '''Class to create tables for database'''

    @staticmethod
    def create_users_table():
        '''method to create users table'''

        DAO.write_to_database(InitializationQueries.CREATE_USERS_TABLE)

    @staticmethod
    def create_credentials_table():
        '''method to create credentials table'''

        DAO.write_to_database(InitializationQueries.CREATE_CREDENTIALS_TABLE)

    @staticmethod
    def create_scores_table():
        '''method to create scores table'''

        DAO.write_to_database(InitializationQueries.CREATE_SCORES_TABLE)

    @staticmethod
    def create_categories_table():
        '''method to create categories table'''

        DAO.write_to_database(InitializationQueries.CREATE_CATEGORIES_TABLE)

    @staticmethod
    def create_questions_table():
        '''method to create questions table'''

        DAO.write_to_database(InitializationQueries.CREATE_QUESTIONS_TABLE)

    @staticmethod
    def create_options_table():
        '''method to create options table'''

        DAO.write_to_database(InitializationQueries.CREATE_OPTIONS_TABLE)
