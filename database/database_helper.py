'''
    Contains methods for establishing database connection
'''

from typing import List
from database.database_connection import DatabaseConnection


class DatabaseHelper:
    ''' A class for database methods
    '''

    @staticmethod
    def read_from_database(query: str, data: tuple = None) -> List:
        '''Reads data from database

        Args:
            query (str): _description_
            data (tuple, optional): _description_. Defaults to None.

        Returns:
            List: _description_
        '''

        with DatabaseConnection('database\\data.db') as connection:
            cursor = connection.cursor()
            if not data:
                cursor.execute(query)
            else:
                cursor.execute(query, data)

        return cursor.fetchall()

    @staticmethod
    def write_to_database(query: str, data: tuple = None) -> None:
        ''' CREATE TABLE / Add / Update / Delete data from database

        Args:
            query (str): _description_
            data (tuple): _description_
        '''

        with DatabaseConnection('database\\data.db') as connection:
            print(connection)
            cursor = connection.cursor()
            if not data:
                cursor.execute(query)
            else:
                cursor.execute(query, data)
