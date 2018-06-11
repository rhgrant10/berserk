# -*- coding: utf-8 -*-


__all__ = ['PerfType', 'Variant', 'Color', 'Room', 'Mode']


class GameType:
    ANTICHESS = 'antichess'
    ATOMIC = 'atomic'
    CHESS960 = 'chess960'
    CRAZYHOUSE = 'crazyhouse'
    HORDE = 'horde'
    KING_OF_THE_HILL = 'kingOfTheHill'
    RACING_KINGS = 'racingKings'
    THREE_CHECK = 'threeCheck'


class PerfType(GameType):
    BULLET = 'bullet'
    BLITZ = 'blitz'
    RAPID = 'rapid'
    CLASSICAL = 'classical'
    ULTRA_BULLET = 'ultraBullet'


class Variant(GameType):
    STANDARD = 'standard'


class Color:
    WHITE = 'white'
    BLACK = 'black'


class Room:
    PLAYER = 'player'
    SPECTATOR = 'spectator'


class Mode:
    CASUAL = 'casual'
    RATED = 'rated'
