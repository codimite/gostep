import subprocess
import traceback

from google.cloud import storage
from google.cloud.storage import Blob
from googleapiclient.discovery import build

from gostep.consts import FUNCTIONS_API
from gostep.consts import FUNCTIONS_API_VERSION
from gostep.consts import GCLOUD_STORAGE_CLASS


def get_service_client(api, version):
    """
        Creates and returns a service resource object.

            Parameters:
                api (string): api type of gcloud service
                version (string): gcloud service version

            Returns:
                service_client (object): A Resource object with methods for
                interacting with the service
    """
    try:
        return build(api, version)
    except Exception:
        print(traceback.format_exc())


def get_storage_client():
    """
        Creates and returns a storage service resource object.

            Returns:
                storage_client (object): storage service object
    """
    try:
        return storage.Client()
    except Exception:
        print(traceback.format_exc())


def get_locations(project):
    """
        Returns a list of available locations for a project.

            Parameters:
                project (string): root directory of the repo
                as 'projects/{project_id}'

            Returns:
                locations_list (list): list of location objects
    """
    try:
        service_client = get_service_client(
            FUNCTIONS_API, FUNCTIONS_API_VERSION)
        project_name = ''.join(['projects', '/', project])
        return service_client.projects().locations().list(
            name=project_name
        ).execute()['locations']
    except Exception:
        print(traceback.format_exc())


def create_bucket(name, location):
    """
        Creates a storage bucket and returns the created bucket object.

            Parameters:
                name (string): name of the bucket
                location (string): location id

            Returns:
                bucket (object): instance of created bucket object
    """
    try:
        client = get_storage_client()
        bucket = storage.Bucket(name=name, client=client)
        bucket.location = location
        bucket.storage_class = GCLOUD_STORAGE_CLASS
        return client.create_bucket(bucket)
    except Exception:
        print(traceback.format_exc())


def get_buckets():
    """
        Returns a list of bucket objects.

            Returns:
                buckets (list): list of bucket objects
    """
    try:
        client = get_storage_client()
        return client.list_buckets()
    except Exception:
        print(traceback.format_exc())


def get_bucket(name):
    """
        Returns the bucket object.

            Parameters:
                name (string): name of the bucket

            Returns:
                bucket (object): instance of a bucket object
    """
    try:
        client = get_storage_client()
        return client.get_bucket(name)
    except Exception:
        print(traceback.format_exc())


def upload_file_to_bucket(bucket_name, file_name, file):
    """
        Uploads a file to a storage bucket and returns it's access path.

            Parameters:
                bucket_name (string): name of the bucket
                file_name (string): name of the file with extension
                file (string): path of the file to be uploaded

            Returns:
                file_path (string): bucket path of the uploaded file
    """
    try:
        bucket = get_bucket(bucket_name)
        blob = Blob(name=file_name, bucket=bucket)
        with open(file, 'rb') as file_object:
            blob.upload_from_file(file_object)
        return ''.join(['gs://', blob.bucket.name, '/', blob.name])
    except Exception:
        print(traceback.format_exc())


def get_cloud_functions(location_path):
    """
        Returns a object list which describes a cloud function in a project.

            Parameters:
                location_path (string): path to function including function id
                as 'projects/{project_id}/locations/{location_id}'

            Returns:
                functions_list (list): list of function objects
    """
    try:
        service_client = get_service_client(
            FUNCTIONS_API, FUNCTIONS_API_VERSION)
        functions = service_client.projects().locations().functions().list(
            parent=location_path
        ).execute()
        if functions == {} or functions == []:
            return []
        return functions['functions']
    except Exception:
        print(traceback.format_exc())


def get_cloud_function(function_path):
    """
        Returns a object which describes a cloud function in a project.

            Parameters:
                function_path (string): path to function including function id
                as projects/{project_id}/locations/{location_id}/functions/{id}


            Returns:
                function (object): a function object
    """
    try:
        service_client = get_service_client(
            FUNCTIONS_API, FUNCTIONS_API_VERSION)
        return service_client.projects().locations().functions().get(
            name=function_path
        ).execute()
    except Exception:
        print(traceback.format_exc())


def deploy_cloud_function(location_path, function_spec):
    """
        Deploys a function for a given specification and returns a function
        object.

            Parameters:
                location_path (string): path to function including function id
                as projects/{project_id}/locations/{location_id}
                function_spec (object): changes to be patched

            Returns:
                function (object): deployed function object
    """
    try:
        service_client = get_service_client(
            FUNCTIONS_API, FUNCTIONS_API_VERSION)
        return service_client.projects().locations().functions().create(
            location=location_path, body=function_spec).execute()
    except Exception:
        print(traceback.format_exc())


def update_cloud_function(function_path, patch_field, update_spec):
    """
        Creates a directory if it does not exist.

            Parameters:
                function_path (string): path to function including function id
                as projects/{project_id}/locations/{location_id}/functions/{id}
                patch_field (string): field to be patched
                update_spec (object): changes to be patched

            Returns:
                function (object): updated function object
    """
    try:
        service_client = get_service_client(
            FUNCTIONS_API, FUNCTIONS_API_VERSION)
        return service_client.projects().locations().functions().patch(
            name=function_path, updateMask=patch_field,
            body=update_spec
        ).execute()
    except Exception:
        print(traceback.format_exc())


def get_projects():
    """
        List down available projects.

            Returns:
                projects_list (object): list of project objects
    """
    try:
        project_list = str(subprocess.check_output(
            ['gcloud', 'projects', 'list'])).replace('b', '') \
            .replace('\'', '').split('\\n')
        return project_list
    except Exception:
        print(traceback.format_exc())


def get_iam_policy(resource):
    """
        Get IAM policy for a given resource.

            Parameters:
                resource: resource path as
                /projects/{}/locations/{}/functions/{}

            Returns:
                iam_policy (object): policy object
    """
    try:
        service_client = get_service_client(FUNCTIONS_API,
                                            FUNCTIONS_API_VERSION)
        return service_client.projects().locations().functions().getIamPolicy(
            resource=resource).execute()
    except Exception:
        print(traceback.format_exc())


def set_iam_policy(resource, policy_request):
    """
        Get IAM policy for a given resource.

            Parameters:
                resource (string): resource path as
                /projects/{}/locations/{}/functions/{}
                policy_request (policy object): policy dictionary object

            Returns:
                iam_policy (object): policy object
    """
    try:
        service_client = get_service_client(FUNCTIONS_API,
                                            FUNCTIONS_API_VERSION)
        return service_client.projects().locations().functions().setIamPolicy(
            resource=resource, body=policy_request).execute()
    except Exception:
        print(traceback.format_exc())


def create_credentials(name, display_name):
    #process = subprocess.check_output(''.join(['gcloud iam service-accounts create ', name,
               #  ' --display-name ', display_name]), shell=True)
    create_acc_proc = 'Created service account [test123]'
    accounts_list_proc = subprocess.check_output('gcloud iam service-accounts list', shell=True)
    print(str(accounts_list_proc).replace('b', '').split())
    return True

