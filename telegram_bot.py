import logging

from environs import Env
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Updater

env = Env()
env.read_env()
tg_token = env.str('TG_TOKEN')

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Hello, {update.effective_chat.first_name}')


updater = Updater(token=tg_token, use_context=True)

dispatcher = updater.dispatcher

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()
