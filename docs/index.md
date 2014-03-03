# Django Qiniu Storage

Django storage for [七牛云存储](http://www.qiniu.com/)

## Install

    pip install django-qiniu-storage

## Configurations

Django Qiniu Storage 需要以下几个配置才能正常工作。这些配置可以环境变量或 setting.py 来设置。环境变量的优先级要高于 setting.py 。

    QINIU_ACCESS_KEY

七牛给开发者分配的 AccessKey

    QINIU_SECRET_KEY
    
七牛给开发者分配的 Secret 

    QINIU_BUCKET_NAME
    
用来存放文件的七牛空间(bucket)的名字

    QINIU_BUCKET_DOMAIN
    
七牛空间(bucket)的域名

## Usage

在 setting.py 里设置 `DEFAULT_FILE_STORAGE` 和 STATICFILES_STORAGE

    DEFAULT_FILE_STORAGE = 'qiniustorage.backends.QiniuMediaStorage'
    STATICFILES_STORAGE  = 'qiniustorage.backends.QiniuStaticStorage'


若 storage 为 `qiniustorage.backends.QiniuStorage`, 文件将存放在bucket的根目录下

若 storage 为 `qiniustorage.backends.QiniuMediaStorage`, 文件将存放在bucket/MEDIA_ROOT目录下

若 storage 为 `qiniustorage.backends.QiniuStaticStorage`, 文件将存放在bucket/STATIC_ROOT目录下

## Documentation

It's hosted on the [Read The Doc](http://django-qiniu-storage.readthedocs.org/zh_CN/latest/
).

## Run Demo

    git clone django-qiniu-storage

    cd django-qiniu-storage/demo-project

    pip install -r demo_requirements.txt

    export DJANGO_SETTINGS_MODULE=settings
    export QINIU_ACCESS_KEY= YOUR KEY
    export QINIU_SECRET_KEY=YOUR KEY
    export QINIU_BUCKET_DOMAIN=YOUR BUCKET DOMAIN
    export QINIU_BUCKET_NAME=YOUR BUCKET NAME

    python manage.py python manage.py collectstatic

## License

基于MIT许可证发布
