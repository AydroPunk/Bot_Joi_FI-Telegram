from telegram.ext import Updater, CommandHandler
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

INPUT_TEXT = 0


def start(update, context):
    button1 = InlineKeyboardButton(
        text='About',
        url='https://github.com/AydroPunk'
    )

    button2 = InlineKeyboardButton(
        text='Enlace',
        url='https://t.me/Computacion_FI_UNAM_Channel'
    )

    update.message.reply_text(
        text='Haz clic en un boton',
        reply_markup=InlineKeyboardMarkup([
            [button1],
            [button2]
        ])
    )


if __name__ == '__main__':
    updater = Updater(token='5738833071:AAEjsUyxfn0e5EuvpAJZo2_xLi_e3zR43zM', use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))

    updater.start_polling()

    updater.idle()
