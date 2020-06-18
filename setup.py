from setuptools import setup

setup(
    name='gostep',
    scripts=[
        './bin/gostep'
    ],
    version='0.1.0-beta1',
    description='Serverless Templates Provider for Google Cloud platform',
    url='https://github.com/codimite/gostep',
    author='Lahiru Pathirage',
    author_email='lahiru@codimite.com',
    license='MIT',
    packages=['gostep'],
    zip_safe=False,
    install_requires=[
        'svn',
        'google-cloud-storage',
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        'oauth2client',
        'pyyaml',
        'checksumdir'
    ]
)
