"""
Translate Package
Provides functionality to translate between data types
Version: 0.1
"""

import itertools
from pprint import pprint
from optparse import OptionParser
import pandas as pd
from pandas.core.indexes.multi import MultiIndex
from collections import Counter
import re


def flatten_df(df):
    """
    Function that will reliably flatten a dataframe
    This function is recommended as a simple interface to the heavy flatten_multiindex function

    :param df: A dataframe
    :return: A dataframe with Index of only one dimension
    """
    df = df.reset_index()
    df.columns = flatten_multiindex(df.columns)
    return df


def flatten_multiindex(mi, sep=" - ", format=None):
    """
    This function is the work horse to handle all range of Indicies on dataframes, such as multi indexed dataframes,
    or any number of dimensions of Indexes

    :param mi: MultiIndex of dataframe
    :param sep: Separator used in heading names
    :param format: Format string for header names
    :return: Flattened index of dataframe
    """

    if issubclass(type(mi), pd.core.indexes.multi.MultiIndex):
        # Flatten multi-index headers
        if format is None:
            # Flatten by putting sep between each header value
            flat_index = [sep.join([str(x) for x in tup]).strip(sep)
                          for tup in mi.values]
        else:
            # Flatten according to the provided format string
            flat_index = []
            for tuple in mi.values:

                placeholders = []
                for name in mi.names:
                    if name is None:
                        name = ""
                    name = "{" + str(name) + "}"
                    placeholders.append(name)

                # Check if index segment contains each placeholder
                if all([item != "" for item in tuple]):
                    # Replace placeholders in format with corresponding values
                    flat_name = format
                    for i, val in enumerate(tuple):  # Iterates over the values in this index segment
                        flat_name = flat_name.replace(placeholders[i], val)
                else:
                    # If the segment doesn't contain all placeholders, just join them with sep instead
                    flat_name = sep.join(tuple).strip(sep)
                flat_index.append(flat_name)
    elif issubclass(type(mi), pd.core.indexes.base.Index):
        return mi
    else:
        raise TypeError(f"Expected Index but got {type(mi)}")

    return flat_index


def dicts_to_data_frame(dicts):
    data_frame = pd.DataFrame(dicts)
    return data_frame


def dict_to_data_frame(dict_data):
    """
    Dataframe from a dict
    :param dict_data:
    :return: a dataframe
    """
    # data_frame = pd.DataFrame.from_dict(dict_data)
    data_frame = pd.DataFrame.from_dict(dict_data, orient='index')
    return data_frame


def json_to_data_frame(json_data, record_path=None, meta=None, max_level=0):
    """
    Function to create data frame from json
    # Example: json_to_data_frame(json_data, record_path=['products'], meta=['registry_name', 'fax_number'])
    :param meta:
    :param record_path:
    :param json_data:
    :type max_level: object
    """
    data_frame = pd.json_normalize(json_data, record_path=record_path, meta=meta, max_level=max_level)
    return data_frame


def data_frame_cols(data_frame, flatten=False):
    """
    Function to return columns of data frame
    :type data_frame: object
    """
    # from column names build the list that gets sent to meta param
    data_frame_meta = [[s for s in c.split(".")] for c in data_frame.columns]

    if flatten:
        flatten = itertools.chain.from_iterable
        data_frame_meta = list(flatten(data_frame_meta))

    return data_frame_meta


def columns_at_level(columns_list, levels, separator='.'):
    """
    Function to subset the columns of a specified depth into a unique list
    :param columns_list:
    :param levels:
    :param separator:
    :return:
    """
    column_sublist = set()
    for column_list in columns_list:
        if len(column_list) >= levels:
            column_sublist.add('.'.join(column_list[:levels]))
    return list(column_sublist)


def columns_with_levels(columns_list, levels=1, start_level=0, separator='.', match_pattern='anything', unique=False, silent=True):
    """
    Function to subset and return columns based on segment lengths, and matching pattern in first segment
    :param match_pattern:
    :param columns_list:
    :param levels:
    :param start_level:
    :param separator:
    :param unique:
    :param silent:
    :return:
    """
    column_subset = set()
    column_sublist_dict = {}
    column_segments = []

    for column_list in columns_list:
        if len(column_list) >= start_level + levels:
            column_start_segments = column_list[:start_level]
            column_end_segments = column_list[start_level:]
            column_segment = separator.join(column_start_segments)
            # column_subset.add(column_segment)

            if re.compile('.*' + match_pattern + '.*').match(column_segment) or match_pattern == 'anything':
                column_subset.add(column_segment)

                if not unique:
                    column_segment_name = '{}.{}'.format(column_segment, column_segments.count(column_segment))
                    column_segments.append(column_segment)
                else:
                    column_segment_name = column_segment
                if column_segment_name not in column_sublist_dict:
                    column_sublist_dict.update({column_segment_name: []})
                column_sublist_dict[column_segment_name].extend(column_end_segments)

    if not silent:
        print('\nColumns matching "{}" with {} or more levels after level {}'.format(match_pattern, levels, start_level))
        pprint(column_sublist_dict, width=160)
        print('Total matched column prefix: {}, unique columns: {}\n'.format(len(column_sublist_dict.keys()), len(column_subset)))

    return list(column_subset)


def get_data_frame_items(data_frame, node_label=None):
    """
    Function to get items from data frame
    :param data_frame:
    :param node_label:
    """
    data_frame_items = data_frame.items()
    for label, content in data_frame_items:
        if node_label:
            if label == node_label:
                pprint('{}: {}'.format(label, content))
        else:
            pprint('{}: {}'.format(label, content))


def lists_in_dataframe(data_frame, silent=True):
    """
    Find columns that have list values
    :param data_frame: A data frame
    :param silent: If True print the resulting data sructure
    :return: A dict of list of unique column names and a dict of all columns containing lists for each row
    """
    df_as_dict = data_frame.to_dict()
    list_keys_dict = {}
    list_keys_unique = set()
    for k in df_as_dict.keys():
        # Do each inner key
        for inner_key in df_as_dict[k].keys():
            # Check if the column value is a list
            if isinstance(df_as_dict[k][inner_key], list) and any(isinstance(i, dict) for i in df_as_dict[k][inner_key]):
                # Add the column name to the dict for current row
                if inner_key not in list_keys_dict:
                    list_keys_dict.update({inner_key: []})
                list_keys_dict[inner_key].append(k)
                # Add the column to the set of unique names
                list_keys_unique.add(k)

    if not silent:
        print('\nDict of dataframe rows that have columns with list values')
        pprint(list_keys_dict)
        print('\nSet of dataframe column names that have list values in any rows')
        pprint(list(list_keys_unique))
        print('Total unique columns: {}\n'.format(len(list_keys_unique)))

    return {'rows_dict': list_keys_dict, 'unique_list': list_keys_unique}


if __name__ == "__main__":
    # Command line options
    opt_parser = OptionParser()
    opt_parser.add_option("-s", "--server", dest="server", help="Redis server to connect to.")
    opt_parser.add_option("-p", "--port", dest="port", default=6379, help="Redis port to connect to. (Default: 6379)")
    opt_parser.add_option("-P", "--password", dest="password", default=None,
                          help="Redis password to use. Defaults to unauthenticated.")
    args = opt_parser.parse_args()[0]
