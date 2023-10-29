'''
    Handlers for Operations related to Users: SuperAdmin, Admin, User
'''

import logging
from typing import List, Tuple

from password_generator import PasswordGenerator
from tabulate import tabulate

from database.database_access import DatabaseAccess as DAO
from database.queries import Queries
from models.user import Admin


logger = logging.getLogger(__name__)


class UserController:
    '''User Controller Class'''

    @staticmethod
    def get_user_scores_by_username(username: str):
        '''Return user's scores'''

        data = DAO.read_from_database(Queries.GET_USER_SCORES_BY_USERNAME, (username, ))
        return data

    @staticmethod
    def get_all_users_by_role(role: str) -> List[Tuple]:
        '''Return all users with their details'''

        data = DAO.read_from_database(Queries.GET_USER_BY_ROLE, (role, ))
        return data

    @staticmethod
    def create_admin() -> None:
        '''Create a new Admin Account'''

        logger.debug('Creating Admin')
        print('\n-----Create a new Admin-----\n')

        admin_data = {}
        admin_data['name'] = input('Enter admin name: ').title()
        admin_data['email'] = input('Enter admin email: ').lower()
        admin_data['username'] = input('Enter admin username: ').lower()
        pwo = PasswordGenerator()
        password = pwo.non_duplicate_password(7)
        admin_data['password'] = password

        admin = Admin(admin_data)
        admin.save_user_to_database()

        logger.debug('Admin created')
        print('\nAdmin created successfully!\n')

    @staticmethod
    def delete_user_by_email(role: str):
        '''Delete a User'''

        data = UserController.get_all_users_by_role(role)
        if not data:
            print(f'\nNo {role.title()} Currently\n')
            return

        logger.debug('Deleting %s', {role.title()})
        print(f'\n-----Delete a {role.title()}-----\n')

        print(
            tabulate(
                data,
                headers={
                    'Username': 'username', 
                    'Name': 'name', 
                    'Email': 'email', 
                    'Registration Date': 'registration_date'
                },
                tablefmt='rounded_outline'
            )
        )

        email = input(f'\nEnter {role.title()} Email: ')

        for data in data:
            if data[2] == email:
                break
        else:
            print(f'No such {role.title()}! Please choose from above!!')
            return

        DAO.write_to_database(Queries.DELETE_USER_BY_EMAIL, (email, ))

        logger.debug('User deleted')
        print(f'\n{role.title()}: {email} deleted successfully!\n')
