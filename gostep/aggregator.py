import re

from gostep.consts import BASE_CONFIG_FILE, BUILD_DIR, GOSTEP_BUCKET, SERVICES, \
    TEMPLATES, NAME, DESCRIPTION, VERSION, SOURCE_DIRECTORY, SOURCE_ARCHIVE, \
    LOCATION_NAME, KIND, LOCATION_ID, PROJECT_ID, DEFAULT_LOCATION, \
    SERVICE_ACCOUNT_EMAIL, ENVIRONMENT, AUTH_FILE, SERVICE_CONFIG_FILE
from gostep.consts import TEMPLATE_DIRECTORY
from gostep.file_manager import copy_dir
from gostep.file_manager import get_dir
from gostep.file_manager import get_json_from_file, create_compressed_file, \
    rewrite_json_file
from gostep.gcloud_service import get_cloud_functions, get_buckets, \
    create_bucket, get_bucket, update_cloud_function, deploy_cloud_function, \
    upload_file_to_bucket, get_locations, set_iam_policy, get_iam_policy, \
    get_cloud_function
from gostep.repo_service import clone_template


def bootstrap_base(root_dir, project_name, description, default_location,
                   version):
    """
        Writes main project configuration.

            Parameters:
                root_dir (string): current workspace directory
                project_name (string): name of the project
                description (string): a little about project
                default_location (string): default location id
                version (string): version of the project

            Returns:
                project_spec (dictionary): generated project specification
    """
    print('Creating project specification...')
    credentials = get_json_from_file(''.join([root_dir, '/', AUTH_FILE]))
    default_location = default_location if default_location is not None else \
        get_locations(credentials[PROJECT_ID])[0]['locationId']
    project_info = {
        NAME: project_name,
        PROJECT_ID: credentials[PROJECT_ID],
        SERVICE_ACCOUNT_EMAIL: ['client_email'],
        DESCRIPTION: description,
        DEFAULT_LOCATION: default_location,
        VERSION: version,
        TEMPLATES: {},
        SERVICES: {}
    }
    project_spec = rewrite_json_file(''.join([root_dir, '/', BASE_CONFIG_FILE]),
                                     project_info)
    get_dir(TEMPLATE_DIRECTORY, root_dir)
    print('Project base %s has been successfully generated.'
          % project_spec[NAME])
    return project_spec


def get_template(root_dir, environment):
    """
        Get template from template store, download if it does not exists.

        Parameters:
            root_dir (string): workspace directory
            kind (string): serverless service kind
            environment (string): runtime

        Returns:
            template_dir (string): path to template
    """
    template_dir = get_dir(TEMPLATE_DIRECTORY, root_dir)
    return get_dir(environment, template_dir)


def bootstrap_service(root_dir, name, description, environment, version):
    """
        Gets template and builds directory for a service.

        Parameters:
            root_dir (string): workspace directory
            name (string): name of the service
            description (string): additional description
            environment (string): runtime
            version (string): version number

        Returns:
            project_spec (object): dictionary object containing configurations
    """
    project_spec_file = ''.join([root_dir, '/', BASE_CONFIG_FILE])
    project_spec = get_json_from_file(project_spec_file)
    service_name = re.sub('[^A-Za-z0-9]+', '-', name).lower()
    if service_name in project_spec[SERVICES].keys():
        print('Service already exists. Please select a different name')
        return project_spec[SERVICES][service_name][SOURCE_DIRECTORY]
    print(''.join(['Preparing template for ', service_name]))
    template_dir = get_template(root_dir, environment)
    if environment not in project_spec.get(TEMPLATES).keys():
        source_template = clone_template(environment, template_dir)
        project_spec[TEMPLATES][environment] = source_template.replace(
            ''.join([root_dir, '/']), '')
        project_spec = rewrite_json_file(''.join(
            [root_dir, '/', BASE_CONFIG_FILE]), project_spec)
    sources_root = get_dir('src', root_dir)
    source_path = copy_dir(template_dir, ''.join([sources_root, '/',
                                                  service_name]))
    function_spec_file = ''.join([source_path, '/', SERVICE_CONFIG_FILE])
    function_spec = get_json_from_file(function_spec_file)
    function_spec[NAME] = service_name
    function_spec[DESCRIPTION] = description
    function_spec[VERSION] = version
    function_spec = rewrite_json_file(function_spec_file, function_spec)
    print('Function specification for %s has been updated.'%function_spec[NAME])
    project_spec[SERVICES][service_name] = {
        NAME: service_name,
        DESCRIPTION: description,
        SOURCE_DIRECTORY: source_path.replace(''.join([root_dir, '/']), ''),
        SOURCE_ARCHIVE: '',
        LOCATION_NAME: '',
        VERSION: version,
        ENVIRONMENT: environment
    }
    project_spec = rewrite_json_file(project_spec_file, project_spec)
    print(''.join(['Template has been configured in ',
                   project_spec[SERVICES][service_name][SOURCE_DIRECTORY]]))
    return project_spec[SERVICES][service_name][SOURCE_DIRECTORY]


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
    return any(name in function[NAME] for function in cloud_functions)


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


def upload_source_to_bucket(workspace_dir, name, service_dir, location):
    """
        Build compressed file and upload it into storage bucket.

        Parameters:
            workspace_dir (string): workspace directory path
            name (string): name of the function
            service_dir (string): path to service source
            location (string): region id

        Returns:
            source_url (string): path to cloud function
    """
    build_dir = get_dir(BUILD_DIR, workspace_dir)
    source_archive = create_compressed_file(name, service_dir, build_dir)
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
            is_exists (boolean): true, if policy bindings exists
    """
    project_spec_file = ''.join([workspace_dir, '/', BASE_CONFIG_FILE])
    project_spec = get_json_from_file(project_spec_file)
    service_name = re.sub('[^A-Za-z0-9]+', '-', name).lower()
    if service_name not in project_spec[SERVICES].keys():
        print('Service does not exists')
        return False
    service_info = project_spec[SERVICES][service_name]
    service_dir = ''.join([workspace_dir, '/', service_info[SOURCE_DIRECTORY]])
    location = location if location is not None else get_locations(
        project_spec[PROJECT_ID])[0]['locationId'] if \
        project_spec[DEFAULT_LOCATION] == '' else project_spec[
        DEFAULT_LOCATION]
    location_name = ''.join(['projects/', project_spec[PROJECT_ID],
                             '/locations/', location])
    function_spec_file = ''.join([service_dir, '/', 'function.json'])
    function_spec = get_json_from_file(function_spec_file)
    source_archive_url = upload_source_to_bucket(workspace_dir, service_name,
                                                 service_dir, location)
    function_spec['sourceArchiveUrl'] = source_archive_url
    function_spec['serviceAccountEmail'] = project_spec[SERVICE_ACCOUNT_EMAIL]
    if cloud_function_exists(service_name, location_name):
        result = update_cloud_function(function_spec[NAME],
                                       'sourceArchiveUrl', function_spec)
        function_spec[NAME] = result['metadata']['target']
    else:
        result = deploy_cloud_function(location_name, function_spec)
        function_spec[NAME] = result['metadata']['target']
    if not invoke_role_exists(function_spec[NAME]):
        authorize_public_invoking(function_spec[NAME])
    rewrite_json_file(function_spec_file, function_spec)
    project_spec[SERVICES][service_name][LOCATION_NAME] = location_name
    project_spec[SERVICES][service_name][LOCATION_ID] = location
    project_spec = rewrite_json_file(project_spec_file, project_spec)
    service = get_cloud_function(project_spec['function'][service_name])
    print(''.join([service_name, ' has been deployed successfully.']))
    return service
