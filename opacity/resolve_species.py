from opacity.filesystem import get_available_datasets

__all__ = [
    'find_matching_maestro_zarr_prefix'
]


def find_matching_maestro_zarr_prefix(species):
    """
    Get the S3 prefix for an exact species name match in the MAESTRO datasets.

    Parameters
    ----------
    species : str
        Unique name of a species in available datasets from MAESTRO.

    Returns
    -------
    prefix : str
        The S3 prefix to the dataset with an exact species name match.

    Raises
    ------
    ValueError
        If no exact prefix match is found for the species.
    """
    datasets = get_available_datasets()

    available_species_names = []
    for prefix in datasets:
        # remove prefix up to zarr path, then remove extension
        zarr_name = prefix.split('/')[-1].split('.zarr')[0]
        available_species_names.append(zarr_name)
        if zarr_name == species:
            return prefix
    else:
        raise ValueError(
            f"No matching MAESTRO opacity array found for {species}. "
            f"Available species include: {available_species_names}"
        )
