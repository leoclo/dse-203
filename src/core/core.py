import requests
import pandas as pd
from .data_transformation import DataFrameTransform
from .award_wiki_crawler import AwardWikiCrawler, AWARD_LIST


def extract_transform(settings):
    df_transform = DataFrameTransform()

    if settings['crawler']['on']:
        crawler_award()

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


def crawler_award(settings):
    award_wiki_crawler = AwardWikiCrawler()

    for row in AWARD_LIST:
        try:
            award_wiki_crawler.load_data(**row)
        except Exception as e:
            print(row)
            raise e
        pass

    for k, data in award_wiki_crawler.dfs.items():
        df = pd.DataFrame(data)
        print(f'=========  Crwaler {k} ========')
        print(df.info())
        print(f'========= end ========')
        df.to_csv(f'src/files/{k}.csv')

    return True
