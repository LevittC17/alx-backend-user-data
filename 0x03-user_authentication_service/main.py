#!/usr/bin/env python3

"""
main module
"""

import requests


BASE_URL = 'http://localhost:5000'
EMAIL = 'guillaume@holberton.io'
PASSWD = 'b4l0u'
NEW_PASSWD = 't4rt1fl3tt3'


def register_user(email, password):
    response = requests.post(
        f'{BASE_URL}/users',
        data={
            'email': email,
            'password': password})
    assert response.status_code == 200, f'Registration failed: \
                                         {response.text}'


def log_in_wrong_password(email, password):
    response = requests.post(
        f'{BASE_URL}/sessions',
        data={
            'email': email,
            'password': password})
    assert response.status_code == 401, f'Login should fail with \
                                         wrong password: {response.text}'


def profile_unlogged():
    response = requests.get(f'{BASE_URL}/profile')
    assert response.status_code == 403, f'Profile should be inaccessibe \
                                         without login: {response.text}'


def log_in(email, password):
    response = requests.post(
        f'{BASE_URL}/sessions',
        data={
            'email': email,
            'password': password})
    assert response.status_code == 200, f'Login failed: {response.text}'
    return response.cookies.get('session_id')


def profile_logged(session_id):
    response = requests.get(
        f'{BASE_URL}/profile',
        cookies={
            'session_id': session_id})
    assert response.status_code == 200, f'Profile retrieval failed: \
                                         {response.text}'


def log_out(session_id):
    response = requests.delete(
        f'{BASE_URL}/sessions',
        cookies={
            'session_id': session_id})
    try:
        assert response.status_code == 200, f'Logout failed: {response.text}'
    except AssertionError as e:
        print(e)
        print(response.text)


def reset_password_token(email):
    response = requests.post(f'{BASE_URL}/reset_password',
                             data={'email': email})
    assert response.status_code == 200, f'Password reset token retrieval \
                                         failed: {response.text}'
    return response.json()['reset_token']


def update_password(email, reset_token, new_password):
    response = requests.put(
        f'{BASE_URL}/reset_password',
        data={'email': email, 'reset_token': reset_token,
              'new_password': new_password},
    )
    assert response.status_code == 200, f'Password update failed: \
                                         {response.text}'


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
