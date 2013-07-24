#coding:utf-8
import os
import shutil
import tempfile
import unittest
import time

from replmon import Replmon


class StatusFileTestCase(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.status_file = os.path.join(self.test_dir, "replmon.status")

        self.mon = Replmon({})
        self.mon.status_file = self.status_file

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def assertFileExists(self, path):
        try:
            open(path)
        except IOError:
            self.fail("File does not exist: {0}".format(path))

    def test_create_status_file(self):
        self.mon.touch_status_file()
        self.assertFileExists(self.status_file)

    def test_touch_status_file(self):
        atime = mtime = 1
        open(self.status_file, "w")
        os.utime(self.status_file, (atime, mtime))

        self.mon.touch_status_file()

        stat = os.stat(self.status_file)
        self.assertNotEqual(atime, stat.st_atime)
        self.assertNotEqual(mtime, stat.st_mtime)

        self.assertAlmostEqual(time.time(), stat.st_atime, delta=2)
        self.assertAlmostEqual(time.time(), stat.st_mtime, delta=2)
