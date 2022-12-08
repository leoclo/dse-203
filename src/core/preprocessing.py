from unidecode import unidecode

# Replace accented characters and special characters, and evens out spacing
def standardize(df, dir_col):
    new_df = df
    new_df[dir_col] = df[dir_col].str.replace(
        '[\W]+', ' ', regex=True
    ).str.strip().str.title().astype("string").map(
        unidecode,na_action="ignore"
    )
    return new_df

def pre_directors(df):
    df = standardize(df, 'name')
    return df

def pre_movies(df):
    cur_df = df.dropna()

    return cur_df

def pre_cast(df):
    df = standardize(df, 'director_name')
    # Because directors can take up other roles, standardize their names as well
    df = standardize(df, 'actor1_name')
    df = standardize(df, 'actor2_name')
    df = standardize(df, 'actor3_name')
    df = standardize(df, 'actor4_name')
    df = standardize(df, 'actor5_name')
    # df = standardize(df, 'title')
    # df = standardize(df, 'editor_name')

    # df["runtime"] = df["runtime"].fillna(-1).astype("int32")

    return df

def pre_award(df):
    df = standardize(df, 'director_name')