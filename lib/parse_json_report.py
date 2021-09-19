"""
  Parse json report
  Reference on Pandas:
    - https://www.skytowner.com/explore/splitting_dictionary_into_separate_columns_in_pandas_dataframe
    - https://github.com/pandas-dev/pandas/issues/36245

    - https://bitbucket.org/hrojas/learn-pandas/src/master/
    - https://pandas.pydata.org/pandas-docs/version/1.0.2/getting_started/tutorials.html
    - https://github.com/BobbyShaftoe/effective-pandas
    - https://nbviewer.jupyter.org/urls/bitbucket.org/hrojas/learn-pandas/raw/master/lessons/Cookbook%20-%20Select.ipynb#
"""
import sys

import lib.weather_report.compose as wrc
import lib.weather_report.load as wrl
import lib.weather_report.translate as wrt
import lib.weather_report.recognise as wrr
import pandas as pd
from pprint import pprint
import json

pd.set_option("large_repr", "truncate")
pd.set_option("expand_frame_repr", False)
pd.set_option("max_rows", 5)
pd.set_option("max_columns", 9)
pd.set_option("max_colwidth", 16)

json_data = wrl.read_json('../template/tfstate_formatted.json')

# Make json data into dataframe
new_df = wrt.json_to_data_frame(json_data, record_path=['resources'])
print('Dataframe columns\n{}'.format(wrt.data_frame_cols(new_df)))

# Display the dataframe schema
dfs = wrr.data_frame_schema(new_df)
print('\nData frame schema\n', json.dumps(dfs, indent=2))

# Show the head of the dataframe
print('\nTop of dataframe')
wrr.easy_print_data_frame(new_df.iloc[1:3])


"""
Begin flattening out nested data across columns - code that follows below
"""

"""First manual step here is to expand just one main nested item that has all the attributes in the main dictionary
   The name of this column with nested records is: `instances` """
# Normalize dataframe and orient by records. This will make dotted name columns for the nested dictionary
new_df = pd.json_normalize(new_df.to_dict(orient='records'), meta=["module", "mode", "type", "name", "provider"],
                           record_path=['instances'], record_prefix='instance.')

# wrr.display_data_frame_as_dict(new_df, head_rows=1)  # Show the result after expanding the nested dictionary

"""This step calls lists_in_dataframe function to discover lists of dictionaries still in the dataframe"""
dataframe_list_items = wrt.lists_in_dataframe(new_df, silent=False)
dataframe_list_columns = dataframe_list_items['unique_list']

"""Loop here iterating over the columns that have nested items"""
for column in dataframe_list_columns:
    print('Expanding column', column)
    # First replace any NaN with empty list of dict
    new_df[column] = new_df[column].apply(lambda d: d if isinstance(d, list) else [{}])

    # Expand nested elements in column for all rows
    new_df = pd.json_normalize(new_df.to_dict(orient='records'), record_path=[column],
                               record_prefix=str(column + '.'), meta=list(new_df.columns))
    # Remove the source column that had the nested data
    new_df = new_df.drop(columns=[column])


print('\nTop of modified dataframe')
wrr.easy_print_data_frame(new_df.iloc[0:10])

"""
Get subset of columns based on name match
Get subset of columns based on depth of nesting
"""
# First get the list of all column names using data_frame_cols function
df_cols = wrt.data_frame_cols(new_df)
pprint(wrt.data_frame_cols(new_df))

print('Columns that have more than 4 levels')
cl = wrt.columns_at_level(df_cols, 5)
pprint(cl)
print('\n')

"""Subset the columns into separate lists for subsetting into separate dataframes"""
# Use the list of dataframe columns to pass into columns_with_levels function
csl = wrt.columns_with_levels(df_cols, levels=0, start_level=4, silent=False)
# csl = wrt.columns_with_levels(df_cols, levels=1, start_level=3, silent=False)
pprint(csl)
# csl = wrt.columns_with_levels(df_cols, levels=1, start_level=3, match_pattern='block', unique=False, silent=False)
# pprint(csl)



print('\nCreating separate dataframes\n')

df1_cols = set(csl).symmetric_difference(set(new_df.columns))
pprint(df1_cols)


res = wrt.flatten_df(new_df)

print('Flatened dataframe\n{}\n'.format(res))
print('Flatened dataframe info\n{}\n'.format(res.info))
print('Flatened dataframe axes\n{}\n'.format(res.axes))









