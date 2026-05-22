import logging
import os
from logging.handlers import RotatingFileHandler
from rich.logging import RichHandler

def setup_logger(name="IQOptionBot"):
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Console handler with Rich
    console_handler = RichHandler(rich_tracebacks=True, markup=True)
    console_handler.setLevel(logging.INFO)
    
    # File handler
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "bot.log"), 
        maxBytes=10*1024*1024, 
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

logger = setup_logger()
