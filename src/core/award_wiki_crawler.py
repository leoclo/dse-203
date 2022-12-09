import requests
from bs4 import BeautifulSoup

AWARD_COLS = ['award_company', 'award_type', 'movie', 'person', 'year']
AWARD_LIST = [
    {
        'award_company': 'oscars',
        'award_type': 'best_director',
        'url': 'https://en.wikipedia.org/wiki/Academy_Award_for_Best_Director'
    },
    {
        'award_company': 'oscars',
        'award_type': 'best_actor',
        'url': 'https://en.wikipedia.org/wiki/Academy_Award_for_Best_Actor'
    },
    {
        'award_company': 'oscars',
        'award_type': 'best_actress',
        'url': 'https://en.wikipedia.org/wiki/Academy_Award_for_Best_Actress'
    },
    {
        'award_company': 'oscars',
        'award_type': 'best_picture',
        'url': 'https://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture'
    },
    {
        'award_company': 'golden_globe',
        'award_type': 'best_director',
        'url': 'https://en.wikipedia.org/wiki/Golden_Globe_Award_for_Best_Director'
    },
    {
        'award_company': 'golden_globe',
        'award_type': 'best_actor',
        'url': 'https://en.wikipedia.org/wiki/Golden_Globe_Award_for_Best_Actor_%E2%80%93_Motion_Picture_Drama'
    },
    {
        'award_company': 'golden_globe',
        'award_type': 'best_actress',
        'url': 'https://en.wikipedia.org/wiki/Golden_Globe_Award_for_Best_Actress_in_a_Motion_Picture_%E2%80%93_Drama'
    },
    {
        'award_company': 'golden_globe',
        'award_type': 'best_picture',
        'url': 'https://en.wikipedia.org/wiki/Golden_Globe_Award_for_Best_Motion_Picture_%E2%80%93_Drama'
    }
]

def get_cell(cell):
    try:
        return cell.find_all('a')[0].text
    except:
        return cell.text

class AwardWikiCrawler():

    def __init__(self):
        self.dfs = {
            'award_won': {c: [] for c in AWARD_COLS},
            'award_nominated': {c: [] for c in AWARD_COLS}
        }

    def __getitem__(self, k):
        return getattr(self, k.replace('best_actress', 'best_actor'))

    def _append_to_dfs(self, key, d):
        for col in AWARD_COLS:
            self.dfs[key][col].append(d.get(col))
        return self

    def load_data(self, url, award_type, award_company):
        class_ref = {
            'oscars': 'wikitable sortable',
            'golden_globe': 'wikitable'
        }
        year = None
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        tables = soup.find_all('table', {'class': class_ref[award_company]})

        for decade_tb in tables:
            for i, row in enumerate(decade_tb.tbody.find_all('tr')[1:]):
                try:
                    d = {}
                    to_append = 'award_nominated'

                    if row.th and award_company == 'oscars':
                        year = row.th.find_all('a')[0].text
                        to_append = 'award_won'

                    if len(row.find_all('td')) == 1 and award_company == 'oscars':
                        year = row.td.find_all('a')[0].text.split('/')[0]
                        continue

                    assemble = self[f'{award_type}_{award_company}'](row)
                    if award_company == 'golden_globe' and 'year' in assemble:
                        year = assemble.pop('year')
                        to_append = 'award_won'

                    d = {
                        'award_type': award_type,
                        'award_company': award_company,
                        'year': year,
                        **assemble
                    }
#                     if d.get('movie') is None:
#                         continue

                except Exception as e:
                    print(row)
                    raise e

                if d:
                    self._append_to_dfs(to_append, d)

        return self

    def best_actor_oscars(self, row):
        d = {}
        for i, cell in enumerate(row.find_all('td')):
            if i == 0:
                d['person'] = get_cell(cell)
            if i == 2:
                d['movie'] = get_cell(cell)
        return d

    def best_director_oscars(self, row):
        d = {}
        for i, cell in enumerate(row.find_all('td')):
            if i == 0:
                d['person'] = get_cell(cell)
            if i == 1:
                d['movie'] = get_cell(cell)
        return d

    def best_picture_oscars(self, row):
        d = {}
        for i, cell in enumerate(row.find_all('td')):
            if i == 0:
                d['movie'] = get_cell(cell)

        return d

    def best_actor_golden_globe(self, row):
        d = {}
        for i, cell in enumerate(row.find_all('td')):
            if len(row.find_all('td')) == 4:
                if i == 0:
                    d['year'] = get_cell(cell)
                if i == 1:
                    d['person'] = get_cell(cell)
                if i == 3:
                    d['movie'] = get_cell(cell)

            if len(row.find_all('td')) == 3:
                if i == 0:
                    d['person'] = get_cell(cell)
                if i == 2:
                    d['movie'] = get_cell(cell)
        return d

    def best_director_golden_globe(self, row):
        d = {}
        for i, cell in enumerate(row.find_all('td')):
            if len(row.find_all('td')) == 3:
                if i == 0:
                    d['year'] = get_cell(cell)
                if i == 1:
                    d['person'] = get_cell(cell)
                if i == 2:
                    d['movie'] = get_cell(cell)

            if len(row.find_all('td')) == 2:
                if i == 0:
                    d['person'] = get_cell(cell)

                if i == 1:
                    d['movie'] = get_cell(cell)

        return d

    def best_picture_golden_globe(self, row):
        d = {}
        for i, cell in enumerate(row.find_all('td')):
            if len(row.find_all('td')) == 4:
                if i == 0:
                    d['year'] = get_cell(cell)
                if i == 1:
                    d['movie'] = get_cell(cell)
                if i == 2:
                    d['person'] = get_cell(cell)

            if len(row.find_all('td')) == 3:
                if i == 0:
                    d['movie'] = get_cell(cell)
                if i == 1:
                    d['person'] = get_cell(cell)

        return d

