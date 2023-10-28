'''
    Handlers for super admin operations
'''

from typing import List, Tuple

from password_generator import PasswordGenerator
from tabulate import tabulate

from database.database_access import DatabaseAccess as DAO
from database.queries import Queries
from models.user import Admin


class SuperAdminController:
    '''Super Admin Controller Class'''

    @staticmethod
    def create_admin() -> None:
        '''Create a new Admin Account'''

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

        print('\nAdmin created successfully!\n')

    @staticmethod
    def get_all_admins() -> List[Tuple]:
        '''Return all admins with their details'''

        role = 'admin'
        data = DAO.read_from_database(Queries.GET_USER_BY_ROLE, (role, ))
        return data

    @staticmethod
    def delete_admin() -> None:
        '''Delete an Admin'''

        print('\n-----Delete Admin-----\n')

        data = SuperAdminController.get_all_admins()

        if not data:
            print('\nNo Admin Currently, Please Create One!\n')
            return

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

        email = input('\nEnter Admin Email: ')

        for data in data:
            if data[2] == email:
                break
        else:
            print('No such admin! Please choose from above!!')
            return

        DAO.write_to_database(Queries.DELETE_USER_BY_EMAIL, (email, ))
        print(f'\nAdmin: {email} deleted successfully!\n')
