import logging    # first of all import the module
import datetime

def error_log(message):
    logging.basicConfig(filename='errorlog.txt', format='%(name)s - %(levelname)s - %(message)s')
    logging.warning(' ' + str(datetime.datetime.now()) + message + '\n')
