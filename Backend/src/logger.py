import logging
from dotenv import load_dotenv, find_dotenv
import os
import sys

load_dotenv(find_dotenv('app.env'))
log_file_path = os.getenv('LOG_FILE_PATH', 'default_app.log')
logging.basicConfig(filename=log_file_path, 
                        format='%(asctime)s %(levelname)s: %(message)s', 
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO)

def logger_msg(message, type="info"):
    # Configure logging
    if(type=="info"):
        logging.info(message)
    elif(type=="error"):
        logging.error(message)
    elif(type=="warning"):
        logging.warning(message)
    elif(type=="debug"):
        logging.debug(message)
    else:
        logging.info(message)

def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        logging.error("Uncaught exception: ", exc_info=(exc_type, exc_value, exc_traceback))

# Configure logging

    # Example usage
    # logging.info('This is an info message')
    # logging.error('This is an error message')
# # Configure logging
# logging.basicConfig(filename='app.log', level=logging.INFO, 
#                     format='%(asctime)s %(levelname)s: %(message)s', 
#                     datefmt='%Y-%m-%d %H:%M:%S')

# # Example usage
# logging.info('This is an info message')
# logging.error('This is an error message')