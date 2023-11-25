from telegram.ext import Updater, CommandHandler

def start(update, context):
    update.message.reply_text('Hola, 25/11/23.')

if __name__ == '__main__':

    updater = Updater(token='6528431792:AAHu8ZazCCXTJj-JO-TBg-uFFrxctsoakf8', use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))

    updater.start_polling()
    updater.idle()