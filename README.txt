FIRST POINT:
We first parsed the JSON file and analyze the structure of the data, after that we created a dictionary in which the nodes were the ID of each author and the values are the list of the authors who the author of the key has worked with.
Then we created the Adjacency matrix in which there is a 1 if two authors share at least one publication and a 0 otherwise.
Taking into account the Adjacency matrix we created the weight matrix, if there is a 1 in the Adjacency matrix, we compute the Jaccard similarity to find the weight.
Now that we have the weight matrix and the adjacency matrix we proceed to create the graph G and then we save it into the same folder in which we are working to visualize it.

SECOND POINT:
Part A:
In this part we have created a list for the id_conference. This list was joined in a dictionary with the authors. So, for each id_conference as key, there are all the id_authors who participated at each conference. Then we created, given a conference in input, a subgraph induced with networkx by the set of authors who published at the input conference at least once. For this subgraph there are some centrality measures that has been plotted.
Part B:
For a given id_author as input we count the number of times that he has collaborate with the other authors, then we create a list of the authors that have collaborate with him at most d times and we plot the subgraph.
THIRD POINT
Part A:
We created a Dijsktra Algorithm to find the shortest path between a given id_author in input and the id of aris, if there is no possible path it will print “There is no path”.
Part B:
For this part we used the Dijkstra algorithm that we have created before, for the start node we use each one of the nodes in the graph G and the ending node of the path is each one of the nodes of the subset given in input, then for each path between each node of G and the nodes of the subset we find the minimum shortest path and assign it to the node of G we are working with
