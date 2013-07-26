#coding:utf-8
from setuptools import setup

setup(
    name="replmon",
    version="0.0.2",
    packages=["replmon"],
    url="https://github.com/krallin/replmon",
    license="Apache 2.0",
    author="Thomas Orozco",
    author_email="thomas@scalr.com",
    install_requires=["python-daemon", "pymysql", "lockfile", "argparse", "procname"],
    entry_points={
        'console_scripts': [
            'replmon = replmon.cli:main',
            ],
        },
    setup_requires=["nose"],
    tests_require=["tox", "nose"],
    description=""
)
