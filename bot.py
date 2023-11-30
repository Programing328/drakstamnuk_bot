from telegram import ChatAction, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters
from datetime import datetime 
import pyshorteners
import qrcode
import os

#alt+92

INPUT_TEXT = 0
INPUT_URL = 1

def start(update, context):

    print('\n/start... ')

    button1 = InlineKeyboardButton(
        text='Whatsapp: ',
        url='https://chat.whatsapp.com/LH6fMqB9jOeGoJ0I6KNW1A'
    )
    button2 = InlineKeyboardButton(
        text='Github: ',
        url='https://github.com/Programing328/drakstamnuk_bot'
    )
    button3 = InlineKeyboardButton(
        text='Drakstamnuk: ',
        url='https://t.me/draka_m'
    )
    buttonQr = InlineKeyboardButton(
        text='QR Code',
        callback_data='qr'
    )
    buttonSt = InlineKeyboardButton(
        text='Acortar URL',
        callback_data='url'
    )

def read_qr_command_handler (update,context):
    qrPhoto = update.message.photo

    update.message.reply_text('Inicializando p_328 bot...')
    update.message.reply_text(
        text='Drakstamnuk.bot se ha inicializado con exito!\n',
        reply_markup=InlineKeyboardMarkup([
            [button1, button2],
            [buttonQr, buttonSt],
            [button3]
        ])
    ) 

def process_message(update, context):
    textG = update.message.text
    if str(textG).__contains__('#channel'):
        context.bot.send_message(
            chat_id='-1002131815103',
            text=str(textG).replace('#channel', '')
        )
    print('\n$> '+textG)
    
def qr_callback_handler(update, context):
    query = update.callback_query
    query.answer()

    query.edit_message_text(
        text='Envía texto para generarlo en formato QR'
    )

    return INPUT_TEXT

def url_callback_handler(update, context):
    query = update.callback_query
    query.answer()

    query.edit_message_text(
        text='Envía un enlace para acortarlo.'
    )

    return INPUT_URL

def qr_command_handler(update, context):
    update.message.reply_text('Envía texto para generarlo en formato QR')
    return INPUT_TEXT

def url_command_handler(update, context):
    update.message.reply_text('Envía un enlace para acortarlo.')
    return INPUT_URL

def dateTime_command_handler(update, context):
    now = datetime.now()
    #dateTime_date = now.date()
    #+'\nFecha: '+dateTime_date
    update.message.reply_text('Date Time: '+str(now))

def generate_qr(text):
    filename = text +'.jpg'
    img = qrcode.make(text)
    img.save(filename)

    return filename

def send_qr(filename, chat):
    chat.send_action(
        action=ChatAction.UPLOAD_PHOTO,
        timeout=None
    )
    
    chat.send_photo(
        photo=open(filename, 'rb')
    )

    os.unlink(filename)

def input_text(update, context):
    text = update.message.text
    print("qr_value: "+text)

    chat = update.message.chat

    filename = generate_qr(text)
    send_qr(filename, chat)

    return ConversationHandler.END

def input_url(update, context):
    url = update.message.text
    chat = update.message.chat

    s = pyshorteners.Shortener()
    short = s.clckru.short(url)

    chat.send_action(
        action=ChatAction.TYPING,
        timeout=None
    )
    
    chat.send_message(
        text='Shortlink: \n'+ short
    )

    print('URL: '+short)

    return ConversationHandler.END


if __name__ == '__main__':

    updater = Updater(token='TOKEN', use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))

    dp.add_handler(ConversationHandler(
        entry_points=[
            CommandHandler('qr', qr_command_handler),
            CommandHandler('url', url_command_handler),
            CommandHandler('dateTime', dateTime_command_handler),
            CommandHandler('readQR', read_qr_command_handler),
            CallbackQueryHandler(pattern='qr', callback=qr_callback_handler),
            CallbackQueryHandler(pattern='url', callback=url_callback_handler)
        ],

        states={
            INPUT_TEXT: [MessageHandler(Filters.text, input_text)],
            INPUT_URL: [MessageHandler(Filters.text, input_url)]
        },

        fallbacks=[]
    ))

    dp.add_handler(MessageHandler(filters=Filters.text, callback=process_message))

    updater.start_polling()
    updater.idle()