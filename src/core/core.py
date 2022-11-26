import pandas as pd
from .data_transformation import DataFrameTransform
from .data_insertion import insert_data


@insert_data
def etl(graph4j, settings):
    df_params = []
    for k, meta in settings['etl'].items():
        df = pd.read_csv(**settings['csv_map'][k])
        df.rename(columns=meta['column_map'], inplace=True)
        df = df[meta['column_map'].values()]
        df = DataFrameTransform(df, k).df

        df_params.append({
            'df': df,
            'node_name': meta['node_name']
        })
    return graph4j, df_params

