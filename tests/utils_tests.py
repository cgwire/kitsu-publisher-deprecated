import gazu
import random

import gazupublisher.utils as utils

def connect():
    if not utils.is_logged_in():
        utils.configure_host("http://localhost/api")
        utils.connect_user("admin@example.com", "mysecretpassword")

def delete_project_from_name(name):
    return utils.delete_project_from_name(name)

def delete_previous_datas(project_dict):
    """
    Delete all the assets of a project
    """
    asset_types = gazu.asset.all_assets_for_project(project_dict)
    for asset in asset_types:
        gazu.asset.remove_asset(asset, force=True)

def get_unique_asset_name(project_dict, asset_type_dict):
    """
    Return an inexisting asset name for the given project and given asset type.
    """
    cpt = 2
    base_name = "Random " + asset_type_dict["name"] + " asset"
    name = base_name
    while gazu.asset.get_asset_by_name(project_dict, name):
        name = base_name + str(cpt)
        cpt += 1
    return name

def create_and_assign_tasks_and_assets(project_dict, nb_tasks=4, with_random=False):
    """
    Create assets and tasks.
    The nature of the assets and tasks can be randomized
    """
    all_asset_types = gazu.asset.all_asset_types()
    all_task_types = gazu.task.all_task_types()
    person = gazu.person.get_person_by_desktop_login("")

    for _ in range(nb_tasks):
        asset_type_dict = random.choice(all_asset_types) if with_random\
            else all_asset_types[0]  # Arbitrary
        name = get_unique_asset_name(project_dict, asset_type_dict)
        asset = gazu.asset.new_asset(
            project_dict,
            asset_type_dict,
            name,
            "Basic asset description"
        )

        task_type = random.choice(all_task_types) if with_random\
            else all_task_types[0]  # Arbitrary
        gazu.task.new_task(asset, task_type, assignees=[person])


def create_test_project(project_name):
    """
    Create the project associated to the given name.
    If it already exists, it returns this instance.
    """
    project = gazu.project.get_project_by_name(project_name)
    if not project:
        return gazu.project.new_project(project_name)
    return project

def generate_project(name):
    """
    Generates a project with a fixed number of assets and tasks (one task by asset)
    """
    project_dict = create_test_project(name)
    delete_previous_datas(project_dict)
    create_and_assign_tasks_and_assets(project_dict, nb_tasks=4)
