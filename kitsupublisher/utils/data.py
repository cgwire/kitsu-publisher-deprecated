"""
Module containing utility functions regarding data retrieving
"""

import gazu

from .date import extract_date, from_datetime_to_date, is_date_x_days_old

organisation = None
user = None

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


def get_project_from_id(id):
    """
    Get a project from its id
    """
    return gazu.project.get_project(id)


def get_current_user():
    """
    Get the current user.
    """
    global user
    if user is None:
        user = gazu.client.get_current_user()
    return user


def get_current_organisation():
    """
    Get the current organisation.
    """
    global organisation
    if organisation is None:
        organisation = gazu.person.get_organisation()
    return organisation


def get_asset_by_name(project_dict, asset_name):
    """
    Get an asset from its project and its name
    """
    return gazu.asset.get_asset_by_name(project_dict, asset_name)


def get_task_status():
    """
    Return a list of dict with all the task statuses provided by the gazu API.
    """
    return gazu.task.all_task_statuses()


def get_accessible_task_status():
    """
    Return a dict with the accessible task status
    """
    all_tasks_status = get_task_status()
    accessible_tasks_status = []
    for task_status in all_tasks_status:
        if task_status["is_artist_allowed"]:
            accessible_tasks_status.append(task_status)
    return accessible_tasks_status


def get_all_tasks_to_do():
    """
    Return a list with all the tasks the user has to do.
    """
    to_do_tasks = gazu.user.all_tasks_to_do()
    done_tasks = get_done_tasks()
    return to_do_tasks + done_tasks


def get_done_tasks():
    """
    Return a list with all the tasks the user has completed over the last X days.
    """
    user = get_current_user()
    all_done_tasks = gazu.task.all_done_tasks_for_person(user)
    number_days_a_done_task_remain = 7
    res = []
    for done_task in all_done_tasks:
        last_date = done_task["last_comment_date"]
        datetime = extract_date(last_date)
        date = from_datetime_to_date(datetime)
        if is_date_x_days_old(date, number_days_a_done_task_remain):
            res.append(done_task)
    return res

def get_all_comments_for_task(task):
    """
    Return a list with all the comments associated to the given task.
    """
    return gazu.task.all_comments_for_task(task)


def get_all_previews_for_task(task):
    """
    Return a list with all the previews for the given task.
    """
    return gazu.files.get_all_preview_files_for_task(task)


def get_last_comment_for_task(task):
    """
    Return the most recent comment for given task.
    """
    return gazu.task.get_last_comment_for_task(task)


def post_comment(task, task_status, text):
    """
    Post a comment for a given task.
    """
    return gazu.task.add_comment(task, task_status, text)


def post_preview(task, comment, path):
    """
    Post a comment and a preview file for a given task.
    """
    gazu.task.add_preview(task, comment, path)

