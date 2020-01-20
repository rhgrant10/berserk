# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timezone


def to_millis(dt):
    return dt.timestamp() * 1000


def datetime_from_seconds(ts):
    return datetime.fromtimestamp(ts, timezone.utc)


def datetime_from_millis(millis):
    return datetime_from_seconds(millis / 1000)


def inner(func, *keys):
    def convert(data):
        for k in keys:
            try:
                data[k] = func(data[k])
            except KeyError:
                pass  # normal for keys to not be present sometimes
        return data
    return convert


def datetime_from_str(dt_str):
    dt = datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    return dt.replace(tzinfo=timezone.utc)


def noop(arg):
    return arg


def build_adapter(mapper, sep='.'):
    """Build a data adapter.

    Uses a map to pull values from an object and assign them to keys.
    For example:

    .. code-block:: python

        >>> mapping = {
        ...   'broadcast_id': 'broadcast.id',
        ...   'slug': 'broadcast.slug',
        ...   'name': 'broadcast.name',
        ...   'description': 'broadcast.description',
        ...   'syncUrl': 'broadcast.sync.url',
        ... }

        >>> cast = {'broadcast': {'id': 'WxOb8OUT',
        ...   'slug': 'test-tourney',
        ...   'name': 'Test Tourney',
        ...   'description': 'Just a test',
        ...   'ownerId': 'rhgrant10',
        ...   'sync': {'ongoing': False, 'log': [], 'url': None}},
        ...  'url': 'https://lichess.org/broadcast/test-tourney/WxOb8OUT'}

        >>> adapt = build_adapter(mapping)
        >>> adapt(cast)
        {'broadcast_id': 'WxOb8OUT',
        'slug': 'test-tourney',
        'name': 'Test Tourney',
        'description': 'Just a test',
        'syncUrl': None}

    :param dict mapper: map of keys to their location in an object
    :param str sep: nested key delimiter
    :return: adapted data
    :rtype: dict
    """
    def get(data, location):
        for key in location.split(sep):
            data = data[key]
        return data

    def adapter(data, default=None, fill=False):
        result = {}
        for key, loc in mapper.items():
            try:
                result[key] = get(data, loc)
            except KeyError:
                if fill:
                    result[key] = default
        return result

    return adapter
