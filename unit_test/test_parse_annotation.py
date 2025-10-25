import unittest

# Library we want to unit test
from parse_annotation import *


class TestAddFunction(unittest.TestCase):
    def test_failed_file_open(self):
        success = parseDronePicsXml('nofile.xml', [])
        self.assertEqual(success, False)

if __name__ == '__main__':
    unittest.main()
