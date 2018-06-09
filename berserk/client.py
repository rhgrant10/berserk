# -*- coding: utf-8 -*-
from . import session
from .formats import JSON, LIJSON, PGN, NDJSON


class Client:
    def __init__(self, session):
        self.session = session

    # # # Account

    def get_account(self):
        path = 'api/account'
        return self.session.get(path)

    def get_account_email(self):
        path = 'api/account/email'
        return self.session.get(path)

    def get_account_preferences(self):
        path = 'api/account/preferences'
        return self.session.get(path)

    def get_kid_mode_status(self):
        path = 'api/account/kid'
        return self.session.get(path)

    def set_kid_mode_status(self, value):
        path = 'api/account/kid'
        params = {'v': value}
        return self.session.post(path, params=params)

    # # # Users

    def get_realtime_user_statuses(self, *user_ids):
        path = 'api/users/status'
        params = {'ids': ','.join(user_ids)}
        return self.session.get(path, params=params)

    def get_all_top10(self):
        path = 'player'
        return self.session.get(path, fmt=LIJSON)

    def get_one_leaderboard(self, perf_type, count=10):
        path = f'player/top/{count}/{perf_type}'
        return self.session.get(path, fmt=LIJSON)

    def get_user_public_data(self, username):
        path = f'api/user/{username}'
        return self.session.get(path)

    def get_user_activity(self, username):
        path = f'api/user/{username}/activity'
        return self.session.get(path)

    def get_users_by_id(self, *usernames):
        path = 'api/users'
        payload = {'usernames': ','.join(usernames)}
        return self.session.post(path, json=payload)

    def get_team_users(self, team_id):
        path = f'team/{team_id}/users'
        return self.session.get(path, fmt=NDJSON)

    def get_live_streamers(self):
        path = 'streamer/live'
        return self.session.get(path)

    # # # Games

    def get_game_export(self, game_id, as_pgn=False, moves=None, tags=None,
                        clocks=None, evals=None, opening=None, literate=None):
        path = f'game/export/{game_id}'
        params = {
            'moves': moves,
            'tags': tags,
            'clocks': clocks,
            'evals': evals,
            'opening': opening,
            'literate': literate,
        }
        fmt = PGN if as_pgn else JSON
        return self.session.get(path, params=params, fmt=fmt)

    def stream_game_exports(self, username, as_pgn=False, since=None,
                            until=None, max=None, vs=None, rated=None,
                            perf_type=None, color=None, analysed=None,
                            moves=None, tags=None, evals=None, opening=None):
        path = f'games/export/{username}'
        params = {
            'since': since,
            'until': until,
            'max': max,
            'vs': vs,
            'rated': rated,
            'perfType': perf_type,
            'color': color,
            'analysed': analysed,
            'moves': moves,
            'tags': tags,
            'evals': evals,
            'opening': opening,
        }
        fmt = PGN if as_pgn else NDJSON
        yield from self.session.get(path, params=params, fmt=fmt, stream=True)

    def stream_game_exports_by_id(self, *game_ids, as_pgn=False, moves=None,
                                  tags=None, clocks=None, evals=None,
                                  opening=None):
        path = 'games/export/_ids'
        params = {
            'moves': moves,
            'tags': tags,
            'clocks': clocks,
            'evals': evals,
            'opening': opening,
        }
        payload = ','.join(game_ids)
        fmt = PGN if as_pgn else NDJSON
        yield self.session.post(path, params=params, data=payload, fmt=fmt,
                                stream=True)

    def stream_current_games(self, *usernames):
        path = 'api/stream/games-by-users'
        payload = ','.join(usernames)
        yield self.session.post(path, data=payload, fmt=NDJSON, stream=True)

    def get_ongoing_games(self, count=10):
        path = 'api/account/playing'
        params = {'nb': count}
        return self.session.get(path, params=params)

    def get_current_tv_games(self):
        path = 'tv/channels'
        return self.session.get(path)

    # # # Bots

    def upgrade_to_bot_account(self):
        path = 'api/bot/account/upgrade'
        return self.session.post(path)

    def stream_incoming_events(self):
        path = 'api/stream/event'
        yield from self.session.get(path, stream=True)

    def stream_game_state(self, game_id):
        path = f'api/bot/game/stream/{game_id}'
        yield from self.session.get(path, stream=True)

    def make_move(self, game_id, move):
        path = f'api/bot/game/{game_id}/move/{move}'
        return self.session.post(path)

    def post_message(self, game_id, text, spectator=False):
        path = f'api/bot/game/{game_id}/chat'
        room = 'spectator' if spectator else 'player'
        payload = {'room': room, 'text': text}
        return self.session.post(path, json=payload)

    def abort_game(self, game_id):
        path = f'api/bot/game/{game_id}/abort'
        return self.session.post(path)

    def resign_game(self, game_id):
        path = f'api/bot/game/{game_id}/resign'
        return self.session.post(path)

    def accept_challenge(self, challenge_id):
        path = f'api/challenge/{challenge_id}/accept'
        return self.session.post(path)

    def decline_challenge(self, challenge_id):
        path = f'api/challenge/{challenge_id}/decline'
        return self.session.post(path)

    # # # Tournaments

    def get_current_tournaments(self):
        path = 'api/tournament'
        return self.session.get(path)

    def create_tournament(self, clock_time, clock_increment, minutes,
                          name=None, wait_minutes=None, variant=None,
                          mode=None, berserkable=None, private=None,
                          password=None):
        path = 'api/tournament'
        payload = {
            'name': name,
            'clockTime': clock_time,
            'clockIncrement': clock_increment,
            'minutes': minutes,
            'waitMinutes': wait_minutes,
            'variant': variant,
            'mode': mode,
            'berserkable': berserkable,
            'private': private,
            'password': password,
        }
        return self.session.post(path, json=payload)


class TokenClient(Client):
    def __init__(self, token):
        token_session = session.TokenSession(token=token)
        super().__init__(session=token_session)
