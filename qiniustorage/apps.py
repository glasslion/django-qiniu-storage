from django.apps import AppConfig
from django.core.checks import register


class QiniuStorageConfig(AppConfig):
    name = 'qiniustorage'

    def ready(self):
        from qiniustorage.checks import check_storage_settings
        register(check_storage_settings, "QiniuStorageCheck")
