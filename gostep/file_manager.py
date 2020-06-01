import fileinput
import os
import shutil
import traceback
from pathlib import Path
from zipfile import ZipFile

import yaml

from gostep.consts import GOSTEP_IGNORE_FILE


def get_all_files_dict(root_dir=os.getcwd()):
    """
        Get directory path and file name mapped structure as a dictionary

            Parameters:
                root_dir (string): root directory path

            Returns:
                dir_dict (dictionary): dictionary object containing filename
                against directory path
    """
    try:
        dir_dict = {}
        for root, dirs, files in os.walk(root_dir):
            for file in files:
                dir_dict[str(Path(os.path.abspath(os.path.join(root, file)))
                             .parent)] = file
        return dir_dict
    except Exception:
        print(traceback.format_exc())


def get_dir(dir_name, root_path=os.getcwd()):
    """
        Creates a directory if it does not exist.

            Parameters:
                root_path (string): root directory of the repo
                dir_name (string): sublevel directory of the repo

            Returns:
                dir_path (string): path of downloaded template
    """
    try:
        dir_path = ''.join([root_path, '/', dir_name])
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
            print('Created directory %s' % dir_path)
        return dir_path
    except Exception:
        print(traceback.format_exc())


def copy_dir(source, destination):
    """
        Copy a directory tree and returns destination path.

            Parameters:
                source (string): source containing root directory path
                destination (string): target root directory path

            Returns:
                destination (string): copied destination path
    """
    try:
        if not os.path.exists(destination):
            os.mkdir(destination)
        shutil.copytree(source, destination)
        return destination
    except Exception:
        print(traceback.format_exc())


def create_compressed_file(name, source_dir, target_dir):
    """
        Creates a compressed zip file removing given list of files to be
        ignored.

            Parameters:
                name (string): name of the compressed file
                source_dir (string): source directory path
                target_dir (string): target directory path

            Returns:
                target_file_path (string): compressed file path
    """
    try:
        target_file_path = ''.join([target_dir, '/', name, '.zip'])
        compressed_file = ZipFile(target_file_path, "w")
        ignore_list = get_yaml_dict(GOSTEP_IGNORE_FILE, source_dir).split(' ')
        for dir_name, sub_dirs, files in os.walk(source_dir):
            len_dir_path = len(dir_name)
            for filename in files:
                file_path = os.path.join(dir_name, filename)
                if any(substring in file_path for substring in ignore_list):
                    continue
                compressed_file.write(file_path, file_path[len_dir_path:])
        compressed_file.close()
        print("Successfully created compressed file %s" % target_file_path)
        return target_file_path
    except Exception:
        print(traceback.format_exc())


def write_to_file(file_name, dir_path, content):
    """
        Rewrite or create and write to file.

            Parameters:
                file_name (string): file name
                dir_path (string): root path which file contains
                content (string): content to be written

            Returns:
                file_path (string): copied destination path
    """
    file_path = ''.join([dir_path, '/', file_name])
    try:
        with open(file_path, 'w') as file_object:
            file_object.write(content)
        return file_path
    except Exception:
        print(traceback.format_exc())


def replace_string_in_file(file_name, dir_path, source_str, target_str):
    """
        Replace a string in a file.

            Parameters:
                file_name (string): file name
                dir_path (string): root path which file contains
                source_str (string): string to be replaced
                target_str (string): string which replace source string

            Returns:
                file_path (string): updated file path
    """
    file_path = ''.join([dir_path, '/', file_name])
    try:
        with fileinput.FileInput(file_path, inplace=True, backup='.bkp'
                                 ) as file_object:
            for line in file_object:
                line.replace(source_str, target_str)
        return file_path
    except Exception:
        print(traceback.format_exc())


def get_yaml_dict(yaml_file, source_dir):
    """
        Reads YAML file to a dictionary.

            Parameters:
                yaml_file (string): file name with the extension
                source_dir (string): target directory

            Returns:
                yaml_dict (dictionary): dictionary object
    """
    try:
        with open(''.join([source_dir, '/', yaml_file])) as yaml_source:
            return yaml.load(yaml_source, Loader=yaml.FullLoader)
    except Exception:
        print(traceback.format_exc())


def build_yaml_file(yaml_file, source_dir, yaml_dict):
    """
        Writes dictionary object to yaml file.

            Parameters:
                yaml_file (string): file name with the extension
                source_dir (string): target directory
                yaml_dict (dictionary): dictionary object to get written

            Returns:
                yaml_dict (dictionary): updated dictionary object
    """
    try:
        with open(''.join([source_dir, '/', yaml_file]), 'w') as yaml_source:
            yaml.dump(yaml_dict, yaml_source)
        return get_yaml_dict(yaml_file, source_dir)
    except Exception:
        print(traceback.format_exc())
