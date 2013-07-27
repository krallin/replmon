#coding:utf-8
from setuptools import setup

setup(
    name="replmon",
    version="0.0.6",
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
    tests_require=["tox", "nose", "unittest2"],
    description="A simple MySQL replication monitor",
    long_description=open("README.rst").read(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: Apache Software License",
    ]
)
