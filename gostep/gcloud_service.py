from googleapiclient.discovery import build
import traceback
from google.cloud import storage
from google.cloud.storage import Blob


GCLOUD_STORAGE_CLASS = 'STANDARD'

FUNCTIONS_API = 'cloudfunctions'
FUNCTIONS_API_VERSION = 'v1'
GOSTEP_BUCKET = 'gostep'

def main():
  api = 'cloudfunctions'
  version = 'v1'
  service = build(api, version)
  print(service.projects().locations()
        .functions().list(parent='projects/serverless-278107/locations/us-east1').execute())


def get_service_client(api, version):
    try:
        return build(api,version)
    except Exception:
        print(traceback.format_exc())


def get_storage_client():
    try:
        return storage.Client()
    except Exception:
        print(traceback.format_exc())


def get_locations(project):
    try:
        service_client = get_service_client(FUNCTIONS_API, FUNCTIONS_API_VERSION)
        project_name = ''.join(['projects', '/', project])
        return service_client.projects().locations().list(name=project_name).execute()['locations']
    except Exception:
        print(traceback.format_exc())


def create_bucket(name, location):
    try:
        client = get_storage_client()
        bucket = storage.Bucket(name=name, client=client)
        bucket.location = location
        bucket.storage_class = GCLOUD_STORAGE_CLASS
        return client.create_bucket(bucket)
    except Exception:
        print(traceback.format_exc())


def get_bucket(name):
    try:
        client = get_storage_client()
        return client.get_bucket(name)
    except Exception:
        print(traceback.format_exc())


def upload_file_to_bucket(bucket_name, file_name, file):
    bucket = get_bucket(bucket_name)
    blob = Blob(name=file_name, bucket=bucket)
    with open(file, 'rb') as file_object:
        blob.upload_from_file(file_object)
    return


def deploy_funtion(location_string, function_spec):
    service_client = get_service_client(FUNCTIONS_API, FUNCTIONS_API_VERSION)
    function = service_client.projects().locations().functions().create(location=location_string, body=function_spec)\
        .execute()
    print(function)


deploy_funtion('projects/serverless-278107/locations/us-east1', {
    'name': 'projects/serverless-278107/locations/us-east1/functions/test1234',
    'entryPoint': 'main',
    'description': 'test',
    'sourceArchiveUrl': 'gs://gostep/1.zip',
    'runtime': 'python37',
    'status': 'ACTIVE',
    'httpsTrigger': {}
})

