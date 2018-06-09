# -*- coding: utf-8 -*-
import urllib

import requests

from .formats import JSON


class LiSession(requests.Session):
    def __init__(self, *args, base_url='https://lichess.org/', **kwargs):
        super().__init__(*args, **kwargs)
        self.base_url = base_url

    def request(self, method, path, *args, headers=None, **kwargs):
        fmt = kwargs.pop('fmt', JSON)
        kwargs['headers'] = fmt.headers
        url = urllib.parse.urljoin(self.base_url, path)
        response = super().request(method, url, *args, **kwargs)
        return fmt.handle(response, is_stream=kwargs.get('stream'))


class TokenSession(LiSession):
    def __init__(self, token, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token
        self.headers = {'Authorization': f'Bearer {token}'}
