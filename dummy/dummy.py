#!/usr/bin/env python3

import logging
import random
import time

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

while True:
    number = random.randrange(0, 4)

    if number == 0:
        logging.info('Hello there!!')
    elif number == 1:
        logging.warning('Hmmm....something strange')
    elif number == 2:
        logging.error('OH NO!!!!!!')
    elif number == 3:
        try:
            raise Exception('this is exception')
        except Exception as e:
            logging.exception(e)

    time.sleep(1)
