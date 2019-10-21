######################
# Graph.py
######################
"""
Defines all necessary classes and functions for the implementation of a Graph
data structure. The main method used for storing vertices and connections is
through a dictionary, where each key-value pair in the dictionary member for a
vertex represents a connected neighbor of that vertex (key) and the weight of
the edge between the two vertices (value).
"""
import math
# This seemed to be the only way that I could import queue without errors
try:
    import queue
except ImportError:
    import Queue as queue
class Vertex:
    """
    A vertex within the graph. Stores connections  and edgeswith a dictionary
    object
    """
    def __init__(self, k=0):
        """
        Constructor
        :param k: the alias of the vertex
        """
        self.name = k
        self.connections = {}
    def insertNeighbor(self, nbr, weight):
        """
        :param nbr: id of the vertex which will become a neighbor
        :param weight: the weight of the edge between self and nbr
        """
        self.connections[nbr] = weight
class Graph:
    """
    A graph object that uses a hybrid of an adjacency matrix and dictionaries to
    store vertices and keep track of connections
    """
    def __init__(self, n):
        """
        Constructor
        :param n: Number of vertices
        """
        self.order = n
        self.size = 0
        # You may put any required initialization code here
        self.vertices = [None] * n
        # fill vertices list with vertices ranging 0 to n
        for i in range(0, n):
            self.vertices[i] = Vertex(i)
        # adjacency matrix for use in find_min_weight_path and is_bipartite
        self.adjacency_mat = [[0]*n for _ in range(n)]
    def insert_edge(self, u, v, w):
        """
        Inserts an edge between vertices u and v with weight w
        :param u: source vertex
        :param v: neighboring vertex
        :param w: weight of edge between the two vertices
        """
        # make sure the vertices are in the graph
        if not self.vertices[u] or not self.vertices[v]:
            raise IndexError
        # if they're not connected, increase size,
        if not self.are_connected(u, v):
            self.size += 1
        # update information in vertices list and adjacency matrix
        self.vertices[u].connections[v] = w
        self.vertices[v].connections[u] = w
        self.adjacency_mat[u][v] = w
        self.adjacency_mat[v][u] = w
    def degree(self, v):
        """
        Returns the number of neighbors a given vertex has
        :param v: the vertex in question
        :return: # of neighbors
        """
        # make sure the vertex exists in the graph
        if not self.vertices[v]:
            raise IndexError
        # return length of connections dictionary for vertex v
        return len(self.vertices[v].connections)
    def are_connected(self, u, v):
        """
        Determines whether two vertices are directly connected (neighbors) to
        one another
        :param u: vertex 1
        :param v: vertex 2
        :return: whether the two are neighbors
        """
        # make sure the vertices are in the graph
        if not self.vertices[u] or not self.vertices[v]:
            raise IndexError
        # return if v is in the list of keys of u's neighbors
        return v in self.vertices[u].connections
    def is_path_valid(self, path):
        """
        Determins if a path is an actually valid path in a graph
        :param path: a list of vertices
        :return: if the path exists in the graph
        """
        # loop through all vertices in path except last one
        for i in range(0, len(path) - 1):
            # make sure that vertex is in the graph
            if not self.vertices[path[i]]or not self.vertices[path[i+1]]:
                raise IndexError
            # if the vertex at i + 1 is not a neighbor of vertex at i,
            # the path is not valid
            if path[i+1] not in self.vertices[path[i]].connections:
                return False
        # if it gets here, return true
        return True
    def edge_weight(self, u, v):
        """
        Returns the weight of the edge between vertices u and v
        :param u: vertex 1
        :param v: vertex 2
        :return: the weight of the edge between the two
        """
        # make sure they're connected in the first place
        if not self.are_connected(u, v):
            return math.inf
        else:
            # return the value in vertex dictionary member connections at key v
            return self.vertices[u].connections[v]
    def path_weight(self, path):
        """
        Gives the total weight of a path between vertices
        :param path: a list of vertices to travel between in the graph
        :return: the total weight of the path
        """
        # make sure the path exists
        if not self.is_path_valid(path):
            return math.inf
        w = 0   # init weight
        # add the weight of each connection between sequential vertices in path
        # from start to finish
        for i in range(0, len(path) - 1):
            w += self.vertices[path[i]].connections[path[i+1]]
        # return
        return w
    def does_path_exist(self, u, v):
        """
        Determines whether a path actually exists between two vertices using BFS
        :param u: vertex 1
        :param v: vertex 2
        :return: whether there exists a path between the two vertices or not
        """
        seen = set()
        # make sure vertices exist in the graph
        if not self.vertices[u] or not self.vertices[v]:
            raise IndexError
        # initialize queue and place first vertex in there
        q = queue.Queue()
        q.put(u)
        # keep looping until queue is empty
        while not q.empty():
            # get first vertex in queue
            vert = q.get()
            # if it's the vertex we're looking for (v), we're done
            if vert == v:
                return True
            # look through all of the neighbors of vert that haven't been
            # visited already
            for nbr in self.vertices[vert].connections.keys():
                if nbr not in seen:
                    # put that unvisited vertex in the queue and into visited
                    # set
                    q.put(nbr)
                    seen.add(nbr)
        # if it isn't found at all, there is not a path to it
        return False
    def find_min_weight_path(self, u, v):
        """
        Finds the minimum weighted path between two vertices using Djikstra's
        Algorithm
        :param u: vertex 1
        :param v: vertex 2
        """
        # make sure that a path does exist in the first place
        if not self.does_path_exist(u, v):
            raise ValueError
        # if u and v are the same thing, it's trivial
        if u == v:
            return [u]
        # initialize distance list, all indices at infinity
        dist = [float("inf")] * self.order
        # parent list: at each index is the vertex that comes before it in the
        # path from u to v
        parent = [-1] * self.order
        # dist from u to u is 0
        dist[u] = 0
        # empty queue
        q = []
        # add all vertices to the queue
        for i in range(self.order):
            q.append(i)
        # while queue isn't empty
        while q:
            # find vertex that is minimum distance from vertex u in graph that
            # hasn't been visited already
            i = self.min_dist(dist, q)
            # if that vertex is v, we just have to make the path list now
            if i == v:
                break
            # remove that vertex from the queue: it has been visited
            q.remove(i)
            # loop through all vertices min vertex could be connected to
            for j in range(self.order):
                # if there exists a connection between min vertex and another
                # one and that other vertex hasn't been visited yet
                if self.adjacency_mat[i][j] and j in q:
                    # AND the weight of the path to the min vertex + the weight
                    # of the edge between these two vertices is less than the
                    # currently stored path weight from start to j,
                    if dist[i] + self.adjacency_mat[i][j] < dist[j]:
                        # update the path weight
                        dist[j] = dist[i] + self.adjacency_mat[i][j]
                        # name the parent of j to be i
                        parent[j] = i
        # get the path using parent list from u to v
        return get_path(v, parent)
    def min_dist(self, dist, q):
        """
        Finds the vertex that hasn't been visited yet with the shortest path
        from the source vertex in find_min_weight_path (Helper function)
        :param dist: a list containing the distances each vertex is away from
        source vertex
        :param q: the queue containg unvisited vertices
        :return: the index of the vertex with shortest path from source that
        hasn't been visited yet
        """
        # initialize minimum and min index params for certain mutability
        minimum = float("inf")
        mindex = -1
        # loop through each vertex
        for x in range(self.order):
            # if that vertex hasn't been visited yet and has a shorter path than
            # others we've already seen
            if dist[x] < minimum and x in q:
                # update minimum and minimum index
                minimum = dist[x]
                mindex = x
        return mindex
    def is_bipartite(self):
        """
        Determines if a graph is bipartite or not using the two-colored vertex
        test
        Color array works like this:
        -1 = Color has not been decided yet
        1 = 1st color
        0 = 2nd color
        :return: if the graph is bipartite
        """
        # Loop through adjacency matrix to find first vertex that we can use as
        # a "source"
        for i in range(0, self.order):
            for j in range(0, self.order):
                if self.adjacency_mat[i][j]:
                    src = i
                    break
            if src == i:
                break
        # initialize a color array with all vertices undecided (-1)
        colorArr = [-1] * self.order
        # make source color a 1
        colorArr[src] = 1
        # init queue and append the source to it
        q = []
        q.append(src)
        # while the queue isn't empty
        while q:
            # get last item in queue
            u = q.pop()
            # if that vertex has a connection to itself, graph cannot be
            # bipartite
            if self.adjacency_mat[u][u]:
                return False
            # loop through all possible connections to vertex u in question
            for v in range(0, self.order):
                # if a connection exists and the second vertex in the connection
                # hasn't been visited yet
                if self.adjacency_mat[u][v] and colorArr[v] == -1:
                    # update color based on its parent
                    colorArr[v] = 1 - colorArr[u]
                    # append that vertex to the queue
                    q.append(v)
                # if the connection exists and the color of child and parent are the same, then it can't be a bipartite graph
                elif self.adjacency_mat[u][v] and colorArr[v] == colorArr[u]:
                    return False
        # return true if you get here
        return True
def get_path(v, parent):
    """
    Gets the min weight path from u to v using the parent list. Goes
    backwards in adding vertices to the path list, starting at v and ending
    at u
    :param u: vertex 1
    :param v: vertex 2
    :param parent: a list that holds the parent vertex of each vertex in the
    min path. First vertex has parent "-1"
    """
    path = []
    # make temp variable for v so you can append v at the end
    i = v
    # while you aren't at the starting vertex u
    while parent[i] != -1:
        # insert the parent of each vertex at front of path list
        path.insert(0, parent[i])
        i = parent[i]
    # add the last vertex to the end and return
    path.append(v)
    return path
    
