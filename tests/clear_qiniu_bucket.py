import os
from qiniu import Auth, BucketManager


QINIU_ACCESS_KEY = os.environ.get('QINIU_ACCESS_KEY')
QINIU_SECRET_KEY = os.environ.get('QINIU_SECRET_KEY')
QINIU_BUCKET_NAME = os.environ.get('QINIU_BUCKET_NAME')
QINIU_BUCKET_DOMAIN = os.environ.get('QINIU_BUCKET_DOMAIN')


def main():
    auth = Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)
    bucket = BucketManager(auth)

    while True:
        ret, eof, info = bucket.list(QINIU_BUCKET_NAME, limit=100)

        if ret is None:
            print("==ret is None: %s==", str(info))
            break

        for item in ret['items']:
            name = item['key']
            print("Deleting %s ..." % name)
            _ret, _info = bucket.delete(QINIU_BUCKET_NAME, name)
            if _ret is None:
                print("    ---%s---" % str(_info))
        if eof:
            break


if __name__ == '__main__':
    main()
