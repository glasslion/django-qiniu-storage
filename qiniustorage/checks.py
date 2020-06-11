from django.core.checks import Critical
from django.conf import settings


def check_storage_settings(app_configs, **kwargs):
    errors = []

    for storage_settings in ["DEFAULT_FILE_STORAGE", "STATICFILES_STORAGE"]:
        qiniu_storage_in_use = getattr(settings, storage_settings, "").startswith("qiniustorage")
        if qiniu_storage_in_use:
            break
    else:
        return []

    try:
        import qiniustorage.backends

        # from qiniustorage.backends import (
        #     QINIU_ACCESS_KEY,  QINIU_SECRET_KEY,  QINIU_BUCKET_NAME,
        #     QINIU_BUCKET_DOMAIN,  QINIU_SECURE_URL)
    except Exception as e:
        errors.append(
            Critical(
                msg="%s: %s" % (type(e).__name__, str(e)),
                id="qiniu_storage.E001")
        )
    return errors

# raise RuntimeError()
