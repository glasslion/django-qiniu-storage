Django Qiniu Storage
====================

Django storage for `七牛云存储 <http://www.qiniu.com/>`__

Install
-------

::

    pip install django-qiniu-storage

Configurations
--------------

Django Qiniu Storage
需要以下几个配置才能正常工作。这些配置通过可以环境变量或 setting.py
来设置。环境变量的优先级要高于 setting.py 。

::

    QINIU_ACCESS_KEY

七牛给开发者分配的 AccessKey

::

    QINIU_SECRET_KEY

七牛给开发者分配的 Secret

::

    QINIU_BUCKET_NAME

用来存放文件的七牛空间(bucket)的名字

::

    QINIU_BUCKET_DOMAIN

七牛空间(bucket)的域名

Usage
-----

在 setting.py 里设置 ``DEFAULT_FILE_STORAGE`` 为
``qiniustorage.backends.QiniuStorage``

::

    DEFAULT_FILE_STORAGE = 'qiniustorage.backends.QiniuStorage'

Documentation
-------------

It's hosted on the `Read The
Doc <http://django-qiniu-storage.readthedocs.org/zh_CN/latest/>`__.

Changelog
---------

-  1.1.0 加上了比较完整的单元测试。Django 1.7 相关的 bug fix.
-  1.0.1 Bug fix. 使用 6.x 版本的 七牛 Python SDK.

License
-------

基于MIT许可证发布
