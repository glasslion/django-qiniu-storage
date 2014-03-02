"""
Helper functions for the Qiniu Cloud storage
"""
import qiniu.rsf


def bucket_lister(bucket_name, prefix=None, marker=None, limit=None):
    """
    A generator function for listing keys in a bucket.
    """
    rs = qiniu.rsf.Client()
    err = None
    while err is None:
        ret, err = rs.list_prefix(bucket_name, prefix=prefix, limit=limit,
                                  marker=marker)
        marker = ret.get('marker', None)
        for item in ret['items']:
            yield item

    if err is not qiniu.rsf.EOF:
        raise IOError("Failed to list bucket '%s'. "
                      "Error message: %s" % (bucket_name, err))
