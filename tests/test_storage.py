# -*- coding: utf-8 -*-
from datetime import datetime
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
        except (IOError, AttributeError):
            pass

    def test_init(self):
        self.file = fil = QiniuFile('foo', self.storage, mode='rb')
        assert fil._mode == 'rb'
        assert fil._name == "foo"

    def test_write_to_read_only_file(self):
        with pytest.raises(AttributeError):
            self.file = QiniuFile('foo', self.storage, mode='rb')
            self.file.write("goto fail")

    def test_write_and_delete_file(self):
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

        time_delta = datetime.now() - self.storage.modified_time(ASSET_FILE_NAME)
        assert time_delta.total_seconds() < 60

        self.storage.delete(ASSET_FILE_NAME)
        assert self.storage.exists(ASSET_FILE_NAME) == False

    def test_read_file(self):
        ASSET_FILE_NAME = 'bootstrap.min.css'

        with open(join(dirname(__file__),'assets', ASSET_FILE_NAME), 'rb') as assset_file:
            self.storage.save(ASSET_FILE_NAME, assset_file)

        self.file = self.storage.open(ASSET_FILE_NAME, 'r')

        assert self.file._is_read == False

        content = self.file.read()
        assert content.startswith("/*!")

        assert self.file._is_read == True

    def test_dirty_file(self):
        ASSET_FILE_NAME = 'bootstrap.min.css'

        self.file = self.storage.open(ASSET_FILE_NAME, 'rw')

        assert self.file._is_read == False
        assert self.file._is_dirty == False
        assert self.storage.exists(ASSET_FILE_NAME) == False

        with open(join(dirname(__file__),'assets', ASSET_FILE_NAME), 'r') as assset_file:
            content = assset_file.read()
            self.file.write(content)

        assert self.file._is_read == True
        assert self.file._is_dirty == True

        self.file.close()
        assert self.storage.exists(ASSET_FILE_NAME) == True