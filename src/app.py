import sys
from utils import utils
from graphneo4j import GraphNeo4j
from core import core

class App():

    def __init__(self, settings):
        self.settings = settings
        self.graph4j = GraphNeo4j(**settings['neo4j'])

    def __getitem__(self, k):
        return getattr(self, k)

    def extract_transform(self):
        return core.extract_transform(self.settings)

    def etl(self, dfs=None):
        if dfs is None:
            dfs = self.extract_transform()
        return core.load(self.graph4j, dfs, self.settings['load'])



def run_app(settings, action):
    app = App(settings)
    try:
        res = app[action]()
        return res
    except Exception as e:
        print('====== FAIL ======')
        utils.pretty_print(e.args)
        if len(app.graph4j.queries):
            print(app.graph4j.queries[-1])





if __name__ == '__main__':
    run_app(utils.get_settings(), sys.argv[2])