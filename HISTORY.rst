=======
History
=======

0.3.2 (2020-01-04)
------------------

* Fix bug where options not passed for challenge creation
* Convert requirements from pinned to sematically compatible
* Bump all developer dependencies
* Use pytest instead of the older py.test
* Use py37 in tox

0.3.1 (2018-12-23)
------------------

* Convert datetime string in tournament creation response into datetime object

0.3.0 (2018-12-23)
------------------

* Convert all timestamps to datetime in all responses
* Provide support for challenging other players to a game

0.2.1 (2018-12-08)
------------------

* Bump requests dependency to >=2.20.0 (CVE-2018-18074)


0.2.0 (2018-12-08)
------------------

* Add `position` and `start_date` params to `Tournament.create`
* Add `Position` enum


0.1.2 (2018-07-14)
------------------

* Fix an asine bug in the docs


0.1.1 (2018-07-14)
------------------

* Added tests for session and formats modules
* Fixed mispelled PgnHandler class (!)
* Fixed issue with trailing whitespace when splitting multiple PGN texts
* Fixed the usage overview in the README
* Fixed the versions for travis-ci
* Made it easier to test the `JsonHandler` class
* Salted the bumpversion config to taste


0.1.0 (2018-07-10)
------------------

* First release on PyPI.
