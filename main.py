import argparse
import datetime
import logging
import time

import requests
import telegram
from environs import Env


class TelegramLogsHandler(logging.Handler):
    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.chat_id, text=log_entry)


def get_response(dvmn_token, timestamp):
    params = {
        'timestamp': timestamp,
    }
    headers = {
        'Authorization': f'Token {dvmn_token}',
    }
    url = 'https://dvmn.org/api/long_polling/'
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def main():
    env = Env()
    env.read_env()

    dvmn_token = env.str('DVMN_TOKEN')
    tg_token = env.str('TG_API_TOKEN')
    tg_chat_id = env.str('TG_CHAT_ID')

    logger = logging.getLogger('bot')

    parser = argparse.ArgumentParser(description='Бот уведомляюший о проверке работ на сайте https://dvmn.org/')
    parser.add_argument('-c', '--chat_id', help='Id пользователя в телеграме', default=tg_chat_id)
    args = parser.parse_args()
    chat_id = args.chat_id

    bot = telegram.Bot(token=tg_token)
    timestamp = datetime.datetime.now().timestamp()

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    logger.addHandler(TelegramLogsHandler(bot, tg_chat_id))

    logger.info('Старт бота')
    while True:
        try:
            review = get_response(dvmn_token, timestamp)
            if review['status'] == 'timeout':
                continue
            else:
                if review['new_attempts'][0]['is_negative']:
                    bot.sendMessage(chat_id=chat_id,
                                    text=f'''У вас проверили работу [{review['new_attempts'][0]['lesson_title']}]({review['new_attempts'][0]['lesson_url']})
                                        \nК сожалению, в работе нашлись ошибки''',
                                    parse_mode=telegram.ParseMode.MARKDOWN_V2)
                    timestamp = review['new_attempts'][0]['timestamp']
                else:
                    bot.sendMessage(chat_id=chat_id,
                                    text=f'''У вас проверили работу [{review['new_attempts'][0]['lesson_title']}]({review['new_attempts'][0]['lesson_url']})
                                        \nПреподавателю всё понравилось, можно приступать к следующему уроку''',
                                    parse_mode=telegram.ParseMode.MARKDOWN_V2)
                    timestamp = review['new_attempts'][0]['timestamp']
        except requests.exceptions.ReadTimeout as error:
            logger.exception(error)
            continue
        except requests.exceptions.ConnectionError as error:
            logger.exception(error)
            time.sleep(10)
            continue


if __name__ == '__main__':
    main()
