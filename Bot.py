# from telegram import Update
import os
import qrcode
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ChatAction

INPUT_TEXT = 0


def start(update, context):
    update.message.reply_text(
        text='Hola, bienvenido, ¿que deseas hacer?\n\nUsa /qr para generar un codigo qr',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton(text='Enlace', url='https://t.me/Computacion_FI_UNAM_Channel')],
            [InlineKeyboardButton(text='Generar qr', callback_data='qr')],
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

    print(filename)

    return ConversationHandler.END


if __name__ == '__main__':
    updater = Updater(token='YOUR_TOKEN', use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))

    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('qr', qr_command_handler),
                    CallbackQueryHandler(pattern='qr', callback=qr_callback_handler)
                    ],

        states={INPUT_TEXT: [MessageHandler(Filters.text, input_text)]},

        fallbacks=[]
    ))

    updater.start_polling()

    updater.idle()
