#coding:utf-8
import argparse
import logging

import procname
import daemon
import lockfile.pidlockfile

from replmon import Replmon


logger = logging.getLogger()
logger.setLevel(logging.INFO)


DEFAULT_LOG_FILE = "/var/log/replmon.log"
DEFAULT_PID_FILE = "/var/run/replmon.pid"


def main():
    parser = argparse.ArgumentParser(description="Monitor your MySQL replication status")
    parser.add_argument("username", help="The MySQL username to use to connect")
    parser.add_argument("password", help="The MySQL password to use to connect")

    args = parser.parse_args()

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    file_handler = logging.FileHandler(DEFAULT_LOG_FILE)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    mon = Replmon({"user":args.username, "passwd":args.password})

    with daemon.DaemonContext(pidfile=lockfile.pidlockfile.PIDLockFile(DEFAULT_PID_FILE),
                              files_preserve=[file_handler.stream]):
        procname.setprocname("replmon")
        mon.run()

if __name__ == "__main__":
    main()