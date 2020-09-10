import xml.etree.ElementTree as ET
from pathlib import Path
import pandas as pd

pd.set_option('display.max_rows', 1000)

in_folder = Path(r'/path/to/directory/for/twb/file')
infile = r'tableau_filename.twb'  # Note: Must be .twb file, not .twbx file
outfile = r'parameters_from_tableau.xlsx'

tree = ET.parse(in_folder / infile)
root = tree.getroot()

rows = []
for datasources in root.findall('datasources'):
    for datasource in datasources:
        if datasource.attrib['name'] == 'Parameters':
            for column in datasource:
                try:
                    rows.append([column.attrib['caption'], column.attrib['value']])
                except:
                    pass

out_df = pd.DataFrame(rows, columns=['Parameter', 'Value'])

# round values to 2 decimal places and drop non-numeric parameters
out_df['Value'] = pd.to_numeric(out_df['Value'], errors='coerce').round(decimals=2)
out_df = out_df[out_df['Value'].notnull()].reset_index(drop=True)

# output to excel and print to screen
out_df.to_excel(in_folder / outfile, index=None)
print(out_df)
