import logging
import os

# create logger with 'spam_application'
logger = logging.getLogger('beans-bot')
logger.setLevel(logging.DEBUG)

log_dir = os.getenv('LOG_DIR')
log_filename = f"{log_dir}/beans-bot.log"
os.makedirs(os.path.dirname(log_filename), exist_ok=True)

# create file handler which logs even debug messages
fh = logging.FileHandler(log_filename)
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - '
                              '%(name)s - '
                              '%(levelname)s -'
                              '%(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)
