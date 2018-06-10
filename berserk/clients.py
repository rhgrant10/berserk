# -*- coding: utf-8 -*-
from .session import Requestor
from .formats import JSON, LIJSON, PGN, NDJSON


class Client:
    def __init__(self, session, base_url='https://lichess.org/',
                 pgn_as_default=False):
        self._r = Requestor(session, base_url, default_fmt=JSON)
        self.account = Account(session, base_url)
        self.users = Users(session, base_url)
        self.games = Games(session, base_url, pgn_as_default=pgn_as_default)
        self.bots = Bots(session, base_url)
        self.tournaments = Tournaments(session, base_url)


class Account(Client):
    def get(self):
        """Get your public information."""
        path = 'api/account'
        return self._r.get(path)

    def get_email(self):
        """Get your email address."""
        path = 'api/account/email'
        return self._r.get(path)

    def get_preferences(self):
        """Get your account preferences."""
        path = 'api/account/preferences'
        return self._r.get(path)

    def get_kid_mode(self):
        """Get your kid mode status."""
        path = 'api/account/kid'
        return self._r.get(path)

    def set_kid_mode(self, value):
        """Set your kid mode status."""
        path = 'api/account/kid'
        params = {'v': value}
        return self._r.post(path, params=params)

    def upgrade_to_bot(self):
        """Upgrade your account to a bot account."""
        path = 'api/bot/account/upgrade'
        return self._r.post(path)


class Users(Client):
    def get_realtime_statuses(self, *user_ids):
        """Get the online, playing, and streaming statuses of players."""
        path = 'api/users/status'
        params = {'ids': ','.join(user_ids)}
        return self._r.get(path, params=params)

    def get_all_top_10(self):
        """Get the top 10 players for each speed and variant."""
        path = 'player'
        return self._r.get(path, fmt=LIJSON)

    def get_leaderboard(self, perf_type, count=10):
        """Get the leaderboard for one speed or variant."""
        path = f'player/top/{count}/{perf_type}'
        return self._r.get(path, fmt=LIJSON)

    def get_public_data(self, username):
        """Get the public data for a user."""
        path = f'api/user/{username}'
        return self._r.get(path)

    def get_activity_feed(self, username):
        """Get the activity feed of a user."""
        path = f'api/user/{username}/activity'
        return self._r.get(path)

    def get_by_id(self, *usernames):
        """Get multiple users by their IDs."""
        path = 'api/users'
        payload = {'usernames': ','.join(usernames)}
        return self._r.post(path, json=payload)

    def get_by_team(self, team_id):
        """Get members of a team."""
        path = f'team/{team_id}/users'
        return self._r.get(path, fmt=NDJSON)

    def get_live_streamers(self):
        """Get basic information about currently streaming users."""
        path = 'streamer/live'
        return self._r.get(path)


class Games(Client):
    def __init__(self, session, base_url='https://lichess.org/',
                 pgn_as_default=False):
        super().__init__(session, base_url)
        self.pgn_as_default = pgn_as_default

    def _use_pgn(self, as_pgn):
        return as_pgn if as_pgn is not None else self.pgn_as_default

    def get_export(self, game_id, as_pgn=None, moves=None, tags=None,
                   clocks=None, evals=None, opening=None, literate=None):
        """Get one finished game as PGN or JSON."""
        path = f'game/export/{game_id}'
        params = {
            'moves': moves,
            'tags': tags,
            'clocks': clocks,
            'evals': evals,
            'opening': opening,
            'literate': literate,
        }
        fmt = PGN if self._use_pgn(as_pgn) else JSON
        return self._r.get(path, params=params, fmt=fmt)

    def stream_exports(self, username, as_pgn=None, since=None, until=None,
                       max=None, vs=None, rated=None, perf_type=None,
                       color=None, analysed=None, moves=None, tags=None,
                       evals=None, opening=None):
        """Get all games of any user as PGN or JSON."""
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
        fmt = PGN if self._use_pgn(as_pgn) else NDJSON
        yield from self._r.get(path, params=params, fmt=fmt, stream=True)

    def stream_exports_by_id(self, *game_ids, as_pgn=None, moves=None,
                             tags=None, clocks=None, evals=None, opening=None):
        """Get games by ID in PGN or JSON."""
        path = 'games/export/_ids'
        params = {
            'moves': moves,
            'tags': tags,
            'clocks': clocks,
            'evals': evals,
            'opening': opening,
        }
        payload = ','.join(game_ids)
        fmt = PGN if self._use_pgn(as_pgn) else NDJSON
        yield self._r.post(path, params=params, data=payload, fmt=fmt,
                           stream=True)

    def stream_by_users(self, *usernames):
        """Get the games currently being played between players."""
        path = 'api/stream/games-by-users'
        payload = ','.join(usernames)
        yield self._r.post(path, data=payload, fmt=NDJSON, stream=True)

    def get_ongoing(self, count=10):
        """Get your currently ongoing games."""
        path = 'api/account/playing'
        params = {'nb': count}
        return self._r.get(path, params=params)

    def get_tv_channels(self):
        """Get basic information about the best games being played."""
        path = 'tv/channels'
        return self._r.get(path)


class Bots(Client):
    def stream_incoming_events(self):
        """Get your realtime stream of incoming events."""
        path = 'api/stream/event'
        yield from self._r.get(path, stream=True)

    def stream_game_state(self, game_id):
        """Get the stream of events for a bot game."""
        path = f'api/bot/game/stream/{game_id}'
        yield from self._r.get(path, stream=True)

    def make_move(self, game_id, move):
        """Make a move in a bot game."""
        path = f'api/bot/game/{game_id}/move/{move}'
        return self._r.post(path)

    def post_message(self, game_id, text, spectator=False):
        """Post a message in a bot game."""
        path = f'api/bot/game/{game_id}/chat'
        room = 'spectator' if spectator else 'player'
        payload = {'room': room, 'text': text}
        return self._r.post(path, json=payload)

    def abort_game(self, game_id):
        """Abort a bot game."""
        path = f'api/bot/game/{game_id}/abort'
        return self._r.post(path)

    def resign_game(self, game_id):
        """Resign a bot game."""
        path = f'api/bot/game/{game_id}/resign'
        return self._r.post(path)

    def accept_challenge(self, challenge_id):
        """Accept an incoming challenge."""
        path = f'api/challenge/{challenge_id}/accept'
        return self._r.post(path)

    def decline_challenge(self, challenge_id):
        """Decline an incoming challenge."""
        path = f'api/challenge/{challenge_id}/decline'
        return self._r.post(path)


class Tournaments(Client):
    def get(self):
        """Get recently finished, ongoing, and upcoming tournaments."""
        path = 'api/tournament'
        return self._r.get(path)

    def create(self, clock_time, clock_increment, minutes, name=None,
               wait_minutes=None, variant=None, mode=None, berserkable=None,
               private=None, password=None):
        """Create a new tournament."""
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
        return self._r.post(path, json=payload)
