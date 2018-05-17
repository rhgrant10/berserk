import os

import pytest
import berserk


@pytest.fixture
def session():
    token = os.environ.get("LICHESS_TOKEN")
    assert token
    return berserk.TokenClient(token=token)


@pytest.fixture
def username():
    return 'rpgraham84'


@pytest.fixture
def usernames():
    return ['rpgraham84', 'rpgraham84bot']


@pytest.fixture
def team_id():
    return 'coders'


@pytest.fixture
def game_type():
    return 'classical'


@pytest.fixture
def game_id():
    return 'Ig2XxulZ'
