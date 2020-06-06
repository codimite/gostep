GCLOUD_STORAGE_CLASS = 'STANDARD'
FUNCTIONS_API = 'cloudfunctions'
FUNCTIONS_API_VERSION = 'v1'
SERVICE_KINDS = [
    'function',
    'run'
]
SERVICE_ENTRY_POINT = 'main'
ENVIRONMENTS = [
    'python',
    'nodejs'
]

TEMPLATE_REPO = 'https://github.com/codimite/gostep-templates/trunk'
ROOT_CONFIG_FILE = 'config.json'
TEMPLATE_DIRECTORY = 'templates'
BUILD_DIR = 'build'
GOSTEP_IGNORE_FILE = '.gostepignore'
GOSTEP_BUCKET = 'gostep'

SERVICES = 'services'
TEMPLATES = 'templates'
NAME = 'name'
DESCRIPTION = 'description'
ENVIRONMENT = 'env'
VERSION = 'version'
SOURCE_DIRECTORY = 'source_dir'
SOURCE_ARCHIVE = 'source_archive'
LOCATION_NAME = 'location_name'
LOCATION_ID = 'location_id'
DEFAULT_LOCATION = 'default_location'
KIND = 'kind'
PROJECT_ID = 'project_id'
SERVICE_ACCOUNT_EMAIL = 'service_account_email'

COMMANDS = [
    'gcloud', 'credentials', 'creds', 'projects',
]