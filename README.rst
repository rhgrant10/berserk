=======
berserk
=======


.. image:: https://img.shields.io/pypi/v/berserk.svg
        :target: https://pypi.python.org/pypi/berserk
        :alt: Available on PyPI

.. image:: https://img.shields.io/travis/rhgrant10/berserk.svg
        :target: https://travis-ci.org/rhgrant10/berserk
        :alt: Continuous Integration

.. image:: https://codecov.io/gh/rhgrant10/berserk/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/rhgrant10/berserk
        :alt: Code Coverage

.. image:: https://readthedocs.org/projects/berserk/badge/?version=latest
        :target: https://berserk.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Python client for the `Lichess API`_ (modified).

.. _Lichess API: https://lichess.org/api

* Free software: GNU General Public License v3
* Documentation: https://berserk.readthedocs.io.


Features
========

* handles JSON and PGN formats at user's discretion
* token auth session
* easy integration with OAuth2
* automatically converts time values to datetimes

Usage
=====

You can use any ``requests.Session``-like object as a session, including those
from ``requests_oauth``. A simple token session is included, as shown below:

.. code-block:: python

    import berserk

    session = berserk.TokenSession(API_TOKEN)
    client = berserk.Client(session=session)

Most if not all of the API is available:

.. code-block:: python

    client.account.get()
    client.account.get_email()
    client.account.get_preferences()
    client.account.get_kid_mode()
    client.account.set_kid_mode()
    client.account.upgrade_to_bot()

    client.users.get_puzzle_activity()
    client.users.get_realtime_statuses()
    client.users.get_all_top_10()
    client.users.get_leaderboard()
    client.users.get_public_data()
    client.users.get_activity_feed()
    client.users.get_by_id()
    client.users.get_by_team()
    client.users.get_live_streamers()
    client.users.get_users_followed()
    client.users.get_users_following()
    client.users.get_rating_history()

    client.teams.get_members()
    client.teams.join()
    client.teams.leave()
    client.teams.kick_member()

    client.games.export()
    client.games.export_by_player()
    client.games.export_multi()
    client.games.get_among_players()
    client.games.get_ongoing()
    client.games.get_tv_channels()

    client.challenges.create()
    client.challenges.create_ai()
    client.challenges.create_open()
    client.challenges.create_with_accept()
    client.challenges.accept()
    client.challenges.decline()

    client.board.stream_incoming_events()
    client.board.seek()
    client.board.stream_game_state()
    client.board.make_move()
    client.board.post_message()
    client.board.abort_game()
    client.board.resign_game()
    client.board.handle_draw_offer()
    client.board.offer_draw()
    client.board.accept_draw()
    client.board.decline_draw()

    client.bots.stream_incoming_events()
    client.bots.stream_game_state()
    client.bots.make_move()
    client.bots.post_message()
    client.bots.abort_game()
    client.bots.resign_game()
    client.bots.accept_challenge()
    client.bots.decline_challenge()

    client.tournaments.get()
    client.tournaments.create()
    client.tournaments.export_games()
    client.tournaments.stream_results()
    client.tournaments.stream_by_creator()

    client.broadcasts.create()
    client.broadcasts.get()
    client.broadcasts.update()
    client.broadcasts.push_pgn_update()

    client.simuls.get()

    client.studies.export_chapter()
    client.studies.export()


Details for each function can be found in the `full documentation <https://berserk.readthedocs.io>`_.


Credits
=======

This package was created with Cookiecutter_ and the
`audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
