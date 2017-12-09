import logging
import os
import random
import sys
import telegram
from retrying import retry

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.INFO, filename=u'picbot.log')

TOKEN = '300052001:AAE6fdytbvLS9Za1w4RjYPibVQQe6URGKYg'
bot = telegram.Bot(TOKEN)

photodir = '/root/picbot/photos/'


@retry(stop_max_attempt_number=5, wait_fixed=1000)
def send_photo(ph):
    bot.send_photo('@easterneurope2017', ph)


try:
    file = random.choice(os.listdir(photodir))
except Exception:
    logging.error("No more photos :(")
    sys.exit(0)

try:
    photo = open(photodir + file, 'rb')
except Exception:
    logging.error("Failed to open " + file)
    sys.exit(0)

try:
    send_photo(photo)
except Exception:
    logging.error("Failed to send " + file)
    sys.exit(0)

logging.info("Photo " + file + " successfully sent")
os.remove(photodir + file)
