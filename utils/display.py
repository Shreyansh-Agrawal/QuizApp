'''
    Pretty print using tabulate library
'''

from typing import List, Tuple
from tabulate import tabulate
from utils.custom_error import DataNotFoundError


def pretty_print(data: List[Tuple], headers: List):
    '''Method to pretty print using tabulate'''

    row_id = list(range(1, len(data) + 1))
    headers.insert(0, 'SNo.')
    print(tabulate(data, headers=headers, tablefmt='rounded_grid', showindex=row_id))


def show_categories(data: List[Tuple], header: List):
    '''Display Categories on Console'''

    if not data:
        print('\nNo Categories Currently, Please add a Category!!\n')
        raise DataNotFoundError('No Categories Currently, Please add a Category!!')

    print('\n-----Quiz Categories-----\n')

    categories = [(tup[0], ) for tup in data]
    pretty_print(data=categories, headers=header)
