# Configuration file for the Sphinx documentation builder.
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(".."))))

current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.remove(current_path)
import ampalibe

sys.path.insert(0, current_path)

# -- Project information

project = "Ampalibe"
copyright = "2021, iTeam-$"
author = "iTeam-$"

release = ampalibe.__version__
version = ampalibe.__version__

# Html cinfiguration
html_theme = "sphinx_rtd_theme"
html_static_path = ["../_static"]
html_logo = "../_static/ampalibe_logo.png"
html_favicon = "../_static/ampalibe_logo.png"
html_theme_options = {
    "display_version": False,
    "style_nav_header_background": "#106262",
}
# -- General configuration

extensions = [
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["../_templates"]

# -- Options for HTML output

html_theme = "sphinx_rtd_theme"

# -- Options for EPUB output
epub_show_urls = "footnote"
