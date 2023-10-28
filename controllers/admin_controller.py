'''
    Handlers for admin operations
'''

from tabulate import tabulate
from database.database_access import DatabaseAccess as DAO
from database.queries import Queries
from models.quiz import Category, Question, Option

class AdminController:
    '''Admin Controller Class'''

    @staticmethod
    def get_all_users():
        '''Return all users with their details'''

        role = 'user'
        data = DAO.read_from_database(Queries.GET_USER_BY_ROLE, (role, ))
        return data

    @staticmethod
    def get_all_categories():
        '''Return all Quiz Categories'''

        data = DAO.read_from_database(Queries.GET_ALL_CATEGORIES)
        return data

    @staticmethod
    def get_all_questions():
        '''Return all quiz questions'''

        data = DAO.read_from_database(Queries.GET_ALL_QUESTIONS)
        return data

    @staticmethod
    def create_category(username: str):
        '''Add a Quiz Category'''

        data = DAO.read_from_database(Queries.GET_ADMIN_ID_NAME_BY_USERNAME, (username, ))
        admin_id, admin_name = data[0]

        print('\n-----Create a new Quiz Category-----\n')

        category_data = {}
        category_data['admin_id'] = admin_id
        category_data['admin_name'] = admin_name
        category_data['category_name'] = input('Enter Category Name: ').title()

        category = Category(category_data)
        category.save_to_database()

    @staticmethod
    def create_question(username: str):
        '''Add Questions in a Category'''

        data = AdminController.get_all_categories()
        if not data:
            print('\nNo Categories Currently, Please add a Category!!\n')
            return

        print('\n-----Create a new Quiz Question-----\n')

        print(
            tabulate(
                data,
                headers={
                    'Category': 'category_name', 
                    'Created By': 'admin_name', 
                },
                tablefmt='rounded_outline'
            )
        )

        category_name = input('\nEnter Category Name: ')

        for data in data:
            if data[0] == category_name:
                break
        else:
            print('No such Category! Please choose from above!!')
            return

        category_id = DAO.read_from_database(Queries.GET_CATEGORY_ID_BY_NAME, (category_name, ))
        data = DAO.read_from_database(Queries.GET_ADMIN_ID_NAME_BY_USERNAME, (username, ))
        admin_id, admin_name = data[0]

        question_data = {}
        question_data['category_id'] = category_id[0][0]
        question_data['admin_id'] = admin_id
        question_data['admin_name'] = admin_name
        question_data['question_text'] = input('Enter Question Text: ').title()
        question_data['question_type'] = input('Enter Question Type (MCQ, T/F, ONE WORD): ').upper()

        question = Question(question_data)

        match question_data['question_type']:
            case 'MCQ':
                for _ in range(4):
                    option_data = {}
                    option_data['question_id'] = question.question_id
                    option_data['option_text'] = input('Enter Option Text: ').title()
                    option_data['is_correct'] = int(input('Enter 1 if correct else 0: '))

                    option = Option(option_data)
                    question.add_option(option)
            case 'T/F' | 'ONE WORD':
                option_data = {}
                option_data['question_id'] = question.question_id
                option_data['option_text'] = input('Enter Option Text: ').title()
                option_data['is_correct'] = 1

                option = Option(option_data)
                question.add_option(option)
            case _:
                print('Invalid Type!')

        question.save_to_database()

    @staticmethod
    def delete_user():
        '''Delete a User'''

        data = AdminController.get_all_users()
        if not data:
            print('\nNo User Currently\n')
            return

        print('\n-----Delete a User-----\n')

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

        email = input('\nEnter User Email: ')

        for data in data:
            if data[2] == email:
                break
        else:
            print('No such User! Please choose from above!!')
            return

        DAO.write_to_database(Queries.DELETE_USER_BY_EMAIL, (email, ))
        print(f'\nUser: {email} deleted successfully!\n')
