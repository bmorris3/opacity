import os
import xarray as xr
import zarr
from zarr.experimental.cache_store import CacheStore

from opacity.filesystem import s3_filesystem
from opacity.resolve_species import find_matching_maestro_zarr_prefix

__all__ = [
    "open_dataset",
]

default_cache_path = os.path.join(os.path.expanduser("~"), "opacities")


def open_dataset(
    species,
    cache=True,
    cache_path=None,
    fsspec_filesystem=None,
    local_cache_store=None,
    max_cache_size_gb=20.0,
):
    """Open an `~xarray.Dataset` for ``species``, and optionally cache
    downloads.

    Parameters
    ----------
    species : str
        Name of the atom or molecule
    cache : bool, optional
        On retrieving (all, or parts of) a remote array cache the
        result locally. Default is True,
    cache_path : str or None, optional
        If specified and ``cache=True``, the dataset will be cached
        in a zarr array located at ``cache_path``. Default is None.
    fsspec_filesystem : `~fsspec.filesystem`, optional
        Remote filesystem, with or without signed requests. Default is None.
    local_cache_store : `~zarr.storage.LocalStore`, optional
        User-defined local Zarr cache store. Default is None.
    max_cache_size_gb : float, optional
        Maximum Zarr array size cached in local memory. Default is 20.

    Returns
    -------
    `~xarray.Dataset`
        Opacity Dataset.

    Raises
    ------
    ValueError
        If ``species`` is None.
    """
    if species is None:
        raise ValueError(
            f'opacity.open_dataset requires a species, got {species}.'
        )

    zarr_s3_prefix = find_matching_maestro_zarr_prefix(species)

    # access to a remote S3 bucket as a file system
    if fsspec_filesystem is None:
        fsspec_filesystem = s3_filesystem()

    remote_store = zarr.storage.FsspecStore(
        fs=fsspec_filesystem,
        read_only=True,
        path=zarr_s3_prefix
    )

    if cache:
        # create local cache for reads from the remote array, give the
        # zarr array the same name as the remote zarr array
        zarr_name = zarr_s3_prefix.split('/')[-1]

        if local_cache_store is None:
            if cache_path is None:
                cache_path = os.path.join(default_cache_path, zarr_name)
            local_cache_store = zarr.storage.LocalStore(cache_path)

        # prepare a cache store that links the remote data to the local cache.
        # do not use >max_cache_size_gb GB of local memory towards the cache
        load_store = CacheStore(
            store=remote_store,
            cache_store=local_cache_store,
            max_size=max_cache_size_gb * 1024 ** 3
        )
    else:
        load_store = remote_store

    # open the dataset with zarr:
    ds = xr.open_dataset(load_store, engine='zarr')
    return ds
