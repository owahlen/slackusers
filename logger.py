import logging
import sys


def configure_logger():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[
            logging.FileHandler('slackusers.log', mode='w'),
            logging.StreamHandler(sys.stdout)
        ]
    )
