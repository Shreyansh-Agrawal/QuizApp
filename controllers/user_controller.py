'''Controllers for Operations related to Users: SuperAdmin, Admin, User'''

import logging
import sqlite3
from typing import List, Tuple

from password_generator import PasswordGenerator

from database.database_access import DatabaseAccess as DAO
from constants.queries import Queries
from models.user import Admin
from utils import validations
from utils.custom_error import LoginError
from utils.pretty_print import pretty_print


logger = logging.getLogger(__name__)

def get_user_scores_by_username(username: str):
    '''Return user's scores'''

    data = DAO.read_from_database(Queries.GET_USER_SCORES_BY_USERNAME, (username, ))
    return data


def get_all_users_by_role(role: str) -> List[Tuple]:
    '''Return all users with their details'''

    data = DAO.read_from_database(Queries.GET_USER_BY_ROLE, (role, ))
    return data


def create_admin() -> None:
    '''Create a new Admin Account'''

    logger.debug('Creating Admin')
    print('\n-----Create a new Admin-----\n')

    admin_data = {}
    admin_data['name'] = validations.validate_name('Enter admin name: ')
    admin_data['email'] = validations.validate_email('Enter admin email: ')
    admin_data['username'] = validations.validate_username('Create admin username: ')
    pwo = PasswordGenerator()
    password = pwo.non_duplicate_password(7)
    admin_data['password'] = password

    admin = Admin(admin_data)

    try:
        admin.save_user_to_database()
    except sqlite3.IntegrityError as e:
        raise LoginError('\nUser already exists! Try with different credentials...') from e

    logger.debug('Admin created')
    print('\nAdmin created successfully!\n')


def delete_user_by_email(role: str):
    '''Delete a User'''

    data = get_all_users_by_role(role)
    if not data:
        print(f'\nNo {role.title()} Currently\n')
        return

    logger.debug('Deleting %s', {role.title()})
    print(f'\n-----Delete a {role.title()}-----\n')

    pretty_print(data=data, headers=['Username', 'Name', 'Email', 'Registration Date'])

    email = validations.validate_email(prompt=f'\nEnter {role.title()} Email: ')

    for data in data:
        if data[2] == email:
            break
    else:
        print(f'No such {role.title()}! Please choose from above!!')
        return

    DAO.write_to_database(Queries.DELETE_USER_BY_EMAIL, (email, ))

    logger.debug('User deleted')
    print(f'\n{role.title()}: {email} deleted successfully!\n')
