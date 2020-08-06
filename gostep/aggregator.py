import re
from os.path import join

from gostep.builders import build_java_project
from gostep.consts import BASE_CONFIG_FILE, BUILD_DIR, GOSTEP_BUCKET, SERVICES, \
    TEMPLATES, NAME, DESCRIPTION, VERSION, SOURCE_DIRECTORY, SOURCE_ARCHIVE, \
    LOCATION_NAME, LOCATION_ID, PROJECT_ID, DEFAULT_LOCATION, \
    ENVIRONMENT, AUTH_FILE, SERVICE_CONFIG_FILE, CHECKSUM, TRIGGER, RUNTIME, JAVA_RUNTIME, \
    ALLOW_ALL
from gostep.consts import TEMPLATE_DIRECTORY
from gostep.file_manager import copy_dir, get_checksum
from gostep.file_manager import get_dir
from gostep.file_manager import get_json_from_file, create_compressed_file, \
    rewrite_json_file
from gostep.gcloud_ops import get_cloud_functions, get_buckets, \
    create_bucket, get_bucket, update_cloud_function, deploy_cloud_function, \
    upload_file_to_bucket, get_locations, set_iam_policy, get_iam_policy, \
    get_cloud_function
from gostep.repo_service import clone_template


def bootstrap_base(workspace_dir, project_name, description, default_location,
                   version):
    """
        Writes main project configuration.

            Parameters:
                workspace_dir (string): current workspace directory
                project_name (string): name of the project
                description (string): a little about project
                default_location (string): default location id
                version (string): version of the project

            Returns:
                project_spec (dictionary): generated project specification
    """
    print('Creating project specification...')
    credentials = get_json_from_file(''.join([workspace_dir, '/', AUTH_FILE]).replace('\\', ''))
    default_location = default_location if default_location is not None else \
        get_locations(credentials[PROJECT_ID])[0]['locationId']
    project_info = {
        NAME: project_name,
        PROJECT_ID: credentials[PROJECT_ID],
        DESCRIPTION: description,
        DEFAULT_LOCATION: default_location,
        VERSION: version,
        TEMPLATES: {},
        SERVICES: {}
    }
    project_spec = rewrite_json_file(
        ''.join([workspace_dir, '/', BASE_CONFIG_FILE]), project_info)
    get_dir(TEMPLATE_DIRECTORY, workspace_dir)
    print('Project base %s has been successfully generated.'
          % project_spec[NAME])
    return project_spec


def get_template(workspace_dir, environment):
    """
        Get template from template store, download if it does not exists.

        Parameters:
            workspace_dir (string): workspace directory
            environment (string): runtime

        Returns:
            template_dir (string): path to template
    """
    template_dir = get_dir(TEMPLATE_DIRECTORY, workspace_dir)
    return get_dir(environment, template_dir)


def get_template_from_store(environment, trigger, workspace_dir, project_spec):
    """
        Gets template from local store, download if it does not exists locally.

        Parameters:
            workspace_dir (string): workspace directory
            environment (string): runtime
            trigger (string): function invocation trigger
            project_spec (dictionary): base project config

        Returns:
            template_dir (string): path to template in local store
    """
    template_id = ''.join([environment, '/', trigger])
    template_path = ''.join([TEMPLATE_DIRECTORY, '/', template_id])
    if template_id not in project_spec.get(TEMPLATES).keys():
        template_path = get_dir(template_path, workspace_dir)
        source_template = clone_template(template_id, template_path)
        project_spec[TEMPLATES][template_id] = source_template.replace(''.join([workspace_dir, '/']), '')
        rewrite_json_file(''.join([workspace_dir, '/', BASE_CONFIG_FILE]), project_spec)
        return source_template
    return join(workspace_dir, project_spec[TEMPLATES][template_id])


def bootstrap_service(workspace_dir, name, description, environment, location, version, trigger, allow_all=False):
    """
        Gets template and builds directory for a service.

        Parameters:
            workspace_dir (string): workspace directory
            name (string): name of the service
            description (string): additional description
            environment (string): runtime
            location (string): gcloud location id
            version (string): version number,
            trigger (string): function invocation trigger,
            allow_all (boolen): allow invoke access to public

        Returns:
            service_spec (object): dictionary object containing service info
    """
    project_spec_file = ''.join([workspace_dir, '/', BASE_CONFIG_FILE])
    project_spec = get_json_from_file(project_spec_file)
    service_name = re.sub('[^A-Za-z0-9]+', '-', name).lower()
    if service_name in project_spec[SERVICES].keys():
        print('Service already exists. Please select a different name')
        return project_spec[SERVICES][service_name][SOURCE_DIRECTORY]
    print(''.join(['Fetching template from store for ', service_name]))
    template_dir = get_template_from_store(environment, trigger, workspace_dir, project_spec)
    sources_root = get_dir('src', workspace_dir)
    source_path = copy_dir(template_dir, ''.join([sources_root, '/', service_name]))
    location_name = ''.join(['projects/', project_spec[PROJECT_ID], '/locations/', location])
    function_name = ''.join([location_name, '/functions/', service_name])
    function_spec_file = ''.join([source_path, '/', SERVICE_CONFIG_FILE])
    function_spec = get_json_from_file(function_spec_file)
    function_spec[NAME] = function_name
    function_spec[DESCRIPTION] = description
    function_spec = rewrite_json_file(function_spec_file, function_spec)
    print('Function specification for %s has been updated.' % function_spec[NAME])
    project_spec = get_json_from_file(project_spec_file)
    project_spec[SERVICES][service_name] = {
        NAME: service_name,
        DESCRIPTION: description,
        SOURCE_DIRECTORY: source_path.replace(''.join([workspace_dir, '/']), ''),
        SOURCE_ARCHIVE: '',
        LOCATION_NAME: location_name,
        LOCATION_ID: location,
        VERSION: version,
        ENVIRONMENT: environment,
        TRIGGER: trigger,
        CHECKSUM: '',
        ALLOW_ALL: allow_all
    }
    project_spec = rewrite_json_file(project_spec_file, project_spec)
    print(''.join(['Function has been configured in ', project_spec[SERVICES][service_name][SOURCE_DIRECTORY]]))
    return project_spec[SERVICES][service_name]


def cloud_function_exists(name, location_path):
    """
        Find that function already has been deployed.

        Parameters:
            name (string): name of the service
            location_path (string): location path of the functions

        Returns:
            is_exists (boolean): true, if function already has been deployed
    """
    cloud_functions = get_cloud_functions(location_path)
    return any(name == function[NAME] for function in cloud_functions)


def bucket_exists(name):
    """
        Find that storage bucket already has been deployed.

        Parameters:
            name (string): name of the bucket

        Returns:
            is_exists (boolean): true, if bucket has been created
    """
    buckets = list(get_buckets())
    return any(name == bucket.name for bucket in buckets)


def get_storage_bucket(name, location):
    """
        Get the storage bucket, create one if it does not exists.

        Parameters:
            name (string): name of the bucket
            location(string): storage bucket location

        Returns:
            bucket (object): storage bucket object
    """
    if not bucket_exists(name):
        return create_bucket(name, location)
    return get_bucket(name)


def authorize_public_invoking(resource_path):
    """
        Add IAM policy to resource, for public invoking.

        Parameters:
            resource_path (string): path to function as
            /projects/{}/locations/{}/functions/{}

        Returns:
            policy (object): updated policy
    """
    return set_iam_policy(resource_path, {
        'policy': {
            'bindings': [
                {
                    'role': 'roles/cloudfunctions.invoker',
                    'members': ['allUsers']
                }
            ]
        }
    })


def invoke_role_exists(resource_path):
    """
        Find that policies have been set for the resource.

        Parameters:
            resource_path (string): path to function as
            /projects/{}/locations/{}/functions/{}

        Returns:
            is_exists (boolean): true, if policy bindings exists
    """
    policy = get_iam_policy(resource_path)
    return 'bindings' in policy


def upload_source_to_bucket(workspace_dir, name, service_dir, location, runtime):
    """
        Build compressed file and upload it into storage bucket.

        Parameters:
            workspace_dir (string): workspace directory path
            name (string): name of the function
            service_dir (string): path to service source
            location (string): region id
            runtime (string): runtime environment

        Returns:
            source_url (string): path to cloud function
    """
    build_dir = get_dir(BUILD_DIR, workspace_dir)
    service_root = service_dir
    if JAVA_RUNTIME in runtime:
        service_dir = build_java_project(service_dir)
    source_archive = create_compressed_file(name, service_root, service_dir, build_dir)
    storage_bucket = get_storage_bucket(GOSTEP_BUCKET, location)
    return upload_file_to_bucket(storage_bucket.name, name, source_archive)


def deploy(name, location, workspace_dir):
    """
        Deploy a cloud function service, redeploy if already has been deployed.

        Parameters:
            name (string): service name
            location (string): region id
            workspace_dir (string): workspace directory path

        Returns:
            function (object): cloud function object
    """
    project_spec_file = ''.join([workspace_dir, '/', BASE_CONFIG_FILE])
    project_spec = get_json_from_file(project_spec_file)
    service_name = re.sub('[^A-Za-z0-9]+', '-', name).lower()
    if service_name not in project_spec[SERVICES].keys():
        print('Service does not exists.')
        return False
    service_info = project_spec[SERVICES][service_name]
    service_dir = ''.join([workspace_dir, '/', service_info[SOURCE_DIRECTORY]])
    location = location if location is not None else get_locations(
        project_spec[PROJECT_ID])[0]['locationId'] if project_spec[DEFAULT_LOCATION] == '' else project_spec[
        DEFAULT_LOCATION]
    location_name = ''.join(['projects/', project_spec[PROJECT_ID], '/locations/', location])
    function_name = ''.join([location_name, '/functions/', service_name])
    function_spec_file = ''.join([service_dir, '/', 'function.json'])
    function_spec = get_json_from_file(function_spec_file)
    source_archive_url = upload_source_to_bucket(workspace_dir, service_name, service_dir, location,
                                                 function_spec[RUNTIME])
    function_spec[NAME] = function_name
    function_spec['sourceArchiveUrl'] = source_archive_url
    if cloud_function_exists(function_name, location_name):
        result = update_cloud_function(function_spec[NAME], 'sourceArchiveUrl', function_spec)
        function_spec[NAME] = result['metadata']['target']
    else:
        result = deploy_cloud_function(location_name, function_spec)
        function_spec[NAME] = result['metadata']['target']
    if project_spec[SERVICES][service_name][ALLOW_ALL] and not invoke_role_exists(function_spec[NAME]):
        authorize_public_invoking(function_spec[NAME])
    rewrite_json_file(function_spec_file, function_spec)
    project_spec[SERVICES][service_name][LOCATION_NAME] = location_name
    project_spec[SERVICES][service_name][LOCATION_ID] = location
    rewrite_json_file(project_spec_file, project_spec)
    service = get_cloud_function(function_spec[NAME])
    print(''.join(['New deployment has been triggered for ', service_name]))
    return service


def deploy_all(workspace_dir):
    project_spec_file = ''.join([workspace_dir, '/', BASE_CONFIG_FILE])
    project_spec = get_json_from_file(project_spec_file)
    for service_key in project_spec[SERVICES].keys():
        service = project_spec[SERVICES][service_key]
        service_dir = ''.join([workspace_dir, '/', service[SOURCE_DIRECTORY]])
        service_checksum = get_checksum(service_dir)
        if service_checksum != service[CHECKSUM]:
            print("Deploying service %s..." % service[NAME])
            deploy(service[NAME], service[LOCATION_ID], workspace_dir)
            service_checksum = get_checksum(service_dir)
            project_spec[SERVICES][service_key][CHECKSUM] = service_checksum
            project_spec = rewrite_json_file(project_spec_file, project_spec)
            print(''.join([service[NAME], ' service checksum updated ', service_checksum, '.']))
    print('All up to date.')
    return project_spec
