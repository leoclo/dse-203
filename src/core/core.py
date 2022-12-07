import pandas as pd
from .data_transformation import DataFrameTransform

def extract_transform(settings):
    df_transform = DataFrameTransform()
    for k, meta in settings['transform'].items():

        df = pd.read_csv(**settings['extract'][k])

        df = df[meta['column_map'].keys()]
        df.rename(columns=meta['column_map'], inplace=True)
        df = df[meta['column_map'].values()]


        df_transform[k](df)

    return df_transform.dfs


def load(graph4j, dfs, load_settings):
    for c in load_settings['constraints']:
        graph4j.create_constraint(**c)

    for k, df in dfs.items():
        graph4j.df2neo4j(df, load_settings['data'][k])
    return graph4j