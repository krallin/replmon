#coding:utf-8
from setuptools import setup

setup(
    name="replmon",
    version="0.0.1",
    packages=["replmon"],
    url="",
    license="Apache 2.0",
    author="Thomas Orozco",
    author_email="thomas@scalr.com",
    install_requires=["python-daemon", "pymysql", "lockfile", "argparse", "procname"],
    entry_points={
        'console_scripts': [
            'replmon = replmon.cli:main',
            ],
        },
    description=""
)