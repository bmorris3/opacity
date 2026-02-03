import fsspec

__all__ = [
    's3_filesystem',
    'get_available_datasets'
]

maestro_s3_prefix = "s3://stpubdata/mast/hlsp/maestro/"


def s3_filesystem(anon=True, asynchronous=True):
    return fsspec.filesystem('s3', anon=anon, asynchronous=asynchronous)


def get_available_datasets():
    fs = s3_filesystem(asynchronous=False)
    objects = fs.ls(maestro_s3_prefix)
    zarrs = [obj for obj in objects if obj.endswith('.zarr')]
    return zarrs
