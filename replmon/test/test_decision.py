#coding:utf-8
import unittest
from replmon import Replmon


def mysql_parlance(b):
    """
    :type b: bool
    """
    return {True:"Yes", False:"No"}.get(b)

class DummyCursor(object):
    EXPECTED_QUERY = "SHOW SLAVE STATUS"

    def __init__(self, io_active, sql_active):
        self.io_active = io_active
        self.sql_active = sql_active
        self.executed = False

    def execute(self, query):
        assert query == self.EXPECTED_QUERY, "Query does not match %s" % self.EXPECTED_QUERY
        self.executed = True
        return 1

    def fetchone(self):
        assert self.executed, "Did no execute before fetching"
        self.executed = False
        return {"Slave_IO_Running": mysql_parlance(self.io_active),
                "Slave_SQL_Running": mysql_parlance(self.sql_active)}

class DummyConnection(object):
    def __init__(self):
        self.io_active = True
        self.sql_active = True

    def __enter__(self):
        return DummyCursor(self.io_active, self.sql_active)

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class StubbedMonitor(Replmon):
    """
    A Test class that uses a dummy connection
    """
    def __init__(self, *args, **kwargs):
        super(StubbedMonitor, self).__init__(*args, **kwargs)
        self.conn = DummyConnection()

    def get_connection(self):
        return self.conn


class DecisionTestCase(unittest.TestCase):
    """
    Here, we check that replmon makes the right decisions
    """
    def setUp(self):
        self.mon = StubbedMonitor({})

    def test_ok(self):
        self.mon.conn.io_active = True
        self.mon.conn.sql_active = True
        self.assertTrue(self.mon.check_replication())

    def test_ko(self):
        self.mon.conn.io_active = False
        self.mon.conn.sql_active = True
        self.assertFalse(self.mon.check_replication())

        self.mon.conn.io_active = True
        self.mon.conn.sql_active = False
        self.assertFalse(self.mon.check_replication())

        self.mon.conn.io_active = False
        self.mon.conn.sql_active = False
        self.assertFalse(self.mon.check_replication())
