import logging
import logging.handlers

def create_logger(name):
    logging.basicConfig()
    return logging.getLogger(name)
