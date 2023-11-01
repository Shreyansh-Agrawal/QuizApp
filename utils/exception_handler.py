'''Exception Handler'''

import functools
import logging
import sqlite3

from utils.custom_error import DataNotFoundError, DuplicateEntryError, LoginError, InvalidInputError

logger = logging.getLogger(__name__)

def exception_handler(func):
    '''A decorator for handling errors'''

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except LoginError as e:
            print(e)
            logger.error(e)
        except DuplicateEntryError as e:
            print(e)
            logger.error(e)
        except DataNotFoundError as e:
            print(e)
            logger.error(e)
        except InvalidInputError as e:
            print(e)
            logger.error(e)
        except sqlite3.Error as e:
            print(e)
            logger.error(e)
        except Exception as e:
            print(e)
            logger.error(e)

    return wrapper
