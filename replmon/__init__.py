#coding:utf-8
import time
import os
import logging

import pymysql


logger = logging.getLogger(__name__)


DEFAULT_PIDFILE = "/var/run/replmon.pid"
DEFAULT_STATUS_FILE = "/var/run/replmon.status"
DEFAULT_INTERVAL = 10


class IsMaster(Exception):
    """
    Raised if Replmon is started against a Master MySQL host.
    """


class Replmon(object):
    def __init__(self, mysql_args):
        self.mysql_args = mysql_args
        self.pid_file = DEFAULT_PIDFILE
        self.status_file = DEFAULT_STATUS_FILE
        self.interval = DEFAULT_INTERVAL

    def touch_status_file(self):
        if not os.path.exists(self.status_file):
            open(self.status_file, "w")
        os.utime(self.status_file, None)

    def get_connection(self):
        logger.debug("Connecting to MySQL")
        conn = pymysql.Connect(**self.mysql_args)
        conn.cursorclass = pymysql.cursors.DictCursor
        return conn

    def check_replication(self):
        with self.get_connection() as cursor:
            ret = cursor.execute("SHOW SLAVE STATUS")
            status = cursor.fetchone()
            logger.debug("Query status: %s", ret)

        if status is None:
            raise IsMaster()

        return (status["Slave_IO_Running"], status["Slave_SQL_Running"]) == ("Yes", "Yes")

    def run(self):
        logger.info("Starting monitoring loop")
        try:
            while 1:
                if self.check_replication():
                    logger.debug("Status: OK")
                    self.touch_status_file()
                else:
                    logger.warning("Status: KO")
                    time.sleep(self.interval)
        except IsMaster:
            logger.warning("Running on master server. Exiting.")
