#!/usr/bin/env python
# pylint: disable=C0103
import codecs
import sys

from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
  user_options = [('pytest-args=', 'a', "Arguments to pass into py.test")]

  def initialize_options(self):
    TestCommand.initialize_options(self)
    try:
      from multiprocessing import cpu_count

      self.pytest_args = ['-n', str(cpu_count()), '--boxed']
    except (ImportError, NotImplementedError):
      self.pytest_args = ['-n', '1', '--boxed']

  def finalize_options(self):
    TestCommand.finalize_options(self)
    self.test_args = []
    self.test_suite = True

  def run_tests(self):
    import pytest

    errno = pytest.main(self.pytest_args)
    sys.exit(errno)


requirements = codecs.open('./requirements.txt').read().splitlines()
long_description = codecs.open('./README.md').read()
version = codecs.open('./VERSION').read().strip()

test_requirements = [
  'pytest-cov',
  'pytest-forked',
  'pytest-xdist',
  'pytest',
]

setup(
  name='pokeapi',
  version=version,
  author='Lance Thompson',
  description='Pokeapi Python SDK',
  long_description=long_description,
  long_description_content_type='text/markdown',
  license='MIT',
  url='https://github.com/lancethomps/speakeasy-pokeapi',
  project_urls={
    'Bug Reports': 'https://github.com/lancethomps/speakeasy-pokeapi/issues',
    'Source': 'https://github.com/lancethomps/speakeasy-pokeapi',
  },
  packages=find_packages(where='src'),
  python_requires='>=3.8',
  install_requires=requirements,
  tests_require=test_requirements,
  cmdclass={
    'test': PyTest,
  },
  package_dir={'': 'src'},
  package_data={'pokeapi': ['py.typed']},
)
