from setuptools import setup, find_packages

from vcloudtools import __version__

requirements = [
    'argh==0.17.2',
    'lxml==3.0.1',
    'requests==0.14.2',
    'simplejson==2.6.2',
]

python_scripts = [
    'browse',
    'login',
    'org',
]

setup(
    name='vcloudtools',
    version=__version__,
    packages=find_packages(exclude=['test*']),

    # metadata for upload to PyPI
    author='Nick Stenning',
    author_email='nick@whiteink.com',
    maintainer='Government Digital Service',
    url='https://github.com/alphagov/vcloudtools',

    description='vCloud: tools for interacting with the vCloud API',
    license='MIT',
    keywords='sysadmin vcloud vmware virtualisation api',

    install_requires=requirements,

    entry_points={
        'console_scripts': [
            'vcloud-{0}=vcloudtools.command.{1}:main'.format(s, s.replace('-', '_')) for s in python_scripts
        ]
    }
)
