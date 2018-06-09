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

    def get_json_stream(self, *args, headers=None, **kwargs):
        headers = headers or {}
        headers.setdefault('Accept', 'application/x-ndjson')
        kwargs['headers'] = headers
        with self.session.get(*args, stream=True, **kwargs) as response:
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')
                    yield json.loads(decoded_line)

    def get_pgn_stream(self, *args, headers=None, **kwargs):
        headers = headers or {}
        headers.setdefault('Accept', 'application/x-chess-pgn')
        kwargs['headers'] = headers
        with self.session.get(*args, stream=True, **kwargs) as response:
            lines = []
            last_line = True
            for line in response.iter_lines():
                line = line.decode('utf-8')
                if last_line or line:
                    lines.append(line)
                else:
                    yield '\n'.join(lines)
                    lines = []
                last_line = line
