"""Indicator: Woningtekort Data"""

import pandas as pd

from indicatorenplan_limburg.configs.paths import get_path_data

PATH_DATA_WONINGTEKORT = get_path_data(name='Woningtekort', subfolder=None)
# Voorbeeld regio_mapping
REGIO_MAPPING = {

    'Noord-Limburg': 'NL_LIM_NL',
    'Midden-Limburg': 'NL_LIM_ML',
    'Zuid-Limburg': 'NL_LIM_ZL',
    'Nederland': 'NL'
}

def load_data_woningtekort_2024():
    df_2024 = pd.read_excel(PATH_DATA_WONINGTEKORT / 'Woningtekort - 2024 - COROP-gebieden.xlsx', skiprows=1)

    # only retain the information with percentages woningtekort per region
    df_2024 = df_2024.iloc[:3, :]
    df_2024.columns = ['Regio', 'aantal']
    df_2024['period'] = '2024'
    df_2024['aantal'] = df_2024['aantal'].replace("%", "").astype(float).abs() * 100
    return df_2024

def load_data_woningtekort_2023():
    df_2023 = pd.read_excel(PATH_DATA_WONINGTEKORT / 'Woningtekort - COROP-gebieden 2023.xlsx'
                            ).iloc[[2], 1:4]

    df_2023.columns = ['Noord-Limburg', 'Midden-Limburg', 'Zuid-Limburg']

    # Data in lang formaat zetten (melt)
    df_2023 = df_2023.melt(var_name='Regio', value_name='woningtekort')

    # Voeg de periode toe
    df_2023['period'] = '2023'

    # Voeg woningvoorraad waardes toe uit Woningmonitor 2024
    df_2023['woningvoorraad'] = [296021, 111531, 127375]

    # Bereken het percentage woningtekort
    df_2023['aantal'] = abs((df_2023['woningtekort'] / df_2023['woningvoorraad']) * 100)

    # Drop de onnodige kolommen
    df_2023.drop(['woningtekort', 'woningvoorraad'], axis=1, inplace=True)
    return df_2023

def laad_woningtekort_data(regio_mapping):
    df_2024 = load_data_woningtekort_2024()
    df_2023 = load_data_woningtekort_2023()


    # 2022
    df_2022 = pd.read_excel(PATH_DATA_WONINGTEKORT / 'Actueel woningtekort Primos 2022.xlsx').iloc[:3, [0, 2]]
    df_2022 = df_2022.rename(columns={'Unnamed: 0': 'Regio', 'Woningtekort 2022 (%)': 'aantal'})
    df_2022['period'] = '2022'
    df_2022['aantal'] = df_2022['aantal'].astype(float).abs() * 100

    # 2021
    df_2021 = pd.read_excel(PATH_DATA_WONINGTEKORT / 'Actueel woningtekort Primos 2021.xlsx',
                            sheet_name='Actueel woningtekort').iloc[:3, [0, 2]]
    df_2021 = df_2021.rename(columns={'Unnamed: 0': 'Regio', 'Actueel woningtekort (%)': 'aantal'})
    df_2021['period'] = '2021'
    df_2021['aantal'] = df_2022['aantal'].astype(float)

    # 2019
    # 2019 Woningvoorraad
    df_2019_woningvoorraad = pd.read_excel(
        PATH_DATA_WONINGTEKORT / 'Primos 2019 Ontwikkeling woningvoorraad  - NL Limburg COROP-gebieden.xls'
    ).iloc[[3], [1, 5, 9, 13]]
    df_2019_woningvoorraad.columns = ['Noord-Limburg', 'Midden-Limburg', 'Zuid-Limburg', 'Nederland']
    df_2019_woningvoorraad = df_2019_woningvoorraad.melt(var_name='Regio', value_name='woningvoorraad')

    # 2019 Woningbehoefte
    df_2019_woningbehoefte = pd.read_excel(
        PATH_DATA_WONINGTEKORT / 'Primos 2019 woningbehoefte  - NL Limburg COROP-gebieden 2019.xls'
    ).iloc[[3], [5, 10, 15, 20]]
    df_2019_woningbehoefte.columns = ['Noord-Limburg', 'Midden-Limburg', 'Zuid-Limburg', 'Nederland']
    df_2019_woningbehoefte = df_2019_woningbehoefte.melt(var_name='Regio', value_name='woningbehoefte')

    # Samenvoegen van de dataframes
    df_2019 = pd.merge(df_2019_woningvoorraad, df_2019_woningbehoefte, on='Regio')
    df_2019['period'] = '2019'

    # Berekening van het tekort
    df_2019['aantal'] = ((df_2019['woningbehoefte'] - df_2019['woningvoorraad']) / df_2019['woningvoorraad']) * 100

    # Drop onnodige kolommen
    df_2019.drop(['woningvoorraad', 'woningbehoefte'], axis=1, inplace=True)

    ### Voeg missende Nederland waardes toe
    dict_ned = {
        2020: 4.2,  # https://www.rijksoverheid.nl/actueel/nieuws/2020/06/15/staat-van-de-woningmarkt-2020
        2021: 3.5,
        # https://www.volkshuisvestingnederland.nl/actueel/nieuws/2021/07/05/staat-van-de-woningmarkt-2021-woningmarkt-oververhit
        2022: 3.9,
        # https://www.rijksoverheid.nl/actueel/nieuws/2023/07/12/woningbouwopgave-stijgt-naar-981.000-tot-en-met-2030
        2023: 4.8,
        # https://www.rijksoverheid.nl/actueel/nieuws/2023/07/12/woningbouwopgave-stijgt-naar-981.000-tot-en-met-2030
        2024: 4.9,
        # https://www.rijksoverheid.nl/actueel/nieuws/2024/07/12/seinen-op-groen-om-jaarlijks-100.000-nieuwe-woningen-te-bouwen
    }

    # Voeg Nederland-waarden dynamisch toe aan een DataFrame
    df_nederland = pd.DataFrame(
        [{'Regio': 'Nederland', 'period': year, 'aantal': value} for year, value in dict_ned.items()]
    )

    # Combine the datasets into a single DataFrame
    df = pd.concat([df_2019, df_2021, df_2022, df_2023, df_2024, df_nederland], ignore_index=True)
    df['period'] = pd.to_numeric(df['period'], errors='coerce').astype('Int64')

    # Transformeer de processing
    df_mo_11a = transformeer_woonderzoek_data(df, regio_mapping)

    df_mo_11a = df_mo_11a.rename(columns={'aantal': 'df_mo_11a'})

    return df_mo_11a


def transformeer_woonderzoek_data(df, region_mapping, column_renames=None):
    """
    Transformeert het gecombineerde woonderzoek DataFrame.
    Deze functie voert de volgende stappen uit:
    1. Voegt een 'geolevel' kolom toe.
    2. Mapt de regio's naar hun respectievelijke codes.
    3. Hernoemt de kolommen volgens de gespecificeerde mapping.
    4. Hernoemt 'Regio' naar 'geoitem'.
    5. Hernoemt 'Jaartal' naar 'period' (optioneel).
    6. Voorziet dimensie-item-kolommen (dim_*) van gestandaardiseerde waarden in lowercase
       zonder spaties.

    Args:
        df (pd.DataFrame): Gecombineerd DataFrame van Limburg en Nederland woonderzoek
        region_mapping (dict): Mapping van regio namen naar hun codes
        column_renames (dict): Mapping van oude kolomnamen naar nieuwe kolomnamen

    Returns:
        pd.DataFrame: Getransformeerd DataFrame
    """
    # Stap 1: Voeg 'geolevel' kolom toe
    df['geolevel'] = df['Regio'].map(lambda x: "nederland" if x == "Nederland" else "corop_id")

    # Stap 2: Map de regio's naar hun codes
    df['Regio'] = df['Regio'].map(region_mapping)

    # Stap 3: Rename de Regio kolom naar geoitem
    df.rename(columns={'Regio': 'geoitem'}, inplace=True)

    # Stap 4: Rename de Jaartal kolom naar period (optioneel)
    if "Jaartal" in df.columns:
        df.rename(columns={'Jaartal': 'period'}, inplace=True)

    # Stap 5: Hernoem de overige kolommen (optioneel)
    if column_renames:
        df = df.rename(columns=column_renames)

    # Stap 6: Hernoem dimensie-items naar lowercase en verwijder spaties
    for col in df.columns:
        if col.startswith('dim_'):
            df[col] = df[col].apply(lambda x: str(x).lower().replace(" ", "_").replace(",", "") if isinstance(x, str) else x)

    return df


if __name__ == "__main__":


    # Laad de woningtekort data
    df_woningtekort = laad_woningtekort_data(REGIO_MAPPING)
    print(df_woningtekort)
