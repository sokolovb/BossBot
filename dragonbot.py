from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import logging

# Enable logging
# logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#                     level=logging.INFO, filename=u'dragonbot.log')


TOKEN = '300052001:AAHWk8zjvpqgDe96-OhF6s9Vdqb661_TgXM'
USERFILE = 'test.txt'
USERS = {}


# my chat_id: 216241563
# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.


def register(bot, update):
    user = update.message.from_user
    if user.name not in USERS:
        with open(USERFILE, "a") as myfile:
            myfile.write(user.name + ' ' + str(user.id))
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


def main():
    global USERS
    with open(USERFILE) as f:
        for line in f:
            (key, val) = line.split()
            USERS[key] = val
    f.close()

    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text, parse_msg))
    dp.add_handler(CommandHandler('register', register))
    dp.add_handler(CommandHandler('unregister', unregister))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling(timeout=20)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
