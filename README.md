# Neo4j dse-203 Final Project

# Introduction

Project to create graph database for movies kaggle dataset and custom data crawlers for the DSE 203 course

Clone the repository or download the .zip file and extract it on the desired directory


## Local Enviroment Setup with Docker
___

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
___

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


## Wikipedia/DBPedia data points

- Movies
- Directors

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

## Tasks

- [ ] Need to find directors from a given movie name (All movies details cleaned dataset)
  - Use movie titles, search via wikipedia or dbpedia for the movie director. Try to get tmbd/imbdb ID so we can easily match entites.
- [ ] Join together relationship

## Nodes
- Person
  - tmdbID (optional)
- Movie
 - Title
 - tmbdID
- Award
- Language
- Genre

## Relationships

- Directed (Person->Movie)
- Acted_In (Person->Movie)
- Speaks (Movie->Language)
- Won (Person->Award)
  - Years
- Nominated (Person->Award)
  - Years
- Belongs_In (Movie->Genre)
