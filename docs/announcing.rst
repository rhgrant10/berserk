Hi everyone,

I'm pleased to announce the release of berserk v0.7.0!

What's New?
-----------

It's been a while since the last slew of commits and lots has happened since v0.3.2:

**Features**

* Add ``ApiError`` for all other request errors
* Add ``ResponseError`` for 4xx and 5xx responses with status code, reason, and cause
* Add a utility for easily converting API objects into update params
* Add logging to the ``berserk.session`` module
* Add new ``Teams`` client: join, get members, kick member, and leave
* Add simuls
* Add studies export and export chapter
* Add support for the broadcast endpoints
* Add tests for all utils
* Add tournament results, games export, and list by creator
* Add user followers, users following, rating history, and puzzle activity

**Deprecations**

* Deprecated ``Users.get_by_team`` - use ``Teams.get_members`` instead

**Bugfixes**

* Fix bug in ``Broadcasts.push_pgn_update``
* Fix exception message when no cause
* Fix multiple bugs with the tournament create endpoint
* Fix py36 issue preventing successful build
* Fix test case broken by 0.4.0 release
* Fix multiple bugs in ``Tournaments.export_games``

**Misc**

* Update development status classifier to 4 - Beta
* Update documentation and tweak the theme
* Update the travis build to include py37
* Update the Makefile


What is berserk?
----------------

berserk is the Python client for the Lichess API. It supports JSON and PGN,
provides pluggable session auth, and implements most if not all of the API.

License: GNU General Public License v3

* Read the **docs**: https://berserk.readthedocs.io/
* Install from **PyPI**: https://pypi.org/project/berserk/
* Contribute **source**: https://github.com/rhgrant10/berserk


Example
-------

.. code-block:: python

    >>> import berserk

    >>> session = berserk.TokenSession('my-api-token')
    >>> client = berserk.Client(session)

    >>> my = client.account.get()
    >>> games = list(client.games.export_by_player(my['username'], as_pgn=True))
    >>> len(games)
    18


Enjoy!

-- Rob
