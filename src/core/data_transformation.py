import pandas as pd
from .preprocessing import pre_directors, pre_cast


class DataFrameTransform():
    """Use to create specific dataframe transformations"""

    def __init__(self):
        self.dfs = {}
        return None

    def __getitem__(self, k):
        print(f'==== TRANSFORM {k} ====')
        return getattr(self, k)

    def directors(self, df):
        # df = df[df['acad_fellow'] > 0].dropna()
        self.dfs['directors'] = pre_directors(df)
        return self.dfs['directors']

    def movies(self, df):
        self.dfs['movies'] = df.dropna()
        #
        return self.dfs['movies']

    def cast(self, df):
        df = pre_cast(df)

        companies = []
        people = []
        genres = []
        final_df_data = {
            'movie_id': [],
            'imdb_id': [],
            'lang': [],
            'title': [],
            'overview': [],
            'genres': [],
            'actors': [],
            'directors': [],
            'companies': []
        }
        # filtering directors

        df = df[df['director_name'].isin(self.dfs['directors']['name'])]
        df = pd.merge(df, self.dfs['movies'], how='left', left_on='movie_id', right_on='movie_id')

        for row in df.to_dict('records'):
            c = False
            for k, v in row.items():
                if pd.isnull(v):
                    c = True
            if c:
                continue

            for k in ["movie_id", "imdb_id", "lang", "title", "overview"]:
                final_df_data[k].append(row[k])

            # directors
            director = {
                'name': row['director_name'],
                'gender': row['director_gender']
            }
            final_df_data['directors'].append([director])
            people.append(director)

            actors = []
            for i in range(1, 6):
                if row[f'actor{i}_name'] and row[f'actor{i}_gender']:
                    actor = {
                        'name': row[f'actor{i}_name'],
                        'gender': row[f'actor{i}_gender'],
                    }
                    actors.append(actor)
                    people.append(actor)
                    actors.append({
                        'name': row[f'actor{i}_name'],
                        'gender': row[f'actor{i}_gender'],
                    })

            final_df_data['actors'].append(actors)

            try:
                genres_list = []
                for genre in row['genres'].split('|'):
                    genres.append({'name': genre})
                    genres_list.append({'name': genre})
                final_df_data['genres'].append(genres_list)
            except:
                final_df_data['genres'].append([])

            company = {'name': row['company']}
            companies.append(company)
            final_df_data['companies'].append([company])

        self.dfs = {
            'company': pd.DataFrame(companies).drop_duplicates(subset='name'),
            'people': pd.DataFrame(people).drop_duplicates(subset='name'),
            'genres': pd.DataFrame(genres).drop_duplicates(),
            'movies': pd.DataFrame(final_df_data)
        }




