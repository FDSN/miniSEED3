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
# import sys
# sys.path.insert(0, os.path.abspath('.'))
import sphinx_rtd_theme

from json_schema_for_humans.generate import generate_from_filename
from json_schema_for_humans.generation_configuration import GenerationConfiguration

# -- Project information -----------------------------------------------------

project = 'FDSN miniSEED 3'
copyright = '2023, International FDSN'
author = 'FDSN'

version = '3'
release = '2023-01-18'

# Documentation version: major + release date
doc_version = 'v' + version + ' rev. ' + release

# Allow |doc_version| and |major_version| to be used in RST
rst_epilog = f"""
.. |doc_version|   replace:: {doc_version}
.. |major_version| replace:: {version}
"""

# -- General configuration ---------------------------------------------------

# Default in Sphinx 2, but not in older versions
master_doc = 'index'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
  'sphinx_rtd_theme',
  'sphinxmark',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['docs', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# Allow :strike:`TEXT` to be used in RST for strikethrough styling
rst_prolog = """
.. role:: strike
    :class: strike
"""

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'sticky_navigation': False,
}

html_logo='_static/FDSN-logo.png'
html_favicon = '_static/favicon.ico'
html_title = 'FDSN miniSEED 3'
html_show_sphinx = False
html_search_language = 'en'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_css_files = [
  'css/fdsn_rtd_theme.css',
  'css/custom.css',
#  'css/schema_doc.css',
]

html_js_files = [
  'js/sidebar_context.js',
#  'js/schema_doc.min.js',
]

# -- Generate JSON schema documentation -------------------------------
jsfh_config = GenerationConfiguration(copy_css=True,
                                      copy_js=True,
                                      expand_buttons=True,
                                      with_footer=False)

generate_from_filename("extra-headers/ExtraHeaders-FDSN-v1.0.schema-2023-07.json",
                       "extra-headers/ExtraHeaders-FDSN-v1.0.schema.html",
                        config=jsfh_config)

os.rename("extra-headers/schema_doc.css", "_static/css/schema_doc.css")
os.rename("extra-headers/schema_doc.min.js", "_static/js/schema_doc.min.js")

# Mark as draft, disable for releases
sphinxmark_enable = False

# Sphinxmark options, 'document' is the div for the RTD theme body
sphinxmark_div = 'document'
