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

def get_task_status():
    """
    Return a list of dict with all the task statuses provided by the gazu API
    """
    return gazu.task.all_task_statuses()

def get_task_status_names():
    """
    Return a dict with the short names of the tasks as keys, and the full names as values
    """
    all_tasks = get_task_status()
    task_name = {}
    for task_dict in all_tasks:
        task_name[task_dict["name"]] = task_dict["short_name"]
    return task_name

def qtazu_login():
    """
    Display qtazu login window and check for credentials
    """
    widget = Login()
    return widget.exec()

