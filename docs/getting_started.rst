
Getting started
===============

.. code-block:: python

    import opacity
    import matplotlib.pyplot as plt

    dataset = opacity.open_dataset('VO')

    select = dict(
        temperature=750,  # [K]
        pressure=1e-5     # [bar]
    )
    cross_section = dataset.cross_section.sel(select)
    metadata = cross_section.attrs

    fig, ax = plt.subplots(figsize=(10, 5), dpi=300)
    ax.loglog(ds.wavenumber, cross_section)

    title = (
        f"{metadata['molecule']}, "
        f"T={select['temperature']} {cross_section.temperature.unit}, "
        f"P={select['pressure']} {cross_section.pressure.unit}"
    )

    ax.set(
        ylim=(1e-40, 1e-10),
        xlabel=f"Wavenumber [{cross_section.wavenumber.attrs['unit']}]",
        ylabel=f"Cross section [{metadata['unit']}]",
        title=title
    )