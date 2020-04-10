"""
Module containing utility functions regarding connecti
"""

import gazu
import urllib


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
        data = urllib.request.urlopen(req)
        return data
    except urllib.error.HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error message : ', e.reason)
        print('Error code: ', e.code)
        raise

