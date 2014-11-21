import os
from os.path import dirname,join
import unittest

import django
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo-project.settings")
django.setup()
from django.conf import settings
from qiniustorage.backends import QiniuStorage, QiniuFile


class QiniuStorageTest(unittest.TestCase):
    def setUp(self):
        self.storage = QiniuStorage()

    def tearDown(self):
        try:
            self.storage.delete(self.file._name)
        except IOError:
            pass

    def test_init(self):
        self.file = fil = QiniuFile('foo', self.storage, mode='rb')
        assert fil._mode == 'rb'
        assert fil._name == "foo"

    def test_write_to_read_only_file(self):
        with pytest.raises(AttributeError):
            self.file = QiniuFile('foo', self.storage, mode='rb')
            self.file.write("goto fail")

    def test_write_file(self):
        ASSET_FILE_NAME = 'jquery-1.11.1.min.js'
        assert self.storage.exists(ASSET_FILE_NAME) == False
        self.file = QiniuFile(ASSET_FILE_NAME, self.storage, mode='wb')

        with open(join(dirname(__file__),'assets', ASSET_FILE_NAME), 'rb') as assset_file:
            content = assset_file.read()

            assset_file.seek(0, os.SEEK_END)
            assset_file_size = assset_file.tell()
            
            self.file.write(content)
            self.storage._save(ASSET_FILE_NAME, self.file)
            
            assert self.storage.exists(ASSET_FILE_NAME)

        assert self.storage.size(ASSET_FILE_NAME) == assset_file_size

        self.storage.delete(ASSET_FILE_NAME)
        assert self.storage.exists(ASSET_FILE_NAME) == False
