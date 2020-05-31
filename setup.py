from setuptools import setup

setup(
    name='gostep',
    scripts=[
        'bin/gcloud_service.py'
    ],
    version='0.1.0',
    description='Google Serverless Templates Provider',
    url='https://github.com/codimite/gostep',
    author='Lahiru Pathirage',
    author_email='lahiru@codimite.com',
    license='',
    packages=['gostep'],
    zip_safe=False,
    install_requires=[
        'PyYAML',
        'svn',
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib'
    ]
)