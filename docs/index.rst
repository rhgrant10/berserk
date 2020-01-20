Welcome to berserk's documentation!
======================================

.. image:: https://img.shields.io/pypi/v/berserk.svg
        :target: https://pypi.python.org/pypi/berserk

.. image:: https://img.shields.io/travis/rhgrant10/berserk.svg
        :target: https://travis-ci.org/rhgrant10/berserk

.. image:: https://readthedocs.org/projects/berserk/badge/?version=latest
        :target: https://berserk.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Python client for the Lichess API

* Free software: GNU General Public License v3
* Documentation: https://berserk.readthedocs.io.

----

**berserk** makes it easy to interact with the `Lichess API <https://lichess.org/api>`_:

.. code-block:: python

    >>> import berserk

    >>> session = berserk.TokenSession('my-api-token')
    >>> client = berserk.Client(session)

    >>> my = client.account.get()
    >>> games = list(client.games.export_by_player(my['username'], as_pgn=True))
    >>> len(games)
    18


.. toctree::
   :maxdepth: 4
   :hidden:

   installation
   usage
   api
   contributing
   authors
   history


Client Features
---------------

* session-based auth
* custom exceptions
* extensible design
* arbitrary requests
* ample logging
* PGN and JSON

API Features
------------

* account preferences
* bot account upgrade
* kid mode
* top 10 lists
* leaderboard
* activity feed
* realtime statuses
* live streams
* TV channels
* game exports
* users and teams
* challenges
* tournaments
* broadcasts
* bots

Indices and tables
==================
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
