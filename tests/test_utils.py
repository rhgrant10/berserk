# -*- coding: utf-8 -*-
import datetime

from berserk import utils


def test_datetime_from_millis():
    dt = utils.datetime_from_millis(1514505150384)
    assert dt.timestamp() == 1514505150.384


def test_inner_datetime_fromtimestamp():
    converter = utils.inner_datetime_fromtimestamp('foo')
    result = converter({'foo': 1514505150, 'bar': 'baz', 'qux': 123})
    assert result == {
        'foo': datetime.datetime(2017, 12, 28, 23, 52, 30,
                                 tzinfo=datetime.timezone.utc),
        'bar': 'baz',
        'qux': 123,
    }


def test_noop():
    assert 'foo' == utils.noop('foo')
