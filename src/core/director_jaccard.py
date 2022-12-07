import py_stringmatching as sm

# create a Jaccard similarity measure object
jac = sm.Jaccard()
# create a whitespace tokenizer
ws_tok = sm.WhitespaceTokenizer()


# Test if the string is approximately present using jaccard similarity score
def jac_in(string1, string_arr, thres):
    for string2 in string_arr:
        if jac_similar(string1, string2, thres):
            return True
    return False

# Estimate equality based on jaccard similarity score and return true if similar
def jac_similar(string1, string2, thres):
    if string1 is None or string2 is None \
    or string1 is np.nan or string2 is np.nan \
    or pd.isnull(string1) \
    or pd.isnull(string2):
        return False

    tok1 = ws_tok.tokenize(string1)
    tok2 = ws_tok.tokenize(string2)
    
    tok1_len = len(tok1)
    tok2_len = len(tok2)
    
    # Exit if the nomber of tokens is too dissimilar
    if ((tok1_len * thres > tok2_len) or (tok1_len * 1/thres < tok2_len)):
            return False
        
    return jac.get_sim_score(tok1, tok2) >= thres

# Returns a string from the array if it roughly matches the first argument
def jac_trans(string1, string_arr, thres):
    for string2 in string_arr:
        if jac_similar(string1, string2, thres):
            return string2
    return None

# Creates a dictionary to map a dataframe's director names to the names in the acclaimed directors file
def mapDirectors(dir_df, to_df, other_name = "director_name"):
    dir_names = dir_df["name"]
    other_names = to_df[other_name].unique()
    
    dir_map = {}
    
    for name in dir_names:
        # Perform a jaccard similarity score test and put it in the map if it pases
        trans = jac_trans(name, other_names, 0.8)
        if trans is not None:
            dir_map[trans] = name
    
    print("Names given:",len(dir_names), "; Names used:", len(dir_map)) 
    
    return dir_map