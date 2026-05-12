# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
project = 'SignBridge'
copyright = '2026, Anuki Kithara, Dulitha Chandrasiri, Dulneth Kurunduwatte, Nuha Rilwan, Shivangi Sritharan'
author = 'Anuki Kithara, Dulitha Chandrasiri, Dulneth Kurunduwatte, Nuha Rilwan, Shivangi Sritharan'
release = '0.4.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx_wagtail_theme']
 
templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo" # try switching this to "alabaster" or "furo"
html_static_path = ['_static']
html_css_files = ["custom.css"]
html_logo = "_static/logo.svg"
html_theme_options = dict(
    project_name = "SignBridge",
    logo = "_static/logo.svg",
    logo_alt = "SignBridge",
    logo_url = "/",
    github_url = "https://github.com/nuhaaaaaaa24/SignBridge/blob/main/docs/source/"
) 