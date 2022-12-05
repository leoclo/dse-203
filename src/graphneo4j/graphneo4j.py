import pandas as pd
from neo4j import GraphDatabase


def write_merges(merges):
    return '\n'.join([
        write_node_merge(**merge) for merge in merges
    ])

def write_node(ref, node_name, cols, row):
    cols_query = '{' + ', '.join([f'{col}: {row}.{col}' for col in cols]) + '}'
    return f'({ref}:{node_name} {cols_query})'

def write_node_merge(node_name, cols, ref, unwind=None, needs=None, relations=None):
    row = 'row'
    merge = 'MERGE'
    unwind_query = ''
    if unwind:
        merge = 'MATCH'
        row = unwind
        unwind_query = f'WITH row, {needs}\nUNWIND row.{unwind} AS {unwind}'

    relation_qry = ''
    if relations:
        relation_qry = write_relations(relations)

    node_query = write_node(ref, node_name, cols, row)

    return f'{unwind_query}\n{merge} {node_query}\n{relation_qry}'


def write_relation_merge(begins, begins_dir, name, ends, ends_dir):
    return f'MERGE ({begins}){begins_dir}[:{name}]{ends_dir}({ends})'


def write_relations(relations):
    return '\n'.join([
        write_relation_merge(**rel) for rel in relations
    ])


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
        query = query.strip()
        print(query)
        if self.db:
            with self.driver.session(database=self.db) as session:
                self.res.append(list(session.run(query, params)))
                self.queries.append(query)
            return

        with self.driver.session() as session:
            self.res.append(list(session.run(query, params)))
            self.queries.append(query)

    def create_constraint(self, name, node_name, field):
        query = (
        f'''CREATE CONSTRAINT {name}
        IF NOT EXISTS ON (c:{node_name})
        ASSERT c.{field} IS UNIQUE''')
        self.run_query(query, {})

    def df2neo4j(self, df, merges):
        if self.clear_data:
            try:
                query = f'''MATCH (n:{node_name}) DELETE n'''
                self.run_query(query, {})
            except: pass


        merge_qry = write_merges(merges)
        if self.insertion_mode == 'csv_file':
            return self.df2neo4j_csv(df, merge_qry)

        return self.df2neo4j_batch(df, merge_qry)

    def df2neo4j_batch(self, df, merge_qry):
        total = 0
        batch = 0
        result = None

        max_rows = df.shape[0]
        if self.cap_insert:
            max_rows = self.cap_insert

        while batch * self.batch_size < max_rows:
            print(f'batch {batch}')

            query = (
            f'''UNWIND $rows AS row\n{merge_qry}\nRETURN count(*) as total''')
            self.run_query(query, {'rows': df.iloc[batch*self.batch_size:(batch+1)*self.batch_size].to_dict('records')})
            total += self.res[-1][0]['total']
            batch += 1

        return self

    def df2neo4j_csv(self, df, merge_qry):
        file_name = f'final_data.csv'
        df.iloc[0:self.cap_insert].to_csv(f'{self.file_folder}{file_name}')

        query = (
        f''':auto USING PERIODIC COMMIT {self.batch_size}
        LOAD CSV  WITH HEADERS FROM 'file:///{file_name}' AS row\n{merge_qry}\nRETURN count(*) as total''')

        self.run_query(query, {})
        return self









