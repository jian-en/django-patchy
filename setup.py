import os
import re
from setuptools import setup


def read_md(f):
    return open(f, 'r', encoding='utf-8').read()


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
    license='MIT License',
    description='Useful django patch for large project',
    long_description=read_md('README.md'),
    author='Fu Jian',
    author_email='fujian@luojilab.com',
    packages=get_packages('patchy'),
    install_requires=[],
    zip_safe=False,
    classifiers=[
        'Framework :: Django',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: MIT License',
        'Operating Systems :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)
