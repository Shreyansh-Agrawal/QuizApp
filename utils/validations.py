'''Input Validations'''

import re
import functools
from utils.custom_error import InvalidInputError


def error_handling(func):
    '''A decorator for error handling for regex validator'''

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
        except InvalidInputError as e:
            print(f'\n{e} Please try again...\n')
            return False

        return res

    return wrapper


@error_handling
def validator(pattern: str, data: str, error_msg: str):
    '''Validates using: re.fullmatch(regex, data)'''    

    match_obj = re.fullmatch(pattern, data)

    if not match_obj:
        raise InvalidInputError(error_msg)

    return True


def validate_name(prompt: str):
    '''Checks user's name, category name input'''

    result = False
    name = ''
    regex_pattern = '[A-Za-z\s]{2,25}'

    while not result:
        name = input(prompt).title()
        result = validator(pattern=regex_pattern, data=name, error_msg='Invalid name!')

    return name


def validate_email(prompt: str):
    '''Checks email input'''

    result = False
    email = ''
    regex_pattern = '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}'

    while not result:
        email = input(prompt).lower()
        result = validator(pattern=regex_pattern, data=email, error_msg='Invalid email!')

    return email


def validate_username(prompt: str):
    ''' Checks username input -
    
        limited to 30 characters
        must contain only letters, numbers, periods, and underscores
    '''

    result = False
    username = ''
    regex_pattern = '[A-Za-z0-9._]{2,30}'

    while not result:
        username = input(prompt).lower()
        result = validator(pattern=regex_pattern, data=username, error_msg='Invalid username!')

    return username


def validate_question_text(prompt: str):
    '''Checks question text'''

    result = False
    question = ''
    regex_pattern = '.{10,100}'

    while not result:
        question = input(prompt).title()
        result = validator(pattern=regex_pattern, data=question, error_msg='Invalid question!')

    return question


def validate_option_text(prompt: str):
    '''Checks option text'''

    result = False
    option_text = ''
    regex_pattern = '.{1,50}'

    while not result:
        option_text = input(prompt).title()
        result = validator(pattern=regex_pattern, data=option_text, error_msg='Invalid option!')

    return option_text
