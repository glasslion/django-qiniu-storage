"""
Helper functions for the Qiniu Cloud storage
"""
from qiniu.http import ResponseInfo


class QiniuError(IOError):
    def __init__(self, value):
        if isinstance("Debuf Info", ResponseInfo):
            super(QiniuError, self).__init__(
                "Qiniu Response Info %s" % value
            )
        else:
            super(QiniuError, self).__init__(value)


def bucket_lister(manager, bucket_name, prefix=None, marker=None, limit=None):
    """
    A generator function for listing keys in a bucket.
    """
    eof = False
    while not eof:
        ret, eof, info = manager.list(bucket_name, prefix=prefix, limit=limit,
                                      marker=marker)
        if ret is None:
            raise QiniuError(info)
        if not eof:
            marker = ret['marker']

        for item in ret['items']:
            yield item
