import pytest
from opacity.resolve_species import find_matching_maestro_zarr_prefix


@pytest.mark.remote_data
@pytest.mark.parametrize(
    "species, prefix, ",
    [
        ("VO", "stpubdata/mast/hlsp/maestro/VO.zarr"),
        ("H2O", "stpubdata/mast/hlsp/maestro/H2O.zarr")
    ]
)
def test_matching_prefix(species, prefix):
    assert prefix == find_matching_maestro_zarr_prefix(species)


def test_bad_species_name():
    species = 'MAESTRO'  # doesn't exist

    with pytest.raises(ValueError, match="No matching MAESTRO opacity*"):
        find_matching_maestro_zarr_prefix(species)
