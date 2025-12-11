"""
Voorbeelden gebruik van CBS Open Data v3 in Python
https://www.cbs.nl/nl-nl/onze-diensten/open-data
Auteur: Jolien Oomens
Centraal Bureau voor de Statistiek

Minimale voorbeelden van het ophalen van een tabel, het koppelen van metadata
en het filteren van data voor het downloaden.
"""

import pandas as pd
import cbsodata

# Downloaden van tabeloverzicht
toc = pd.DataFrame(cbsodata.get_table_list())

# Downloaden van gehele tabel (kan een halve minuut duren)
table_id = '86006NED'
data = pd.DataFrame(cbsodata.get_data(table_id))
print(data.head())

# Downloaden van metadata
metadata = pd.DataFrame(cbsodata.get_meta(table_id, 'DataProperties'))

print(metadata[['Key','Title']])

# Downloaden van selectie van data
data = pd.DataFrame(
        cbsodata.get_data(table_id,
                          filters="WijkenEnBuurten eq 'GM0363    '",
                          select=['WijkenEnBuurten','AantalInwoners_5']))
print(data.head())