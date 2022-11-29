


class DataFrameTransform():
    """Use to create specific dataframe transformations"""

    def __init__(self, df, k):
        self.df = self[k](df)
        return None

    def __getitem__(self, k):
        return getattr(self, k)

    def directors(self, df):
        return df.dropna()

    def movies(self, df):
        df = df.iloc[0:8000]
        df = df[df['lang'] == 'en']
        return df.dropna()