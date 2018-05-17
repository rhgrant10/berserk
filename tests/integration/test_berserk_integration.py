#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `berserk` package."""


def test_get_player(session):
    """Sample pytest test function with the pytest fixture as an argument."""
    player = session.get_player()
    assert player
