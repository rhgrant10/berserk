# -*- coding: utf-8 -*-
import urllib

import requests

from .formats import JSON


class LiSessionAdapter:
    def __init__(self, session, base_url=None):
        self.session = session
        self.base_url = base_url

    def __getattr__(self, name):
        return getattr(self.session, name)

    def request(self, method, path, *args, headers=None, **kwargs):
        fmt = kwargs.pop('fmt', JSON)
        kwargs['headers'] = fmt.headers
        url = urllib.parse.urljoin(self.base_url, path)
        response = self.session.request(method, url, *args, **kwargs)
        return fmt.handle(response, is_stream=kwargs.get('stream'))

    def get(self, *args, **kwargs):
        return self.request('GET', *args, **kwargs)

    def post(self, *args, **kwargs):
        return self.request('POST', *args, **kwargs)

    def put(self, *args, **kwargs):
        return self.request('PUT', *args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.request('PATCH', *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.request('DELETE', *args, **kwargs)

    def options(self, *args, **kwargs):
        return self.request('OPTIONS', *args, **kwargs)

    def head(self, *args, **kwargs):
        return self.request('HEAD', *args, **kwargs)


class TokenSession(requests.Session):
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.headers = {'Authorization': f'Bearer {token}'}
