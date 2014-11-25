"""
Helper functions for the Qiniu Cloud storage
"""


def bucket_lister(manager, bucket_name, prefix=None, marker=None, limit=None):
    """
    A generator function for listing keys in a bucket.
    """
    eof = False 
    while not eof:
        ret, eof, info = manager.list(bucket_name, prefix=prefix, limit=limit,
                                    marker=marker)
        if ret is None:
            raise IOError("Failed to list bucket '%s'. "
                          "Error message: %s" % (bucket_name, err))
        if not eof:
            marker = ret['marker']

        for item in ret['items']:
            yield item