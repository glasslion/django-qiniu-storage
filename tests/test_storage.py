# -*- coding: utf-8 -*-
from datetime import datetime
import os
from os.path import dirname,join
import unittest
import uuid

import django
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo-project.settings")

try:
    django.setup()
except AttributeError:
   # Setup isn't necessary in Django < 1.7
   pass

from django.conf import settings
from qiniustorage.backends import QiniuStorage, QiniuFile
from qiniustorage.utils import QiniuError

UNIQUE_PATH = str(uuid.uuid4())

class QiniuStorageTest(unittest.TestCase):
    def setUp(self):
        self.storage = QiniuStorage()

    def tearDown(self):
        try:
            self.storage.delete(self.file._name)
        except (QiniuError, AttributeError):
            pass

    def test_file_init(self):
        self.file = fil = QiniuFile('foo', self.storage, mode='rb')
        assert fil._mode == 'rb'
        assert fil._name == "foo"

    def test_write_to_read_only_file(self):
        with pytest.raises(AttributeError):
            self.file = QiniuFile('foo', self.storage, mode='rb')
            self.file.write("goto fail")

    def test_write_and_delete_file(self):
        ASSET_FILE_NAME = 'jquery-1.11.1.min.js'
        REMOTE_PATH = join(UNIQUE_PATH, ASSET_FILE_NAME)
        assert self.storage.exists(REMOTE_PATH) == False
        self.file = QiniuFile(REMOTE_PATH, self.storage, mode='wb')

        with open(join(dirname(__file__),'assets', ASSET_FILE_NAME), 'rb') as assset_file:
            content = assset_file.read()

            assset_file.seek(0, os.SEEK_END)
            assset_file_size = assset_file.tell()
            
            self.file.write(content)
            self.storage._save(REMOTE_PATH, self.file)
            
            assert self.storage.exists(REMOTE_PATH)

        assert self.storage.size(REMOTE_PATH) == assset_file_size

        time_delta = datetime.now() - self.storage.modified_time(REMOTE_PATH)
        assert time_delta.seconds < 60

        self.storage.delete(REMOTE_PATH)
        assert self.storage.exists(REMOTE_PATH) == False

    def test_read_file(self):
        ASSET_FILE_NAME = 'bootstrap.min.css'
        REMOTE_PATH = join(UNIQUE_PATH, ASSET_FILE_NAME)

        with open(join(dirname(__file__),'assets', ASSET_FILE_NAME), 'rb') as assset_file:
            self.storage.save(REMOTE_PATH, assset_file)

        self.file = self.storage.open(REMOTE_PATH, 'r')

        assert self.file._is_read == False

        content = self.file.read()
        assert content.startswith("/*!")

        assert self.file._is_read == True

    def test_dirty_file(self):
        ASSET_FILE_NAME = 'bootstrap.min.css'
        REMOTE_PATH = join(UNIQUE_PATH, ASSET_FILE_NAME)

        self.file = self.storage.open(REMOTE_PATH, 'rw')

        assert self.file._is_read == False
        assert self.file._is_dirty == False
        assert self.storage.exists(REMOTE_PATH) == False

        with open(join(dirname(__file__),'assets', ASSET_FILE_NAME), 'r') as assset_file:
            content = assset_file.read()
            self.file.write(content)

        assert self.file._is_read == True
        assert self.file._is_dirty == True

        self.file.close()
        assert self.storage.exists(REMOTE_PATH) == True

    def test_listdir(self):
        dirnames = ['', 'foo', 'bar']
        filenames = ['file1', 'file2', 'file3']
        for dirname in dirnames:
            for filename in filenames:
                fil = self.storage.open(join(UNIQUE_PATH, dirname, filename), 'w')
                fil.write('test text')
                fil.close()

        dirs, files = self.storage.listdir(UNIQUE_PATH)
        assert dirs == ['foo', 'bar']
        assert files == filenames

        dirs, files = self.storage.listdir(join(UNIQUE_PATH, 'foo'))
        assert dirs == []
        assert files == filenames

        for dirname in dirnames:
            for filename in filenames:
                self.storage.delete(join(UNIQUE_PATH, dirname, filename))
   
