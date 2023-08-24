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
        return self

    def __next__(self):
        batch_index = self.index % self.limit
        if batch_index == 0:
            # fetch next page every self.limit indices
            self.params['limit'] = self.limit
            self.headers['Authorization'] = 'Bearer ' + self.credentials.token
            self.cookies['d'] = self.credentials.cookie
            if self.cursor != None:
                self.params['cursor'] = self.cursor
            response = requests.request("POST", self.url, params=self.params, headers=self.headers,
                                        cookies=self.cookies, **self.kwargs)
            response_json = response.json()
            self.cursor = response_json['response_metadata']['next_cursor']
            self.batch = response_json['members']
        if batch_index >= len(self.batch) - 1 and self.cursor == "":
            raise StopIteration
        next_item = self.batch[batch_index]
        self.index += 1
        return next_item
