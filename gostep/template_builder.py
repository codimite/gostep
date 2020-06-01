import re

from gostep.consts import ROOT_CONFIG_FILE
from gostep.consts import SERVICE_ENTRY_POINT
from gostep.consts import TEMPLATE_DIRECTORY
from gostep.file_manager import build_yaml_file
from gostep.file_manager import copy_dir
from gostep.file_manager import get_dir
from gostep.file_manager import get_yaml_dict
from gostep.repo_service import clone_template


def bootstrap_project(root_dir, project_name, description, version, authors=[]):
    """
        Write root project configuration.

            Parameters:
                root_dir (string): working directory
                project_name (string): name of the project
                description (string): a little about project
                authors (list[string]): developers
                version (string): version of the project

            Returns:
                project_spec (dictionary): generated project specification
    """
    print('Creating project specification...')
    project_info = {
        'name': project_name,
        'description': description,
        'author': authors,
        'version': version,
        'environments': [],
        'templates': []
    }
    project_spec = build_yaml_file(ROOT_CONFIG_FILE, root_dir, project_info)
    get_dir(TEMPLATE_DIRECTORY, root_dir)
    print('Project base %s has been successfully generated.' % project_spec['project'])
    return project_spec


def get_template(root_dir, kind, environment):
    template_dir = get_dir(TEMPLATE_DIRECTORY, root_dir)
    kind_dir = get_dir(kind, template_dir)
    return get_dir(environment, kind_dir)


def bootstrap_service(root_dir, name, description, environment, version, kind, authors=[]):
    print('Creating service specification...')
    project_spec = get_yaml_dict(ROOT_CONFIG_FILE, root_dir)
    template_dir = get_template(root_dir, kind, environment)
    if environment not in project_spec['environments']:
        clone_template(kind, environment, template_dir)
        project_spec['environments'].append(environment)
        project_spec = build_yaml_file(ROOT_CONFIG_FILE, root_dir, project_spec)
    service_info = {
        'name': name,
        'project': project_spec['name'],
        'description': description,
        'entry_point': SERVICE_ENTRY_POINT,
        'version': version,
        'environment': environment,
        'kind': kind,
        'authors': authors
    }
    service_root = get_dir(kind, root_dir)
    service_dir = re.sub('[^A-Za-z0-9]+', '_', name).lower()
    service_dir_path = get_dir(service_dir, service_root)
    service_spec = build_yaml_file(ROOT_CONFIG_FILE, service_dir_path, service_info)
    copy_dir(template_dir, service_dir_path)
    print('Service base %s has been successfully generated.' % service_spec['name'])
    return project_spec
