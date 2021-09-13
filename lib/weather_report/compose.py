"""
Compose Package
Provides functionality to generate formatted files of different from data
Version: 0.1
"""

import pandas as pd


def html_table_from_data_frame(data_frame, class_list=None):
    """
    Function to generate an HTML table from a Pandas data frame
    CSS classes can be provided as a list: class_list=["table-bordered", "table-striped", "table-hover"]
    :param class_list:
    :type data_frame: df
    :param data_frame: a data frame
    :return:
    """
    if class_list is None:
        class_list = ['table', 'table-striped']
    html_table = data_frame.to_html(classes=class_list, justify='left', bold_rows=True)
    return html_table


def write_html_file(html, html_file):
    """
    Function that writes an html file
    :param html:
    :param html_file:
    """
    with open(html_file, 'w') as h:
        h.write('<link rel="stylesheet"' + ' href="style.css">')
        h.write(html)
