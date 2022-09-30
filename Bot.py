# from telegram import Update
# id del grupo oficial = -100165914287
import os
import pyshorteners
import qrcode
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ChatAction
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler

# token = os.environ['TOKEN']

INPUT_TEXT = 0
INPUT_URL = 0


# today = datetime.date.today()
# files = {'photo': open('/home/aydropunk/Descargas/Joi_qr.png', 'rb')}
# resp = requests.post(
#    'https://api.telegram.org/bot5738833071:AAEHaPCg879LS771hD3rRBnKfOKLWf_0dcs/sendPhoto?chat_id=-1001659142876'
#    '&caption={}\nEscanea la imagen para que te lleve al link de autentificacion\nPresione /start para iniciar el bot'.format(today),
#    files=files)
# print(resp.status_code)

# def welcome_msg(item):
#    chad_id = item["message"]["chat"]["id"]
#    user_id = item["message"]["new_chat_member"]["id"]
#    user_name = item["message"]["new_chat_member"].get("username", user_id)
#
#    welcome_msg = '''
#                <a href="tg://user?id={}">@{}</a> , Bienvenido a este grupo 👋. Por favor, lea las reglas de los grupos y adhiérase a ellas
#                '''.format(user_id, user_name)
#    to_url = 'https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&parse_mode=HTML'.format(token, chad_id,
#                                                                                                    welcome_msg)
#    resp = requests.get(to_url)


################
# endTime = datetime.datetime.now() + datetime.timedelta(minutes=2)

# old_id = -100165914287

# while endTime > datetime.datetime.now():
#    time.sleep(1)
#    base_url = 'https://api.telegram.org/bot{}/getUpdates'.format(token)
#    resp = requests.get(base_url)
#    data = resp.json()
#    for item in data['result']:
#        new_id = item["update_id"]
#        if old_id < new_id:
#            old_id = int(item["update_id"])
#            print(item)
#            try:
#                if "new_chat_member" in item["message"]:
#                    welcome_msg(item)
#            except:
#                pass

def start(update, context):
    update.message.reply_text(
        text='Hola, bienvenido, ¿que deseas hacer?\n\n',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Generar qr', callback_data='qr')],
            [InlineKeyboardButton(text='reglas', url='https://t.me/Computacion_FI_UNAM_Channel/10')],
            [InlineKeyboardButton(text='Acortar URL', callback_data='url')],
            [InlineKeyboardButton(text='About', url='https://github.com/AydroPunk')]
        ])
    )


def qr_command_handler(update, context):
    update.message.reply_text('Enviame el texto para generarte un codigo QR')

    return INPUT_TEXT


def qr_callback_handler(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text='Enviame el texto para generarte un codigo QR'
    )
    return INPUT_TEXT


def url_callback_handler(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(
        text='Enviame un enlace para acortarlo'
    )
    return INPUT_URL


def generate_qr(text):
    filename = text + '.png'  # Hola = Hola.png

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

    filename = generate_qr(text)

    chat = update.message.chat

    # print(chat)

    send_qr(filename, chat)

    # print(filename)

    chat.send_action(
        action=ChatAction.UPLOAD_PHOTO,
        timeout=None
    )
    chat.send_photo(
        photo=open(filename, 'rb')
    )
    return ConversationHandler.END


def input_url(update, context):
    url = update.message.text

    chat = update.message.chat

    # acortar url

    s = pyshorteners.Shortener()

    short = s.chilpit.short(url)

    chat.send_action(
        action=ChatAction.TYPING,
        timeout=None
    )
    chat.send_message(
        text=short
    )
    # print(chat)

    return ConversationHandler.END


def process_message_channel(update, context):
    text = update.message.text

    # print(update)

    if str(text).__contains__('#channel'):
        # Enviamos el mensaje al canal
        context.bot.send_message(
            chat_id='-1001824249754',
            text=str(text).replace('#channel', '')
        )


def process_message_noticias(update, context):
    text = update.message.text

    # print(update)

    if str(text).__contains__('#noticias'):
        # Enviamos el mensaje al canal de noticias
        context.bot.send_message(
            chat_id='-1001893316955',
            text=str(text).replace('#noticias', '')
        )


if __name__ == '__main__':
    updater = Updater(token=os.environ['TOKEN'], use_context=True)

    dp = updater.dispatcher

    dp.add_handler(MessageHandler(filters=Filters.text, callback=process_message_channel))

    dp.add_handler(MessageHandler(filters=Filters.text, callback=process_message_noticias))

    dp.add_handler(CommandHandler('start', start))

    dp.add_handler(ConversationHandler(
        entry_points=[
            CallbackQueryHandler(pattern='url', callback=url_callback_handler)
        ],

        states={INPUT_URL: [MessageHandler(Filters.text, input_url)]
                },
        fallbacks=[]
    ))

    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('qr', qr_command_handler),
                      CallbackQueryHandler(pattern='qr', callback=qr_callback_handler)
                      ],
        states={INPUT_TEXT: [MessageHandler(Filters.text, input_text)]
                },

        fallbacks=[]
    ))

    updater.start_polling()

    updater.idle()
