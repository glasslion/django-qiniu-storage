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
            print info
            break

        for item in ret['items']:
            name = item['key']
            print "Deleting %s ..." % name
            ret, info = bucket.delete(QINIU_BUCKET_NAME, name)
            if ret is None:
                print info
        if eof:
            break


if __name__ == '__main__':
    main()
