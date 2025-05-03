import os
import shutil


def move_files(source_dir: str, target_dir: str):
    """
    Move files from source directory to target directory.
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for file in os.listdir(source_dir):
        shutil.move(os.path.join(source_dir, file), os.path.join(target_dir, file))


def move_folders(source_dir: str, target_dir: str):
    """
    Move folders from source directory to target directory.
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    for folder in os.listdir(source_dir):
        shutil.move(os.path.join(source_dir, folder), os.path.join(target_dir, folder))


def get_all_files_in_dir(dir_path: str) -> list[str]:
    """
    Get all files in a directory.
    """
    return [
        os.path.join(dir_path, file)
        for file in os.listdir(dir_path)
        if os.path.isfile(os.path.join(dir_path, file))
    ]


def get_all_folders_in_dir(dir_path: str) -> list[str]:
    """
    Get all folders in a directory.
    """
    return [
        os.path.join(dir_path, folder)
        for folder in os.listdir(dir_path)
        if os.path.isdir(os.path.join(dir_path, folder))
    ]


def get_all_files_in_dir_with_format(
    dir_path: str, format: tuple[str, ...]
) -> list[str]:
    """
    Get all files in a directory with a specific format.
    """
    return [
        os.path.join(dir_path, file)
        for file in os.listdir(dir_path)
        if os.path.isfile(os.path.join(dir_path, file)) and file.endswith(format)
    ]


def check_folder_exists_or_file_exists(path: str) -> bool:
    """
    Check if a folder exists or a file exists.
    """
    return os.path.exists(path)


def copy_folder(source_dir: str, target_dir: str):
    """
    Copy a folder from source directory to target directory.
    """
    try:
        shutil.copytree(source_dir, target_dir)
    except FileExistsError:
        print(f"Folder {target_dir} already exists. Skipping copy.")


def create_folder(folder_path: str):
    """
    Create a folder.
    """
    os.makedirs(folder_path)


def create_file(file_path: str):
    """
    Create a file.
    """
    open(file_path, 'w+').close()


def copy_file(source_file: str, target_file: str):
    """
    Copy a file from source file to target file.
    """
    try:
        shutil.copy(source_file, target_file)
    except FileExistsError:
        print(f"File {target_file} already exists. Skipping copy.")
