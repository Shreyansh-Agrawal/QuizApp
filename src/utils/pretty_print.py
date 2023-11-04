'''Pretty print using tabulate library'''

import logging
from pprint import pprint
from typing import List, Tuple

from tabulate import tabulate

from config.display_prompts import DisplayPrompts

logger = logging.getLogger(__name__)


def pretty_print(data: List[Tuple], headers: List):
    '''Method to pretty print using tabulate'''

    row_id = list(range(1, len(data) + 1))
    headers.insert(0, 'SNo.')

    try:
        print(tabulate(data, headers=headers, tablefmt='rounded_grid', showindex=row_id))
    except ValueError as e:
        logger.exception('tabulate error: %s', e)
        print(DisplayPrompts.TABULATE_ERROR_MSG)
        pprint(data)
