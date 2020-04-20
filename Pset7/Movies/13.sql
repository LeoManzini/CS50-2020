SELECT name FROM people WHERE id in
(SELECT person_id FROM stars WHERE id in
(SELECT movie_id FROM stars WHERE person_id =
(SELECT id FROM people WHERE name = 'Kevin Bacon')));