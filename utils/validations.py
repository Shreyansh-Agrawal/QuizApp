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
            if res is False:
                raise InvalidInputError('\nInvalid Input, Please try again...\n')
        except InvalidInputError as e:
            print(e)

        return res

    return wrapper


@error_handling
def validator(pattern, input_data):
    '''Validates using: re.fullmatch(regex, data)'''    

    match_obj = re.fullmatch(pattern, input_data)

    if not match_obj:
        return False

    return True


def validate_name(prompt: str):
    '''Checks user's name, category name input'''

    result = False
    name = ''

    while not result:
        name = input(prompt).title()
        result = validator('[A-Za-z\s]{2,25}', name)

    return name


def validate_email(prompt: str):
    '''Checks email input'''

    result = False
    email = ''

    while not result:
        email = input(prompt).lower()
        result = validator('[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}', email)

    return email


def validate_username(prompt: str):
    ''' Checks username input -
    
        limited to 30 characters
        must contain only letters, numbers, periods, and underscores
    '''

    result = False
    username = ''

    while not result:
        username = input(prompt).lower()
        result = validator('[A-Za-z0-9._]{2,30}', username)

    return username


def validate_question_text(prompt: str):
    '''Checks question text'''

    result = False
    question = ''

    while not result:
        question = input(prompt).title()
        result = validator('.{10,100}', question)

    return question


def validate_option_text(prompt: str):
    '''Checks option text'''

    result = False
    option_text = ''

    while not result:
        option_text = input(prompt).title()
        result = validator('.{1,50}', option_text)

    return option_text
