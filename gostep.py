import sys
import argparse
import json
import os

from gostep import get_locations, set_credential_file, bootstrap_service
from gostep import get_projects
from gostep import create_credentials
from gostep import bootstrap_base

from gostep.consts import COMMANDS, AUTH_FILE, BASE_CONFIG_FILE
from gostep.file_manager import path_exists
from gostep.file_manager import get_json_from_file
from gostep import default_gcloud_project


def projects():
    print("Available projects in Google cloud platform")
    for project in get_projects():
        print(project)


def locations(project_id):
    for location in get_locations(project_id):
        print(location)


def credentials(cred_file_path):
    return get_json_from_file(cred_file_path)


parser = argparse.ArgumentParser()
modified_args = []


if len(sys.argv) > 0:
    for arg_index in range(1, len(sys.argv)):
        if sys.argv[arg_index] in COMMANDS:
             modified_args.append(''.join(['--', sys.argv[arg_index]]))
        else:
            modified_args.append(sys.argv[arg_index])


parser.add_argument('-P', '--projects', action='store_true', help='GCloud projects list')

parser.add_argument('-p', '--project', help='Gostep project related operations.')

parser.add_argument('-l', '--locations', help='GCloud locations list')

parser.add_argument('-L', '--location', help='GCloud location Id')

parser.add_argument('-a', '--auth', action='store_true', help='Credentials related operations')

parser.add_argument('-i', '--init', help='Initialize something new. Value must be unique and greater than 6 chars.')

parser.add_argument('-b', '--base', action='store_true', help='Base configurations of the services cluster.')

parser.add_argument('-s', '--show', action='store_true', help='Show what you\'ve asked for.')

parser.add_argument('-S', '--service', action='store_true', help='Services related options')

parser.add_argument('-d', '--inside', help='Target directory.')

parser.add_argument('-E', '--explains', help='Description of something you want to create.')

parser.add_argument('-n', '--name', help='Name identifier. Must be unique and greater than 6 chars.')

parser.add_argument('-N', '--displayname', help='Display name.')

parser.add_argument('-e', '--env', help='Service runtime environment.')

parser.add_argument('-v', '--version', help='Version of the base.')

args = parser.parse_args(modified_args)



if args.auth:
    if args.init is not None:
        print('Creating service account authentication file...')
        project = default_gcloud_project()
        if project == '' or project is None:
            print("Error: Gcloud project is mandatory.")
        else:
            create_credentials(
                args.init,
                project,
                args.init if args.displayname is None else args.displayname,
                '.' if args.inside is None else args.inside
            )
    elif args.init is None and args.show:
        auth_file_path = ''.join(['.' if args.inside is None else args.inside, '/',AUTH_FILE])
        if not path_exists(auth_file_path):
            print('You can create credentials file by doing, \n'
                  'gostep auth init <service-account-name> as '
                  '<account-display-name> inside <workspace-dir>')
        else:
            print(json.dumps(credentials(auth_file_path), indent=4))
    elif args.init is None and not args.show and args.inside is None:
        print('Usage: gostep auth init <service-account-name> as <account-display-name> inside <workspace-dir>')
    elif not args.init and args.inside is not None:
        cred_file_path = ''.join([args.inside, '/', AUTH_FILE])
        print(''.join(['Setting credential file in ', cred_file_path]))
        set_credential_file(cred_file_path)

elif args.projects:
    projects()

elif args.base:
    if args.init is not None:
        project = default_gcloud_project()
        workspace = '.' if args.inside is None else args.inside
        if project == '' or project is None:
            print("Error: Gcloud project is mandatory.\ngcloud config set project <project-id>")
        else:
            cred_file_path = ''.join([workspace, '/', AUTH_FILE])
            if not path_exists(cred_file_path):
                create_credentials(
                    ''.join([args.init, '-service-account']),
                    project,
                    args.init if args.displayname is None else args.displayname,
                    workspace
                )
            print(''.join(['Setting credential file in ', cred_file_path]))
            set_credential_file(cred_file_path)
        locations = get_locations(default_gcloud_project())
        location = None
        if args.location is None or args.location not in locations:
            print('Warning: location is not in available locations. Default location will be set')
            location = locations[0]['locationId']
        else:
            location = args.location
        bootstrap_base(
            workspace,
            args.init,
            '<description>' if args.explains is None else args.explains,
            location,
            '0.1.0' if args.version is None else args.version
        )
    else:
        base_config_file = ''.join([
            '.' if args.inside is None else args.inside,
            '/', BASE_CONFIG_FILE
        ])
        if path_exists(base_config_file):
            print(get_json_from_file(base_config_file))
        else:
            print('You can initiate project base by doing,\ngostep base init <project-name> location <gcloud-location-id> inside <workspace-dir> version <version-tag> explains <description>')

elif args.service:
    if args.init is not None:
        workspace = '.' if args.inside is None else args.inside
        cred_file_path = ''.join([workspace, '/', AUTH_FILE])
        cred_exists = path_exists(cred_file_path)
        if not cred_exists or args.env is None:
            if not cred_exists:
                print(''.join([workspace, ' is not a gostep workspace. You can create a workspace by,\ngostep base init <project-name> location <gcloud-location-id> inside <workspace-dir> version <version-tag> explains <description']))
            if args.env is None:
                print('-e --env Runtime environment is required.')
        else:
            set_credential_file(cred_file_path)
            bootstrap_service(
                workspace,
                args.init,
                '<description>' if args.explains is None else args.explains,
                args.env,
                '0.1.0' if args.version is None else args.version
            )

else:
    print('Serverless templates provider for Google cloud platform')
    print('Version: 0.1.0')
    print('-h, --help for how to use')
