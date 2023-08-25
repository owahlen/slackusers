import logging
import time

import requests

from credentials import Credentials


class SlackApiIterator:
    """
    Iterator for Slack paged API responses
    """

    def __init__(self, url, credentials: Credentials, limit=100, **kwargs):
        self.url = url
        self.credentials = credentials
        self.limit = limit
        self.kwargs = kwargs
        self.params = self.kwargs.pop('params', {})
        self.headers = self.kwargs.pop('headers', {})
        self.cookies = self.kwargs.pop('cookies', {})

    def __iter__(self):
        self.index = 0
        self.cursor = None
        self.stop_iteration = False
        return self

    def __next__(self):
        if self.stop_iteration:
            raise StopIteration
        batch_index = self.index % self.limit
        if batch_index == 0:
            # fetch next page every self.limit indices
            self.params['limit'] = self.limit
            self.headers['Authorization'] = 'Bearer ' + self.credentials.token
            self.cookies['d'] = self.credentials.cookie
            if self.cursor is not None:
                self.params['cursor'] = self.cursor
            attempt = 0
            max_attempts = 5
            while True:
                response = requests.request("POST", self.url, params=self.params, headers=self.headers,
                                            cookies=self.cookies, **self.kwargs)
                attempt += 1
                response_json = response.json()
                if response_json['ok']:
                    if attempt > 1:
                        logging.info(f'retry successfully!')
                    break
                logging.warning(
                    f'waiting before retrying network error "{response_json["error"]}" ({attempt}/{max_attempts})')
                if attempt > max_attempts:
                    logging.error(f'failed due to network error {response_json["error"]}')
                    raise Exception("Network error: ", response_json['error'])
                time.sleep(5)

            self.cursor = response_json['response_metadata']['next_cursor']
            self.batch = response_json['members']
        if batch_index == len(self.batch) - 1 and self.cursor == "":
            # batch_index is pointing to last element of batch and cursor indicates last batch
            self.stop_iteration = True
        next_item = self.batch[batch_index]
        self.index += 1
        return next_item
