'''
    Runs at the start to create super admin and other tables in database
'''
import logging
import sqlite3
import super_admin_credentials
from database.database_access import DatabaseAccess as DAO
from database.queries import InitializationQueries
from models.users import SuperAdmin


logger = logging.getLogger(__name__)

class Initializer:
    '''Class containing methods to create super admin'''

    @staticmethod
    def create_super_admin():
        '''method to create a super admin '''

        super_admin_obj = {}
        super_admin_obj['name'] = super_admin_credentials.NAME
        super_admin_obj['email'] = super_admin_credentials.EMAIL
        super_admin_obj['username'] = super_admin_credentials.USERNAME
        super_admin_obj['password'] = super_admin_credentials.HASHED_PASSWORD

        super_admin = SuperAdmin(super_admin_obj)
        super_admin.save_user_to_database()
        print('Super Admin created!')

    @staticmethod
    def initialize_app():
        '''method to initialize application'''

        InitializeDatabase.create_users_table()
        InitializeDatabase.create_credentials_table()
        InitializeDatabase.create_scores_table()
        InitializeDatabase.create_categories_table()
        InitializeDatabase.create_questions_table()
        InitializeDatabase.create_options_table()

        try:
            Initializer.create_super_admin()
        except sqlite3.IntegrityError:
            print("Super Admin Already Created")

        logger.debug('Initialization Complete')
        print('\nInitialization Complete!\n')


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
