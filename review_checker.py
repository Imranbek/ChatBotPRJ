import json
import os

import requests
from dotenv import load_dotenv

from chat_bot_v1 import DvmnBot

load_dotenv()

folder = 'fogy'
url = 'https://dvmn.org/api/long_polling/'
token = os.environ['DVMN_TOKEN']
headers = {
    'Authorization': f'Token {token}'
}


def main():
    chat_id = input("Please enter your chat_id:\n")
    timestamp = {}
    my_bot = DvmnBot()
    while True:
        try:
            # print('New req ' + str(timestamp))
            checking_body = ask_for_events(timestamp=timestamp if timestamp else None)

            if checking_body['status'] == 'timeout':
                # print('No events. Retrying.')
                timestamp = {'timestamp': checking_body['timestamp_to_request']}
            elif checking_body['status'] == 'found':
                # print(json.dumps(checking_body, indent=1))

                review_info = checking_body['new_attempts'][0]
                my_bot.send_review_message(chat_id, review_info)

                timestamp = {'timestamp': checking_body['last_attempt_timestamp']}
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            continue


def ask_for_events(timestamp):
    checking = requests.get(url, headers=headers, timeout=5, params=timestamp)
    checking.raise_for_status()

    return checking.json()


if __name__ == '__main__':
    main()