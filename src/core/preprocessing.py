from unidecode import unidecode

# Replace accented characters and special characters, and evens out spacing
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

def pre_movies(df):
    return df

def pre_cast(df):
    df = standardize(df, 'director_name')
    # Because directors can take up other roles, standardize their names as well
    df = standardize(df, 'actor1_name')
    df = standardize(df, 'actor2_name')
    df = standardize(df, 'actor3_name')
    df = standardize(df, 'actor4_name')
    df = standardize(df, 'actor5_name')

    return df

def pre_award(df):
    df = standardize(df, 'director_name')