#coding:utf-8
import argparse
import logging
import ConfigParser

import procname
import daemon
import lockfile.pidlockfile

from replmon import Replmon


logger = logging.getLogger()
logger.setLevel(logging.INFO)


DEFAULT_CNF_FILE = "/etc/replmon.ini"
DEFAULT_LOG_FILE = "/var/log/replmon.log"
DEFAULT_PID_FILE = "/var/run/replmon.pid"


def main():
    parser = argparse.ArgumentParser(description="Monitor your MySQL replication status")
    parser.add_argument("--config", help="Path to the replmon config file (default: {0})".format(DEFAULT_CNF_FILE),
                        default=DEFAULT_CNF_FILE)
    args = parser.parse_args()

    parser = ConfigParser.ConfigParser()
    parser.read(args.config)

    mysql_args = dict(parser.items("mysql"))
    mon = Replmon(mysql_args)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = logging.FileHandler(DEFAULT_LOG_FILE)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    with daemon.DaemonContext(pidfile=lockfile.pidlockfile.PIDLockFile(DEFAULT_PID_FILE),
                              files_preserve=[file_handler.stream]):
        procname.setprocname("replmon")
        # noinspection PyBroadException
        try:
            mon.run()
        except Exception:
            logger.exception("An error occurred")


if __name__ == "__main__":
    main()