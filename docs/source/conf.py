# Configuration file for the Sphinx documentation builder.

# -- Project information
import ampalibe

project = 'Ampalibe'
copyright = '2021, iTeam-$'
author = 'Gatan Jonathan and iTeam-$ members'

release = ampalibe.__version__
version = ampalibe.__version__

# Html cinfiguration
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_logo = "_static/ampalibe.png"
html_favicon = "_static/LOGO.png"
html_theme_options = {
    'logo_only': True,
    'display_version': False,
}
# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'

# -- Options for EPUB output
epub_show_urls = 'footnote'
