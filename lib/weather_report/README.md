
# Weather Report

### Python package providing data handling functionality 

#### Load and read data structures
- Data frames
- JSON
- CSV
- More

#### Function components
- Transmogrify
- Transpose
- Translate
- Recognise


```
import lib.weather_report.compose as wrc
import lib.weather_report.load as wrl
import lib.weather_report.translate as wrt
import lib.weather_report.recognise as wrr
import pandas as pd
from pprint import pprint

json_data = wrl.read_json('./template/tfstate_formatted.json')
df = wrt.json_to_data_frame(json_data, record_path=['resources'])

wrt.data_frame_cols(df)

dfs = wrr.data_frame_schema(df)
pprint(dfs)

wrr.easy_print_data_frame(df)
```

#### Manipulate columns or rows
```
df = df.drop(['instances'], axis=1)
wrr.easy_print_data_frame(df)
```

#### Generate HTML and other file types
```
df_html = wrc.html_table_from_data_frame(df)
wrc.write_html_file(df_html, 'data_frame_table.html')
```

#### Grouping 
```
# "true" is translated to python True
announce_grp = df.groupby(['recent_announcement'])
announce_grp.get_group(True)
announce_grp['name_short'].value_counts()

# Create new df from series generated using groupby object
new_df = pd.concat([series1, series2], axis='columns', sort=False)
new_df.rename(columns={'col1': 'new_name', 'col2': 'new_name2'}, inplace=True)
```


```
import lib.weather_report.recognise as wrr
import lib.weather_report.load as wrl
import lib.weather_report.translate as wrt
import lib.weather_report.compose as wrc
json_data = wrl.read_json('./template/tfstate_formatted.json')
Returned <class 'dict'>: return_type argument not present in decorated function signature
df = wrt.json_to_data_frame(json_data, record_path=['resources'])
df = df.drop(['instances'], axis=1)
df_html = wrc.html_table_from_data_frame(df)
wrc.write_html_file(df_html, 'data_frame_table.html')
```






```
       mode                              type                      name      provider
1      data              aws_internet_gateway                        ig  provider.aws
2      data                           aws_vpc                  selected  provider.aws
```
