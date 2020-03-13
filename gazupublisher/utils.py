"""
Module containing utility functions
"""

import gazu
from qtazu.qtazu.widgets.login import Login

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


def qtazu_login():
    """
    Display qatzu login window and check for credentials
    """
    widget = Login()
    return widget.exec()

