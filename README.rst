=======
berserk
=======


.. image:: https://img.shields.io/pypi/v/berserk.svg
        :target: https://pypi.python.org/pypi/berserk

.. image:: https://img.shields.io/travis/rhgrant10/berserk.svg
        :target: https://travis-ci.org/rhgrant10/berserk

.. image:: https://readthedocs.org/projects/berserk/badge/?version=latest
        :target: https://berserk.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Python client for the lichess API


* Free software: GNU General Public License v3
* Documentation: https://berserk.readthedocs.io.


Features
--------

* handles JSON and PGN formats at user's discretion
* *all* endpoints implemented
* token auth support provided
* easy integration with oauth2

Usage
-----

You can use any ``requests.Session``-like object as a session, including those
from ``requests_oauth``. A simple token session is included, as shown below:

.. code-block:: python

    import berserk

    lichess.account.get()
    lichess.account.get_email()
    lichess.account.get_preferences()
    lichess.account.get_kid_mode()
    lichess.account.set_kid_mode()
    lichess.account.upgrade_to_bot()

    lichess.users.get_realtime_statuses()
    lichess.users.get_all_top_10()
    lichess.users.get_leaderboard()
    lichess.users.get_public_data()
    lichess.users.get_activity_feed()
    lichess.users.get_by_id()
    lichess.users.get_by_team()
    lichess.users.get_live_streamers()

    lichess.games.export()
    lichess.games.export_by_player()
    lichess.games.export_multi()
    lichess.games.get_among_players()
    lichess.games.get_ongoing()
    lichess.games.get_tv_channels()

    lichess.challenges.create()
    lichess.challenges.accept()
    lichess.challenges.decline()

    lichess.bots.stream_incoming_events()
    lichess.bots.stream_game_state()
    lichess.bots.make_move()
    lichess.bots.post_message()
    lichess.bots.abort_game()
    lichess.bots.resign_game()
    lichess.bots.accept_challenge()
    lichess.bots.decline_challenge()

    lichess.tournaments.get()
    lichess.tournaments.create()


Details for each function can be found in the full documentation.


Credits
-------

This package was created with Cookiecutter_ and the
`audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
