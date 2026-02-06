import pytest
from opacity import get_available_datasets


@pytest.mark.remote_data
@pytest.mark.parametrize(
    "zarr_name,",
    [
        ('CaH.zarr',), ('H2O.zarr',), ('TiO.zarr',)
    ]
)
def test_available_datsets(zarr_name):
    dataset_prefixes = get_available_datasets()
    assert any(prefix.endswith(zarr_name) for prefix in dataset_prefixes)
