#coding:utf-8
import time
import os
import logging

import pymysql


logger = logging.getLogger(__name__)


DEFAULT_PIDFILE = "/var/run/replmon.pid"
DEFAULT_STATUS_FILE = "/var/run/replmon.status"
DEFAULT_INTERVAL = 10


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

    def run(self):
        logger.info("Starting monitoring loop")
        # noinspection PyBroadException
        try:
            while 1:
                logger.debug("Connecting to MySQL")
                conn = pymysql.Connect(**self.mysql_args)
                conn.cursorclass = pymysql.cursors.DictCursor

                with conn as cursor:
                    ret = cursor.execute("SHOW SLAVE STATUS")
                    status = cursor.fetchone()
                    logger.debug("Query status: %s", ret)

                if status is None:
                    logger.info("Running on master server. Exiting.")
                    break

                if (status["Slave_IO_Running"], status["Slave_SQL_Running"]) == ("Yes", "Yes"):
                    logger.debug("Status: OK")
                    self.touch_status_file()
                else:
                    logger.warning("Status: KO")

                time.sleep(self.interval)
        except Exception:
            logger.exception("An error occured")
