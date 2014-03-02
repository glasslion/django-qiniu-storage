"""
Qiniu Storage Backends
"""
from __future__ import absolute_import
import datetime
import os
from urlparse import urljoin

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

import qiniu.conf
import qiniu.io
import qiniu.rs
import qiniu.rsf
import requests

from django.conf import settings
from django.core.files.base import File
from django.core.files.storage import Storage
from django.core.exceptions import ImproperlyConfigured

from .utils import bucket_lister


def get_qiniu_config(name):
    """
    Get configuration variable from environment variable
    or django setting.py
    """
    config = os.environ.get(name, settings.get(name, None))
    if config:
        return config
    else:
        raise ImproperlyConfigured(
            "Can't find config for '%s' either in environment"
            "variable or in setting.py" % name)


QINIU_ACCESS_KEY = get_qiniu_config('QINIU_ACCESS_KEY')
QINIU_SECRET_KEY = get_qiniu_config('QINIU_SECRET_KEY')
QINIU_BUCKET_NAME = get_qiniu_config('QINIU_BUCKET_NAME')
QINIU_BUCKET_DOMAIN = get_qiniu_config('QINIU_BUCKET_DOMAIN')


class QiniuStorage(Storage):
    """
    Qiniu Storage Service
    """
    def __init__(
            self,
            access_key=QINIU_ACCESS_KEY,
            secret_key=QINIU_SECRET_KEY,
            bucket_name=QINIU_BUCKET_NAME,
            bucket_domain=QINIU_BUCKET_DOMAIN):
        qiniu.conf.ACCESS_KEY = access_key
        qiniu.conf.SECRET_KEY = secret_key
        self.bucket_name = bucket_name
        self.put_policy = qiniu.rs.PutPolicy(self.bucket_name)
        self.bucket_domain = bucket_domain

    def _clean_name(self, name):
        if type(name) is unicode:
            return name.encode('utf-8')
        else:
            return name

    def _open(self, name, mode='rb'):
        return QiniuFile(name, self, mode)

    def _save(self, name, content):
        name = self._clean_name(name)
        ret, err = qiniu.io.put(self.put_policy.token(), name, content)
        content.close()
        if err:
            raise IOError(
                "Failed to save file '%s'. "
                "Error message: %s" % (name, err))
        return name

    def _read(self, name):
        return requests.get(self.url(name)).content

    def delete(self, name):
        name = self._clean_name(name)
        ret, err = qiniu.rs.Client().delete(self.bucket_name, name)
        if err:
            raise IOError(
                "Failed to delete file '%s'. "
                "Error message: %s" % (name, err))

    def _file_stat(self, name):
        name = self._clean_name(name)
        ret, err = qiniu.rs.Client().stat(self.bucket_name, name)
        if err:
            raise IOError(
                "Failed to get stats of file '%s'. "
                "Error message: %s" % (name, err))
        return ret

    def exists(self, name):
        stats = self._file_stat(name)
        return True if stats else False

    def size(self, name):
        stats = self._file_stat(name)
        return stats['fsize']

    def modified_time(self, name):
        stats = self._file_stat(name)
        time_stamp = float(stats['putTime'])/10000000
        return datetime.datetime.fromtimestamp(time_stamp)

    def listdir(self, name):
        name = self._clean_name(name)
        if name and not name.endswith('/'):
            name += '/'

        dirlist = bucket_lister(self.bucket_name)
        files = []
        dirs = set()
        base_parts = name.split("/")[:-1]
        for item in dirlist:
            parts = item.name.split("/")
            parts = parts[len(base_parts):]
            if len(parts) == 1:
                # File
                files.append(parts[0])
            elif len(parts) > 1:
                # Directory
                dirs.add(parts[0])
        return list(dirs), files

    def url(self, name):
        return urljoin(self.bucket_domain, name)


class QiniuFile(File):
    def __init__(self, name, storage, mode):
        self._name = name
        self._storage = storage
        self._mode = mode
        self.file = StringIO()
        self._is_dirty = False
        self._is_read = False

    @property
    def size(self):
        if not hasattr(self, '_size'):
            self._size = self._storage.size(self._name)
        return self._size

    def read(self, num_bytes=None):
        if not self._is_read:
            self.file = StringIO(self._storage._read(self._name))
            self._is_read = True
        return self.file.read(num_bytes)

    def write(self, content):
        if 'w' not in self._mode:
            raise AttributeError("File was opened for read-only access.")
        self.file.write(content)
        self._is_dirty = True
        self._is_read = True

    def close(self):
        if self._is_dirty:
            self._storage._put_file(self._name, self.file.getvalue())
        self.file.close()
