# -*- coding: utf-8 -*-
import json

import ndjson


class FormatHandler:
    def __init__(self, mime_type):
        self.mime_type = mime_type
        self.headers = {'Accept': mime_type}

    def handle(self, response, is_stream):
        if is_stream:
            return iter(self.parse_stream(response))
        else:
            return self.parse(response)

    def parse(self, response):
        return response

    def parse_stream(self, response):
        yield response


class JsonHandler(FormatHandler):
    decoder_ring = {
        'application/json': json.JSONDecoder,
        'application/vnd.lichess.v3+json': json.JSONDecoder,
        'application/x-ndjson': ndjson.Decoder,
    }

    def __init__(self, mime_type='application/json', *args, **kwargs):
        super().__init__(*args, mime_type=mime_type, **kwargs)
        self.decoder = self.decoder_ring.get(self.mime_type)

    def parse(self, response):
        return response.json(cls=self.decoder)

    def parse_stream(self, response):
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8')
                yield json.loads(decoded_line)


class PgnHanlder(FormatHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, mime_type='application/x-chess-pgn', **kwargs)

    def parse(self, response):
        return response.text

    def parse_stream(self, response):
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


JSON = JsonHandler(mime_type='application/json')
LIJSON = JsonHandler(mime_type='application/vnd.lichess.v3+json')
NDJSON = JsonHandler(mime_type='application/x-ndjson')
PGN = PgnHanlder()
