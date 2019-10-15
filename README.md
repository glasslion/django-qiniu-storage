# Django Qiniu Storage

[![Build Status](https://travis-ci.org/glasslion/django-qiniu-storage.svg?branch=master)](https://travis-ci.org/glasslion/django-qiniu-storage)

### Django storage for [七牛云存储](http://www.qiniu.com/)

## 安装

    pip install django-qiniu-storage

## 配置及使用指南

### 什么是 Django Storage ?
Django Storage System 是 Django 框架对文件存储系统做的一层抽象。由于 Django 为不同的存储系统抽象出了一套相同的文件读写接口， Django 应用可以轻松地将其文件存储载体替换为本地文件系统, AWS S3, Openstack, Azue, Mongodb 或者是 国内的七牛云存储， 又拍云， 阿里云 ， 而无需改动应用层代码。

如果你对 Django 的 Storage 系统尚不熟悉的话，建议你首先阅读下 Django 的这几篇官方文档:
- [Managing files](https://docs.djangoproject.com/en/1.7/topics/files/)
- [Managing static files](https://docs.djangoproject.com/en/1.7/howto/static-files/)
- [The staticfiles app](https://docs.djangoproject.com/en/1.7/ref/contrib/staticfiles/)

这些都是很不错的阅读材料。 在了解一些基本的概念和配置项的含义后，再来看本教程接下来有关具体配置的内容。

### 怎样配置 Django Storage ?
Django 和 storage 相关的 [settings](https://docs.djangoproject.com/en/dev/ref/settings/) 有两项: `STATICFILES_STORAGE`  和 `DEFAULT_FILE_STORAGE` 分别对应*网站自身的js, css, 图片等静态资源* 和*用户上传的文件*.

以 `DEFAULT_FILE_STORAGE` 为例, 它的默认值是 `django.core.files.storage.FileSystemStorage`， 即 storage class 的路径。要换成七牛的话， 改成 `qiniustorage.backends.QiniuStorage` 就行了。

```python
from qiniustorage.backends import QiniuStorage

class MyQiniuStorage(QiniuStorage):
    access_key = os.environ['QINIU_ACCESS_KEY'] # 强烈建议不要在代码里写死 等敏感信息
    secret_key = os.environ['QINIU_SECRET_KEY']
    bucket_domain = 'xxxxx'

DEFAULT_FILE_STORAGE = MyQiniuStorage
```

#### 用例1： 只用七牛托管动态生成的文件（例如用户上传的文件）

在 settings.py 里设置 `DEFAULT_FILE_STORAGE` :

    DEFAULT_FILE_STORAGE = 'qiniustorage.backends.QiniuStorage'

#### 用例2： 用七牛托管动态生成的文件以及站点自身的静态文件（相当于 CDN）
首先，检查你的 `INSTALLED_APPS` setting， 确保安装了 `django.contrib.staticfiles` 这个 app。

`staticfiles`  提供了一个名为 `collectstatic` 的命令。 它会收集各个 app 的根目录下的 `static` 子目录下的文件， 并汇总到一个地方。如果将 django settings 里的 `STATICFILES_STORAGE` 设置为  `QiniuStorage`，`collectstatic` 收集到的静态文件就会被统一上传到七牛。

## 从 2.X 升级到 3.X 版的说明
在 2.X 及以下的版本中，  Django Qiniu Storage 默认是通过环境变量来进行一些七牛的参数(例如 access key, bucket name)配置。 这种做法主要是参考了在 Django 社区里十分流行的， 由 Heroku 首倡的 [The Twelve-Factor App](https://12factor.net/) 规范。 2.X 版本里具体的环境变量可以见下表。

| Django Settings / Environment Variable | 说明                                 |
|----------------------------------------|--------------------------------------|
| QINIU_ACCESS_KEY                       | 七牛给开发者分配的 AccessKey         |
| QINIU_SECRET_KEY                       | 七牛给开发者分配的 Secret            |
| QINIU_BUCKET_NAME                      | 用来存放文件的七牛空间(bucket)的名字 |
| QINIU_BUCKET_DOMAIN                    | 七牛空间(bucket)的域名               |
| QINIU_SECURE_URL                       | 是否通过 HTTPS 来访问七牛云存储上的资源(若为'是', 可填True, true 或 1；若为'否', 可填False, false 或 0) 默认为否。|

注 1: Django Qiniu Storage 配置既可以通过环境变量, 也可以通过在 settings.py 里设置同名变量来设置。环境变量的优先级要高于 settings.py 。
注 2: 关于 HTTPS域名配置的详情， 可以参考七牛官方文档 [如何通过 SSL 的形式来访问七牛云存储上的资源](http://kb.qiniu.com/https-support)


然而在一些我当初没有意料到的场景下， 通过预先设定的环境变量来进行配置会变得比较不方便。 这主要是因为不同的用户使用 Django Qiniu Storage 的方式是不一样的：

- 有些用户只是用七牛托管静态文件， 例如 js, css, 图片之类的网站自身的资源， 对应的需要设置 Django 的 `STATICFILES_STORAGE` 设置。
- 有些用户只是用七牛托管用户上传的文件，对应的需要设置 Django 的 `DEFAULT_FILE_STORAGE` 设置。
- 有些用户会同时用七牛托管静态文件和用户上传的文件， 两者分别上传到同一个 bucket 的不同目录下( 例如 /static 和 /media )。
- 有些用户出于安全和其他因素考虑， 希望静态文件和用户上传的文件使用不同的 bucket, 甚至是使用不同的七牛账号。
- 有些用户希望 用户上传的文件不能被公开下载，需要被授权才能下载

...

当使用者需要在一个 Django 应用里使用多个配置不同的 QiniuStorage 实例时， 预先设定的哪些环境变量就不能满足需求了。 
**注意**, 



我在 3.X

## Read The Doc

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
