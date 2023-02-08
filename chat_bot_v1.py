import os
from random import choice

import telegram
from dotenv import load_dotenv

load_dotenv()


class DvmnBot:
    def __init__(self):
        token = os.environ['BOT_TOKEN']
        self.bot = telegram.Bot(token=token)
        self.message_positive = 'Поздравляем, Вы проделали отличную работу! Преподавателю все понравилось, можете приступать к следующему уроку!'
        self.message_negative = ['К сожалению, в работе нашлись ошибки, которые необходимо исправить. Удачи на следующем ревью! Мы верим в Вас!',
                                 'В работе нашлись ошибки. Исправьте их и попробуйте еще раз =) Удачи!',
                                 'Вы отлично потрудились, но в работе были найдены ошибки, которые необходимо исправить. Удачи на следующем ревью!'
                                 ]

    def send_review_message(self, chat_id, review_info):
        lesson_url = review_info['lesson_url']
        review_result = choice(self.message_negative) if review_info['is_negative'] else self.message_positive
        lesson_title = review_info['lesson_title']

        message_text = f'Преподаватель проверил Вашу работу по уроку \'{lesson_title}\'.\n\n' \
            f'{review_result}\n-------\n' \
            f'Ссылка на урок: {lesson_url}'

        self.bot.send_message(chat_id=chat_id, text=message_text)
