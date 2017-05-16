
import time
import telepot
from telepot.loop import MessageLoop


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    bot.sendMessage(chat_id, 'Sorry, BossBot is under maintenance for a while')

TOKEN = '300052001:AAE6fdytbvLS9Za1w4RjYPibVQQe6URGKYg'

bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()

while 1:
    time.sleep(10)