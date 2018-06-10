# -*- coding: utf-8 -*-
import json

import ndjson


class FormatHandler:
    """Provide request headers and parse responses for a particular format.

    Instances of this class should override the :meth:`parse_stream` and
    :meth:`parse` methods to support handling both streaming and non-streaming
    responses.

    :param str mime_type: the MIME type for the format
    """

    def __init__(self, mime_type):
        self.mime_type = mime_type
        self.headers = {'Accept': mime_type}

    def handle(self, response, is_stream):
        """Handle the response by returning the data.

        :param response: raw response
        :type response: :class:`requests.Response`
        :param bool is_stream: ``True`` if the response is a stream
        :return: either all response data or an iterator of response data
        """
        if is_stream:
            return iter(self.parse_stream(response))
        else:
            return self.parse(response)

    def parse(self, response):
        """Parse all data from a response.

        :param response: raw response
        :type response: :class:`requests.Response`
        :return: response data
        """
        return response

    def parse_stream(self, response):
        """Yield the parsed data from a stream response.

        :param response: raw response
        :type response: :class:`requests.Response`
        :return: iterator over the response data
        """
        yield response


class JsonHandler(FormatHandler):
    """Handle JSON data.

    :param str mime_type: the MIME type for the format
    """

    #: mapping of MIME types to :class:`~json.JSONDecoder` classes
    decoder_ring = {
        'application/json': json.JSONDecoder,
        'application/vnd.lichess.v3+json': json.JSONDecoder,
        'application/x-ndjson': ndjson.Decoder,
    }

    def __init__(self, mime_type):
        super().__init__(mime_type=mime_type)
        self.decoder = self.decoder_ring.get(self.mime_type)

    def parse(self, response):
        """Parse all JSON data from a response.

        :param response: raw response
        :type response: :class:`requests.Response`
        :return: response data
        :rtype: JSON
        """
        return response.json(cls=self.decoder)

    def parse_stream(self, response):
        """Yield the parsed data from a stream response.

        :param response: raw response
        :type response: :class:`requests.Response`
        :return: iterator over multiple JSON objects
        """
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                yield json.loads(decoded_line)


class PgnHanlder(FormatHandler):
    """Handle PGN data."""

    def __init__(self):
        super().__init__(mime_type='application/x-chess-pgn')

    def parse(self, response):
        """Parse all text data from a response.

        :param response: raw response
        :type response: :class:`requests.Response`
        :return: response text
        :rtype: str
        """
        return response.text

    def parse_stream(self, response):
        """Yield the parsed PGN games from a stream response.

        :param response: raw response
        :type response: :class:`requests.Response`
        :return: iterator over multiple PGN texts
        """
        lines = []
        last_line = True
        for line in response.iter_lines():
            decoded_line = line.decode('utf-8')
            if last_line or decoded_line:
                lines.append(decoded_line)
            else:
                yield '\n'.join(lines)
                lines = []
            last_line = decoded_line


#: Handles vanilla JSON
JSON = JsonHandler(mime_type='application/json')

#: Handles oddball LiChess JSON (normal JSON, crazy MIME type)
LIJSON = JsonHandler(mime_type='application/vnd.lichess.v3+json')

#: Handles newline-delimited JSON
NDJSON = JsonHandler(mime_type='application/x-ndjson')

#: Handles PGN
PGN = PgnHanlder()
