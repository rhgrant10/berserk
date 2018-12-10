# -*- coding: utf-8 -*-
from . import utils


class model(type):
    @property
    def conversions(cls):
        return {k: v for k, v in vars(cls).items() if not k.startswith('_')}


class Model(metaclass=model):
    @classmethod
    def convert(cls, data):
        if isinstance(data, (list, tuple)):
            return cls.convert_multiple(data)
        return cls.convert_one(data)

    @classmethod
    def convert_one(cls, data):
        for k in set(data) & set(cls.conversions):
            data[k] = cls.conversions[k](data[k])
        return data

    @classmethod
    def convert_multiple(cls, data):
        for datum in data:
            cls.convert_one(datum)
        return data


class Account(Model):
    createdAt = utils.datetime_from_millis
    seenAt = utils.datetime_from_millis


class User(Model):
    createdAt = utils.datetime_from_millis
    seenAt = utils.datetime_from_millis


class Activity(Model):
    interval = utils.inner_datetime_fromtimestamp('start', 'end')


class Game(Model):
    createdAt = utils.datetime_from_millis
    lastMoveAt = utils.datetime_from_millis


class GameState(Model):
    createdAt = utils.datetime_from_millis
    wtime = utils.datetime_from_millis
    btime = utils.datetime_from_millis
    winc = utils.datetime_from_millis
    binc = utils.datetime_from_millis
