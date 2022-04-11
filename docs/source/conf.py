# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import msmb_theme
sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'FabNEPTUNE'
copyright = '2022, Kevin Bronik, Derek Groen, Ed Threlfall'
author = 'Kevin Bronik, Derek Groen, Ed Threlfall'

# The short X.Y version
version = ''
# The full version, including alpha/beta/rc tags
release = ''


# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.mathjax',
    # 'readthedocs_ext.readthedocs',
]

templates_path = ['_templates']

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_static_path = ['_static']

master_doc = 'index'

# -- Options for HTML output -------------------------------------------------
html_logo = "../../logo.png"

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'FabNEPTUNEdoc'

# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'FabNEPTUNE', 'FabNEPTUNE Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

texinfo_documents = [
    (master_doc, 'FabNEPTUNE', 'FabNEPTUNE Documentation',
     author, 'FabNEPTUNE', 'One line description of project.',
     'Miscellaneous'),
]

# -- Options for Epub output -------------------------------------------------

epub_title = project

epub_exclude_files = ['search.html']

# -- Options for HTML output -------------------------------------------------

# https://pypi.org/project/msmb_theme/
html_theme = 'msmb_theme'
html_theme_path = [msmb_theme.get_html_theme_path()]


source_suffix = '.rst'
language = None
pygments_style = None

'''
# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

latex_documents = [
    (master_doc, 'FabNEPTUNE.tex', 'FabNEPTUNE Documentation',
     'Kevin Bronik, Derek Groen, Ed Threlfall', 'manual'),
]
'''
