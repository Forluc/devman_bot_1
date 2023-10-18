import datetime

import requests
import telegram
from environs import Env

env = Env()
env.read_env()

dvmn_token = env.str('DVMN_TOKEN')
tg_token = env.str('TG_API_TOKEN')
chat_id = env.str('TG_CHAT_ID')

bot = telegram.Bot(token=tg_token)

headers = {
    'Authorization': f'Token {dvmn_token}',
}
url_long = 'https://dvmn.org/api/long_polling/'
timestamp = datetime.datetime.now().timestamp()

while True:
    params = {
        'timestamp': timestamp,
    }
    try:
        response = requests.get(url_long, headers=headers, timeout=60, params=params)
        response.raise_for_status()
        for message in response:
            if message:
                bot.sendMessage(chat_id=chat_id, text='Преподаватель проверил работу!')
                break
        timestamp = response.json()['new_attempts'][0]['timestamp']
    except requests.exceptions.ReadTimeout:
        continue
    except requests.exceptions.ConnectionError:
        continue
