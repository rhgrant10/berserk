=======
History
=======

0.8.0 (2020-03-08)
==================

* Add new ``Board`` client: stream_incoming_events, stream_game_state, make_move, post_message, abort_game, and resign_game

0.7.0 (2020-01-26)
==================

* Add simuls
* Add studies export and export chapter
* Add tournament results, games export, and list by creator
* Add user followers, users following, rating history, and puzzle activity
* Add new ``Teams`` client: join, get members, kick member, and leave
* Updated documentation, including new docs for some useful utils
* Fixed bugs in ``Tournaments.export_games``
* Deprecated ``Users.get_by_team`` - use ``Teams.get_members`` instead


0.6.1 (2020-01-20)
==================

* Add py37 to the travis build
* Update development status classifier to 4 - Beta
* Fix py36 issue preventing successful build
* Make updates to the Makefile


0.6.0 (2020-01-20)
==================

* Add logging to the ``berserk.session`` module
* Fix exception message when no cause
* Fix bug in ``Broadcasts.push_pgn_update``
* Update documentation and tweak the theme


0.5.0 (2020-01-20)
==================

* Add ``ResponseError`` for 4xx and 5xx responses with status code, reason, and cause
* Add ``ApiError`` for all other request errors
* Fix test case broken by 0.4.0 release
* Put all utils code under test


0.4.0 (2020-01-19)
==================

* Add support for the broadcast endpoints
* Add a utility for easily converting API objects into update params
* Fix multiple bugs with the tournament create endpoint
* Improve the reusability of some conversion utilities
* Improve many docstrings in the client classes


0.3.2 (2020-01-04)
==================

* Fix bug where options not passed for challenge creation
* Convert requirements from pinned to sematically compatible
* Bump all developer dependencies
* Use pytest instead of the older py.test
* Use py37 in tox


0.3.1 (2018-12-23)
==================

* Convert datetime string in tournament creation response into datetime object


0.3.0 (2018-12-23)
==================

* Convert all timestamps to datetime in all responses
* Provide support for challenging other players to a game


0.2.1 (2018-12-08)
==================

* Bump requests dependency to >=2.20.0 (CVE-2018-18074)


0.2.0 (2018-12-08)
==================

* Add `position` and `start_date` params to `Tournament.create`
* Add `Position` enum


0.1.2 (2018-07-14)
==================

* Fix an asine bug in the docs


0.1.1 (2018-07-14)
==================

* Added tests for session and formats modules
* Fixed mispelled PgnHandler class (!)
* Fixed issue with trailing whitespace when splitting multiple PGN texts
* Fixed the usage overview in the README
* Fixed the versions for travis-ci
* Made it easier to test the `JsonHandler` class
* Salted the bumpversion config to taste


0.1.0 (2018-07-10)
==================

* First release on PyPI.
