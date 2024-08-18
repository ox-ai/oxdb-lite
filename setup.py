import os
from setuptools import setup, find_packages

setup(
    name="ox-db",
    version="0.0.71",
    description="An OX-AI vector database",
    author="Lokeshwaran M",
    author_email="lokeshwaran.m23072003@gmail.com",
    url="https://github.com/ox-ai/ox-db.git",
    license="MIT",
    packages=find_packages(),
    package_data={"": ["requirements.txt", "README.md"]},
    install_requires=open("requirements.txt").readlines(),
    entry_points={
        "console_scripts": [
            "oxdb.shell=ox_db.shell.log:main", 
            "oxdb.server=ox_db.server.log:run_server", 
        ],
    },
    include_package_data=True,
    python_requires=">=3.6",
    keywords="ox-db ox-ai",
)
