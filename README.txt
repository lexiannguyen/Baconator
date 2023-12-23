The primary problem is the "6 degrees of Kevin Bacon".  The actor
Kevin Bacon has appeared in numerous movies, so it is reasonable to
find a path from an arbitrary film actor to Kevin Bacon within a few
movies.

Thus the party game among movie trivia experts is to come up with a
"Bacon Path", a series of movies and actors to go from the starting
actor to Kevin Bacon.  Thus, for example, Zoe Saldana appeared in
Guardians of The Galaxy along with Brendan Fehr, while Brendan Feir
was also in X-Men: First Class with Kevin Bacon. [1]

And yes, there is a wikipedia page:

https://en.wikipedia.org/wiki/Six_Degrees_of_Kevin_Bacon


The problem consists of 4 primary functions: loading the movie
database (in a .csv file) into a graph, doing a graph traversal to
come up with a minimum Bacon Path for an intended actor, a validation
function to validate that a path is a valid Bacon Path, and a
validation function to validate that a path is a minimum distance
Bacon Path.

There is a final function where you need to return a string that
matches a JSON data format to get yourself 20 paints...


You are going to need to also start with your graph.py file from
Homework 4 and modify it as appropirate.  In particular the graph
edges become movies and a minimum bacon path is derived from a breadth
first traversal.  Since two actors can appear in multiple movies
together but the current design for graph.py only supports one edge
between two nodes this is clearly insufficient.

Note that the autograder will include a lot of corner case checks when
it is released in addition to the sanity checks, but unlike project 1
these tests will be visible.  You are strongly advised to write a lot
of checking code in the __main__ and/or python unit tests, but such
code will not be actively graded by the autograder.



[1] There is a similar game for academic citation, the "Erdos Number".
Nick's Erdos Number is 5: He coauthored with Vern Paxson, who
coauthored with Mark Handley, who coauthored with Richard Karp who
coauthored with Alon Noga who coauthored with Paul Erdos.  There is
also the "Erdos/Bacon Number" which is the sum of the two.
