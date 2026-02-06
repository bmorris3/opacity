import os
import pytest

import numpy as np
import zarr

from opacity import open_dataset


grid1460_pressure = np.array(
    [1.e-06, 3.e-06, 1.e-05, 3.e-05, 1.e-04, 3.e-04, 1.e-03, 3.e-03,
     1.e-02, 3.e-02, 1.e-01, 3.e-01, 1.e+00, 3.e+00, 1.e+01, 3.e+01,
     1.e+02, 3.e+02, 1.e+03, 3.e+03]
)

grid1460_temperature = np.array(
    [75., 100., 110., 120., 130., 140., 150., 160., 170.,
     180., 190., 200., 210., 220., 230., 240., 250., 260.,
     270., 275., 280., 290., 300., 310., 320., 330., 340.,
     350., 375., 400., 425., 450., 475., 500., 525., 550.,
     575., 600., 650., 700., 750., 800., 850., 900., 950.,
     1000., 1100., 1200., 1300., 1400., 1500., 1600., 1700., 1800.,
     1900., 2000., 2100., 2200., 2300., 2400., 2500., 2600., 2700.,
     2800., 2900., 3000., 3100., 3200., 3300., 3400., 3500., 3750.,
     4000.]
)


@pytest.mark.remote_data
@pytest.mark.parametrize(
    "species, coord, expected, set_local_cache_store,", [
        ('H2O', 'temperature', grid1460_temperature, True),
        ('H2O', 'pressure', grid1460_pressure, False),
        ('VO', 'temperature', grid1460_temperature, True),
        ('VO', 'pressure', grid1460_pressure, False),
    ]
)
def test_open_dataset_cache_coordinates(
    tmpdir, species, coord, expected, set_local_cache_store
):
    tmp_path = os.path.join(tmpdir, species + '.zarr')

    if set_local_cache_store:
        local_cache_store = zarr.storage.LocalStore(tmp_path)
    else:
        local_cache_store = None

    ds = open_dataset(
        species=species,
        cache_path=tmp_path,
        local_cache_store=local_cache_store,
        max_cache_size_gb=1e-3
    )
    assert all(ds[coord] == expected)


@pytest.mark.remote_data
@pytest.mark.parametrize(
    "species, coord, expected", [
        ('H2O', 'temperature', grid1460_temperature),
        ('H2O', 'pressure', grid1460_pressure),
        ('VO', 'temperature', grid1460_temperature),
        ('VO', 'pressure', grid1460_pressure),
    ]
)
def test_open_dataset_nocache_coordinates(tmpdir, species, coord, expected):
    ds = open_dataset(
        species=species,
        cache=False,
        max_cache_size_gb=1e-3
    )
    assert all(ds[coord] == expected)


def test_open_dataset_no_species(tmpdir, species=None):
    with pytest.raises(
        ValueError,
        match="opacity.open_dataset requires a species*"
    ):
        _ = open_dataset(
            species=species,
            cache=False,
            max_cache_size_gb=1e-3
        )
