import sys
import argparse

from gostep import get_locations
from gostep import get_projects
from gostep import create_credentials

from gostep.consts import COMMANDS

def projects():
    for project in get_projects():
        print(project)


def locations(project_id):
    for location in get_locations(project_id):
        print(location)


def gcloud_credentials(workspace_dir):
    print('')


parser = argparse.ArgumentParser()
modified_args = []


if len(sys.argv) > 0:
    for arg_index in range(1, len(sys.argv)):
        if sys.argv[arg_index] in COMMANDS:
             modified_args.append(''.join(['--', sys.argv[arg_index]]))
        else:
            modified_args.append(sys.argv[arg_index])


parser.add_argument(
    '-g', '--gcloud', action='store_true', help='Gcloud related settings'
)

parser.add_argument(
    '-p', '--projects', action='store_true', help='GCloud projects list'
)

parser.add_argument(
    '-l', '--locations', help='GCloud locations list'
)

parser.add_argument(
    '-c', '--credentials', action='store_true', help='Generate credentials'
)

parser.add_argument(
    '-n', '--name', help='Name identifier'
)

parser.add_argument(
    '-N', '--display-name', help='Display name'
)


args = parser.parse_args(modified_args)

if args.gcloud and args.projects:
    projects()

if args.gcloud and args.locations is not None:
    print(args)
    locations(args.locations)

if args.gcloud and args.credentials is not None and args.name is not None:
    print(create_credentials(args.name, args.name if args.display_name is None else args.display_name))
