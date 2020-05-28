import traceback
import os


def create_dir(root_path, dir_name):
    """
        Create a directory.

                Parameters:
                        root_path (string): root directory of the repo
                        dir_name (string): sublevel directory of the repo
                Returns:
                        dir_path (str): path of downloaded template
    """
    try:
        dir_path = ''.join([root_path, '/', dir_name])
        os.mkdir(dir_path)
        print('Created directory %s'%dir_path)
        return dir_path
    except Exception:
        print(traceback.format_exc())


