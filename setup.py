__author__ = 'Kristoffer Dalby <kradalby@kradalby.no>'
__version__ = '0.0.1'

from setuptools import setup, find_packages

with open('requirements.txt') as requirements_file:
    install_requirements = requirements_file.read().splitlines()
    if not install_requirements:
        print('Unable to read requirements from the requirements.txt file'
              'That indicates this copy of the source code is incomplete.')
        sys.exit(2)

setup(
    name='tail.py',
    version=__version__,
    description='Tail job STDOUT from AWX or Tower in the terminal',
    author=__author__,
    author_email='kradalby@kradalby.no',
    url='https://github.com/kradalby/awx-job-tailer',
    license='MIT',
    # Ansible will also make use of a system copy of python-six and
    # python-selectors2 if installed but use a Bundled copy if it's not.
    install_requires=install_requirements,
    scripts=[
        'tail.py',
    ],
    data_files=[],
    # Installing as zip files would break due to references to __file__
    zip_safe=False)
