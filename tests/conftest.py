import os

import pytest
import berserk


@pytest.fixture
def session():
    token = os.environ.get("LICHESS_TOKEN")
    assert token
    return berserk.TokenClient(token=token)
