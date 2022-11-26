import pandas as pd
from neo4j import GraphDatabase


class GraphNeo4j():
    """
        A class that is used to comunicate with neo4j database

        Parameters
        ----------

        uri : str:
            host where the Neo4j Bolt server is located.
        username : str:
            Neo4j authorized user username
        password : str
            Neo4j authorized user password
    """

    def __init__(self, uri, username, password, db):
        # self.uri = uri
        # self.auth = (username, password)
        self.driver = GraphDatabase.driver(uri, auth=(username, password))
        self.db = db
        # self.gds = GraphDataScience(uri, auth=(username, password))
        self.res = []
        self.queries = []

    def __getitem__(self, k):
        return getattr(self, k)

    @classmethod
    def from_settings(cls, settings):
        return cls(**settings['neo4j'])

    def close(self):
        self.driver.close()

    def run_query(self, query, params):
        if self.db:
            with self.driver.session(database=self.db) as session:
                self.res.append(list(session.run(query, params)))
                self.queries.append(query)
            return
        with self.driver.session() as session:
            self.res.append(list(session.run(query, params)))
            self.queries.append(query)

    def df2neo4j(self, df, node_name):
        cols_query = '{' + ','.join([f'{col}: row.{col}' for col in df.columns]) + '}'
        query = f'''
            UNWIND $rows AS row
            MERGE (:{node_name} {cols_query})
            RETURN count(*) as total
        '''
        self.run_query(query, {'rows': df.to_dict('records')})





