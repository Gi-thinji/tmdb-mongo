import logging
import pytz
import datetime
from logging.handlers import TimedRotatingFileHandler

def logger_config():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    file_handler = TimedRotatingFileHandler('app.log', when='midnight', backupCount=0)
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)

    tz = pytz.timezone('Africa/Nairobi')
    file_handler.converter = lambda x: datetime.fromtimestamp(x, tz)

    logger.addHandler(file_handler)

    return logger