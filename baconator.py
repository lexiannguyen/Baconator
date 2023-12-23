#!/usr/bin/env python3

import sys
import csv

import graph

class Baconator():

    def __init__(self, filename):
        """Filename is a .csv file, where the first column is the
        movie name and the subsequent columns are the actors.  There
        is NO header on the .csv file.
        """
        #initializes graph
        self.bacongraph = graph.Graph()

        with open(filename, "r") as csvfile: # opens file in read mode
            reader = csv.reader(csvfile) # creates a reader object, allows iteration
            for row in reader: 
                movie = row[0] #movie is first in list
                actors = row[1:] #actors = rest of items in list

                 # add actor nodes if not already in it
                for actor in actors:
                    if actor not in self.bacongraph: 
                        self.bacongraph[actor] = None #initialize actor node
                    #connects the actor nodes
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

        Uses breadth first traversal and returns the minimum baconpath

        """
        
        myPath = []
        kevinNode = None
        #if actor is kevin bacon, min path is [kevin bacon]]
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
        
        #goes backwards from the traversal path
        while kevinNode.previous != None:

            movie = kevinNode.previous.edges[kevinNode][0]
            myPath.append(kevinNode.name)
            myPath.append(movie) 
            kevinNode = kevinNode.previous
        
        if kevinNode.name == actor: # arrived at the actor
            myPath.append(actor) 
            return list(reversed(myPath)) # should be from [ actor --> kevin bacon]
        else:
            return []
        
    
    def is_baconpath(self, path):
        """A check to see if something is a valid Baconpath, but not
        necessarily a minimal baconpath
        
        Makes sure the actors are actually connected to each other by that movie
        Checks the graphnode to see if the wreight btwn the 2 actors is the movie"""

    
          
        
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

