import argparse
import datetime
import time

import requests
import telegram
from environs import Env


def get_response(dvmn_token, timestamp):
    timeout = 2
    params = {
        'timestamp': timestamp,
    }
    headers = {
        'Authorization': f'Token {dvmn_token}',
    }
    url = 'https://dvmn.org/api/long_polling/'
    response = requests.get(url, headers=headers, params=params, timeout=timeout)
    response.raise_for_status()
    return response.json()


def sending_messages(dvmn_token, tg_token, chat_id):
    bot = telegram.Bot(token=tg_token)
    timestamp = datetime.datetime.now().timestamp()
    while True:
        try:
            response = get_response(dvmn_token, timestamp)
            if response['status'] == 'timeout':
                continue
            else:
                if response['new_attempts'][0]['is_negative']:
                    bot.sendMessage(chat_id=chat_id,
                                    text=f'''У вас проверили работу [{response['new_attempts'][0]['lesson_title']}]({response['new_attempts'][0]['lesson_url']})
                                    \nК сожалению, в работе нашлись ошибки''',
                                    parse_mode=telegram.ParseMode.MARKDOWN_V2)
                    timestamp = response['new_attempts'][0]['timestamp']
                else:
                    bot.sendMessage(chat_id=chat_id,
                                    text=f'''У вас проверили работу [{response['new_attempts'][0]['lesson_title']}]({response['new_attempts'][0]['lesson_url']})
                                    \nПреподавателю всё понравилось, можно приступать к следующему уроку''',
                                    parse_mode=telegram.ParseMode.MARKDOWN_V2)
                    timestamp = response['new_attempts'][0]['timestamp']
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            time.sleep(10)
            continue


def main():
    env = Env()
    env.read_env()

    dvmn_token = env.str('DVMN_TOKEN')
    tg_token = env.str('TG_API_TOKEN')

    parser = argparse.ArgumentParser(description='Бот уведомляюший о проверке работ на сайте https://dvmn.org/')
    parser.add_argument('-c', '--chat_id', help='Id пользователя в телеграме', default=env.str('TG_CHAT_ID'))
    args = parser.parse_args()
    chat_id = args.chat_id

    sending_messages(dvmn_token, tg_token, chat_id)


if __name__ == '__main__':
    main()
