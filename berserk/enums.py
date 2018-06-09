# -*- coding: utf-8 -*-


class _GameVariation:
    ANTICHESS = 'antichess'
    ATOMIC = 'atomic'
    CHESS960 = 'chess960'
    CRAZYHOUSE = 'crazyhouse'
    HORDE = 'horde'
    KINGOFTHEHILL = 'kingOfTheHill'
    RACINGKINGS = 'racingKings'
    THREECHECK = 'threeCheck'


class PerfType(_GameVariation):
    BULLET = 'bullet'
    BLITZ = 'blitz'
    RAPID = 'rapid'
    CLASSICAL = 'classical'
    ULTRABULLET = 'ultraBullet'


class Variant(_GameVariation):
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
