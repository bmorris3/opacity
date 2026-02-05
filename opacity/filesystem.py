import fsspec

__all__ = [
    's3_filesystem',
    'get_available_datasets'
]

maestro_s3_prefix = "s3://stpubdata/mast/hlsp/maestro/"


def s3_filesystem(anon=True, asynchronous=True, **kwargs):
    """Return an `~fsspec.filesystem` for S3.

    Parameters
    ----------
    anon : bool, optional
        Anonymous access to public data.
    asynchronous : bool, optional
        Asynchronous access.

    Returns
    -------
    `~fsspec.filesystem`
        Python API for access to objects in S3 buckets.
    """
    return fsspec.filesystem(
        's3',
        anon=anon,
        asynchronous=asynchronous,
        **kwargs
    )


def get_available_datasets():
    """List available datasets in the MAESTRO S3 holdings.

    Returns
    -------
    list of str
        Available (remote) Zarr arrays stored in S3.
    """
    fs = s3_filesystem(asynchronous=False)
    objects = fs.ls(maestro_s3_prefix)
    zarrs = [obj for obj in objects if obj.endswith('.zarr')]
    return zarrs
