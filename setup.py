import os
import re
from setuptools import setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `init.py`
    """
    init_py = open(os.path.join(package, '__init__.py')).read()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]

version = get_version('patchy')

setup(
    name='djangopatchy',
    version=version,
    description='Useful django patch for luojilab team',
    author='Fu Jian',
    author_email='fujian@luojilab.com',
    packages=get_packages('patchy'),
    zip_safe=False
)
