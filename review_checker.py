import os

import requests
from dotenv import load_dotenv

from chat_bot_v1 import DvmnBot

dvmn_url = 'https://dvmn.org/api/long_polling/'
dvmn_token = os.environ['DVMN_TOKEN']
headers = {
    'Authorization': f'Token {dvmn_token}'
}


def main():
    chat_id = input("Please enter your chat_id:\n")
    print('Start looking for new reviews')
    timestamp = {}
    bot = DvmnBot()
    while True:
        try:
            checking_new_event = requests.get(dvmn_url, headers=headers, timeout=5, params=timestamp)
            checking_new_event.raise_for_status()
            checking_body = checking_new_event.json()

            if checking_body['status'] == 'timeout':
                timestamp = {'timestamp': checking_body['timestamp_to_request']}

            elif checking_body['status'] == 'found':
                review_info = checking_body['new_attempts'][0]
                bot.send_review_message(chat_id, review_info)

                timestamp = {'timestamp': checking_body['last_attempt_timestamp']}

        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            continue


if __name__ == '__main__':
    load_dotenv()
    main()
