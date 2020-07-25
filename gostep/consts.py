GOSTEP_VERSION = 'v0.1.0beta'

GCLOUD_STORAGE_CLASS = 'STANDARD'
FUNCTIONS_API = 'cloudfunctions'
FUNCTIONS_API_VERSION = 'v1'
SERVICE_ENTRY_POINT = 'main'
ENVIRONMENTS = [
    'python',
    'nodejs',
    'java/plain',
    'java/spring'
]

TEMPLATE_REPO = 'https://github.com/codimite/gostep-templates/trunk'
BASE_CONFIG_FILE = 'config.json'
AUTH_FILE = 'credentials.json'
SERVICE_CONFIG_FILE = 'function.json'
TEMPLATE_DIRECTORY = 'templates'
BUILD_DIR = '../build'
GOSTEP_IGNORE_FILE = '.gostepignore'
GOSTEP_BUCKET = 'gostep'

SERVICES = 'services'
TEMPLATES = 'templates'
NAME = 'name'
ALLOW_ALL = 'allow_all'
RUNTIME = 'runtime'
JAVA_RUNTIME = 'java'
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
CHECKSUM = 'checksum'
TRIGGER = 'trigger'
HTTP = 'http'
HTTPS_TRIGGER_KEY = 'httpsTrigger'
EVENT_TRIGGER_KEY = 'eventTrigger'
EVENT_TYPE = 'eventType'
EVENT_TYPE_PUBSUB = 'cloud.pubsub'
EVENT_TYPE_STORAGE = 'cloud.storage'
RESOURCE = 'resource'
VALIDATION_MESSAGES = 'msgs'
REQUIRED_FIELDS = 'required'
TYPE = 'type'
TEXT = 'text'
BOOLEAN = 'boolean'
TRIGGERS = ['http', 'pubsub', 'storage']

COMMANDS = [
    'auth',
    'init',
    'inside',
    'projects',
    'location',
    'locations',
    'display-name',
    'show',
    'base',
    'location',
    'env',
    'service',
    'deploy',
    'gcloud',
    'trigger',
    'allow-all',
    'version'
]

CMD_BRANCHES = [
    'auth',
    'base',
    'deploy',
    'gcloud',
    'service'
]

CMD_TREE = {
    'auth': {
        TYPE: BOOLEAN,
        'init': {
            TYPE: TEXT,
            VALIDATION_MESSAGES: [
                'Error: Invalid command.\nUsage:'
                '  gostep auth init <project name>',
                '    Optional args:\n'
                '        display-name <service account display name>\n'
                '        inside <workspace directory>'
            ]
        },
        'inside': {
            TYPE: TEXT,
            VALIDATION_MESSAGES: [
                'Error: Invalid command.\nUsage:',
                '  gostep auth inside <workspace directory>'
            ]
        },
        'show': {
            TYPE: BOOLEAN
        },
        VALIDATION_MESSAGES: [
            'Error: Invalid command.\nUsage:',
            '  gostep auth init <project name>',
            '    Optional args:\n'
            '        display-name <service account display name>\n'
            '        inside <workspace directory>'
            '  gostep auth show',
            '    Optional args:\n'
            '        inside <workspace directory>'
        ]
    },
    'base': {
        TYPE: BOOLEAN,
        'init': {
            TYPE: TEXT,
            VALIDATION_MESSAGES: [
                'Error: Invalid command.\nUsage:'
                '  gostep base init <project name>',
                '    Optional args:\n'
                '        explains <project info>\n'
                '        inside <workspace directory>\n'
                '        location <gcloud region id>\n'
                '        version <project version>'
            ]
        },
        'show': {
            TYPE: BOOLEAN
        },
        VALIDATION_MESSAGES: [
            'Error: Invalid command.\nUsage:',
            '  gostep base init <project name>',
            '    Optional args:\n'
            '        explains <project info>\n'
            '        inside <workspace directory>\n'
            '        location <gcloud region id>\n'
            '        version <project version>'
            '  gostep base show',
            '    Optional args:\n'
            '        inside <workspace directory>'
        ]
    },
    'deploy': {
        TYPE: TEXT,
        VALIDATION_MESSAGES: [
            'Error: Invalid command.\nUsage:',
            '  gostep deploy diff',
            '    Optional args:\n'
            '        inside <workspace directory>'
            '  gostep deploy <service name>',
            '    Optional args:\n'
            '        inside <workspace directory>'
        ]
    },
    'gcloud': {
        TYPE: BOOLEAN,
        REQUIRED_FIELDS: [
            {
                'projects': {
                    TYPE: BOOLEAN
                }
            },
            {
                'locations': {
                    TYPE: BOOLEAN
                }
            }
        ],
        VALIDATION_MESSAGES: [
            'Error: Invalid command.\nUsage:',
            '  gostep gcloud projects',
            '  gostep gcloud locations',
            '    Optional args:\n'
            '        inside <workspace directory>'
        ]
    },
    'service': {
        TYPE: BOOLEAN,
        'init': {
            TYPE: TEXT,
            REQUIRED_FIELDS: {
                'env': {
                    TYPE: TEXT,
                },
                'trigger': {
                    TYPE: TEXT
                }
            },
            VALIDATION_MESSAGES: [
                'Error: Invalid command.\nUsage:',
                '  gostep service init <service name> env <runtime environment> trigger <function invoker>',
                '    Optional args:\n'
                '        explains <project info>\n'
                '        inside <workspace directory>\n'
                '        location <gcloud region id>\n'
                '        version <project version>\n'
                '        allow-all'
            ]
        },
        VALIDATION_MESSAGES: [
            'Error: Invalid command.\nUsage:',
            '  gostep service init <service name> env <runtime environment> trigger <function invoking type>',
            '    Optional args:\n'
            '        explains <project info>\n'
            '        inside <workspace directory>\n'
            '        location <gcloud region id>\n'
            '        version <project version>\n'
            '        allow-all'
        ]
    },
    VALIDATION_MESSAGES: [
        'GOSTEP - Serverless templates provider for Google cloud platform',
        'Version: %s' % GOSTEP_VERSION,
        'Usage:',
        '  gostep auth init <gcloud service account name>',
        '  gostep auth inside <workspace directory>',
        '  gostep auth show',
        '  gostep base init <project name>',
        '  gostep base show',
        '  gostep deploy diff',
        '  gostep deploy <service name>',
        '  gostep gcloud locations',
        '  gostep gcloud projects',
        '  gostep service init <service name> env <runtime environment> trigger <function invoking type>'
    ]
}
