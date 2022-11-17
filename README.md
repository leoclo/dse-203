## Dataset

- https://www.kaggle.com/datasets/stephanerappeneau/350-000-movies-from-themoviedborg?select=AllMoviesDetailsCleaned.csv
- https://www.kaggle.com/datasets/stephanerappeneau/350-000-movies-from-themoviedborg?select=220k_awards_by_directors.csv
- https://www.kaggle.com/datasets/stephanerappeneau/350-000-movies-from-themoviedborg?select=AllMoviesCastingRaw.csv

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
