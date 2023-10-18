import argparse
import datetime

import requests
import telegram
from environs import Env


def sending_messages(dvmn_token, tg_token, chat_id):
    bot = telegram.Bot(token=tg_token)
    headers = {
        'Authorization': f'Token {dvmn_token}',
    }
    url_long = 'https://dvmn.org/api/long_polling/'

    timeout = 60
    timestamp = datetime.datetime.now().timestamp()

    while True:
        params = {
            'timestamp': timestamp,
        }
        try:
            response = requests.get(url_long, headers=headers, timeout=timeout, params=params)
            response.raise_for_status()
            response_data = response.json()['new_attempts'][0]
            for message in response:
                if message:
                    if response_data['is_negative']:
                        bot.sendMessage(chat_id=chat_id,
                                        text=f'У вас проверили работу [{response_data["lesson_title"]}]'
                                             f'({response_data["lesson_url"]})\n\nК сожалению, в работе нашлись ошибки',
                                        parse_mode=telegram.ParseMode.MARKDOWN_V2)
                    else:
                        bot.sendMessage(chat_id=chat_id,
                                        text=f'У вас проверили работу [{response_data["lesson_title"]}]'
                                             f'({response_data["lesson_url"]})\n\nПреподавателю всё понравилось, '
                                             f'можно приступать к следующему уроку',
                                        parse_mode=telegram.ParseMode.MARKDOWN_V2)
                    break
            timestamp = response_data['timestamp']
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
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
