import os
import fsspec

import xarray as xr

import zarr
from zarr.experimental.cache_store import CacheStore

from opacity.filesystem import s3_filesystem
from opacity.resolve_species import find_matching_maestro_zarr_prefix

__all__ = [
    "open_dataset",
]


def open_dataset(
    species,
    fsspec_filesystem=None,
    local_cache_store=None,
    max_cache_size_gb=20.0,
):
    if species is None:
        raise ValueError(f'opacity.open requires a species, got {species}.')

    zarr_s3_prefix = find_matching_maestro_zarr_prefix(species)

    # access to a remote S3 bucket as a file system
    if fsspec_filesystem is None:
        fsspec_filesystem = s3_filesystem()

    remote_store = zarr.storage.FsspecStore(
        fs=fsspec_filesystem,
        read_only=True,
        path=zarr_s3_prefix
    )

    # create local cache for reads from the remote array, give the zarr array
    # the same name as the remote zarr array

    zarr_name = zarr_s3_prefix.split('/')[-1]

    if local_cache_store is None:
        local_cache_store = zarr.storage.LocalStore(zarr_name)

    # prepare a cache store that links the remote data to the local cache.
    # do not use >20 GB of local memory towards the cache
    cache = CacheStore(
        store=remote_store,
        cache_store=local_cache_store,
        max_size=max_cache_size_gb * 1024 ** 3
    )

    # open the dataset with zarr:
    ds = xr.open_dataset(cache, engine='zarr')
    return ds
