# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, print_function
from datetime import datetime
import os
from os.path import dirname, join
import sys
import time
import unittest
import uuid

import logging
LOGGING_FORMAT = '\n%(levelname)s %(asctime)s %(message)s'
logging.basicConfig(level=logging.INFO, format=LOGGING_FORMAT)
logger = logging.getLogger(__name__)

import six
import django
import pytest
from requests.exceptions import ConnectionError


from qiniu import set_default, BucketManager, Zone

zone_overseas = Zone('up.qiniug.com', 'upload.qiniug.com')



from .utils import retry


# Add repo/demo_site to sys.path
DEMO_SITE_DIR = join(dirname(dirname(__file__)), 'demo_site')
sys.path.append(DEMO_SITE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo_site.settings")

try:
    django.setup()
except AttributeError:
   # Setup isn't necessary in Django < 1.7
   pass

from django.conf import settings
from qiniustorage.backends import QiniuStorage, QiniuFile
from qiniustorage.utils import QiniuError

USING_TRAVIS = os.environ.get('USING_TRAVIS', None) is None

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
        ASSET_FILE_NAMES = [u'Write&Deltete.txt', u'写和删.txt']
        for assert_file_name in ASSET_FILE_NAMES:
            REMOTE_PATH = join(UNIQUE_PATH, assert_file_name)

            assert self.storage.exists(REMOTE_PATH) == False
            fil = QiniuFile(REMOTE_PATH, self.storage, mode='wb')

            content = u"你好世界 Hello World"

            # get file size
            dummy_file = six.BytesIO()
            dummy_file.write(content.encode('utf-8'))
            dummy_file.seek(0, os.SEEK_END)
            file_size = dummy_file.tell()

            fil.write(content)
            self.storage._save(REMOTE_PATH, fil)

            assert self.storage.exists(REMOTE_PATH)

            assert self.storage.size(REMOTE_PATH) == file_size

            now = datetime.utcnow()
            modified_time = self.storage.modified_time(REMOTE_PATH)
            # Datetime on Qiniu servers may be faster or slower than the local
            # machine. Thus the absolute delta within 60s should be considered
            # acceptable.
            time_delta = max(now, modified_time) - min(now, modified_time)
            assert time_delta.seconds < 180

            self.storage.delete(REMOTE_PATH)
            assert self.storage.exists(REMOTE_PATH) == False

    @retry(ConnectionError,tries=10, backoff=1, logger=logger)
    def test_read_file(self):
        ASSET_FILE_NAMES =  [u'Read.txt', u'读.txt']
        for assert_file_name in ASSET_FILE_NAMES:
            REMOTE_PATH = join(UNIQUE_PATH, assert_file_name)

            test_file = six.BytesIO()
            test_file.write(u"你好世界 Hello World".encode('utf-8'))
            test_file.seek(0)
            self.storage.save(REMOTE_PATH, test_file)

            fil = self.storage.open(REMOTE_PATH, 'r')

            assert fil._is_read == False

            content = fil.read()
            assert content.startswith(u"你好")

            assert fil._is_read == True

            # Test open mode
            fil = self.storage.open(REMOTE_PATH, 'rb')
            bin_content = fil.read()
            assert bin_content.startswith(u"你好".encode('utf-8'))

    def test_dirty_file(self):
        ASSET_FILE_NAME = u'测试脏文件.txt'
        REMOTE_PATH = join(UNIQUE_PATH, ASSET_FILE_NAME)

        fil = self.storage.open(REMOTE_PATH, 'rw')

        assert fil._is_read == False
        assert fil._is_dirty == False
        assert self.storage.exists(REMOTE_PATH) == False

        fil.write("Hello World.")

        assert fil._is_read == True
        assert fil._is_dirty == True

        fil.close()
        assert self.storage.exists(REMOTE_PATH) == True


    @retry(QiniuError, tries=10, backoff=1, logger=logger)
    def test_listdir(self):
        dirnames = ['', 'foo', 'bar']
        filenames = ['file1', 'file2', 'file3', u'file四']
        for dirname in dirnames:
            for filename in filenames:
                fil = self.storage.open(join(UNIQUE_PATH, dirname, filename), 'w')
                fil.write('test text')
                fil.close()
        time.sleep(3)

        dirs, files = self.storage.listdir(UNIQUE_PATH)
        assert sorted(dirs) == sorted(['foo', 'bar'])

        dirs, files = self.storage.listdir(join(UNIQUE_PATH, 'foo'))
        assert dirs == []
        assert sorted(files) == sorted(filenames)


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
                if six.PY2:
                    name = name.encode('utf-8')
                ret, info = bucket.delete(storage.bucket_name, name)
                if ret is None:
                    print(info)
            if eof:
                break
