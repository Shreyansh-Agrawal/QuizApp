'''
    Pretty print using tabulate library
'''

from typing import List, Tuple
from tabulate import tabulate


def pretty_print(data: List[Tuple], headers: List):
    '''Method to pretty print using tabulate'''

    row_id = list(range(1, len(data) + 1))
    headers.insert(0, 'SNo.')
    print(tabulate(data, headers=headers, tablefmt='rounded_grid', showindex=row_id))
