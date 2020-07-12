from os import path
from setuptools import setup


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='gostep',
    long_description=long_description,
    long_description_content_type='text/markdown',
    scripts=[
        './bin/gostep'
    ],
    version='0.1.0-beta3',
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
