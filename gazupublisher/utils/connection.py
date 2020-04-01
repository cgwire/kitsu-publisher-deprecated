"""
Module containing utility functions regarding connecti
"""

import gazu
import requests.exceptions
import urllib.request


def connect_user(user, password):
    """
    Log in kitsu.
    """
    gazu.log_in(user, password)


def configure_host(host):
    """
    Connexion to the gazu API.
    """
    gazu.client.set_host(host)


def is_logged_in():
    """
    Return whether you are currently logged in with Gazu.
    """

    try:
        user = gazu.client.get_current_user()
        if user:
            return True
    except (
        gazu.exception.NotAuthenticatedException,
        requests.exceptions.ConnectionError,
    ):
        # If we are not authenticated assume we are not
        # logged in and allow it to pass.
        pass

    return False


def get_host():
    """
    Return the host for the current session.
    """
    return gazu.client.get_host()


def get_auth_header():
    """
    Return the authentication header.
    """
    return gazu.client.make_auth_header()


def get_data_from_url(url):
    """
    Return data found at url
    """
    try:
        req = urllib.request.Request(url, None, get_auth_header())
        data = urllib.request.urlopen(req).read()
    except:
        pass
    return data
