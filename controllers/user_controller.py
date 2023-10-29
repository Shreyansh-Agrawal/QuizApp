'''
    Handlers for user operations
'''

from database.database_access import DatabaseAccess as DAO
from database.queries import Queries

class UserController:
    '''User Controller Class'''

    @staticmethod
    def start_quiz():
        '''Start a New Quiz'''

    @staticmethod
    def get_leaderboard():
        '''Return top 10 scores for leaderboard'''

        data = DAO.read_from_database(Queries.GET_LEADERBOARD)
        return data

    @staticmethod
    def get_user_scores(username: str):
        '''Return user's scores'''

        data = DAO.read_from_database(Queries.GET_USER_SCORES_BY_USERNAME, (username, ))
        return data
