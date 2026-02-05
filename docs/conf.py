# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

import datetime

# -- Project information -----------------------------------------------------

# The full version, including alpha/beta/rc tags
from opacity import __version__

release = __version__

project = "opacity"
author = "Brett Morris"
copyright = f"{datetime.datetime.now().year}, {author}"  # noqa: A001

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named "sphinx.ext.*") or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.inheritance_diagram",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.doctest",
    "sphinx.ext.mathjax",
    "sphinx_automodapi.automodapi",
    "sphinx_automodapi.smart_resolver",
    "matplotlib.sphinxext.plot_directive",
    "numpydoc",
]

# Add any paths that contain templates here, relative to this directory.
# templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# Treat everything in single ` as a Python reference.
default_role = 'py:obj'

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/objects.inv", None),
    'numpy': ("https://numpy.org/doc/stable/", None),
    'xarray': ("https://docs.xarray.dev/en/stable/", None),
    'zarr': ("https://zarr.readthedocs.io/en/stable/", None),
    'fsspec': ("https://filesystem-spec.readthedocs.io/en/latest/", None),
}

# -- Options for HTML output -------------------------------------------------
# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_book_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_logo = "assets/logo.png"
# html_favicon = "assets/logo.ico"

html_theme_options = {
    "use_download_button": True,
    "repository_url": "https://github.com/opacities/opacity",
    "repository_branch": "main",
    "path_to_docs": "docs",
}

numpydoc_show_class_members = False
autodoc_inherit_docstrings = True

html_context = {
    "display_github": True,
    "github_user": "opacities",
    "github_repo": "opacity",
    "github_version": "main",
    "conf_py_path": "docs/",
}

autosectionlabel_prefix_document = True
autoclass_content = 'both'

# -- Other options ----------------------------------------------------------
