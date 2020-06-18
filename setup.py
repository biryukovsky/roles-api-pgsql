import json
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as test_command


def readme():
    with open('README.MD', 'r') as f:
        return f.read()


install_requires = []
tests_require = []


with open('Pipfile.lock') as fd:
    lock_data = json.load(fd)
    install_requires = [
        package_name + package_data['version']
        for package_name, package_data in lock_data['default'].items()
    ]
    tests_require = [
        package_name + package_data['version']
        for package_name, package_data in lock_data['develop'].items()
    ]


class PyTest(test_command):
    pytest_args = []
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        test_command.initialize_options(self)

    def finalize_options(self):
        test_command.finalize_options(self)

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name="roles_api_pgsql",
    version="0.0.1",
    description="Roles CRUD API",
    author="TASS",
    long_description=readme(),
    package_dir={'': 'src'},
    packages=find_packages('src', exclude=('*.tests',)),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    cmdclass={'test': PyTest},
    dependency_links=[
    ],
    entry_points={
        'console_scripts': [
            'roles-api-pgsql-ctl = roles_api_pgsql.commands:cli'
        ]
    },
)
