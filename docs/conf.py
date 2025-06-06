# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import datetime
import sys

# Get configuration information from setup.cfg
try:
    from ConfigParser import ConfigParser
except ImportError:
    from configparser import ConfigParser
conf = ConfigParser()

conf.read([os.path.join(os.path.dirname(__file__), "..", "setup.cfg")])
setup_cfg = dict(conf.items("metadata"))


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'GenAI Code Test'
copyright = '2024, NIST'
author = 'NIST'

__import__(setup_cfg["name"])
package = sys.modules[setup_cfg["name"]]

# The short X.Y version.
version = str(package.__version__).split("-", 1)[0]
# The full version, including alpha/beta/rc tags.
release = str(package.__version__)

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.coverage",
    "sphinx.ext.viewcode",
    "sphinx.ext.imgmath",
    "sphinx.ext.napoleon",  # google- or numpy-style docstrings
    # 'recommonmark',  # markdown files
    # OR
    "m2r",  # markdown files AND .. mdinclude:: file  directive
    # "sphinxcontrib.autoprogram",   # .. autoprogram:: directive
]
napoleon_include_private_with_doc = True
source_suffix = {".rst": "restructuredtext", ".md": "markdown"}

# The master toctree document.
master_doc = "index"

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']
