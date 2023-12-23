#!/usr/bin/env python3
print("version2")
import sys
import csv

# You are going to want to start with your homework4 graph.py file,
# but you will want to add/modify things to support the notion of
# multiple valid edges between two nodes.

import graph

# Needed for the "Gimme20" method
import json

class Baconator():

    def __init__(self, filename):
        """Filename is a .csv file, where the first column is the
        movie name and the subsequent columns are the actors.  There
        is NO header on the .csv file.
        """
        # alt = dont touch bfs,just get the nodes and edit all_Edges to iterate through that node's edges
        # then find the movie common to the previous actor and take that as the weight
        self.bacongraph = graph.Graph()

        with open(filename, "r") as csvfile: # opens file in read mode
            reader = csv.reader(csvfile) # creates a reader object, allows iteration
            for row in reader: 
                movie = row[0] 
                actors = row[1:] 
                #movies and actors are being read correctly...

                 # add actor nodes
                for actor in actors:
                    if actor not in self.bacongraph: 
                        self.bacongraph[actor] = None

                    for other_actor in actors:
                            if other_actor != actor:
                                #connect takes in the names
                                self.bacongraph.connect(actor, other_actor, movie)
           
    
    def find_min_baconpath(self, actor):
        """Returns a minimum length baconpath between the named actor
        and "Kevin Bacon", or None if no such path exists or if the
        actor is not found.

        A baconpath is a python list of the form [actor, movie, actor,
        movie..] with the final actor being "Kevin Bacon", and for
        every movie the actor both before and after the movie title
        appeared in that movie.

        As an example, a minimum baconpath for the actor Zoe Saldana is:

        ['Zoe Saldana', 'Guardians of the Galaxy', 'Brendan Fehr', 'X-Men: First Class', 'Kevin Bacon']

        That is, Zoe Saldana appeared in Guardians of the Galaxy with
        Brendan Fehr, who appeared in X-Men: First Class with Kevin
        Bacon.

        The best way to discover a baconpath is a breadth first
        traversal, either starting from the targeted actor or Kevin
        Bacon and using the resulting path as the minimum baconpath.

        You are going to need to modify your graph.py file as well to
        support multiple edges, as two actors can be in multiple
        movies together, but the baconpath itself only includes one of
        the movies.

        """
        
        print("starting find min baconpath for kevin to "+str(actor))
        myPath = []
        kevinNode = None
        curMovie = None
        #if actor is kevin bacon, min path is [kb]
        if actor == "Kevin Bacon":
            myPath.append(actor)
            return myPath
        
        #what if the actor isn't in the graph ?
        if actor not in self.bacongraph:
            return None
        foundBacon = False
        for actorNode in self.bacongraph.bfs_traversal(actor): #actor is the start
            if actorNode.name == "Kevin Bacon":
                foundBacon = True
                kevinNode = actorNode #kevinNode = graphnode
        if foundBacon == False:
            return None
        

        while kevinNode.previous != None:

            movie = kevinNode.previous.edges[kevinNode][0]
            myPath.append(kevinNode.name)
            myPath.append(movie) #changed from movie
            print(myPath)
            kevinNode = kevinNode.previous
            print(kevinNode)
        
        print(myPath)
        if kevinNode.name == actor: # arrived at the actor
            myPath.append(actor) 
            return list(reversed(myPath)) # should be from [ actor --> kevin bacon]
        else:
            return []
        
    
    def is_baconpath(self, path):
        """A check to see if something is a valid Baconpath, but not
        necessarily a minimal baconpath"""

        """
          make sure the actors are actually connected to each other by that movie
          check the graphnode to see if the weight between the 2 actors is the movie

          garnered from gradescope tests:
          bacon --> in the cut --> bacon = valid path
          end of the list should be kevin bacon

          problem:
          testing non list, empty list, and known wrong length for is_baconpath
            Testing that nonexistant name gives an empty list OR None when trying to find a baconpath

            Test Failed: Unable to find nobody
        """
        print("check is_baconpath for : "+str(path))
        # not a list
        if not isinstance(path, list):
            return False
        # 0 length
        if len(path) == 0:
            return None # changed from false
        # 1 length
        if len(path) == 1:
            if path == ["Kevin Bacon"]:
                return True
            else:
                return False
        # known wrong path length ?? not odd ? 
        if len(path) % 2 == 0:
            return False
        #check 1 : is kevin in the path?
        foundBacon = False
        if path[len(path)-1] != "Kevin Bacon":
            return False
        else: 
            foundBacon = True
            print("foundBacon!")

        # check 2 : are all of the actors actually actors?
        i = 0
        while i < len(path)-2:
            actor = path[i]
            if actor not in self.bacongraph:
                return False
            i += 2
 
        # check 3: are the actors connected by that movie?
        rightMovie = True
        i = 0
        while i < len(path)-2:
            actor = path[i]
            actor2 = path[i+2]
            movie = path[i+1]

            # check if actors are connected
            if actor != actor2 and self.bacongraph.connected(actor, actor2) == False:
                return False
                

            # check if they're connected by that movie
            dict1 = self.bacongraph[actor].edges #other actors actor is connnected to
            dict2 = self.bacongraph[actor2].back_edges #other actors actor2 is connected to
            otherActorNode = self.bacongraph[actor2] #gets the node of actors, since keys of .edges are nodes
            actorNode = self.bacongraph[actor]
            
            # edge case: actors are kevin bacon
            if actor == "Kevin Bacon" and actor2 == "Kevin Bacon": 
                rightMovie = True
            else:
                if movie not in dict2[actorNode] or movie not in dict1[otherActorNode]:
                    rightMovie = False
            i += 2

        return foundBacon and rightMovie

    def is_min_baconpath(self, path):
        """This should additionally check if a valid Baconpath is minimal"""
        assert self.is_baconpath # check if its a valid baconpath
        actor = path[0]
        #if looking for min path from bacon to bacon, should be [bacon]
        if actor == "Kevin Bacon":
            if path != ["Kevin Bacon"]:
                return False
        
        # check if the 2 list lengths are the same
        if len(path) == len(self.find_min_baconpath(actor)):
            return True
        return False        

    def gimme_20(self):
        """This should return a string that is a JSON object for an
        entry in the tests list

        https://gradescope-autograders.readthedocs.io/en/latest/specs/

        that will be visible, and have a score of 20 and a max-score
        of 20, and be named 'gimme 20' """
        answer = {
            "score": 20,
            "max_score": 20,
            "visibility": "visible",
            "name": "gimme 20"
        }

        # Convert the dictionary to a JSON string
            # indent = more readable
        json_answer = json.dumps(answer, indent=2)
        return json_answer
    
if __name__ == "__main__":
    baconator = None
    if len(sys.argv) > 1:
        baconator = Baconator(sys.argv[1])
    else:
        baconator = Baconator("moviedata.csv")
   
    path = baconator.find_min_baconpath("Taylor Swift")
    print(path)

    # given = ['Nicholas Weaver', 'Deep Web', 'Meg Ryan', 'In the Cut', 'Kevin Bacon']
    # assert baconator.is_baconpath(given)

    
    # Some basic sanity tests, since Meg Ryan only appeared in one
    # movie with Kevin Bacon we know this is the only valid minimum
    # baconpath.
    # path = baconator.find_min_baconpath("Meg Ryan")
    # print("path: " + str(path))
    # assert path == ['Meg Ryan', 'In the Cut', 'Kevin Bacon']

    # assert baconator.is_baconpath(path)
    # assert baconator.is_min_baconpath(path)

    # assert not baconator.is_baconpath(['Meg Ryan'])
    # assert baconator.is_baconpath(['Meg Ryan', "You've Got Mail",
    #                                "Tom Hanks", "Apollo 13", 'Kevin Bacon'])
    # assert not baconator.is_min_baconpath(['Meg Ryan', "You've Got Mail",
    #                                        "Tom Hanks", "Apollo 13",
    #                                        'Kevin Bacon'])
    
    # path[1] = "bogus"
    # assert not baconator.is_baconpath(path)

