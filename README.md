# Neo4j dse-203 Final Project

# Introduction

This project is to create graph database for movies kaggle dataset and custom data crawlers to extract award data from wikipedia.

(Paraphrased from the Presentation)
This program creates a knowledge graph from a dataset containing 800-900 movie directors, the movies they directed, the awards they won, as well as the cast of the movies these directors worked on.

The graph's object is to determine what we can use to describe the similarity of movies’ contents besides genre, such as if we can take keywords from a movie’s summary and categorize them using them instead. What (dis)similarities would they find?

We also wanted to see if there are opportunities to create or rediscover working relationships between actors based on commonly-shared networks of people.

## Acquiring the repository

Clone the repository or download the .zip file and extract it on the desired directory

## Local Enviroment Setup with Docker

---

To setup app local enviroment install [docker](https://docs.docker.com/get-docker/)
and run the following command on the root directory of the project, this will create
containers. For reference [neo4j docker](https://neo4j.com/docs/operations-manual/current/docker/introduction/).

```bash
make run
```

On your browser you will be able to login to neo4j on the following URL: http://localhost:7474/browser/
Username: neo4j
Password: 1234

## Local Installation

---

Create a virtual environment with the command:

```bash
python3 -m venv venv
```

Activate the created enviroment:

```bash
source venv/bin/activate
```

Install the requirements for the project

```bash
pip install -r requirements.txt
```

## Dataset Download Kaggle

Download the dataset archive from the download button at the top and unzip the archive folder into folder src/files. The files should be in src/files/archive and you should get the following tree.

- [repository root]
  - src
    - files
      - archive
        - 220k_awards_by_directors.csv
        - 500 favorite directors_with wikipedia summary.csv
        - AllMoviesCastingRaw.csv
        - AllMoviesDetailsCleaned.csv
        - language to country.csv
        - MostCommonLanguageByDirector.csv
        - spielberg_awards.csv
        - 900_acclaimed_directors_awards
          - 900_acclaimed_directors_awards.csv

## Running ETL

Run the final_app.ipynb notebook for complete graph creation

On your browser login to neo4j on the following URL:

http://localhost:7474/browser/

Got to the database and see Node labels created

Note:

There is a notebook in root folder called final_app.ipynb that can also be used for
using app modules

# How it works

final_app.ipynb:

```
settings = utils.get_settings_notebook('../settings_topics.json')

```

We use a JSON file to set the behavior of the overall program. This determines where the .csv source files are kept, how the columns should be mapped, and how the nodes are created and loaded in from the pre-processed data. It also has a switch for whether or not the web crawler is activated during the run.

`settings_topics.json` simply loads in the data for directors, cast, and movies, and does not perform any actions with neo4j.

final_app.ipynb:

```
app = App(settings)
dfs = app.extract_transform()
```

We start by runing `extract_transform()`, which performs the action of both extracting the data from the csv files and transforming them into a dictionary of dataframes called `dfs`.

core.py:

```
def extract_transform(settings):
    df_transform = DataFrameTransform()

    if settings['crawler']['on']:
        crawler_award(settings)

    for k, meta in settings['transform'].items():
        df = pd.read_csv(**settings['extract'][k])
        df = df[meta['column_map'].keys()]
        df.rename(columns=meta['column_map'], inplace=True)
        df = df[meta['column_map'].values()]
        df_transform[k](df)

    return df_transform.dfs
```

The extraction process takes a dictionary in which the keys are the names of columns in the csv, and maps them to a new dataframe with the value designating the target column in the dataframe. Not all columns need to be selected.

We also perform a crawl using `crawler_award(settings)` if enabled, which writes out the award files first before they are extracted.

While each dataframe is extraccted, it undergoes a transformation in `df_transform[k](df)` which preprocesses the data and adds it to `df_transform.dfs`.

Using `settings_topics.json`, we extract and transform the movie, cast, and director dataframes.

final_app.ipynb:

```
movie_topics = gen_topics()
# (df_movie_topics, df_topic_words) = movie_topics.batch_process(data_df['movies'][data_df['movies']['lang'] == 'en'])
(df_movie_topics, df_topic_words) = movie_topics.batch_process(dfs['movies'][
    dfs['movies']['overview'].apply(lambda x: x is not None and len(x) > 30)
])
df_topic_words.reset_index(drop=True, inplace=True)
df_movie_topics.reset_index(drop=True, inplace=True)
# display(df_topic_words)
# display(df_movie_topics)
df_topic_words.to_csv('./files/archive/topic_words.csv', index=True)
df_movie_topics.to_csv('./files/archive/movie_topic_ids.csv', index=True)
```

Using this limited dictionary of dataframes, we take the movies we prunned down to and generate topics for them and write them into a file.

With the graph created, a query is then passed in to create the final keyword node, which unravels the topic nodes into their component keywords and merge them together by their unique value. This allows the nodes to connect across the scope of all movies, not just within the batch of 30.

final_app.ipynb:

```
settings = utils.get_settings_notebook('../settings.json')
app = App(settings)
app.etl()
```

Using `settings.json` extracts from all the files, including data for awards and topics.

`app.etl` calls the same `extract_transform()` function from before, but with the new settings file, all the data we are working with is extracted and transformed. Then, using the connection and authentication data provided in the settings file, connects to neo4j and exports the information in the dataframes to the database based on the template provided by the settings file.

final_app.ipynb:

```
graph4j = GraphNeo4j(**{**settings['neo4j'], 'clear_data': False})
qry = '''
    MATCH (t:Topic)<-[]-(m:Movie) UNWIND(t.topics) as keyword
    MERGE (k:Keyword {keyword: keyword})
    MERGE (k)<-[:HAS_KEYWORD]-(m)
'''
graph4j.run_query(qry, {})
```

Lastly, the first query for the new data is executed so as to create the keyword nodes from the topic nodes and link them up with all the movies each keyword is associated with by topic.

Note: Since the keyword comes from the topic node, not the overview of the movies they link to, the keyword value might not actually be in the overview.

# Queries For Project

- What popular keywords does the romance genre turn up? Does it compare meaningfully from comedy? What about Warner Brothers company next to Paramount? Are the differing words informative enough that we can use keywords to differentiate the two?

```
MATCH (k:Keyword)--(m:Movie)--(a:Genre {name: "Romance"}) with a.name AS genre, k.keyword AS word, COUNT(*) as present
RETURN word
ORDER BY present DESC LIMIT 10

MATCH (k:Keyword)--(m:Movie)--(a:Genre {name: "Comedy"}) with a.name AS genre, k.keyword AS word, COUNT(*) as present
RETURN word
ORDER BY present DESC LIMIT 10

MATCH (k:Keyword)--(m:Movie)--(a:Company {name: "Warner Bros."}) with a.name AS genre, k.keyword AS word, COUNT(*) as present
RETURN word
ORDER BY present DESC LIMIT 10

MATCH (k:Keyword)--(m:Movie)--(a:Company {name: "Paramount Pictures"}) with a.name AS genre, k.keyword AS word, COUNT(*) as present
RETURN word
ORDER BY present DESC LIMIT 10
```

- Which actors that have not worked in the current list of movies have won in the same award category and share keywords between the movies?

```
MATCH (a:Person)-[:ACTED_IN]->(m:Movie)--(b:Person)--(n:Movie)<-[:ACTED_IN]-(c:Person),
(a)-[:WON]->(w1:Award),
(c)-[:WON]->(w2:Award),
(m)-[:HAS_KEYWORD]->(k:Keyword)<-[:HAS_KEYWORD]-(n)
WHERE a.name < c.name AND w1.award_type = w2.award_type
AND NOT (a)--(:Movie)--(c) AND k.keyword = 'friend'
RETURN DISTINCT a.name, c.name,  k.keyword
```

- In the same vein, which actors that have not worked in the current list of movies are likely to have done so in an unlisted film, based on the network of people they’ve worked in common with?
  - A and B have not worked together in the given movies.
  - Find actors A and B have in common from other movies. So if actor A and B have worked with actor C and director X in a movie.
  - Actors must speak at least one common language (determined by original language of movies worked in)
  - Give the top 10 actors by # of finds for that specific actor.

```
MATCH (a:Person)-[:ACTED_IN]->(m:Movie)--(b:Person)--(n:Movie)<-[:ACTED_IN]-(c:Person)
WHERE a.name < c.name
WITH a, c, COUNT(*) AS network
WHERE NOT (a)--(:Movie)--(c)
RETURN a.name, c.name, network ORDER BY network DESC LIMIT 10
```

## Nodes

- Person
  - name (string)
  - gender (int)
- Movie
  - movie_id (int)
  - lang (string)
  - title (string)
  - imdbID (string)
  - overview (string)
- Award
  - award_id (string)
  - award_comany (string)
  - award_type (string)
  - award_year (int)
- Company
  - name (string)
- Genre
  - name (string)
- Topic (temporary)
  - topic_id (int)
  - topics (String[])
- Keyword
  - keyword (string)

## Relationships

- DIRECTED (Person->Movie)
- PRODUCED (Compnay->Movie)
- ACTED_IN (Person->Movie)
- ACTED_IN (Person->Award)
- NOMINATED (Person->Award)
- HAS_GENRE (Movie->Genre)
- HAS_TOPIC (Movie->Topic)
- HAS_KEYWORD(Movie->Keyword)

# Other Interesting Queries

### From the notebook, reorganize topics into keywords. Reaches outside of the slices the topics were made.

```
MATCH (t:Topic)<-[]-(m:Movie) UNWIND(t.topics) as keyword
MERGE (k:Keyword {keyword: keyword})
MERGE (k)<-[:HAS_KEYWORD]-(m)
```

### Most number of keywords used by movies

```
MATCH (m:Movie)-[:HAS_KEYWORD]-(k:Keyword)
RETURN k, COUNT(m) as amt_movies
ORDER BY amt_movies DESC

```

### Keywords that were most nominated for awards

```
MATCH (m:Movie)-[:HAS_KEYWORD]-(k:Keyword),
      (m:Movie)-[:NOMINATED]-(a:Award)
RETURN k, COUNT(m) as amt_movies
ORDER BY amt_movies DESC

```

### Comedy films by Quentin Tarantino

```
MATCH (a:Person)-[:ACTED_IN]-(m:Movie)-[:DIRECTED]-(d:Person), (m:Movie)-[:HAS_GENRE]-(g:Genre)
WHERE d.name='Quentin Tarantino' AND g.name = 'Comedy'
RETURN DISTINCT a.name, m.title
```

### Movies produced by Vía Digital

```
MATCH (m:Movie)-[:PRODUCED]-(c:Company)
WHERE c.name='Vía Digital'
RETURN DISTINCT m.title
```

```
MATCH (a:Person)-[:NOMINATED]-(aw:Award), (a:Person)-[:ACTED_IN]-(m:Movie)
RETURN DISTINCT a.name, aw.year, aw.award_company, aw.award_type, m.title
```

### Awards won by Quentin Tarantino for action films

```
MATCH
	(a:Person)-[:ACTED_IN]-(m:Movie)-[:DIRECTED]-(d:Person),
	(m:Movie)-[:HAS_GENRE]-(g:Genre),
	(a:Person)-[:NOMINATED]-(aw:Award)
WHERE d.name='Quentin Tarantino' AND g.name = 'Action'
RETURN DISTINCT a.name, m.title, aw.award_company, aw.award_type
```

### Drama films by Roman Polanski that were nominated

```
MATCH
	(a:Person)-[:ACTED_IN]-(m:Movie)-[:DIRECTED]-(d:Person),
	(m:Movie)-[:HAS_GENRE]-(g:Genre),
	(a:Person)-[:NOMINATED]-(aw:Award)
WHERE  d.name='Roman Polanski'AND g.name = 'Drama'
RETURN DISTINCT d.name, a.name, m.title, aw.award_company, aw.award_type, aw.year, g.name
```

### Drama films by Roman polanski that were nominated and has 'spacecraft' in its topic node

```
MATCH
	(a:Person)-[:ACTED_IN]-(m:Movie)-[:DIRECTED]-(d:Person),
	(m:Movie)-[:HAS_GENRE]-(g:Genre),
	(m:Movie)-[:HAS_TOPIC]-(t:Topic),
	(a:Person)-[:NOMINATED]-(aw:Award)
WHERE  d.name='Roman Polanski'AND g.name = 'Drama' AND any(x IN t.topics WHERE x IN ['pianist'])
RETURN DISTINCT t.topics, d.name, a.name, m.title, aw.award_company, aw.award_type, aw.year, g.name
```
