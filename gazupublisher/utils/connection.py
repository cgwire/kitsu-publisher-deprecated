"""
Module containing utility functions regarding connecti
"""

import gazu
import qtazu
import requests.exceptions


def connect_user(user, password):
    """
    Log in kitsu
    """
    gazu.log_in(user, password)

def configure_host(host):
    """
    Connexion to the gazu API
    """
    gazu.client.set_host(host)

def is_logged_in():
    """Return whether you are currently logged in with Gazu"""

    try:
        user = gazu.client.get_current_user()
        if user:
            return True
    except (gazu.exception.NotAuthenticatedException,
            requests.exceptions.ConnectionError):
        # If we are not authenticated assume we are not
        # logged in and allow it to pass.
        pass

    return False

def qtazu_login():
    """
    Display qtazu login window and check for credentials
    """
    widget = qtazu.qtazu.widgets.login.Login()
    return widget.exec()

