import threading
import time
import telepot
from telepot.loop import MessageLoop


# [(chat_id, activity)]
activity = []

# [(chat_id, note, date, key)]
table = []


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    if content_type == 'text':

        print(msg['chat']['first_name'], msg['chat']['last_name'], content_type, chat_type, chat_id, msg['text'])

        if msg['text'] == '/notification':
            activity.append([chat_id, 'notification'])
            bot.sendMessage(chat_id, 'Привет, ' + msg['chat']['first_name'])
            bot.sendMessage(chat_id, 'Создадим напоминание')
            bot.sendMessage(chat_id, 'Введи текст напоминания:')
            table.append([chat_id, 'null', 'null', 'note'])

        elif [chat_id, 'notification'] in activity:
            flag = True
            flag1 = True
            for i in range(0, len(table)):
                if table[i] == [chat_id, 'null', 'null', 'note']:
                    table[i] = [chat_id, msg['text'], 'null', 'date']
                    bot.sendMessage(chat_id, 'OK, теперь введи дату в формате HH:MM.DD-MM-YY')
                    flag = False
                    flag1 = False
                    break

            if flag1:
                for i in range(0, len(table)):
                    if table[i][0] == chat_id and table[i][3] == 'date':
                        table[i][2] = msg['text']
                        table[i][3] = 'ready'
                        bot.sendMessage(chat_id, 'Готово!')
                        activity.remove([chat_id, 'notification'])
                        flag = False
                        break

            if flag:
                bot.sendMessage(chat_id, 'Пользуйся командами, пес')

        if msg['text'] == '/show_notifications':
            bot.sendMessage(chat_id, 'Список твоих уведомлений:')
            for i in range(0, len(table)):
                if table[i][0] == chat_id:
                    bot.sendMessage(chat_id, table[i][1] + ", " + table[i][2])

        if msg['text'] == '/delete_notification':
            bot.sendMessage(chat_id,
                            'В формате HH:MM.DD-MM-YY введи дату, '
                            'на которую у тебя стоит уведомление, которое ты хочешь удалить')
            activity.append([chat_id, 'delete_notification'])

        elif [chat_id, 'delete_notification'] in activity:
            flag2 = True
            for i in range(0, len(table)):
                if table[i][0] == chat_id and table[i][2] == msg['text']:
                    bot.sendMessage(chat_id, 'Уведомление ' + table[i][1] + ' от ' + table[i][2] + ' удалено')
                    del table[i]
                    flag2 = False
                    break
            if flag2:
                bot.sendMessage(chat_id, 'на это время уведомлений нет')
            activity.remove([chat_id, 'delete_notification'])

    else:
        print(msg['chat']['first_name'], msg['chat']['last_name'], content_type, chat_type, chat_id)
        if [chat_id, 'notification'] in activity:
            bot.sendMessage(chat_id, 'нужно напоминание!')
        else:
            bot.sendMessage(chat_id, 'Пользуйся командами, пес')


def notify():
    while 1:
        k = -1
        for i in range(0, len(table)):
            if time.strftime("%H:%M.%d-%m-%y", time.localtime()) == table[i][2]:
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