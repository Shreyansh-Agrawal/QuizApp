'''
    General Logger
'''

import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    level=logging.DEBUG,
    filename='logs.txt'
)

class Logger:
    '''A class for logging
    '''
    logger = logging.getLogger(__name__)
