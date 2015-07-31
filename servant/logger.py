import logging
import logging.handlers

def create_logger(name):
    logging.basicConfig(level=logging.DEBUG)
    return logging.getLogger(name)
