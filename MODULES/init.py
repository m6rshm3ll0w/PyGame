import json
import os
import shutil
import pygame
import logging
import logging.handlers

logger = logging.getLogger("main")

def set_logging():
    global logger
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(filename)s[%(lineno)-2d] %(levelname)-1s [%(asctime)s] %(message)s')
    file_logger = logging.handlers.RotatingFileHandler("./DATA/log/main.log", maxBytes=10000000, backupCount=5)
    file_logger.setLevel(logging.DEBUG)
    file_logger.setFormatter(formatter)
    console_logger = logging.StreamHandler()
    console_logger.setLevel(logging.INFO)
    console_logger.setFormatter(formatter)
    logger.addHandler(file_logger)
    logger.addHandler(console_logger)


with open('./DATA/settings.json', "r", encoding="UTF-8") as json_data:
    CONFIG = json.load(json_data)
    logger.info("Config loaded!")

BLACK = (0, 0, 0)
RED = (255, 0, 0)


def check_tmp(clear:bool=False) -> None:
    if not clear:
        dirs = CONFIG["dirs"]["temp_paths"]
        for path in dirs:
            if not os.path.exists(os.getcwd()+path):
                os.makedirs(os.getcwd()+path)
        logger.info("dirs created")
    if clear:
        path = CONFIG["dirs"]["temp_folder"]
        if os.path.exists(os.getcwd()+path):
            shutil.rmtree(os.getcwd()+path)
        logger.info("temp folder deleted")