'''
    Assign menu as per the role
'''
from utils import prompts

class Menu:
    '''Menu class to assign menu'''

    @staticmethod
    def super_admin_menu(username: str):
        '''Menu for Super Admin'''

        print('----Super Admin Dashboard----')
        print(f'\n----Welcome {username}!----\n')

        while True:
            user_choice = input(prompts.SUPER_ADMIN_PROMPTS)
            match user_choice:
                case '1':
                    print("Creating a new admin...")
                case '2':
                    print("Viewing all admins...")
                case '3':
                    print("Deleting an admin...")
                case 'q':
                    break
                case _:
                    print('Wrong input! Please choose from the above given options...')

    @staticmethod
    def admin_menu(username: str, is_password_changed: int):
        '''Menu for Admin'''

        print('----Admin Dashboard----')
        print(f'\n----Welcome {username}!----\n')

        if not is_password_changed:
            print('Please change your password')

        while True:
            user_choice = input(prompts.ADMIN_PROMPTS)
            match user_choice:
                case '1':
                    print("Managing users...")

                    while True:
                        user_sub_choice = input(prompts.ADMIN_MANAGE_USER_PROMPTS)
                        match user_sub_choice:
                            case '1':
                                print("Viewing all users...")
                            case '2':
                                print("Deleting a user...")
                            case 'q':
                                break
                            case _:
                                print('Wrong input! Please choose from the above given options...')
                case '2':
                    print("Managing quizzes...")

                    while True:
                        user_sub_choice = input(prompts.ADMIN_MANAGE_QUIZZES_PROMPTS)
                        match user_sub_choice:
                            case '1':
                                print("Viewing all categories...")
                            case '2':
                                print("Viewing questions...")
                            case '3':
                                print("Adding a new category...")
                            case '4':
                                print("Adding a question...")
                            case 'q':
                                break
                            case _:
                                print('Wrong input! Please choose from the above given options...')
                case 'q':
                    break
                case _:
                    print('Wrong input! Please choose from the above given options...')

    @staticmethod
    def user_menu(username: str):
        '''Menu for User'''

        print('----User Dashboard----')
        print(f'\n----Welcome {username}!----\n')

        while True:
            user_choice = input(prompts.USER_PROMPTS)
            match user_choice:

                case '1':
                    print("Quiz Starting...")
                case '2':
                    print("Leaderboard...")
                case '3':
                    print("Your scores History...")
                case 'q':
                    break
                case _:
                    print('Wrong input! Please choose from the above given options...')

    @staticmethod
    def assign_menu(data):
        '''Assign menu according to the role'''

        username, role, is_password_changed = data
        match role:
            case 'super admin':
                Menu.super_admin_menu(username)
            case 'admin':
                Menu.admin_menu(username, is_password_changed)
            case 'user':
                Menu.user_menu(username)
            case _:
                print('Invalid Role!: ', role)
