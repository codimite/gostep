GCLOUD_STORAGE_CLASS = 'STANDARD'
FUNCTIONS_API = 'cloudfunctions'
FUNCTIONS_API_VERSION = 'v1'
SERVICE_ENTRY_POINT = 'main'
ENVIRONMENTS = [
    'python',
    'nodejs'
]

TEMPLATE_REPO = 'https://github.com/codimite/gostep-templates/trunk'
BASE_CONFIG_FILE = 'config.json'
AUTH_FILE = 'credentials.json'
SERVICE_CONFIG_FILE = 'function.json'
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
    'auth', 'init', 'inside', 'project', 'projects', 'project', 'locations', 'name', 'show', 'base', 'location', 'env', 'service'
]
