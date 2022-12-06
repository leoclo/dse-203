from unidecode import unidecode

def standardize(df, dir_col):
    df[dir_col] = df[dir_col].str.replace(
        '[\W]+', ' ', regex=True
    ).str.strip().str.title().astype("string").map(
        unidecode,na_action="ignore"
    )
    return df

def pre_directors(df):
    df = standardize(df, 'name')
    return df


def pre_cast(df):
    df = standardize(df.dropna(), 'director_name')
    return df