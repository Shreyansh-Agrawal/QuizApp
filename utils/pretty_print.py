'''
    Pretty print using tabulate library
'''

from typing import Dict, List, Tuple
from tabulate import tabulate


def pretty_print(data: List[Tuple], headers: Dict):
    '''Method to pretty print using tabulate'''

    print(tabulate(data, headers=headers, tablefmt='rounded_outline'))
