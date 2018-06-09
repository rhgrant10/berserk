# -*- coding: utf-8 -*-
import json

import ndjson
import requests


class LiSession:
    def __init__(self, session=None):
        if session is None:
            session = requests.Session()
        self.session = session

    def __getattr__(self, name):
        return getattr(self.session, name)

    def get_json(self, *args, headers=None, **kwargs):
        headers = headers or {}
        headers.setdefault('Accept', 'application/json')
        response = self.session.get(*args, headers=headers, **kwargs)
        return response.json()

    def get_ndjson(self, *args, headers=None, **kwargs):
        headers = headers or {}
        headers.setdefault('Accept', 'application/x-ndjson')
        response = self.session.get(*args, headers=headers, **kwargs)
        return response.json(cls=ndjson.Decoder)

    def get_lichessjson(self, *args, headers=None, **kwargs):
        headers = headers or {}
        headers.setdefault('Accept', 'application/vnd.lichess.v3+json')
        response = self.session.get(*args, headers=headers, **kwargs)
        return response.json()

    def get_pgn(self, *args, headers=None, **kwargs):
        headers = headers or {}
        headers.setdefault('Accept', 'application/x-chess-pgn')
        response = self.session.get(*args, headers=headers, **kwargs)
        return response.text

    def get_stream(self, *args, **kwargs):
        with self.session.get(*args, stream=True, **kwargs) as r:
            for line in r.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    yield json.loads(decoded_line)


class TokenSession(LiSession):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.session.headers = {'Authorization': f'Bearer {token}'}
