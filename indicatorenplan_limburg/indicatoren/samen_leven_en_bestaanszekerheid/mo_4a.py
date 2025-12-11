import pandas as pd
import cbsodata

# Downloaden van tabeloverzicht
toc = pd.DataFrame(cbsodata.get_table_list())

# Downloaden van gehele tabel (kan een halve minuut duren)
table_id = '85146NED'
data = pd.DataFrame(cbsodata.get_data(table_id))
print(data.head())

# Downloaden van metadata
metadata = pd.DataFrame(cbsodata.get_meta(table_id, 'DataProperties'))

print(metadata[['Key','Title']])

data = pd.DataFrame(cbsodata.get_data(table_id))
# filter data for regio contains '(PV)' and Perioden = 2023 and Marges = 'Waarde' and column SocialeCohesieSchaalscore_15
data_filtered = data[
    (data['RegioS'].str.contains('(PV)')) &
    (data['Perioden'] == '2023') &
    (data['Marges'] == 'Waarde')
][['RegioS', 'SocialeCohesieSchaalscore_15']]
print(data_filtered.head())