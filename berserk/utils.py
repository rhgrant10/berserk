# -*- coding: utf-8 -*-
from datetime import datetime


def datetime_from_millis(millis):
    return datetime.fromtimestamp(millis / 1000)


def inner_datetime_fromtimestamp(*keys):
    def convert(data):
        for k in keys:
            data[k] = datetime.fromtimestamp(data[k])
        return data
    return convert


def noop(arg):
    return arg
