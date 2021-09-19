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


def formatter(return_type=None):
    """
    Decorator function that formats functions return value into different types

    :type return_type: string
    :return: func return
    """

    def inner(func):
        def wrapper(*args, **kwargs):
            return_data = None
            if return_type == 'string':
                return_data = str(func(*args, **kwargs))
            elif return_type == 'json_string':
                return_data = json.dumps(func(*args, **kwargs), indent=2)
            elif return_type == 'json_dict':
                return_data = json.loads(func(*args, **kwargs))
            elif return_type == 'dataframe':
                return_data = pd.DataFrame(func(*args, **kwargs))
            else:
                return_data = func(*args, **kwargs)
            return return_data
        return wrapper
    return inner


@formatter(return_type=None)
def read_json(json_file):
    """
    Function to read JSON file
    :param json_file:
    """

    with open(json_file, 'r') as file:
        data = json.load(file)

    return data


@formatter(return_type='json_string')
def read_json_as_string(json_file):
    """
    Function to read JSON file
    :param json_file:
    """

    with open(json_file, 'r') as file:
        data = json.load(file)

    return data


@formatter(return_type='string')
def read_excel(excel_file):
    """
    Function to read Excel file
    :param excel_file:
    """
    data = pd.read_excel(excel_file)
    return data


@formatter(return_type='string')
def read_csv(csv_file):
    """
    Function to read CSV file
    :param csv_file:
    """
    data = pd.read_csv(csv_file, delimiter=',')
    return data


@formatter(return_type='string')
def read_sqlite(db_file):
    """
    Function to read sqlite3 file
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
