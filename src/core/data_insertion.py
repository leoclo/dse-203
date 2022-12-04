from functools import wraps

def insert_data(func):
    """ Decorator to insert in neo4j data assembled in core """

    @wraps(func)
    def core_method(*args, **kwargs):
        graph4j, df_params = func(*args, **kwargs)

        for params in df_params:
            print(f'========= INSERT DATA - NODE - {params["node_name"]} =============')
            graph4j.df2neo4j(**params)

        return graph4j

    return core_method