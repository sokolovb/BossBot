from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import logging

ProjectRoot = '/root/BossBot/'

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO, filename=ProjectRoot + u'dragonbot.log')

TOKEN = '491311774:AAHvib3HoaTTphNom7B9T6-YcI3kEMM7cB8'
USERFILE = ProjectRoot + 'users.txt'
USERS = {}


# my chat_id: 216241563


def register(bot, update):
    user = update.message.from_user
    if user.name not in USERS:
        with open(USERFILE, "a") as myfile:
            myfile.write(user.name + ' ' + str(user.id) + '\n')
            myfile.close()
        USERS[user.name] = str(user.id)
        bot.send_message(chat_id=update.message.chat_id,
                         text='You\'ve been registered!\n' +
                              'Now add me in groups that you want to receive notification from.\n' +
                              'When people will tag you with "' + user.name + '" you\'ll receive a message here!\n\n' +
                              'Remember to do /register again when you change username!')
        logging.info('User ' + user.name + ' has just registered in')
        print(USERS)
        return

    bot.send_message(chat_id=update.message.chat_id, text='You are already registered')


def unregister(bot, update):
    user = update.message.from_user
    print(user.name in USERS)
    if user.name in USERS:
        with open(USERFILE, "r") as f:
            lines = f.readlines()
            f.close()

        with open(USERFILE, "w") as f:
            for line in lines:
                if line.split()[0] != user.name:
                    f.write(line)
            f.close()

        del USERS[user.name]

        bot.send_message(chat_id=update.message.chat_id, text='You\'ve just unregistered')
        return

    bot.send_message(chat_id=update.message.chat_id, text='You are not registered')


def parse_msg(bot, update):
    entities = update.message.parse_entities('mention')
    global USERS
    for entity in entities:
        if entities[entity] in USERS:
            group = ''
            tagger = ''
            msg = ''
            try:
                group = update.message.chat.title
                tagger = '@' + update.message.from_user.username
                msg = update.message.text
            except:
                pass

            bot.send_message(chat_id=USERS[entities[entity]],
                             text='You\'ve been tagged!' +
                                  '\nGroup: ' + group +
                                  '\nTagged by: ' + tagger +
                                  '\nMessage:\n' + msg)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logging.warning('Update "%s" caused error "%s"', update, error)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Hi there! Use /register to subscribe on notifications!')


def main():
    global USERS
    try:
        with open(USERFILE) as f:
            for line in f:
                (key, val) = line.split()
                USERS[key] = val
            f.close()
    except:
        pass

    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text, parse_msg))
    dp.add_handler(CommandHandler('register', register))
    dp.add_handler(CommandHandler('unregister', unregister))
    dp.add_handler(CommandHandler('start', start))
    dp.add_error_handler(error)

    updater.start_polling(timeout=20)

    updater.idle()


if __name__ == '__main__':
    main()
