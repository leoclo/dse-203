


class DataFrameTransform():
    """Use to create specific dataframe transformations"""

    def __init__(self):
        self.dfs = {}

        return None

    def __getitem__(self, k):
        print(f'==== TRANSFORM {k} ====')
        return getattr(self, k)

    def directors(self, df):
        self.dfs['directors'] = df.dropna()
        return self.dfs['directors']

    def movies(self, df):
        df = df[df['lang'] == 'en'].dropna()
        import ipdb; ipdb.set_trace()
        self.dfs['movies'] = df
        return self.dfs['movies']

    def cast(self, df):
        self.dfs['cast'] = df.dropna()
        return self.dfs['cast']




