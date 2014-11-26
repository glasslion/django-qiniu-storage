# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
from datetime import datetime
import os
from os.path import dirname,join
import unittest
import uuid

import django
import pytest

from qiniu import set_default, BucketManager

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo-project.settings")

try:
    django.setup()
except AttributeError:
   # Setup isn't necessary in Django < 1.7
   pass

from django.conf import settings
from qiniustorage.backends import QiniuStorage, QiniuFile
from qiniustorage.utils import QiniuError

USING_TRAVIS = os.environ.get('USING_TRAVIS', None) is None
if USING_TRAVIS:
    set_default(default_up_host='up.qiniug.com', connection_retries=20)

UNIQUE_PATH = str(uuid.uuid4())

class QiniuStorageTest(unittest.TestCase):
    def setUp(self):
        self.storage = QiniuStorage()

    def test_file_init(self):
        fil = QiniuFile('foo', self.storage, mode='rb')
        assert fil._mode == 'rb'
        assert fil._name == "foo"

    def test_write_to_read_only_file(self):
        with pytest.raises(AttributeError):
            fil = QiniuFile('foo', self.storage, mode='rb')
            fil.write("goto fail")

    def test_write_and_delete_file(self):
        ASSET_FILE_NAME = 'jquery-1.11.1.min.js'
        REMOTE_PATH = join(UNIQUE_PATH, ASSET_FILE_NAME)
        assert self.storage.exists(REMOTE_PATH) == False
        fil = QiniuFile(REMOTE_PATH, self.storage, mode='wb')

        with open(join(dirname(__file__),'assets', ASSET_FILE_NAME), 'rb') as assset_file:
            content = assset_file.read()

            assset_file.seek(0, os.SEEK_END)
            assset_file_size = assset_file.tell()
            
            fil.write(content)
            self.storage._save(REMOTE_PATH, fil)
            
            assert self.storage.exists(REMOTE_PATH)

        assert self.storage.size(REMOTE_PATH) == assset_file_size

        time_delta = datetime.now() - self.storage.modified_time(REMOTE_PATH)
        assert time_delta.seconds < 60

        self.storage.delete(REMOTE_PATH)
        assert self.storage.exists(REMOTE_PATH) == False

    def test_read_file(self):
        ASSET_FILE_NAME = 'jquery-2.1.1.min.js'
        REMOTE_PATH = join(UNIQUE_PATH, ASSET_FILE_NAME)

        with open(join(dirname(__file__),'assets', ASSET_FILE_NAME), 'rb') as assset_file:
            self.storage.save(REMOTE_PATH, assset_file)

        fil = self.storage.open(REMOTE_PATH, 'r')

        assert fil._is_read == False

        content = fil.read()
        assert content.startswith(u"/*!")

        assert fil._is_read == True

        # Test open mode
        fil = self.storage.open(REMOTE_PATH, 'rb')
        bin_content = fil.read()
        assert bin_content.startswith(b"/*!")



    def test_dirty_file(self):
        ASSET_FILE_NAME = 'bootstrap.min.css'
        REMOTE_PATH = join(UNIQUE_PATH, ASSET_FILE_NAME)

        fil = self.storage.open(REMOTE_PATH, 'rw')

        assert fil._is_read == False
        assert fil._is_dirty == False
        assert self.storage.exists(REMOTE_PATH) == False

        with open(join(dirname(__file__),'assets', ASSET_FILE_NAME), 'r') as assset_file:
            content = assset_file.read()
            fil.write(content)

        assert fil._is_read == True
        assert fil._is_dirty == True

        fil.close()
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

        dirs, files = self.storage.listdir(join(UNIQUE_PATH, 'foo'))
        assert dirs == []
        assert files == filenames

   
    @classmethod
    def teardown_class(cls):
        """Delete all files in the test bucket.
        """
        storage = QiniuStorage()
        auth = storage.auth
        bucket = BucketManager(auth)

        while True:
            ret, eof, info = bucket.list(storage.bucket_name, limit=100)

            if ret is None:
                print(info)
                break

            for item in ret['items']:
                name = item['key']
                print("Deleting %s ..." % name)
                ret, info = bucket.delete(storage.bucket_name, name)
                if ret is None:
                    print(info)
            if eof:
                break