import logging
from telegram.ext import Updater
from telegram.ext import CommandHandler
from os import listdir
from os.path import isfile, join
# my bot TOKEN
# create KEYS.py and insert TOKEN:str variable for work this bot
from KEYS import TOKEN

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

REQUEST_KWARGS = {
    'proxy_url': 'socks5://195.201.159.93:443',
    'urllib3_proxy_kwargs': {
        'username': 'telegram',
        'password': 'a3c985860a1e361371c2457f71e825fe',
    }
}

updater = Updater(
    token=TOKEN,
    use_context=True,
    request_kwargs=REQUEST_KWARGS)

dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Приветики, я могу показать тебе файлы, если ты введёшь /lsfiles"
    )
################################################################################
folder_path = './telegram_files'
file_names = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]

def lsfiles(update,context):
    '''
        Send message with file names list from ./telegram_files
    '''
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='\n'.join(file_names)
    )
#################################################################################
dispatcher.add_handler(
    CommandHandler('start', start)
)
dispatcher.add_handler(
    CommandHandler('lsfiles', lsfiles)
)

updater.start_polling()
