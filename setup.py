"""
scramble
"""
import sys
from setuptools import setup, find_packages

from scramble import __version__ as version


install_requires = [
    'setuptools']

setup(
    name='scramble',
    version=version,
    description="Symlink python modules into a folder",
    classifiers=[
        "Programming Language :: Python 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    keywords='',
    author='Ryan Northey',
    author_email='ryan@3ca.org.uk',
    url='http://github.com/phlax/scramble',
    license='GPL',
    packages=find_packages(),
    include_package_data=True,
    test_suite="scramble.tests",
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'scramble = scramble.command:main',
    ]})
