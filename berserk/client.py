# -*- coding: utf-8 -*-
import urllib

from . import session


class Client:
    def __init__(self, session):
        self.session = session

    def get_account(self):
        path = 'api/account'
        return self.session.get_json(path)

    def get_account_email(self):
        path = 'api/account/email'
        return self.session.get_json(path)

    def get_account_preferences(self):
        path = 'api/account/preferences'
        return self.session.get_json(path)

    def get_account_kid(self):
        path = 'api/account/kid'
        return self.session.get_json(path)

    def get_users_status(self, *user_ids):
        path = 'api/users/status'
        params = {'ids': ','.join(user_ids)}
        return self.session.get_json(path, params=params)

    def get_player(self):
        path = 'player'
        return self.session.get_lichessjson(path)

    def get_player_top(self, perf_type, count=10):
        path = f'player/top/{count}/{perf_type}'
        return self.session.get_lichessjson(path)

    def get_user(self, username):
        path = f'api/user/{username}'
        return self.session.get_json(path)

    def get_users_by_id(self, *usernames):
        path = 'api/users'
        payload = {'usernames': ','.join(usernames)}
        response = self.session.post(path, json=payload)
        return response.json()

    def get_user_activity(self, username):
        path = f'api/user/{username}/activity'
        return self.session.get_json(path)

    def get_team_users(self, team_id):
        path = f'team/{team_id}/users'
        return self.session.get_ndjson(path)

    def get_stream_event(self):
        path = 'api/stream/event'
        return self.session.get_json_stream(path)

    def get_bot_game_stream(self, game_id):
        path = f'api/bot/game/stream/{game_id}'
        yield from self.session.get_json_stream(path)

    def get_tournament(self):
        path = 'api/tournament'
        return self.session.get_json(path)

    def get_game_export(self, game_id, as_pgn=False, **params):
        path = f'game/export/{game_id}'
        if as_pgn:
            return self.session.get_pgn(path, params=params)
        else:
            return self.session.get_json(path, params=params)

    def get_games_export_stream(self, username, as_pgn=False, **params):
        path = f'games/export/{username}'
        if as_pgn:
            yield from self.session.get_pgn_stream(path, params=params)
        else:
            yield from self.session.get_json_stream(path, params=params)


class TokenClient(Client):
    def __init__(self, token):
        token_session = session.TokenSession(token=token)
        super().__init__(session=token_session)


""" Example usage:
import berserk


with open('.lichess.org') as f:
    token = f.read().strip()

client = berserk.TokenClient(token=token)
"""
