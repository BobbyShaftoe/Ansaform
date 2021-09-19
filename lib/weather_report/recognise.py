"""
Recognise Package
Provides functionality to recognise and provide understanding of data structures
Version: 0.1
"""

from optparse import OptionParser
import pandas as pd
import json
from pandas.io.json import build_table_schema
from pprint import pprint
from . import translate as wrt


def display_data_frame(data_frame):
    """
    Function to nicely print data frame or a data frame's components
    :param data_frame:
    """

    with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
        print(data_frame)


def easy_print_data_frame(data_frame):
    """
    Function to simply print a data frame
    :param data_frame:
    """

    print(data_frame.to_string())


def data_frame_schema(data_frame):
    """
    Function to get the schema of a data frame
    
    :param data_frame:
    :return:
    """
    data_frame_table_schema = build_table_schema(data_frame)
    return data_frame_table_schema


def data_frame_info(data_frame):
    print('Dataframe columns\n{}'.format(wrt.data_frame_cols(data_frame)))
    print('Dataframe schema')
    print(json.dumps(data_frame_schema(data_frame), indent=2))


def display_data_frame_as_dict(data_frame, head_rows=1):
    # Here we show the structure as dict for reference and get the keys that have nested structures as values
    unique_keys = set()
    df_as_dict = data_frame.to_dict(orient='records')
    for dict_item in df_as_dict:
        for k, v in dict_item.items():
            if isinstance(v, dict):
                unique_keys.add(v.keys())
            else:
                unique_keys.add(k)

    print('\nShowing dictionary structure of {} nodes'.format(head_rows))
    pprint(df_as_dict[0:head_rows])
    print('\nUnique keys')
    pprint(unique_keys)


if __name__ == "__main__":
    # Command line options
    opt_parser = OptionParser()
    opt_parser.add_option("-s", "--server", dest="server", help="Redis server to connect to.")
    opt_parser.add_option("-p", "--port", dest="port", default=6379, help="Redis port to connect to. (Default: 6379)")
    opt_parser.add_option("-P", "--password", dest="password", default=None,
                          help="Redis password to use. Defaults to unauthenticated.")
    args = opt_parser.parse_args()[0]
