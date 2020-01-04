# -*- coding: utf-8 -*-
import requests

from .session import Requestor
from .formats import JSON, LIJSON, PGN, NDJSON
from . import models


__all__ = [
    'Client', 'Account', 'Users', 'Games', 'Challenges', 'Bots', 'Tournaments',
]


class BaseClient:

    def __init__(self, session, base_url):
        self._r = Requestor(session, base_url, default_fmt=JSON)


class Client(BaseClient):
    """Main touchpoint for the API.

    The client contains all the endpoints in logical (hopefully) namespaces.

    - :class:`account <berserk.clients.Account>` - managing account information
    - :class:`users <berserk.clients.Users>` - getting information about users
    - :class:`games <berserk.clients.Games>` - getting and exporting games
    - :class:`bots <berserk.clients.Challenges>` - using challenges
    - :class:`bots <berserk.clients.Bots>` - performing bot operations
    - :class:`tournaments <berserk.clients.Tournaments>` - getting and creating
      tournaments

    :param session: request session, authenticated as needed
    :type session: :class:`requests.Session`
    :param str base_url: base URL for the API
    :param bool pgn_as_default: ``True`` if PGN should be the default format
                                for game exports when possible. This defaults
                                to ``False`` and is used as a fallback when
                                ``as_pgn`` is left as ``None`` for methods that
                                support it.
    """

    def __init__(self, session=None, base_url='https://lichess.org/',
                 pgn_as_default=False):
        session = session or requests.Session()
        super().__init__(session, base_url)
        self.account = Account(session, base_url)
        self.users = Users(session, base_url)
        self.games = Games(session, base_url, pgn_as_default=pgn_as_default)
        self.challenges = Challenges(session, base_url)
        self.bots = Bots(session, base_url)
        self.tournaments = Tournaments(session, base_url)


class Account(BaseClient):
    """Client for account-related endpoints."""

    def get(self):
        """Get your public information.

        :return: public information about the authenticated user
        :rtype: dict
        """
        path = 'api/account'
        return self._r.get(path, converter=models.Account.convert)

    def get_email(self):
        """Get your email address.

        :return: email address of the authenticated user
        :rtype: str
        """
        path = 'api/account/email'
        return self._r.get(path)['email']

    def get_preferences(self):
        """Get your account preferences.

        :return: preferences of the authenticated user
        :rtype: dict
        """
        path = 'api/account/preferences'
        return self._r.get(path)['prefs']

    def get_kid_mode(self):
        """Get your kid mode status.

        :return: current kid mode status
        :rtype: bool
        """
        path = 'api/account/kid'
        return self._r.get(path)['kid']

    def set_kid_mode(self, value):
        """Set your kid mode status.

        :param bool value: whether to enable or disable kid mode
        :return: success
        :rtype: bool
        """
        path = 'api/account/kid'
        params = {'v': value}
        return self._r.post(path, params=params)['ok']

    def upgrade_to_bot(self):
        """Upgrade your account to a bot account.

        Requires bot:play oauth scope. User cannot have any previously played
        games.

        :return: success
        :rtype: bool
        """
        path = 'api/bot/account/upgrade'
        return self._r.post(path)['ok']


class Users(BaseClient):
    """Client for user-related endpoints."""

    def get_realtime_statuses(self, *user_ids):
        """Get the online, playing, and streaming statuses of players.

        Only id and name fields are returned for offline users.

        :param user_ids: one or more user IDs (names)
        :return: statuses of given players
        :rtype: list
        """
        path = 'api/users/status'
        params = {'ids': ','.join(user_ids)}
        return self._r.get(path, params=params)

    def get_all_top_10(self):
        """Get the top 10 players for each speed and variant.

        :return: top 10 players in each speed and variant
        :rtype: dict
        """
        path = 'player'
        return self._r.get(path, fmt=LIJSON)

    def get_leaderboard(self, perf_type, count=10):
        """Get the leaderboard for one speed or variant.

        :param perf_type: speed or variant
        :type perf_type: :class:`~berserk.enums.PerfType`
        :param int count: number of players to get
        :return: top players for one speed or variant
        :rtype: list
        """
        path = f'player/top/{count}/{perf_type}'
        return self._r.get(path, fmt=LIJSON)['users']

    def get_public_data(self, username):
        """Get the public data for a user.

        :param str username: username
        :return: public data available for the given user
        :rtype: dict
        """
        path = f'api/user/{username}'
        return self._r.get(path, converter=models.User.convert)

    def get_activity_feed(self, username):
        """Get the activity feed of a user.

        :param str username: username
        :return: activity feed of the given user
        :rtype: list
        """
        path = f'api/user/{username}/activity'
        return self._r.get(path, converter=models.Activity.convert)

    def get_by_id(self, *usernames):
        """Get multiple users by their IDs.

        :param usernames: one or more usernames
        :return: user data for the given usernames
        :rtype: list
        """
        path = 'api/users'
        return self._r.post(path, data=','.join(usernames),
                            converter=models.User.convert)

    def get_by_team(self, team_id):
        """Get members of a team.

        :param str team_id: ID of a team
        :return: users on the given team
        :rtype: iter
        """
        path = f'team/{team_id}/users'
        return self._r.get(path, fmt=NDJSON, stream=True,
                           converter=models.User.convert)

    def get_live_streamers(self):
        """Get basic information about currently streaming users.

        :return: users currently streaming a game
        :rtype: list
        """
        path = 'streamer/live'
        return self._r.get(path)


class Games(BaseClient):
    """Client for games-related endpoints.

    :param session: request session, authenticated as needed
    :type session: :class:`requests.Session`
    :param str base_url: base URL for the API
    :param bool pgn_as_default: ``True`` if PGN should be the default format
                                for game exports when possible. This defaults
                                to ``False`` and is used as a fallback when
                                ``as_pgn`` is left as ``None`` for methods that
                                support it.
    """

    def __init__(self, session, base_url='https://lichess.org/',
                 pgn_as_default=False):
        super().__init__(session, base_url)
        self.pgn_as_default = pgn_as_default

    def _use_pgn(self, as_pgn):
        return as_pgn if as_pgn is not None else self.pgn_as_default

    def export(self, game_id, as_pgn=None, moves=None, tags=None, clocks=None,
               evals=None, opening=None, literate=None):
        """Get one finished game as PGN or JSON.

        :param str game_id: the ID of the game to export
        :param bool as_pgn: whether to return the game in PGN format
        :param bool moves: whether to include the PGN moves
        :param bool tags: whether to include the PGN tags
        :param bool clocks: whether to include clock comments in the PGN moves
        :param bool evals: whether to include analysis evaluation comments in
                           the PGN moves when available
        :param bool opening: whether to include the opening name
        :param bool literate: whether to include literate the PGN
        :return: exported game, as JSON or PGN
        """
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
        return self._r.get(path, params=params, fmt=fmt,
                           converter=models.Game.convert)

    def export_by_player(self, username, as_pgn=None, since=None, until=None,
                         max=None, vs=None, rated=None, perf_type=None,
                         color=None, analysed=None, moves=None, tags=None,
                         evals=None, opening=None):
        """Get games by player.

        :param str username: which player's games to return
        :param bool as_pgn: whether to return the game in PGN format
        :param int since: lowerbound on the game timestamp
        :param int until: upperbound on the game timestamp
        :param int max: limit the number of games returned
        :param str vs: filter by username of the opponent
        :param bool rated: filter by game mode (``True`` for rated, ``False``
                           for casual)
        :param perf_type: filter by speed or variant
        :type perf_type: :class:`~berserk.enums.PerfType`
        :param color: filter by the color of the player
        :type color: :class:`~berserk.enums.Color`
        :param bool analysed: filter by analysis availability
        :param bool moves: whether to include the PGN moves
        :param bool tags: whether to include the PGN tags
        :param bool clocks: whether to include clock comments in the PGN moves
        :param bool evals: whether to include analysis evaluation comments in
                           the PGN moves when available
        :param bool opening: whether to include the opening name
        :param bool literate: whether to include literate the PGN
        :return: iterator over the exported games, as JSON or PGN
        """
        path = f'api/games/user/{username}'
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
        yield from self._r.get(path, params=params, fmt=fmt, stream=True,
                               converter=models.Game.convert)

    def export_multi(self, *game_ids, as_pgn=None, moves=None, tags=None,
                     clocks=None, evals=None, opening=None):
        """Get multiple games by ID.

        :param game_ids: one or more game IDs to export
        :param bool as_pgn: whether to return the game in PGN format
        :param bool moves: whether to include the PGN moves
        :param bool tags: whether to include the PGN tags
        :param bool clocks: whether to include clock comments in the PGN moves
        :param bool evals: whether to include analysis evaluation comments in
                           the PGN moves when available
        :param bool opening: whether to include the opening name
        :return: iterator over the exported games, as JSON or PGN
        """
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
        yield from self._r.post(path, params=params, data=payload, fmt=fmt,
                                stream=True, converter=models.Game.convert)

    def get_among_players(self, *usernames):
        """Get the games currently being played among players.

        Note this will not includes games where only one player is in the given
        list of usernames.

        :param usernames: two or more usernames
        :return: iterator over all games played among the given players
        """
        path = 'api/stream/games-by-users'
        payload = ','.join(usernames)
        yield from self._r.post(path, data=payload, fmt=NDJSON, stream=True,
                                converter=models.Game.convert)

    # move this to Account?
    def get_ongoing(self, count=10):
        """Get your currently ongoing games.

        :param int count: number of games to get
        :return: some number of currently ongoing games
        :rtype: list
        """
        path = 'api/account/playing'
        params = {'nb': count}
        return self._r.get(path, params=params)['nowPlaying']

    def get_tv_channels(self):
        """Get basic information about the best games being played.

        :return: best ongoing games in each speed and variant
        :rtype: dict
        """
        path = 'tv/channels'
        return self._r.get(path)


class Challenges(BaseClient):

    def create(self, username, rated, clock_limit=None, clock_increment=None,
               days=None, color=None, variant=None, position=None):
        """Challenge another player to a game.

        :param str username: username of the player to challege
        :param bool rated: whether or not the game will be rated
        :param int clock_limit: clock initial time (in seconds)
        :param int clock_increment: clock increment (in seconds)
        :param int days: days per move (for correspondence games; omit clock)
        :param color: color of the accepting player
        :type color: :class:`~berserk.enums.Color`
        :param variant: game variant to use
        :type variant: :class:`~berserk.enums.Variant`
        :param position: use one of the custom initial positions (cannot be a
                         rated game)
        :type position: :class:`~berserk.enums.Position`
        :return: success indicator
        :rtype: bool
        """
        path = f'api/challenge/{username}'
        payload = {
            'username': username,
            'rated': rated,
            'clock.limit': clock_limit,
            'clock.increment': clock_increment,
            'days': days,
            'color': color,
            'variant': variant,
            'position': position,
        }
        return self._r.post(path, json=payload,
                            converter=models.Tournament.convert)

    def accept(self, challenge_id):
        """Accept an incoming challenge.

        :param str challenge_id: id of the challenge to accept
        :return: success indicator
        :rtype: bool
        """
        path = f'api/challenge/{challenge_id}/accept'
        return self._r.post(path)['ok']

    def decline(self, challenge_id):
        """Decline an incoming challenge.

        :param str challenge_id: id of the challenge to decline
        :return: success indicator
        :rtype: bool
        """
        path = f'api/challenge/{challenge_id}/decline'
        return self._r.post(path)['ok']


class Bots(BaseClient):
    """Client for bot-related endpoints."""

    def stream_incoming_events(self):
        """Get your realtime stream of incoming events."""
        path = 'api/stream/event'
        yield from self._r.get(path, stream=True)

    def stream_game_state(self, game_id):
        """Get the stream of events for a bot game."""
        path = f'api/bot/game/stream/{game_id}'
        yield from self._r.get(path, stream=True,
                               converter=models.GameState.convert)

    def make_move(self, game_id, move):
        """Make a move in a bot game."""
        path = f'api/bot/game/{game_id}/move/{move}'
        return self._r.post(path)['ok']

    def post_message(self, game_id, text, spectator=False):
        """Post a message in a bot game."""
        path = f'api/bot/game/{game_id}/chat'
        room = 'spectator' if spectator else 'player'
        payload = {'room': room, 'text': text}
        return self._r.post(path, json=payload)['ok']

    def abort_game(self, game_id):
        """Abort a bot game."""
        path = f'api/bot/game/{game_id}/abort'
        return self._r.post(path)['ok']

    def resign_game(self, game_id):
        """Resign a bot game."""
        path = f'api/bot/game/{game_id}/resign'
        return self._r.post(path)['ok']

    def accept_challenge(self, challenge_id):
        """Accept an incoming challenge."""
        path = f'api/challenge/{challenge_id}/accept'
        return self._r.post(path)['ok']

    def decline_challenge(self, challenge_id):
        """Decline an incoming challenge."""
        path = f'api/challenge/{challenge_id}/decline'
        return self._r.post(path)['ok']


class Tournaments(BaseClient):
    """Client for tournament-related endpoints."""

    def get(self):
        """Get recently finished, ongoing, and upcoming tournaments."""
        path = 'api/tournament'
        return self._r.get(path, converter=models.Tournaments.convert_values)

    def create(self, clock_time, clock_increment, minutes, name=None,
               wait_minutes=None, variant=None, mode=None, berserkable=None,
               start_date=None, position=None, private=None, password=None):
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
            'start_date': start_date,
            'position': position,
            'private': private,
            'password': password,
        }
        return self._r.post(path, json=payload,
                            converter=models.Tournament.convert)
