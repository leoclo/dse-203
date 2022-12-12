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

https://www.kaggle.com/datasets/stephanerappeneau/350-000-movies-from-themoviedborg

Download the dataset and unzip the archive folder into folder src/files. The files should be in src/files/archive.

## Running ETL

With the pyenv activate:

```bash
source venv/bin/activate
```

Run the following

```bash
 python src/app.py settings.json etl

```

On your browser login to neo4j on the following URL:

http://localhost:7474/browser/

Got to the database and see Node labels created

Note:

There is a notebook in root folder called final_app.ipynb that can also be used for
using app modules

# How it works

We use a JSON file to set the behavior of the



With the graph created, this query is then passed in to create the final keyword node, which unravels the topic nodes into their component keywords and merge them together by their unique value. This allows the nodes to connect across the scope of all movies, not just within the batch of 30.


'''

'''

Note: the keyword comes from the topic node, not the overview of the movies they link to, and as such might not actually be in the overview.

# Queries For Project

- What popular keywords does the romance genre turn up? Does it compare meaningfully from comedy? What about Warner Brothers company next to Paramount? Are the differing words informative enough that we can use keywords to differentiate the two?

```
MATCH (k:Keyword)--(m:Movie)--(a:Genre {name: "Romance"}) with a.name AS genre, k.keyword AS word, COUNT() as present
RETURN word
ORDER BY present DESC LIMIT 10

MATCH (k:Keyword)--(m:Movie)--(a:Genre {name: "Comedy"}) with a.name AS genre, k.keyword AS word, COUNT() as present
RETURN word
ORDER BY present DESC LIMIT 10

MATCH (k:Keyword)--(m:Movie)--(a:Company {name: "Warner Bros."}) with a.name AS genre, k.keyword AS word, COUNT() as present
RETURN word
ORDER BY present DESC LIMIT 10

MATCH (k:Keyword)--(m:Movie)--(a:Company {name: "Paramount Pictures"}) with a.name AS genre, k.keyword AS word, COUNT() as present
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

###  Drama films by Roman Polanski that were nominated

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
WHERE  d.name='Roman Polanski'AND g.name = 'Drama' AND any(x IN t.topics WHERE x IN ['spacecraft'])
RETURN DISTINCT t.topics, d.name, a.name, m.title, aw.award_company, aw.award_type, aw.year, g.name
```
