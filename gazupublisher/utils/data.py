"""
Module containing utility functions regarding data retrieving
"""

import gazu

def get_task_status():
    """
    Return a list of dict with all the task statuses provided by the gazu API.
    """
    return gazu.task.all_task_statuses()


def get_task_status_names():
    """
    Return a dict with the short names of the tasks as keys, and the full names
    as values.
    """
    all_tasks = get_task_status()
    task_name = {}
    for task_dict in all_tasks:
        task_name[task_dict["name"]] = task_dict["short_name"]
    return task_name


def get_all_tasks_to_do():
    """
    Return a list with all the tasks the user has to do.
    """
    return gazu.user.all_tasks_to_do()


def get_all_projects():
    """
    Return a list with all the projects (open and closed).
    """
    return gazu.project.all_projects()


def get_all_open_projects():
    """
    Return a list with all the open projects.
    """
    return gazu.project.all_open_projects()


def get_all_open_project_names():
    """
    Return a list with the names of all the open projects.
    """
    project_dicts = gazu.project.all_open_projects()
    return sorted([project_dict["name"] for project_dict in project_dicts])


def delete_project(project_id):
    """
    Delete a project from its id.
    """
    project = gazu.project.get_project(project_id)
    gazu.project.close_project(project)
    gazu.project.remove_project(project, force=True)
