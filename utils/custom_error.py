'''
    Custom Errors
'''

class LoginError(Exception):
    '''Exception raised when Login attempts exhausted'''

    def __init__(self, message):
        super().__init__(f"{message}")


class EmptyOptionListError(Exception):
    '''Exception raised when no Options are added for a Question'''

    def __init__(self, message):
        super().__init__(f"{message}")
