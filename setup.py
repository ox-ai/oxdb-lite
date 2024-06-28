import os
from setuptools import setup, find_packages

setup(
    name='ox-db',
    version='0.0.71',
    description='A simple database and vector database',
    author='Lokeshwaran M',
    author_email='lokeshwaran.m23072003@gmail.com',
    url="https://github.com/ox-ai/ox-db.git",
    license="MIT",
    packages=find_packages(),
    package_data={'': ['requirements.txt', 'README.md']},
    install_requires=open('requirements.txt').readlines(),
    keywords='ox-db ox-ai'
)


