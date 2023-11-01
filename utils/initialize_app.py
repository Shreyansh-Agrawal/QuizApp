'''Runs at the start to create super admin and other tables in database'''

import hashlib
import logging
import os
from pathlib import Path
import sqlite3

from dotenv import load_dotenv

from database.database_access import DatabaseAccess as DAO
from constants.queries import InitializationQueries
from models.user import SuperAdmin
from utils.custom_error import DuplicateEntryError


dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)

logger = logging.getLogger(__name__)


class Initializer:
    '''Class containing methods to create super admin'''

    @staticmethod
    def create_super_admin():
        '''method to create a super admin '''

        logger.debug('Creating Super Admin')

        super_admin_data = {}
        super_admin_data['name'] = os.getenv('SUPER_ADMIN_NAME')
        super_admin_data['email'] = os.getenv('SUPER_ADMIN_EMAIL')
        super_admin_data['username'] = os.getenv('SUPER_ADMIN_USERNAME')

        password = os.getenv('SUPER_ADMIN_PASSWORD')
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

        super_admin_data['password'] = hashed_password
        super_admin = SuperAdmin(super_admin_data)
        try:
            super_admin.save_user_to_database()
        except sqlite3.IntegrityError as e:
            raise DuplicateEntryError('Super Admin Already exists!') from e

        logger.debug('Created Super Admin')
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
        except DuplicateEntryError:
            logger.debug('Super Admin Present')

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
