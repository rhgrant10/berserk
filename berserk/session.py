# -*- coding: utf-8 -*-
import urllib

import requests

from . import utils


class Requestor:
    """Encapsulates the logic for making a request.

    :param session: the authenticated session object
    :type session: :class:`requests.Session`
    :param str base_url: the base URL for requests
    :param fmt: default format handler to use
    :type fmt: :class:`~berserk.formats.FormatHandler`
    """

    def __init__(self, session, base_url, default_fmt):
        self.session = session
        self.base_url = base_url
        self.default_fmt = default_fmt

    def request(self, method, path, *args, fmt=None, converter=utils.noop,
                **kwargs):
        """Make a request for a resource in a paticular format.

        :param str method: HTTP verb
        :param str path: the URL suffix
        :param fmt: the format handler
        :type fmt: :class:`~berserk.formats.FormatHandler`
        :param func converter: function to handle field conversions
        :return: response
        :raises requests.exceptions.RequestException: if the status is >=400
        """
        fmt = fmt or self.default_fmt
        kwargs['headers'] = fmt.headers
        url = urllib.parse.urljoin(self.base_url, path)

        response = self.session.request(method, url, *args, **kwargs)
        if not response.ok:
            response.raise_for_status()

        return fmt.handle(response, is_stream=kwargs.get('stream'),
                          converter=converter)

    def get(self, *args, **kwargs):
        """Convenience method to make a GET request."""
        return self.request('GET', *args, **kwargs)

    def post(self, *args, **kwargs):
        """Convenience method to make a POST request."""
        return self.request('POST', *args, **kwargs)


class TokenSession(requests.Session):
    """Session capable of personal API token authentication.

    :param str token: personal API token
    """

    def __init__(self, token):
        super().__init__()
        self.token = token
        self.headers = {'Authorization': f'Bearer {token}'}
