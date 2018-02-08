"""
scrambler
"""

import os

from setuptools import setup, find_packages

version = "0.0.5"


install_requires = ['setuptools']

# collective.recipe.omelette is only installed as it provides a
# good example of a namespaced package
tests_require = install_requires + ['collective.recipe.omelette']


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

long_description = read("README.rst")

setup(
    name='scrambler',
    version=version,
    description=(
        "Symlink (namespaced) python packages into a "
        + "single folder to aid development"),
    long_description=long_description,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    keywords='',
    author='Ryan Northey',
    author_email='ryan@3ca.org.uk',
    url='http://github.com/phlax/scrambler',
    license='GPL',
    packages=find_packages(),
    include_package_data=True,
    test_suite="scrambler.tests",
    tests_require=tests_require,
    zip_safe=False,
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'scrambler = scrambler.command:main']})
