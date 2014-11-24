import os
import random
import string

import qiniu.conf
import qiniu.io
import qiniu.rs
import qiniu.rsf


QINIU_ACCESS_KEY = os.environ.get('QINIU_ACCESS_KEY')
QINIU_SECRET_KEY = os.environ.get('QINIU_SECRET_KEY')
QINIU_BUCKET_NAME = os.environ.get('QINIU_BUCKET_NAME')
QINIU_BUCKET_DOMAIN = os.environ.get('QINIU_BUCKET_DOMAIN')

qiniu.conf.ACCESS_KEY = QINIU_ACCESS_KEY
qiniu.conf.SECRET_KEY = QINIU_SECRET_KEY

QINIU_PUT_POLICY= qiniu.rs.PutPolicy(QINIU_BUCKET_NAME)

def test_put_file():
    token = QINIU_PUT_POLICY.token()
    text = "".join( [random.choice(string.letters) for i in xrange(200)])
    print "Test text: %s" % text
    ret, err = qiniu.io.put(token, text[:10], text)
    if err:
        raise IOError(
            "Error message: %s" % err)