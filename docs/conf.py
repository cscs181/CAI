# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys

sys.path.insert(0, os.path.abspath(".."))

if os.getenv("READTHEDOCS"):
    import subprocess

    requirements_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "requirements.txt"
    )
    prog = subprocess.run(
        f"{sys.executable} -m pip install poetry &&"
        f"{sys.executable} -m poetry export -o {requirements_path} --dev --without-hashes &&"
        f"{sys.executable} -m pip install -r {requirements_path}",
        shell=True,
    )
    assert prog.returncode == 0

# -- Project information -----------------------------------------------------

project = "cai"
copyright = "2021, cscs181"
author = "cscs181"

# The full version, including alpha/beta/rc tags
release = "0.1.0"
language = "zh_CN"

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
import sphinx_rtd_theme

extensions = [
    "sphinxcontrib.napoleon",
    "sphinx_rtd_theme",
    "recommonmark",
    "sphinx_copybutton",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
html_theme_options = {"logo_only": True, "collapse_navigation": False}
html_logo = "assets/logo_text_white.png"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# -- Options for autodoc extension ----------------------------------------------
autodoc_default_options = {
    "member-order": "bysource",
    "ignore-module-all": True,
}
