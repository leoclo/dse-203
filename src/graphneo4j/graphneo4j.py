import pandas as pd
from neo4j import GraphDatabase

def write_node_cols(node_name, cols):
    cols_query = '{' + ','.join([f'{col}: row.{col}' for col in df.columns]) + '}'
    return f'MERGE (:{node_name} {cols_query})'


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

    def __init__(
        self, uri, username, password, db,
        cap_insert=10000,
        insertion_mode='batch_rows',
        batch_size=10000,
        file_folder= 'src/files',
        clear_data=False
    ):
        # self.uri = uri
        # self.auth = (username, password)
        self.clear_data = clear_data
        self.insertion_mode = insertion_mode
        self.file_folder = file_folder
        self.batch_size = batch_size
        self.cap_insert = cap_insert
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
        if self.clear_data:
            try:
                query = f'''
                    MATCH (n:{node_name}) DELETE n;
                '''
                self.run_query(query, {})
            except: pass

        if self.insertion_mode == 'csv_file':
            self.df2neo4j_csv(df, node_name)
            return

        self.df2neo4j_batch(df, node_name)

    def df2neo4j_batch(self, df, node_name):
        total = 0
        batch = 0
        result = None

        max_rows = df.shape[0]
        if self.cap_insert:
            max_rows = self.cap_insert

        merge_qry = write_node_cols(node_name, df.columns)
        while batch * self.batch_size < max_rows:
            print(f'batch {batch}')

            query = f'''
                UNWIND $rows AS row
                {merge_qry}
                RETURN count(*) as total
            '''
            self.run_query(query, {'rows': df[batch*self.batch_size:(batch+1)*self.batch_size].to_dict('records')})
            total += self.res[-1][0]['total']
            batch += 1

    def df2neo4j_csv(self, df, node_name):
        file_name = f'{node_name}.csv'
        df[0:self.cap_insert].to_csv(f'{self.file_folder}{file_name}')

        merge_qry = write_node_cols(node_name, df.columns)
        query = f'''
            :auto USING PERIODIC COMMIT {self.batch_size}
            LOAD CSV  WITH HEADERS FROM 'file:///{file_name}' AS row
            {merge_qry}
            RETURN count(*) as total
        '''

        self.run_query(query, {})









