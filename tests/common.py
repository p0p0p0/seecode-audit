# coding: utf-8

import os
import sys
import unittest
import django.conf

dirname = os.path.dirname
BASEDIR = dirname(dirname(dirname(os.path.abspath(__file__))))

sys.path.append(BASEDIR)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "seecode.settings.dev")
django.setup()


class TestCase(unittest.TestCase):
    """

    """

    skipTest = True

    def setUp(self):
        pass

    def tearDown(self):
        pass
