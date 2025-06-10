# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
import autoscheduler
sys.path.insert(0, os.path.abspath('../autoscheduler'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon'
]

project = 'QCRAFT AutoScheduler'
copyright = '2024, SPILab'
author = 'Jorge Casco Seco'
release = autoscheduler.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

templates_path = ['_templates']
exclude_patterns = []



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

autodoc_member_order = 'bysource'