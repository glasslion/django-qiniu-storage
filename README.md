# Django Qiniu Storage

[![Build Status](https://travis-ci.org/glasslion/django-qiniu-storage.svg?branch=master)](https://travis-ci.org/glasslion/django-qiniu-storage)

### Django storage for [七牛云存储](http://www.qiniu.com/)

## 安装

    pip install django-qiniu-storage

## 配置

Django Qiniu Storage 需要以下几个配置才能正常工作。这些配置通过可以环境变量或 settings.py 来设置。环境变量的优先级要高于 settings.py 。

| Django Settings / Environment Variable | 说明                                 |
|----------------------------------------|--------------------------------------|
| QINIU_ACCESS_KEY                       | 七牛给开发者分配的 AccessKey         |
| QINIU_SECRET_KEY                       | 七牛给开发者分配的 Secret            |
| QINIU_BUCKET_NAME                      | 用来存放文件的七牛空间(bucket)的名字 |
| QINIU_BUCKET_DOMAIN                    | 七牛空间(bucket)的域名               |
| QINIU_SECURE_URL                       | 是否通过 HTTPS 来访问七牛云存储上的资源(若为'是', 可填True, true 或 1；若为'否', 可填False, false 或 0) 默认为否。|

关于 HTTPS域名配置的详情， 可以参考七牛官方文档 [如何通过 SSL 的形式来访问七牛云存储上的资源](http://kb.qiniu.com/https-support)

## 使用指南

### Django Storage 入门
Django Storage System 是 Django 框架对文件存储系统做的一层抽象。由于不同的 storage system 使用同样的文件读写接口， Django 应用可以轻松地将其文件存储载体替换为本地文件系统, AWS S3, Openstack, Azue, Mongodb 或七牛云存储 ， 而无需改动应用代码。

如果你对 Django 的 Storage 系统尚不熟悉的话， Django 官方文档中的这几篇: [Managing files](https://docs.djangoproject.com/en/1.7/topics/files/), [Managing static files](https://docs.djangoproject.com/en/1.7/howto/static-files/), [The staticfiles app](https://docs.djangoproject.com/en/1.7/ref/contrib/staticfiles/) 都是很不错的阅读材料。 建议阅读完后，了解一些基本的概念和配置项的含义后，再来看本教程接下来的内容。

Django 和 storage 相关的 [settings](https://docs.djangoproject.com/en/dev/ref/settings/) 有两项: `STATICFILES_STORAGE`  和 `DEFAULT_FILE_STORAGE` 分别对应*网站自身的js, css, 图片等静态资源* 和*用户上传的文件*.


#### 用例1： 只用七牛托管动态生成的文件（例如用户上传的文件）

在 settings.py 里设置 `DEFAULT_FILE_STORAGE` :

    DEFAULT_FILE_STORAGE = 'qiniustorage.backends.QiniuStorage'

#### 用例2： 用七牛托管动态生成的文件以及站点自身的静态文件（相当于 CDN）
首先，检查你的 `INSTALLED_APPS` setting， 确保安装了 `django.contrib.staticfiles` 这个 app。

`staticfiles`  提供了一个名为 `collectstatic` 的命令。 它会收集各个 app 的根目录下的 `static` 子目录下的文件， 并汇总到一个地方。如果将 django settings 里的 `STATICFILES_STORAGE` 设置为  `QiniuStorage`，`collectstatic` 收集到的静态文件就会被统一上传到七牛。



## Documentation

It's hosted on the [Read The Doc](http://django-qiniu-storage.readthedocs.org/zh_CN/latest/
).

## Changelog

- 2.0.0 使用 7.x 版本的 Python SDK。同时支持 Python 2 和 Python 3， 但也因此不再支持 Django 1.4。
- 新建 ”1.x“ 分支。 今后主分支将使用 7.x 版本的 Python SDK。2.x 会同时支持 Python 2 和 Python 3。
- 1.2.0 主要是测试方面的改进。利用 Travic CI 对 (Python 2.6, 2.7)×( Django 1.4 -1.7) 的每个组合都跑一遍单元测试。
- 1.1.0 加上了比较完整的单元测试。Django 1.7 相关的 bug fix.
- 1.0.1 Bug fix. 使用 6.x 版本的 七牛 Python SDK.

## License

基于MIT许可证发布
