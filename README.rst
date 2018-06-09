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

* both oauth and token authentication supported
* token auth support provided
* all endpoints implemented

Usage
-----

.. code-block::python

    import berserk

    session = berserk.TokenSession('personal-api-token')
    client = berserk.Client(session)

    all_top10 = client.get_all_top10()

.. note::

    Any ``requests.Session``-like object can be used for a session, including one from ``requests_oauth``. A simple token session is included, as shown above.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
