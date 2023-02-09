import argparse
import os
import time
from random import choice

import requests
import telegram
from dotenv import load_dotenv


def main():
    load_dotenv()
    dvmn_url = 'https://dvmn.org/api/long_polling/'
    dvmn_token = os.environ['DVMN_TOKEN']
    headers = {
        'Authorization': f'Token {dvmn_token}'
    }
    bot = turn_on_bot()
    chat_id = parce_chat_id()
    print('Start looking for new reviews')
    timestamp = {}

    while True:
        try:
            new_event_response = requests.get(dvmn_url, headers=headers, params=timestamp)
            new_event_response.raise_for_status()
            event_state = new_event_response.json()

            if event_state['status'] == 'timeout':
                timestamp = {'timestamp': event_state['timestamp_to_request']}

            elif event_state['status'] == 'found':
                review_info = event_state['new_attempts'][0]
                send_review_message(bot, chat_id, review_info)

                timestamp = {'timestamp': event_state['last_attempt_timestamp']}

        except (requests.exceptions.Timeout):
            continue
        except (requests.exceptions.ConnectionError):
            time.sleep(60)
            continue

def send_review_message(bot, chat_id, review_info):
    message_positive = 'Поздравляем, Вы проделали отличную работу! Преподавателю все понравилось, можете приступать к следующему уроку!'
    message_negative = ['К сожалению, в работе нашлись ошибки, которые необходимо исправить. Удачи на следующем ревью! Мы верим в Вас!',
                        'В работе нашлись ошибки. Исправьте их и попробуйте еще раз =) Удачи!',
                        'Вы отлично потрудились, но в работе были найдены ошибки, которые необходимо исправить. Удачи на следующем ревью!'
                        ]

    lesson_url = review_info['lesson_url']
    review_result = choice(message_negative) if review_info['is_negative'] else message_positive
    lesson_title = review_info['lesson_title']

    message_text = f'''Преподаватель проверил Вашу работу по уроку \'{lesson_title}\'.

        {review_result}
        -------
        Ссылка на урок: {lesson_url}'''

    bot.send_message(chat_id=chat_id, text=message_text)


def turn_on_bot():
    token = os.environ['BOT_TOKEN']
    bot = telegram.Bot(token=token)
    return bot


def parce_chat_id():
    parser = argparse.ArgumentParser(
        description='DVMN review controller'
    )
    parser.add_argument('chid', help='Ваш chat_id')
    args = parser.parse_args()

    return args.chid


if __name__ == '__main__':
    main()
