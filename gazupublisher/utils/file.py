import os


def from_list_paths_to_list_files(list_paths):
    """
    Return a list of files from a list of path.
    """
    return [os.path.basename(path) for path in list_paths]
