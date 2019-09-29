# coding: utf-8

from tests.common import TestCase

from seecode.services.gitlab_sync import start


class GitLabSyncTestCase(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_gitlab_sync_start(self):
        start()

