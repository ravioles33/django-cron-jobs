import logging
import os
from datetime import datetime

def setup_logger(script_name):
    today = datetime.now().strftime('%Y-%m-%d')
    time_stamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    log_dir = os.path.join('logs', 'tasks_script_selenium', today)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, f"{time_stamp}_{script_name}.log")
    
    logger = logging.getLogger(script_name)
    logger.setLevel(logging.DEBUG)

    # Evitar duplicados de manejadores de archivos
    if not logger.hasHandlers():
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

    return logger
