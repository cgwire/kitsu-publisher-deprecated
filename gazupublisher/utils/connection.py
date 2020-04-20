"""
Module containing utility functions regarding connecti
"""

import webbrowser
import gazu


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


def get_file_data_from_url(url, full=False):
    """
    Return file data found at given url
    """
    return gazu.client.get_file_data_from_url(url, full)


def open_browser():
    """
    Open the to-do list in the web browser.
    """
    webbrowser.open(get_host()[:-4] + "/todos", new=1)
