import logging
from datetime import datetime

def setup_logger(name, log_file):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)

    if (logger.hasHandlers()):
        logger.handlers.clear()

    logger.addHandler(handler)
    return logger

class Logger:
    _instance = None

    def __init__(self, log_name, log_file):
        if not Logger._instance:
            self.logger = logging.getLogger(log_name)
            self.logger.setLevel(logging.INFO)

            handler = logging.FileHandler(log_file)
            formatter = logging.Formatter('%(asctime)s - %(message)s')
            handler.setFormatter(formatter)

            if (self.logger.hasHandlers()):
                self.logger.handlers.clear()

            self.logger.addHandler(handler)
            
            Logger._instance = self

    @staticmethod
    def get_instance():
        if not Logger._instance:
            raise Exception("Logger must be initialized before getting the instance!")
        return Logger._instance

    def log_message(self, message):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.logger.info(f"[{current_time}] {message}")
    
    def close(self):
        for handler in self.logger.handlers:
            handler.close()
            self.logger.removeHandler(handler)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)