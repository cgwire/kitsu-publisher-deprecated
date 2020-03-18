"""
Module containing utility functions
"""

import gazu
import qtazu
import requests.exceptions

# from qtazu.qtazu.widgets.login import Login



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

def get_task_status():
    """
    Return a list of dict with all the task statuses provided by the gazu API
    """
    return gazu.task.all_task_statuses()

def get_all_tasks_to_do():
    """

    """
    return gazu.user.all_tasks_to_do()

def get_all_projects():
    """
    Return a list with all the projects (open and closed)
    """
    return gazu.project.all_projects()

def get_all_project_names():
    """
    Return a list with the names of all the projects (open and closed)
    """
    project_dicts = gazu.project.all_projects()
    return [project_dict["name"] for project_dict in project_dicts]

def get_all_open_projects():
    """
    Return a list with all the open projects
    """
    return gazu.project.all_open_projects()

def get_all_open_project_names():
    """
    Return a list with the names of all the open projects
    """
    project_dicts = gazu.project.all_open_projects()
    return [project_dict["name"] for project_dict in project_dicts]


def get_task_status_names():
    """
    Return a dict with the short names of the tasks as keys, and the full names as values
    """
    all_tasks = get_task_status()
    task_name = {}
    for task_dict in all_tasks:
        task_name[task_dict["name"]] = task_dict["short_name"]
    return task_name

def delete_project_from_name(name):
    """
    Delete a project from its name
    """
    project = gazu.project.get_project_by_name(name)
    gazu.project.close_project(project)
    gazu.project.remove_project(project, force=True)

def qtazu_login():
    """
    Display qtazu login window and check for credentials
    """
    widget = qtazu.qtazu.widgets.login.Login()
    return widget.exec()

