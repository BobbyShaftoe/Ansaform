
"""

This is A COPY OF the main file in which the configuration for the documentation is made.

"""


import os
import sys
import locale
from datetime import datetime

this_year = str(datetime.now().year)

project = u'Ansaform'
author = u'Jack Shaftoe'
version = u'0.1'
project_repo_url = 'https://github.com/BobbyShaftoe/Ansaform'
main_module_file = 'junit2html.py'


copyright = this_year + ', ' + author


def real_path(rel_path):
    conf_path = os.path.dirname(os.path.realpath(__file__))
    return os.path.abspath(conf_path + '/../../' + rel_path)


sys.path.append(real_path('.'))
sys.path.append(real_path('_ext'))
sys.path.append(real_path('../lib/call_graph'))
sys.path.append(real_path('../lib/junit2html'))

rst_epilog = '.. |project_name| replace:: %s' % project


source_suffix = ['.rst']

master_doc = 'index'

exclude_patterns = [real_path('_build'), real_path('../examples')]
# exclude_patterns = [real_path('_build'), real_path('include/project_summary'), real_path('../examples')]

templates_path = [real_path('_templates')]


# You can find a list of available extension here: http://www.sphinx-doc.org/en/master/extensions.html
extensions = ['sphinx.ext.todo', 'sphinx.ext.viewcode', 'sphinx.ext.autodoc', 'sphinx.ext.imgmath',
              'project_attributes']


todo_include_todos = True


# viewcode: Next to each function/module in the documentation, you will have an internal link to the source code.
#           The source code will have colors defined by the Pygments (syntax highlighting) style.
#           You can checkout the available pygments here: https://help.farbox.com/pygments.html
pygments_style = 'native'


# autodoc:  It allows Sphinx to automatically generate documentation for the docstrings in your code.
#          Get more info here: http://www.sphinx-doc.org/en/master/ext/autodoc.html

# Include both the class's and the init's docstrings.
autoclass_content = "both"
# In the documentation, keep the same order of members as in the code.
autodoc_member_order = 'bysource'
# Default: include the docstrings of all the class/module members.
autodoc_default_flags = ['members']


# imgmath: Sphinx allows use of LaTeX in the html documentation, but not directly. It is first rendered to an image.
# You can add here whatever preamble you are used to adding to your LaTeX document.
imgmath_latex_preamble = r'''
\usepackage{xcolor}
\definecolor{offwhite}{rgb}{238,238,238}
\everymath{\color{offwhite}}
\everydisplay{\color{offwhite}}
'''


# -- Options for HTML output -----------------------------------------------------------------------------------------

html_theme_path = [real_path('_themes')]
html_theme = 'sphinx_rtd_theme'

html_static_path = [real_path('_static')]
html_logo = '_static/logo.png'

print(vars())
