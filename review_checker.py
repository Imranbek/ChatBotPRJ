import os
from random import choice

import requests
import telegram
from dotenv import load_dotenv

dvmn_url = 'https://dvmn.org/api/long_polling/'
dvmn_token = os.environ['DVMN_TOKEN']
headers = {
    'Authorization': f'Token {dvmn_token}'
}


def main():
    chat_id = input("Please enter your chat_id:\n")
    print('Start looking for new reviews')
    timestamp = {}

    while True:
        try:
            checking_new_event = requests.get(dvmn_url, headers=headers, timeout=5, params=timestamp)
            checking_new_event.raise_for_status()
            checking_body = checking_new_event.json()

            if checking_body['status'] == 'timeout':
                timestamp = {'timestamp': checking_body['timestamp_to_request']}

            elif checking_body['status'] == 'found':
                review_info = checking_body['new_attempts'][0]
                send_review_message(chat_id, review_info)

                timestamp = {'timestamp': checking_body['last_attempt_timestamp']}

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            continue


def send_review_message(chat_id, review_info):
    token = os.environ['BOT_TOKEN']
    bot = telegram.Bot(token=token)
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
        -------' \
        Ссылка на урок: {lesson_url}'''

    bot.send_message(chat_id=chat_id, text=message_text)


if __name__ == '__main__':
    load_dotenv()
    main()
