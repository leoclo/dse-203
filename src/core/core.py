import pandas as pd
from .data_transformation import DataFrameTransform
from .data_insertion import insert_data


def extract_transform(settings):
    df_transform = DataFrameTransform()
    for k, meta in settings['transform'].items():
        df = pd.read_csv(**settings['extract'][k])
        df = df[meta['column_map'].keys()]
        df.rename(columns=meta['column_map'], inplace=True)
        df = df[meta['column_map'].values()]

        df_transform[k](df)


    return df_transform.dfs['final']


def extract(settings):
    dfs = []
    df_transform = DataFrameTransform()
    for k in settings['extract']:
        df = pd.read_csv(**settings['extract'][k])
        df = df[meta['column_map'].keys()]
        df.rename(columns=meta['column_map'], inplace=True)
        dfs[k] = df[meta['column_map'].values()]

    return dfs
