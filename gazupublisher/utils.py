"""
Module containing utility functions
"""

import gazu


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

