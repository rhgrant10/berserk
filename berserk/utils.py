# -*- coding: utf-8 -*-
from datetime import datetime
from datetime import timezone


def to_millis(dt):
    return dt.timestamp() * 1000


def datetime_from_seconds(ts):
    return datetime.fromtimestamp(ts, timezone.utc)


def datetime_from_millis(millis):
    return datetime_from_seconds(millis / 1000)


def inner_datetime_fromtimestamp(*keys):
    def convert(data):
        for k in keys:
            data[k] = datetime_from_seconds(data[k])
        return data
    return convert


def datetime_from_str(dt_str):
    dt = datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    return dt.replace(tzinfo=timezone.utc)


def noop(arg):
    return arg
