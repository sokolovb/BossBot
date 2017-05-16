import threading
import time
import telepot
from telepot.loop import MessageLoop


# [(chat_id, note, date, key)]
table = []


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(msg['chat']['first_name'], msg['chat']['last_name'], content_type, chat_type, chat_id, msg['text'])

    if content_type == 'text':

        '''
        flag = False
        for time in table:
            if table[time][0] == chat_id and table[time][2] != 'ready':
                flag = True
                t = time
        if flag:
            table[t][1] = msg['text']
            table[t][2] = 'ready'
        else:
        '''

        if msg['text'] == '/notification':
            bot.sendMessage(chat_id, 'Привет, ' + msg['chat']['first_name'])
            bot.sendMessage(chat_id, 'Создадим напоминание')
            bot.sendMessage(chat_id, 'Введи текст напоминания:')
            table.append([chat_id, 'null', 'null', 'note'])

        else:
            flag = True
            flag1 = True
            for i in range(0, len(table)):
                if table[i] == [chat_id, 'null', 'null', 'note']:
                    table[i] = [chat_id, msg['text'], 'null', 'date']
                    bot.sendMessage(chat_id, 'OK, теперь введи дату в формате HH:MM:SS.DD-MM-YY')
                    flag = False
                    flag1 = False
                    break

            if flag1:
                for i in range(0, len(table)):
                    if table[i][0] == chat_id and table[i][3] == 'date':
                        table[i][2] = msg['text']
                        table[i][3] = 'ready'
                        bot.sendMessage(chat_id, 'Готово!')
                        flag = False
                        break

            if flag:
                bot.sendMessage(chat_id, 'Пользуйся командами, пес')

    else:
        bot.sendMessage(chat_id, 'Пользуйся командами, пес')


def notify():
    while 1:
        k = -1
        for i in range(0, len(table)):
            if time.strftime("%H:%M:%S.%d-%m-%y", time.localtime()) == table[i][2]:
                bot.sendMessage(table[i][0], 'Эй пес, ты помнишь, что ' + table[i][1])
                k = i
        if k >= 0:
            del table[k]
        time.sleep(1)


TOKEN = '300052001:AAE6fdytbvLS9Za1w4RjYPibVQQe6URGKYg'


bot = telepot.Bot(TOKEN)
MessageLoop(bot, handle).run_as_thread()

t = threading.Thread(notify())
t.daemon = True
t.start()

print('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)