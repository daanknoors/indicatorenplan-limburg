"""Get metadata for indicators"""
import numpy as np
import pandas as pd

# Mapping of SBI names to shorter name categories, easier to display
SBI_DICT = {
    'Industrie': 'industrie',
    'Bouwnijverheid': 'bouwnijverheid',
    'Advisering, onderzoek, special. zakelijke dienstverlening': 'onderzoek',
    'Openbaar bestuur, overheidsdiensten, sociale verzekeringen': 'overheid',
    'Logies-, maaltijd- en drankverstrekking': 'logies',
    'Onderwijs': 'onderwijs',
    'Gezondheids- en welzijnszorg': 'gezondheid',
    'Landbouw, bosbouw en visserij': 'landbouw',
    'Overige dienstverlening': 'overig',
    'Informatie en communicatie': 'ict',
    'Cultuur, sport en recreatie': 'csr',
    'Extraterritoriale organisaties en lichamen': 'extraterritoraal',
    'Financiële instellingen': 'financien',
    'Groot- en detailhandel; reparatie van auto’s': 'autoreparatie',
    'Huishoudens als werkgever': 'huishouden',
    'Productie, distributie, handel in elektriciteit en aardgas': 'productie',
    'Verhuur van en handel in onroerend goed': 'onroerend',
    'Verhuur van roerende goederen, overige zakel. dienstverl.': 'roerend',
    'Vervoer en opslag': 'vervoer',
    'Winning van delfstoffen': 'delfstoffen',
    'Winning/distributie van water; afval(water)beheer,sanering': 'afval'
}


def metadata_onderwerpen(indicator_code: str, indicator_name: str, start_period: int = 2023, end_period: int = 2027) -> pd.DataFrame:
    """Get the 'onderwerpen' metadata for the indicator"""
    df_onderwerpen = pd.DataFrame({
        'Indicator code': [indicator_code],
        'Name': [indicator_name],
        'Data type': ['Numeric'],
        'Keywords': ['Indicatorenplan'],
        'Period type': ['Year'],
        'Formula': [np.nan],
        'Aggregation indicator': [np.nan],
        'Unit': ['aantal'],
        'Source': ['ETIL'],
        'Start period': [start_period],
        'End period': [end_period],
        'RoundOff': [1],
        'Description': [
            'Deze indicator maakt onderdeel uit van het Indicatorenplan Statenperiode 2023-2027 en is bedoeld om de maatschappelijke opgaven, doelstellingen of resultaten uit de beleidskaders te monitoren. Vestigingen per grootteklasse per sector.'],
        'More information': [np.nan]
    })
    return df_onderwerpen


def metadata_dim_sbi(dimension_dict: dict):
    """Get the 'sbi_dim' metadata for the indicator"""
    df_dim_sbi = pd.DataFrame({
        'itemcode': dimension_dict.values(),
        'Name': dimension_dict.keys()
    })
    return df_dim_sbi


def metadata_dim_grootteklasse(ranges_grootteklasse: tuple):
    """Get the 'grootteklasse_dim' metadata for the indicator"""
    df_grooteklasse = pd.DataFrame({
        'itemcode': ranges_grootteklasse,
        'Name': [x.replace('_', '-') for x in ranges_grootteklasse]
    })
    return df_grooteklasse


def metadata_geo_item():
    """Get the 'geoitem' metadata for the indicator"""
    df_dim_geoitem = pd.DataFrame({
        'itemcode': ['pv31'],
        'Name': ['Provincie Limburg']
    })
    return df_dim_geoitem