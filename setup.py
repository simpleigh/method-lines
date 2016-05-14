import os
import sys
from setuptools import setup, find_packages


BASE_DIR = os.path.dirname(__file__)


with open(os.path.join(BASE_DIR, 'VERSION')) as version_file:
    version = version_file.read().strip()


with open(os.path.join(BASE_DIR, 'README.rst')) as readme_file:
    long_description = readme_file.read()


requirements = [
    'XlsxWriter',
    'ringing-lib>=0.3',
    'six',
]


# These three lines copied from importlib setup.py
if ((sys.version_info[0] == 2 and sys.version_info[1] < 7) or
        (sys.version_info[0] == 3 and sys.version_info[1] < 1)):
    requirements.append('importlib')


setup(
    name='method-lines',
    version=version,
    author='Leigh Simpson',
    author_email='code@simpleigh.com',
    url='https://github.com/simpleigh/',
    description='Produces method lines and resources for peals in parts.',
    long_description=long_description,
    packages=find_packages(),
    install_requires=requirements,
    scripts=['execute.py'],
    entry_points={'console_scripts':[
        'method-lines = method_lines.commands:execute',
    ]},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    license='GPL',
)
