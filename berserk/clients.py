# -*- coding: utf-8 -*-
from time import time as now
import requests
from deprecated import deprecated

from .session import Requestor
from .formats import JSON, LIJSON, PGN, NDJSON, TEXT
from . import models


__all__ = [
    'Client',
    'Account',
    'Board',
    'Bots',
    'Broadcasts',
    'Challenges',
    'Games',
    'Simuls',
    'Studies',
    'Teams',
    'Tournaments',
    'Users',
    'TV',
    'Puzzles',
    'OpeningExplorer',
]


# Base URL for the API
API_URL = 'https://lichess.org/'


class BaseClient:

    def __init__(self, session, base_url=None):
        self._r = Requestor(session, base_url or API_URL, default_fmt=JSON)


class FmtClient(BaseClient):
    """Client that can return PGN or not.

    :param session: request session, authenticated as needed
    :type session: :class:`requests.Session`
    :param str base_url: base URL for the API
    :param bool pgn_as_default: ``True`` if PGN should be the default format
                                for game exports when possible. This defaults
                                to ``False`` and is used as a fallback when
                                ``as_pgn`` is left as ``None`` for methods that
                                support it.
    """

    def __init__(self, session, base_url=None, pgn_as_default=False):
        super().__init__(session, base_url)
        self.pgn_as_default = pgn_as_default

    def _use_pgn(self, as_pgn=None):
        # helper to merge default with provided arg
        return as_pgn if as_pgn is not None else self.pgn_as_default


class Client(BaseClient):
    """Main touchpoint for the API.

    All endpoints are namespaced into the clients below:

    - :class:`account <berserk.clients.Account>` - managing account information
    - :class:`bots <berserk.clients.Bots>` - performing bot operations
    - :class:`broadcasts <berserk.clients.Broadcasts>` - getting and creating
      broadcasts
    - :class:`challenges <berserk.clients.Challenges>` - using challenges
    - :class:`games <berserk.clients.Games>` - getting and exporting games
    - :class:`simuls <berserk.clients.Simuls>` - getting simultaneous
      exhibition games
    - :class:`studies <berserk.clients.Studies>` - exporting studies
    - :class:`teams <berserk.clients.Teams>` - getting information about teams
    - :class:`tournaments <berserk.clients.Tournaments>` - getting and
      creating tournaments
    - :class:`users <berserk.clients.Users>` - getting information about users
    - :class:`TV <berserk.clients.TV>` - getting information about lichess tv

    :param session: request session, authenticated as needed
    :type session: :class:`requests.Session`
    :param str base_url: base API URL to use (if other than the default)
    :param bool pgn_as_default: ``True`` if PGN should be the default format
                                for game exports when possible. This defaults
                                to ``False`` and is used as a fallback when
                                ``as_pgn`` is left as ``None`` for methods that
                                support it.
    """

    def __init__(self, session=None, base_url=None, pgn_as_default=False):
        session = session or requests.Session()
        super().__init__(session, base_url)
        self.account = Account(session, base_url)
        self.users = Users(session, base_url)
        self.relations = Relations(session, base_url)
        self.teams = Teams(session, base_url)
        self.games = Games(session, base_url, pgn_as_default=pgn_as_default)
        self.challenges = Challenges(session, base_url)
        self.board = Board(session, base_url)
        self.bots = Bots(session, base_url)
        self.tournaments = Tournaments(session, base_url,
                                       pgn_as_default=pgn_as_default)
        self.broadcasts = Broadcasts(session, base_url)
        self.simuls = Simuls(session, base_url)
        self.studies = Studies(session, base_url)
        self.tv = TV(session, base_url)
        self.puzzles = Puzzles(session, base_url)
        self.opening_explorer = OpeningExplorer(session, 'https://explorer.lichess.ovh/')


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

    @deprecated(version='1.0.0', reason='use Bots.upgrade_to_bot instead')
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

    def get_puzzle_activity(self, max=None):
        """Stream puzzle activity history starting with the most recent.

        :param int max: maximum number of entries to stream
        :return: puzzle activity history
        :rtype: iter
        """
        path = 'api/user/puzzle-activity'
        params = {'max': max}
        return self._r.get(path, params=params, fmt=NDJSON, stream=True,
                           converter=models.PuzzleActivity.convert)

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

    @deprecated(version='0.7.0', reason='use Teams.get_members(id) instead')
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

    @deprecated(version='1.0.0', reason='moved to Relations')
    def get_users_followed(self, username):
        """Stream users followed by a user.

        :param str username: a username
        :return: iterator over the users the given user follows
        :rtype: iter
        """
        path = f'/api/user/{username}/following'
        return self._r.get(path, stream=True, fmt=NDJSON,
                           converter=models.User.convert)

    @deprecated(version='1.0.0', reason='moved to relations and removed')
    def get_users_following(self, username):
        """Stream users who follow a user.

        :param str username: a username
        :return: iterator over the users that follow the given user
        :rtype: iter
        """
        path = f'/api/user/{username}/followers'
        return self._r.get(path, stream=True, fmt=NDJSON,
                           converter=models.User.convert)

    def get_rating_history(self, username):
        """Get the rating history of a user.

        :param str username: a username
        :return: rating history for all game types
        :rtype: list
        """
        path = f'/api/user/{username}/rating-history'
        return self._r.get(path, converter=models.RatingHistory.convert)

    def get_performance_statistics(self, username, perf):
        """Get the performance statistics of a user.

        :param str username: a username
        :param str perf: a perf (https://lichess.org/api#operation/apiUserPerf)
        :return: performance history of username in perf
        :rtype: list
        """
        path = f'/api/user/{username}/perf/{perf}'
        return self._r.get(path, converter=models.User.convert)

    def get_crosstable(self, user1, user2, matchup=False):
        """Get the crosstable between user1 and user2.

        When using matchup it adds

        :param str user1: a username
        :param str user2: a username
        :param bool matchup: get matchup
        :return: dict {"user1": ..., "user2": ..., "nbGames": ...
            [, "matchup": {"user1": ..., "user2": ..., "nbGames": ...}]}
            or False if failed.
        :rtype: dict
        """
        matchup = str(matchup).lower()
        path = f'/api/crosstable/{user1}/{user2}?matchup={matchup}'
        result = self._r.get(path, converter=models.User.convert)
        base = {user1: result['users'][user1.lower()],
                user2: result['users'][user2.lower()],
                'nbGames': result['nbGames']}
        if matchup == "true":
            if not base.get('matchup', False):
                return False
            base['matchup'] = {}
            base['matchup'][user1] = result['matchup']['users'][user1.lower()]
            base['matchup'][user2] = result['matchup']['users'][user2.lower()]
            base['matchup']['nbGames'] = result['matchup']['nbGames']
        return base


class Relations(BaseClient):

    def get_users_followed(self, username):
        """Stream users followed by a user.

        :param str username: a username
        :return: iterator over the users the given user follows
        :rtype: iter
        """
        path = f'/api/user/{username}/following'
        return self._r.get(path, stream=True, fmt=NDJSON,
                           converter=models.User.convert)

    @deprecated(version='1.0.0', reason='Removed from Lichess API.')
    def get_users_following(self, username):
        """Stream users who follow a user.

        :param str username: a username
        :return: iterator over the users that follow the given user
        :rtype: iter
        """
        path = f'/api/user/{username}/followers'
        return self._r.get(path, stream=True, fmt=NDJSON,
                           converter=models.User.convert)

    def follow_user(self, username):
        """Follow a user.

        :param str username: username of player to follow.
        :return: success
        :rtype: bool
        """
        path = f'/api/rel/follow/{username}'
        return self._r.post(path)['ok']

    def unfollow_user(self, username):
        """Unfollow a user.

        :param str username: username of player to unfollow.
        :return: success
        :rtype: bool
        """
        path = f'/api/rel/unfollow/{username}'
        return self._r.post(path)['ok']


class Teams(BaseClient):
    
    def get_swiss_tournaments(self, team_id, max_tournaments=100,
                             stream=False):
        """Get swiss tournaments of a team.

        :param str team_id: ID of a team
        :param int max_tournaments: how many entries to download
        :param bool stream: whether to stream data or not
        :return: swiss tournaments of the given team
        :rtype: list or iter
        """
        path = f'api/team/{team_id}/swiss'
        params = {'max': max_tournaments}
        return self._r.get(path, params=params, stream=stream,
                          fmt=NDJSON)

    def get_team(self, team_id):
        """Get a single team informations.

        :param str team_id: ID of a team
        :return: informations about the given team
        :rtype: dict
        """
        path = f'api/team/{team_id}'
        return self._r.get(path)

    def get_popular(self, page=1):
        """Get popular teams, page by page.

        :param int page: page to get
        :return: popular teams infos
        :rtype: dict
        """
        path = f'api/team/all'
        params = {'page': page}
        return self._r.get(path, params=params)

    def get_player_teams(self, username):
        """Get teams of a player.

        :param str username: a username
        :return: teams of the given user
        :rtype: list
        """
        path = f'api/team/of/{username}'
        return self._r.get(path)

    def search_teams(self, text, page=1):
        """Search teams by keyword.

        :param str text: search keyword
        :param int page: page to get
        :return: search results
        :rtype: list
        """
        path = 'api/team/search'
        params = {'text': text, 'page': page}
        return self._r.get(path, params=params)

    def get_members(self, team_id):
        """Get members of a team.

        :param str team_id: ID of a team
        :return: users on the given team
        :rtype: iter
        """
        path = f'api/team/{team_id}/users'
        return self._r.get(path, fmt=NDJSON, stream=True,
                           converter=models.User.convert)

    def get_arena_tournaments(self, team_id, max_tournaments=100,
                             stream=False):
        """Get Arena tournaments of a team.

        :param str team_id: ID of a team
        :param int max_tournaments: how many entries to download
        :param bool stream: whether to stream data or not
        :return: arena tournaments of the given team
        :rtype: list or iter
        """
        path = f'api/team/{team_id}/arena'
        params = {'max': max_tournaments}
        return self._r.get(path, params=params, stream=stream,
                          fmt=NDJSON)

    def join(self, team_id, message=None, password=None):
        """Join a team.

        :param str team_id: ID of a team
        :param str message: optional request message, if the team requires one
        :param str password: optional password, if the team requires one
        :return: success
        :rtype: bool
        """
        path = f'team/{team_id}/join'
        payload = {
            'message': message,
            'password': password,
        }
        return self._r.post(path, data=payload)['ok']

    def leave(self, team_id):
        """Leave a team.

        :param str team_id: ID of a team
        :return: success
        :rtype: bool
        """
        path = f'team/{team_id}/quit'
        return self._r.post(path)['ok']

    def kick_member(self, team_id, user_id):
        """Kick a member out of your team.

        :param str team_id: ID of a team
        :param str user_id: ID of a team member
        :return: success
        :rtype: bool
        """
        path = f'team/{team_id}/kick/{user_id}'
        return self._r.post(path)['ok']

    def message_all(self, team_id, message):
        """Message all members of your team.

        :param str team_id: ID of a team
        :param str message: the message to send to all your team members
        :return: success
        :rtype: bool
        """
        path = f'team/{team_id}/pm-all'
        payload = {'message': message}
        return self._r.post(path, data=payload)['ok']


class Games(FmtClient):
    """Client for games-related endpoints."""

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

    def export_going(self, username, moves=True, pgn_in_json=False, tags=True,
                     clocks=True, evals=True, opening=True, literate=False,
                     players=None):
        """Get ongoing game of a player.

        :param str username: which player's games to return
        :param bool moves: whether to include the PGN moves
        :param bool pgn_in_json: whether to include the full PGN within the
            JSON response, in a ``pgn`` field
        :param bool tags: whether to include the PGN tags
        :param bool clocks: whether to include clock comments in the PGN moves,
            when available
        :param bool evals: whether to include analysis evaluation comments in
            the PGN, when available
        :param bool opening: whether to include the opening name
        :param bool literate: whether to insert textual annotations in the PGN
            about the opening, analysis variations, mistakes,
            and game termination
        :param str players: URL of a text file containing real names and
            ratings, to replace Lichess usernames and ratings in the PGN
        :return: exported game, as JSON or PGN
        """
        path = f'api/user/{username}/current-game'
        params = {
            'moves': moves,
            'pgnInJson': pgn_in_json,
            'tags': tags,
            'clocks': clocks,
            'evals': evals,
            'opening': opening,
            'literate': literate,
            'players': players,
        }
        fmt = PGN if self._use_pgn(not pgn_in_json) else JSON
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
        return self._r.get(path, params=params, fmt=fmt,
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

    @deprecated(version='1.0.0', reason='moved to tv')
    def get_tv_channels(self):
        """Get basic information about the best games being played.

        :return: best ongoing games in each speed and variant
        :rtype: dict
        """
        path = 'tv/channels'
        return self._r.get(path)

    def import_game(self, pgn):
        """Import one game from PGN.

        :param str pgn: the PGN, it can contain only one game
        :return: game id
        :rtype: str
        """
        path = 'api/import'
        payload = {'pgn': pgn}
        return self._r.post(path, data=payload)["id"]

    def stream_moves(self, id):
        """Stream moves of a game as NDJSON.

        :param str id: the ID of the game to stream
        :return: game stream
        :rtype: dict
        """
        path = f'api/stream/game/{id}'
        return self._r.get(path, stream=True)


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
        :param position: custom intial position in FEN (variant must be
                         standard and the game cannot be rated)
        :type position: str
        :return: challenge data
        :rtype: dict
        """
        path = f'api/challenge/{username}'
        payload = {
            'rated': rated,
            'clock.limit': clock_limit,
            'clock.increment': clock_increment,
            'days': days,
            'color': color,
            'variant': variant,
            'fen': position,
        }
        return self._r.post(path, json=payload,
                            converter=models.Tournament.convert)

    def create_with_accept(self, username, rated, token, clock_limit=None,
                           clock_increment=None, days=None, color=None,
                           variant=None, position=None):
        """Start a game with another player.

        This is just like the regular challenge create except it forces the
        opponent to accept. You must provide the OAuth token of the opponent
        and it must have the challenge:write scope.

        :param str username: username of the opponent
        :param bool rated: whether or not the game will be rated
        :param str token: opponent's OAuth token
        :param int clock_limit: clock initial time (in seconds)
        :param int clock_increment: clock increment (in seconds)
        :param int days: days per move (for correspondence games; omit clock)
        :param color: color of the accepting player
        :type color: :class:`~berserk.enums.Color`
        :param variant: game variant to use
        :type variant: :class:`~berserk.enums.Variant`
        :param position: custom intial position in FEN (variant must be
                         standard and the game cannot be rated)
        :type position: :class:`~berserk.enums.Position`
        :return: game data
        :rtype: dict
        """
        path = f'api/challenge/{username}'
        payload = {
            'rated': rated,
            'acceptByToken': token,
            'clock.limit': clock_limit,
            'clock.increment': clock_increment,
            'days': days,
            'color': color,
            'variant': variant,
            'fen': position,
        }
        return self._r.post(path, json=payload,
                            converter=models.Tournament.convert)

    def create_ai(self, level=8, clock_limit=None, clock_increment=None,
                  days=None, color=None, variant=None, position=None):
        """Challenge AI to a game.

        :param int level: level of the AI (1 to 8)
        :param int clock_limit: clock initial time (in seconds)
        :param int clock_increment: clock increment (in seconds)
        :param int days: days per move (for correspondence games; omit clock)
        :param color: color of the accepting player
        :type color: :class:`~berserk.enums.Color`
        :param variant: game variant to use
        :type variant: :class:`~berserk.enums.Variant`
        :param position: use one of the custom initial positions (variant must
                         be standard and cannot be rated)
        :type position: str
        :return: success indicator
        :rtype: bool
        """
        path = 'api/challenge/ai'
        payload = {
            'level': level,
            'clock.limit': clock_limit,
            'clock.increment': clock_increment,
            'days': days,
            'color': color,
            'variant': variant,
            'fen': position,
        }
        return self._r.post(path, json=payload,
                            converter=models.Tournament.convert)

    def create_open(self, clock_limit=None, clock_increment=None,
                    variant=None, position=None):
        """Create a challenge that any two players can join.

        :param int clock_limit: clock initial time (in seconds)
        :param int clock_increment: clock increment (in seconds)
        :param variant: game variant to use
        :type variant: :class:`~berserk.enums.Variant`
        :param position: custom intial position in FEN (variant must be
                         standard and the game cannot be rated)
        :type position: str
        :return: challenge data
        :rtype: dict
        """
        path = 'api/challenge/open'
        payload = {
            'clock.limit': clock_limit,
            'clock.increment': clock_increment,
            'variant': variant,
            'fen': position,
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

    def cancel(self, challenge_id, opponent_token=None):
        """Cancel a challenge you sent, or aborts the game if the
        challenge was accepted, but the game was not yet played.

        :param str challenge_id: id of the challenge to cancel
        :param str opponent_token: optional ``challenge:write`` token of the
            opponent. If set, the game can be canceled even if both players
            have moved
        :return: success indicator
        :rtype: bool
        """
        path = f'api/challenge/{challenge_id}/cancel'
        params = {'opponentToken': opponent_token}
        return self._r.post(path, params=params)['ok']


class Board(BaseClient):
    """Client for physical board or external application endpoints."""

    def stream_incoming_events(self):
        """Get your realtime stream of incoming events.

        :return: stream of incoming events
        :rtype: iterator over the stream of events
        """
        path = 'api/stream/event'
        yield from self._r.get(path, stream=True)

    def seek(self, time, increment, rated=False, variant='standard',
             color='random', rating_range=None):
        """Create a public seek to start a game with a random opponent.

        :param int time: intial clock time in minutes
        :param int increment: clock increment in minutes
        :param bool rated: whether the game is rated (impacts ratings)
        :param str variant: game variant to use
        :param str color: color to play
        :param rating_range: range of opponent ratings
        :return: duration of the seek
        :rtype: float
        """
        if isinstance(rating_range, (list, tuple)):
            low, high = rating_range
            rating_range = f'{low}-{high}'

        path = '/api/board/seek'
        payload = {
            'rated': str(bool(rated)).lower(),
            'time': time,
            'increment': increment,
            'variant': variant,
            'color': color,
            'ratingRange': rating_range or '',
        }

        # we time the seek
        start = now()

        # just keep reading to keep the search going
        for line in self._r.post(path, data=payload, fmt=TEXT, stream=True):
            pass

        # and return the time elapsed
        return now() - start

    def stream_game_state(self, game_id):
        """Get the stream of events for a board game.

        :param str game_id: ID of a game
        :return: iterator over game states
        """
        path = f'api/board/game/stream/{game_id}'
        yield from self._r.get(path, stream=True,
                               converter=models.GameState.convert)

    def make_move(self, game_id, move):
        """Make a move in a board game.

        :param str game_id: ID of a game
        :param str move: move to make
        :return: success
        :rtype: bool
        """
        path = f'api/board/game/{game_id}/move/{move}'
        return self._r.post(path)['ok']

    def post_message(self, game_id, text, spectator=False):
        """Post a message in a board game.

        :param str game_id: ID of a game
        :param str text: text of the message
        :param bool spectator: post to spectator room (else player room)
        :return: success
        :rtype: bool
        """
        path = f'api/board/game/{game_id}/chat'
        room = 'spectator' if spectator else 'player'
        payload = {'room': room, 'text': text}
        return self._r.post(path, json=payload)['ok']

    def abort_game(self, game_id):
        """Abort a board game.

        :param str game_id: ID of a game
        :return: success
        :rtype: bool
        """
        path = f'api/board/game/{game_id}/abort'
        return self._r.post(path)['ok']

    def resign_game(self, game_id):
        """Resign a board game.

        :param str game_id: ID of a game
        :return: success
        :rtype: bool
        """
        path = f'api/board/game/{game_id}/resign'
        return self._r.post(path)['ok']

    def handle_draw_offer(self, game_id, accept):
        """Create, accept, or decline a draw offer.

        To offer a draw, pass ``accept=True`` and a game ID of an in-progress
        game. To response to a draw offer, pass either ``accept=True`` or
        ``accept=False`` and the ID of a game in which you have recieved a
        draw offer.

        Often, it's easier to call :func:`offer_draw`, :func:`accept_draw`, or
        :func:`decline_draw`.

        :param str game_id: ID of an in-progress game
        :param bool accept: whether to accept
        :return: True if successful
        :rtype: bool
        """
        accept = "yes" if accept else "no"
        path = f'/api/board/game/{game_id}/draw/{accept}'
        return self._r.post(path)['ok']

    def offer_draw(self, game_id):
        """Offer a draw in the given game.

        :param str game_id: ID of an in-progress game
        :return: True if successful
        :rtype: bool
        """
        return self.handle_draw_offer(game_id, True)

    def accept_draw(self, game_id):
        """Accept an already offered draw in the given game.

        :param str game_id: ID of an in-progress game
        :return: True if successful
        :rtype: bool
        """
        return self.handle_draw_offer(game_id, True)

    def decline_draw(self, game_id):
        """Decline an already offered draw in the given game.

        :param str game_id: ID of an in-progress game
        :return: True if successful
        :rtype: bool
        """
        return self.handle_draw_offer(game_id, False)


class Bots(BaseClient):
    """Client for bot-related endpoints."""

    def stream_incoming_events(self):
        """Get your realtime stream of incoming events.

        :return: stream of incoming events
        :rtype: iterator over the stream of events
        """
        path = 'api/stream/event'
        yield from self._r.get(path, stream=True)

    def get_online(self, nb):
        """Stream the online bot users, as ndjson.

        :param int nb: how many bot users to fetch
        :return: list of online bots
        :rtype: iter
        """
        path = 'api/bot/online'
        params = {'nb': nb}
        yield from self._r.get(path, stream=True,
                               converter=models.User.convert)

    def upgrade_to_bot(self):
        """Upgrade your account to a bot account.

        :return: success
        :rtype: bool
        """
        path = 'api/bot/account/upgrade'
        return self._r.post(path)['ok']

    def stream_game_state(self, game_id):
        """Get the stream of events for a bot game.

        :param str game_id: ID of a game
        :return: iterator over game states
        """
        path = f'api/bot/game/stream/{game_id}'
        yield from self._r.get(path, stream=True,
                               converter=models.GameState.convert)

    def make_move(self, game_id, move, offering_draw=False):
        """Make a move in a bot game.

        :param str game_id: ID of a game
        :param str move: move to make
        :return: success
        :rtype: bool
        """
        path = f'api/bot/game/{game_id}/move/{move}'
        params = {'offeringDraw': offering_draw}
        return self._r.post(path, params=params)['ok']

    def post_message(self, game_id, text, spectator=False):
        """Post a message in a bot game.

        :param str game_id: ID of a game
        :param str text: text of the message
        :param bool spectator: post to spectator room (else player room)
        :return: success
        :rtype: bool
        """
        path = f'api/bot/game/{game_id}/chat'
        room = 'spectator' if spectator else 'player'
        payload = {'room': room, 'text': text}
        return self._r.post(path, json=payload)['ok']

    def abort_game(self, game_id):
        """Abort a bot game.

        :param str game_id: ID of a game
        :return: success
        :rtype: bool
        """
        path = f'api/bot/game/{game_id}/abort'
        return self._r.post(path)['ok']

    def resign_game(self, game_id):
        """Resign a bot game.

        :param str game_id: ID of a game
        :return: success
        :rtype: bool
        """
        path = f'api/bot/game/{game_id}/resign'
        return self._r.post(path)['ok']

    @deprecated(version='1.0.0', reason='use Challenges.accept_challenge instead')
    def accept_challenge(self, challenge_id):
        """Accept an incoming challenge.

        :param str challenge_id: ID of a challenge
        :return: success
        :rtype: bool
        """
        path = f'api/challenge/{challenge_id}/accept'
        return self._r.post(path)['ok']

    @deprecated(version='1.0.0', reason='use Challenges.decline_challenge instead')
    def decline_challenge(self, challenge_id):
        """Decline an incoming challenge.

        :param str challenge_id: ID of a challenge
        :return: success
        :rtype: bool
        """
        path = f'api/challenge/{challenge_id}/decline'
        return self._r.post(path)['ok']


class Tournaments(FmtClient):
    """Client for tournament-related endpoints."""

    def get(self):
        """Get recently finished, ongoing, and upcoming tournaments.

        :return: current tournaments
        :rtype: list
        """
        path = 'api/tournament'
        return self._r.get(path, converter=models.Tournaments.convert_values)

    def create(self, clock_time, clock_increment, minutes, name=None,
               wait_minutes=None, variant=None, berserkable=None, rated=None,
               start_date=None, position=None, password=None, conditions=None):
        """Create a new tournament.

        .. note::

            ``wait_minutes`` is always relative to now and is overriden by
            ``start_time``.

        .. note::

            If ``name`` is left blank then one is automatically created.

        :param int clock_time: intial clock time in minutes
        :param int clock_increment: clock increment in seconds
        :param int minutes: length of the tournament in minutes
        :param str name: tournament name
        :param int wait_minutes: future start time in minutes
        :param str start_date: when to start the tournament
        :param str variant: variant to use if other than standard
        :param bool rated: whether the game affects player ratings
        :param str berserkable: whether players can use berserk
        :param str position: custom initial position in FEN
        :param str password: password (makes the tournament private)
        :param dict conditions: conditions for participation
        :return: created tournament info
        :rtype: dict
        """
        path = 'api/tournament'
        payload = {
            'name': name,
            'clockTime': clock_time,
            'clockIncrement': clock_increment,
            'minutes': minutes,
            'waitMinutes': wait_minutes,
            'startDate': start_date,
            'variant': variant,
            'rated': rated,
            'position': position,
            'berserkable': berserkable,
            'password': password,
            **{f'conditions.{c}': v for c, v in (conditions or {}).items()},
        }
        return self._r.post(path, json=payload,
                            converter=models.Tournament.convert)

    def export_games(self, id_, as_pgn=False, moves=None, tags=None,
                     clocks=None, evals=None, opening=None):
        """Export games from a tournament.

        :param str id_: tournament ID
        :param bool as_pgn: whether to return PGN instead of JSON
        :param bool moves: include moves
        :param bool tags: include tags
        :param bool clocks: include clock comments in the PGN moves, when
                            available
        :param bool evals: include analysis evalulation comments in the PGN
                           moves, when available
        :param bool opening: include the opening name
        :return: games
        :rtype: list
        """
        path = f'api/tournament/{id_}/games'
        params = {
            'moves': moves,
            'tags': tags,
            'clocks': clocks,
            'evals': evals,
            'opening': opening,
        }
        fmt = PGN if self._use_pgn(as_pgn) else NDJSON
        return self._r.get(path, params=params, fmt=fmt,
                           converter=models.Game.convert)

    def stream_results(self, id_, limit=None):
        """Stream the results of a tournament.

        Results are the players of a tournament with their scores and
        performance in rank order. Note that results for ongoing
        tournaments can be inconsistent due to ranking changes.

        :param str id_: tournament ID
        :param int limit: maximum number of results to stream
        :return: iterator over the stream of results
        :rtype: iter
        """
        path = f'api/tournament/{id_}/results'
        params = {'nb': limit}
        return self._r.get(path, params=params, stream=True)

    def stream_by_creator(self, username):
        """Stream the tournaments created by a player.

        :param str username: username of the player
        :return: tournaments
        :rtype: iter
        """
        path = f'api/user/{username}/tournament/created'
        return self._r.get(path, stream=True)


class Broadcasts(BaseClient):
    """Broadcast of one or more games."""

    def create(self, name, description, sync_url=None, markdown=None,
               credit=None, starts_at=None, official=None, throttle=None):
        """Create a new broadcast.

        .. note::

            ``sync_url`` must be publicly accessible. If not provided, you
            must periodically push new PGN to update the broadcast manually.

        :param str name: name of the broadcast
        :param str description: short description
        :param str markdown: long description
        :param str sync_url: URL by which Lichess can poll for updates
        :param str credit: short text to give credit to the source provider
        :param int starts_at: start time as millis
        :param bool official: DO NOT USE
        :param int throttle: DO NOT USE
        :return: created tournament info
        :rtype: dict
        """
        path = 'broadcast/new'
        payload = {
            'name': name,
            'description': description,
            'syncUrl': sync_url,
            'markdown': markdown,
            'credit': credit,
            'startsAt': starts_at,
            'official': official,
            'throttle': throttle,
        }
        return self._r.post(path, json=payload,
                            converter=models.Broadcast.convert)

    def get(self, broadcast_id, slug='-'):
        """Get a broadcast by ID.

        :param str broadcast_id: ID of a broadcast
        :param str slug: slug for SEO
        :return: broadcast information
        :rtype: dict
        """
        path = f'broadcast/{slug}/{broadcast_id}'
        return self._r.get(path, converter=models.Broadcast.convert)

    def update(self, broadcast_id, name, description, sync_url, markdown=None,
               credit=None, starts_at=None, official=None, throttle=None,
               slug='-'):
        """Update an existing broadcast by ID.

        .. note::

            Provide all fields. Values in missing fields will be erased.

        :param str broadcast_id: ID of a broadcast
        :param str name: name of the broadcast
        :param str description: short description
        :param str sync_url: URL by which Lichess can poll for updates
        :param str markdown: long description
        :param str credit: short text to give credit to the source provider
        :param int starts_at: start time as millis
        :param bool official: DO NOT USE
        :param int throttle: DO NOT USE
        :param str slug: slug for SEO
        :return: updated broadcast information
        :rtype: dict
        """
        path = f'broadcast/{slug}/{broadcast_id}'
        payload = {
            'name': name,
            'description': description,
            'syncUrl': sync_url,
            'markdown': markdown,
            'credit': credit,
            'startsAt': starts_at,
            'official': official,

        }
        return self._r.post(path, json=payload,
                            converter=models.Broadcast.convert)

    def push_pgn_update(self, broadcast_id, pgn_games, slug='-'):
        """Manually update an existing broadcast by ID.

        :param str broadcast_id: ID of a broadcast
        :param list pgn_games: one or more games in PGN format
        :return: success
        :rtype: bool
        """
        path = f'broadcast/{slug}/{broadcast_id}/push'
        games = '\n\n'.join(g.strip() for g in pgn_games)
        return self._r.post(path, data=games)['ok']


class Simuls(BaseClient):
    """Simultaneous exhibitions - one vs many."""

    def get(self):
        """Get recently finished, ongoing, and upcoming simuls.

        :return: current simuls
        :rtype: list
        """
        path = 'api/simul'
        return self._r.get(path)


class Studies(BaseClient):
    """Study chess the Lichess way."""

    def export_chapter(self, study_id, chapter_id):
        """Export one chapter of a study.

        :return: chapter
        :rtype: PGN
        """
        path = f'/study/{study_id}/{chapter_id}.pgn'
        return self._r.get(path, fmt=PGN)

    def export(self, study_id):
        """Export all chapters of a study.

        :return: all chapters as PGN
        :rtype: list
        """
        path = f'/study/{study_id}.pgn'
        return self._r.get(path, fmt=PGN, stream=True)


class TV(FmtClient):
    """Chess TV of Lichess."""

    def get_tv_channels(self):
        """Get basic information about the best games being played.

        :return: best ongoing games in each speed and variant
        :rtype: dict
        """
        path = 'api/tv/channels'
        return self._r.get(path)

    def stream_current(self):
        """Stream current TV game.

        :return: dict of positions and moves of the current TV game
        :rtype: dict
        """
        path = 'api/tv/feed'
        return self._r.get(path, fmt=NDJSON, stream=True)

    def get_best_ongoing(self, channel, nb=10, moves=True,
                         pgn_in_json=False, tags=True,
                         clocks=False, opening=False):
        """Get a list of ongoing games for a given TV channel.

        :param bool moves: whether to include the PGN moves
        :param int nb: number of games to fetch
        :param bool pgn_in_json: whether to include the full PGN within the
            JSON response, in a ``pgn`` field
        :param bool tags: whether to include the PGN tags
        :param bool clocks: whether to include clock comments in the PGN moves,
            when available
        :param bool opening: whether to include the opening name
        :return: exported game, as JSON or PGN
        :rtype: str or dict
        """
        path = f'api/tv/{channel}'
        params = {
            'moves': moves,
            'pgnInJson': pgn_in_json,
            'tags': tags,
            'clocks': clocks,
            'opening': opening,
        }
        fmt = PGN if self._use_pgn(not pgn_in_json) else NDJSON
        return self._r.get(path, params=params, fmt=fmt,
                           converter=models.Game.convert)


class Puzzles(BaseClient):
    """Chess puzzles."""

    def get_daily(self):
        """Get the daily Lichess puzzle.

        :return: daily puzzle
        :rtype: dict
        """
        path = 'api/puzzle/daily'
        return self._r.get(path, fmt=JSON)

    def get_activity(self, max_entries=None):
        """Get your puzzle activity.

        :param int max_entries: how many entries to download
        :return: your puzzle activity
        :rtype: dict
        """
        path = 'api/puzzle/activity'
        params = {'max': max_entries}
        return self._r.get(path, params=params, fmt=NDJSON)

    def get_dashboard(self, days=30):
        """Get your puzzle dashboard.

        :param int days: how many days to look back when aggregating puzzle results
        :return: your puzzle dashboard
        :rtype: dict
        """
        path = f'api/puzzle/dashboard/{days}'
        return self._r.get(path, fmt=JSON)

    def get_storm_dashboard(self, username, days=30):
        """Get storm dashboard of player.

        :param str username: a username
        :param int days: how many days of history to return
        :return: a player storm dashboard
        :rtype: dict
        """
        path = f'api/storm/dashboard/{username}'
        params = {'days': days}
        return self._r.get(path, params=params, fmt=JSON)


class OpeningExplorer(BaseClient):
    """Chess openings explorer."""

    def masters(self, fen=None, play=None, since=1952, until=None, moves=12,
                top_games=15):
        """Get from masters database.

        :param str fen: FEN of the root position
        :param str play: comma separated sequence of legal moves in UCI notation,
            play additional moves starting from ``fen``
        :param int since: include only games from this year or later
        :param int until: include only games from this year or earlier
        :param int moves: number of most common moves to display
        :param int top_games: number of top games to display
        :return: masters database search results
        :rtype: dict
        """
        path = 'masters'
        params = {
            'fen': fen,
            'play': play,
            'since': since,
            'until': until,
            'moves': moves,
            'topGames': top_games,
        }
        return self._r.get(path, params=params)

    def lichess(self, variant='standard', fen=None, play=None, speeds=None,
                ratings=None, since='0000-01', until=None, moves=12,
                top_games=15, recent_games=4):
        """Get from masters database.

        :param str variant: variant
        :param str fen: FEN of the root position
        :param str play: comma separated sequence of legal moves in UCI notation,
            play additional moves starting from ``fen``
        :param str speeds: comma separated list of game speeds to look for
        :param str ratings: comma separated list of rating groups,
            ranging from their value to the next higher group
            (1600, 1800, 2000, 2200, 2500)
        :param int since: include only games from this month or later
        :param int until: include only games from this month or earlier
        :param int moves: number of most common moves to display
        :param int top_games: number of top games to display
        :param int recent_games: number of recent games to display
        :return: lichess database search results
        :rtype: dict
        """
        path = 'lichess'
        params = {
            'variant': variant,
            'fen': fen,
            'play': play,
            'speeds': speeds,
            'ratings': ratings,
            'since': since,
            'until': until,
            'moves': moves,
            'topGames': top_games,
            'recentGames': recent_games,
        }
        return self._r.get(path, params=params)

    def player(self, player, color, variant='standard', fen=None, play=None,
               speeds=None, modes=None, since='0000-01', until=None, moves=12,
               recent_games=4):
        """Get from masters database.

        :param str player: a username
        :param str color: white or black
        :param str variant: variant
        :param str fen: FEN of the root position
        :param str play: comma separated sequence of legal moves in UCI notation,
            play additional moves starting from ``fen``
        :param str speeds: comma separated list of game speeds to look for
        :param str modes: casual or rated
        :param int since: include only games from this month or later
        :param int until: include only games from this month or earlier
        :param int moves: number of most common moves to display
        :param int recent_games: number of recent games to display
        :return: player database search results
        :rtype: dict
        """
        path = 'player'
        params = {
            'player': player,
            'color': color,
            'variant': variant,
            'fen': fen,
            'play': play,
            'speeds': speeds,
            'modes': modes,
            'since': since,
            'until': until,
            'moves': moves,
            'recentGames': recent_games,
        }
        return self._r.get(path, params=params, fmt=NDJSON)

