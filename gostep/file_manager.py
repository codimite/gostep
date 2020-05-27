import os


def create_dir(dir_path, dir_name):
    dir_path = dir_path + '/' + dir_name
    os.mkdir(dir_path)
    print("created directory " + dir_path)

