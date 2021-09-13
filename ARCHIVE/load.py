"""
Load Package
Provides functionality to read and load from data sources
From: Files, APIs, Databases
Version: 0.1
"""

import json
import sqlite3
from optparse import OptionParser
from functools import wraps
import pandas as pd


def formatter(*args, **kwargs):
    """
    Decorator function that formats functions return value into different types
    :return: func return
    """

    def wrapper(func):
        data = func(*args, **kwargs)

        if 'return_type' in kwargs:
            return_type = kwargs['return_type']
        else:
            print('Returned {}: return_type argument not present in decorated function signature'.format(type(data)))
            return_type = None

        if return_type == 'string':
            return_data = str(data)
        elif return_type == 'json_string':
            return_data = json.dumps(data, indent=2)
        elif return_type == 'json_dict':
            return_data = json.loads(data)
        elif return_type == 'dataframe':
            return_data = pd.DataFrame(data)
        else:
            return_data = data

        return return_data

    return wrapper


@formatter(return_type='json_string')
def read_json(json_file):
    """
    Function to read JSON file
    :param json_file:
    """
    return_data = None

    with open(json_file, 'r') as file:
        data = json.load(file)

    return data


@formatter
def read_excel(excel_file, return_type='string'):
    """
    Function to read Excel file
    :param return_type:
    :param excel_file:
    """
    data = pd.read_excel(excel_file)
    return data


@formatter
def read_csv(csv_file, return_type='string'):
    """
    Function to read CSV file
    :param return_type:
    :param csv_file:
    """
    data = pd.read_csv(csv_file, delimiter=',')
    return data


@formatter
def read_sqlite(db_file, return_type='string'):
    """
    Function to read sqlite3 file
    :param return_type:
    :param db_file:
    """
    # open engine connection
    con = sqlite3.connect(db_file)

    # create a cursor object
    cur = con.cursor()

    # Perform query: rs
    rs = cur.execute('select * from TEST')

    # Save results of the query to DataFrame: df
    data = pd.DataFrame(rs.fetchall())

    # Close connection
    con.commit()

    return data


if __name__ == "__main__":
    # Command line options
    opt_parser = OptionParser()
    opt_parser.add_option("-s", "--server", dest="server", help="Redis server to connect to.")
    opt_parser.add_option("-p", "--port", dest="port", default=6379, help="Redis port to connect to. (Default: 6379)")
    opt_parser.add_option("-P", "--password", dest="password", default=None,
                          help="Redis password to use. Defaults to unauthenticated.")
    args = opt_parser.parse_args()[0]
