import os


def from_path_to_file(path):
    return os.path.basename(path)

def from_list_paths_to_list_files(list_paths):
    return [from_path_to_file(path) for path in list_paths]