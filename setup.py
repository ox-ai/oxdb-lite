import os
from setuptools import setup, find_packages

setup(
    name="ox-db",
    version="0.0.1",
    description="An OX-AI vector database",
    author="Lokeshwaran M",
    author_email="lokeshwaran.m23072003@gmail.com",
    url="https://github.com/ox-ai/ox-db.git",
    license="MIT",
    packages=find_packages(),
    install_requires=open("requirements.txt").readlines(),
    entry_points={
        "console_scripts": [
            "oxdb.shell=oxdb.shell.cli:main",
            "oxdb.server=oxdb.server.log:main",
        ],
    },
    package_data={
        "": ["requirements.txt", "README.md"]
    },
    include_package_data=True,
    python_requires=">=3.6",
    keywords="ox-db ox-ai",
)
