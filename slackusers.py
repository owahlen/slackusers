#!/usr/bin/env python3

import argparse
import logging

import pandas as pd

from credentials import Credentials
from logger import configure_logger
from slack_api_iterator import SlackApiIterator


def extract_users(credentials: Credentials):
    users_list_url = "https://slack.com/api/users.list"
    user_it = SlackApiIterator(url=users_list_url, credentials=credentials)
    users = [{
        'id': u['id'],
        'real_name': u['real_name'],
        'title': u['profile']['title'],
        'phone': u['profile']['phone'],
    } for u in user_it if u['deleted'] is False]
    return users


def main(credentials: Credentials, xls_file_name: str):
    logging.info(f'downloading users from workspace...')
    users = extract_users(credentials)
    df = pd.DataFrame(data=users)
    df.to_excel(xls_file_name, index=False)
    logging.info(f'wrote {len(users)} users to file "{xls_file_name}"')


if __name__ == "__main__":
    configure_logger()
    parser = argparse.ArgumentParser(description='Get users from slack workspace')
    parser.add_argument('-t', '--token', required=True, help='Access token for the Slack workspace.')
    parser.add_argument('-c', '--cookie', required=True, help='Access cookie for the Slack workspace.')
    parser.add_argument('-x', '--xls_output', default='users.xlsx', help='Excel output file name.')
    args = parser.parse_args()
    credentials = Credentials(token=args.token, cookie=args.cookie)
    main(credentials=credentials, xls_file_name=args.xls_output)
