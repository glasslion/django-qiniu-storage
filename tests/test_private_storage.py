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
from requests.exceptions import ConnectionError

from qiniu import BucketManager

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
from qiniustorage.backends import QiniuPrivateStorage, QiniuFile, get_qiniu_config
from qiniustorage.utils import QiniuError

USING_TRAVIS = os.environ.get('USING_TRAVIS', None) is None

UNIQUE_PATH = str(uuid.uuid4())


class QiniuStorageTest(unittest.TestCase):
    def setUp(self):
        self.storage = QiniuPrivateStorage(
            bucket_name=get_qiniu_config('QINIU_PRIVATE_BUCKET_NAME'),
            bucket_domain=get_qiniu_config('QINIU_PRIVATE_BUCKET_DOMAIN'),
        )

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

    @classmethod
    def teardown_class(cls):
        """Delete all files in the test bucket.
        """
        storage = QiniuPrivateStorage(
            bucket_name=get_qiniu_config('QINIU_PRIVATE_BUCKET_NAME'),
            bucket_domain=get_qiniu_config('QINIU_PRIVATE_BUCKET_DOMAIN'),
        )
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
