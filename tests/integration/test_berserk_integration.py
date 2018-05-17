#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `berserk` package."""


def test_get_account(session):
    account = session.get_account()
    assert 'error' not in account


def test_get_account_email(session):
    email = session.get_account_email()
    assert 'error' not in email
    assert 'email' in email


def test_get_account_preferences(session):
    preferences = session.get_account_preferences()
    assert 'error' not in preferences
    assert 'prefs' in preferences


def test_get_account_kid(session):
    kid = session.get_account_kid()
    assert 'error' not in kid
    assert 'kid' in kid


def test_get_users_status(session, usernames):
    status = session.get_users_status(*usernames)
    assert len(status)
    assert 'id' in status[0]


def test_get_player(session):
    player = session.get_player()
    assert 'error' not in player
    assert player


def test_get_player_top(session, game_type):
    top_players = session.get_player_top(game_type)
    assert top_players
    assert 'error' not in top_players


def test_get_user(session, username):
    user = session.get_user(username)
    assert user


def test_get_user_activity(session, username):
    activity = session.get_user_activity(username)
    assert activity


def test_get_team_users(session, team_id):
    team_users = session.get_team_users(team_id)
    assert team_users


def test_get_tournament(session):
    tournament = session.get_tournament()
    assert tournament


def test_get_game_export(session, game_id):
    export = session.get_game_export(game_id)
    assert export

