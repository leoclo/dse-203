# Neo4j dse-203 Final Project

# Introduction

Project to create graph database for movies kaggle dataset and custom data crawlers for the DSE 203 course

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

Download the dataset and unzip in folder src/files

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

There is a notebook in root folder called app.ipynb that can also be used for
using app modules

## Questions

- Which directors have the most of awards in a genre ?
- Find actors who worked with the same director but not in the same movie ?
- Find actors who won awards with the same director in the same movie genre ?
- Which actors should work together in a movie ?
  - We could start by finding actors that never worked together but have worked with multiple actors in common. So IF actor A and B have worked with actor C and director X and have won awards with director X in genre Y.
  - A and B have never worked in a movie together.
  - Actors must speak at least one common language (determined by original language of movies worked in)
  - Give the top 10 actors by # of finds for that specific actor.
- Which actors work ONLY with directors who won 1 award or less.

## Nodes

- Person
  - Name (String)
- Movie
  - Language (String)
  - Production Country (String)
  - Genre (String)
  - Title (String)
  - tmbdID (String)
  - imdbID (String)
  - budget (int)
  - popularity (float)
- Award
  - Name (String)
- Production Company
  - Name (string)

## Relationships

- Directed (Person->Movie)
- Produced (Production Compnay->Movie)
- Acted_In (Person->Movie)
- Won (Person->Award)
  - Years (Int[])
- Nominated (Person->Award)
  - Years (Int[])

# Interesting Queries

### Reorganize topics into keywords. Reaches outside of the slices the topics were made

```
MATCH (t:Topic)<-[]-(m:Movie) UNWIND(t.topics) as keyword
MERGE (k:Keyword {keyword: keyword})
MERGE (k)<-[:HAS_KEYWORD]-(m)

```

### Most number of keywords used by movies

```
MATCH (m:Movie)-[:HAS_TOPIC]-(t:Topic)
UNWIND t.topics as t_topics
RETURN DISTINCT t_topics, COUNT(m) as amt_movies
ORDER BY amt_movies DESC

OR (With merge)

# Most number of keywords used by movies
MATCH (m:Movie)-[:HAS_KEYWORD]-(k:Keyword)
RETURN k, COUNT(m) as amt_movies
ORDER BY amt_movies DESC

```

### Keywords that were most nominated for awards

```
MATCH (m:Movie)-[:HAS_TOPIC]-(t:Topic),
      (m:Movie)-[:NOMINATED]-(a:Award)
UNWIND t.topics as t_topics
RETURN DISTINCT t_topics, COUNT(m) as amt_movies
ORDER BY amt_movies DESC

OR (With merge)

MATCH (m:Movie)-[:HAS_KEYWORD]-(k:Keyword),
      (m:Movie)-[:NOMINATED]-(a:Award)
RETURN k, COUNT(m) as amt_movies
ORDER BY amt_movies DESC

```

### Misc

```
MATCH (a:Person)-[:ACTED_IN]-(m:Movie)-[:DIRECTED]-(d:Person), (m:Movie)-[:HAS_GENRE]-(g:Genre)
WHERE d.name='Quentin Tarantino' AND g.name = 'Comedy'
RETURN DISTINCT a.name, m.title

MATCH (m:Movie)-[:PRODUCED]-(c:Company)
WHERE c.name='Vía Digital'
RETURN DISTINCT m.title

MATCH (a:Person)-[:NOMINATED]-(aw:Award), (a:Person)-[:ACTED_IN]-(m:Movie)
RETURN DISTINCT a.name, aw.year, aw.award_company, aw.award_type, m.title


MATCH
	(a:Person)-[:ACTED_IN]-(m:Movie)-[:DIRECTED]-(d:Person),
	(m:Movie)-[:HAS_GENRE]-(g:Genre),
	(a:Person)-[:NOMINATED]-(aw:Award)
WHERE d.name='Quentin Tarantino' AND g.name = 'Action'
RETURN DISTINCT a.name, m.title, aw.award_company, aw.award_type

MATCH
	(a:Person)-[:ACTED_IN]-(m:Movie)-[:DIRECTED]-(d:Person),
	(m:Movie)-[:HAS_GENRE]-(g:Genre),
	(a:Person)-[:NOMINATED]-(aw:Award)
WHERE  d.name='Roman Polanski'AND g.name = 'Drama'
RETURN DISTINCT d.name, a.name, m.title, aw.award_company, aw.award_type, aw.year, g.name


MATCH
	(a:Person)-[:ACTED_IN]-(m:Movie)-[:DIRECTED]-(d:Person),
	(m:Movie)-[:HAS_GENRE]-(g:Genre),
	(m:Movie)-[:HAS_TOPIC]-(t:Topic),
	(a:Person)-[:NOMINATED]-(aw:Award)
WHERE  d.name='Roman Polanski'AND g.name = 'Drama' AND any(x IN t.topics WHERE x IN ['spacecraft'])
RETURN DISTINCT t.topics, d.name, a.name, m.title, aw.award_company, aw.award_type, aw.year, g.name

```
