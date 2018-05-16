# -*- coding: utf-8 -*-
import urllib

import requests


class LiSession:
    def __init__(self, session=None):
        if session is None:
            session = requests.Session()
        self.session = session

    def __getattr__(self, name):
        return getattr(self.session, name)

    # hook into here to log exceptions
    def request(self, *args, **kwargs):
        response = self.session.request(*args, **kwargs)
        # response.raise_for_status()
        return response

    # use json mixin instead?
    def get(self, *args, **kwargs):
        response = self.session.get(*args, **kwargs)
        return response.json()


class TokenSession(LiSession):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.session.headers = {'Authorization': f'Bearer {token}'}


class Client:
    base_url = 'https://lichess.org/api/'

    def __init__(self, session):
        self.session = session
        self.url = self.__class__.base_url

    def get_account(self):
        url = urllib.parse.urljoin(self.url, 'account')
        return self.session.get(url)

    def get_account_email(self):
        url = urllib.parse.urljoin(self.url, 'account/email')
        return self.session.get(url)

    def get_account_preferences(self):
        url = urllib.parse.urljoin(self.url, 'account/preferences')
        return self.session.get(url)

    def get_account_kid(self):
        url = urllib.parse.urljoin(self.url, 'account/kid')
        return self.session.get(url)


class TokenClient(Client):
    def __init__(self, token):
        token_session = TokenSession(token=token)
        super().__init__(session=token_session)


""" Example usage:
import berserk


with open('/Users/rgrant/.lichess.org') as f:
    token = f.read().strip()

client = berserk.TokenClient(token=token)
"""
