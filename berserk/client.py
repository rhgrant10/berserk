# -*- coding: utf-8 -*-
import urllib

from . import session


class Client:
    base_url = 'https://lichess.org/'

    def __init__(self, session, base_url=None):
        self.base_url = base_url or self.base_url
        self.session = session

    def get_account(self):
        url = urllib.parse.urljoin(self.base_url, 'api/account')
        return self.session.get_json(url)

    def get_account_email(self):
        url = urllib.parse.urljoin(self.base_url, 'api/account/email')
        return self.session.get_json(url)

    def get_account_preferences(self):
        url = urllib.parse.urljoin(self.base_url, 'api/account/preferences')
        return self.session.get_json(url)

    def get_account_kid(self):
        url = urllib.parse.urljoin(self.base_url, 'api/account/kid')
        return self.session.get_json(url)

    def get_users_status(self, *user_ids):
        url = urllib.parse.urljoin(self.base_url, 'api/users/status')
        return self.session.get_json(url, params={'ids': ','.join(user_ids)})

    def get_player(self):
        url = urllib.parse.urljoin(self.base_url, 'player')
        return self.session.get_lichessjson(url)

    def get_player_top(self, perf_type, count=10):
        path = f'player/top/{count}/{perf_type}'
        url = urllib.parse.urljoin(self.base_url, path)
        return self.session.get_lichessjson(url)

    def get_user(self, username):
        url = urllib.parse.urljoin(self.base_url, f'api/user/{username}')
        return self.session.get_json(url)

    def get_user_activity(self, username):
        path = f'api/user/{username}/activity'
        url = urllib.parse.urljoin(self.base_url, path)
        return self.session.get_json(url)

    def get_team_users(self, team_id):
        url = urllib.parse.urljoin(self.base_url, f'team/{team_id}/users')
        return self.session.get_ndjson(url)

    def get_stream_event(self):
        url = urllib.parse.urljoin(self.base_url, 'api/stream/event')
        return self.session.get_json_stream(url)

    def get_bot_game_stream(self, game_id):
        url = urllib.parse.urljoin(self.base_url,
                                   f'api/bot/game/stream/{game_id}')
        yield from self.session.get_json_stream(url)

    def get_tournament(self):
        url = urllib.parse.urljoin(self.base_url, 'api/tournament')
        return self.session.get_json(url)

    def get_game_export(self, game_id, as_pgn=False, **params):
        url = urllib.parse.urljoin(self.base_url, f'game/export/{game_id}')
        if as_pgn:
            return self.session.get_pgn(url, params=params)
        else:
            return self.session.get_json(url, params=params)

    def get_games_export_stream(self, username, as_pgn=False, **params):
        url = urllib.parse.urljoin(self.base_url, f'games/export/{username}')
        if as_pgn:
            yield from self.session.get_pgn_stream(url, params=params)
        else:
            yield from self.session.get_json_stream(url, params=params)


class TokenClient(Client):
    def __init__(self, token):
        token_session = session.Session(token=token)
        token_session.headers = {'Authorization': f'Bearer {token}'}
        super().__init__(session=token_session)


""" Example usage:
import berserk


with open('.lichess.org') as f:
    token = f.read().strip()

client = berserk.TokenClient(token=token)
"""
