import networkx as nx
import wikipedia as wiki
import matplotlib.pyplot as plt
import seaborn as sns

G=nx.DiGraph()
#change search_word here
search_word="Data Analysis"
first_list=list()
#find titles linked to the search word defined above
try:
   first_list=wiki.page(search_word).links
except wiki.exceptions.WikipediaException:
    #raise exception if something went wrong
    print("Error raised")
#If no links were found , exit
if len(first_list)==0:
    print("Error!No links found for this search word")
    exit(1)

print("There are "+ str(len(first_list))+" links related to "+search_word+"\n"+" List of links is:\n")
try:
  print(first_list)
except UnicodeEncodeError :
  print("Could not print out first list elements!")
second_list=list()

#loop through all links , add the node if it isn't a part of our graph already
#check for exceptions raised , add all links linked to that node into the graph as well
#repeat this procedure
for i in first_list:
    if (search_word,i) not in G.edges():
       G.add_edge(search_word,i)
    try:
        second_list=(wiki.page(i).links)
    except wiki.exceptions.WikipediaException:
        print("Error raised for " + i)
    for j in second_list:
        if (i,j) not in G.edges():
          G.add_edge(i,j)
#graph is created, analyze procedure follows
#remove nodes with an out degree equal to 0 since these nodes do not point any node of the graph and therefore they
#can be removed so that a better much smaller and easier version of the graph is produced, easier to visualize and
# with as less property losses of the originial graph as possible
nodes_to_delete=list()
for i in G.nodes():
    if G.out_degree(i)==0:
        nodes_to_delete.append(i)
#remove all of these nodes
G.remove_nodes_from(nodes_to_delete)
#first figure ,histplot for Degree distribution
plt.figure(figsize=(10,7), dpi= 80)
deg=list(dict(nx.degree(G)).values())
sns.histplot(deg,kde=True)
plt.ylabel('Count')
plt.xlabel('Degree')
plt.title("Degree distribution for "+search_word)
#second figure ,histplot for PageRank distribution
plt.figure(figsize=(13,8),dpi=80)
page_rank=list(nx.pagerank_numpy(G).values())
sns.histplot(page_rank,kde=True)
plt.ylabel('Count')
plt.xlabel('PageRank')
plt.title('PageRank distribution for '+search_word)
#third figure has twosubplots for two different centralities , histplot for Eigenvector centrality  distribution
plt.figure(figsize=(10,7), dpi= 80)
plt.subplot(1, 2, 1)
centrality = list(nx.eigenvector_centrality(G).values())
sns.histplot(centrality)
plt.ylabel('Count')
plt.xlabel('Eigenvector centrality')
plt.title('Eigenvector centrality distribution')

plt.subplot(1, 2, 2)
close_centrality=list(nx.closeness_centrality(G).values())
sns.histplot(close_centrality)
plt.ylabel("Count")
plt.xlabel("Closeness centrality")
plt.title("Closeness centrality distribution"  )
#fourth figure plots a histplot of clustering Coefficient distribution for all nodes of the graph generated
clustering_nodes=list(nx.clustering(G).values())
plt.figure(figsize=(10,7), dpi= 80)
sns.histplot(clustering_nodes)
plt.ylabel("Count")
plt.xlabel("Clustering Coefficient")
plt.title("Clustering Coefficient distribution for "+ search_word)

print(f"The radius of the UNDIRECTED graph is : {nx.radius(G.to_undirected())}\n")
print(f"The diameter of the UNDIRECTED graph is : {nx.diameter(G.to_undirected())}\n")
print(f"The density of the UNDIRECTED graph is: {nx.density(G.to_undirected())}\n")
center=nx.center(G.to_undirected())
print("The center of the graph consists "+str(len(center))+" node(s) and these are \n")
print(center)

periphery=nx.periphery(G.to_undirected())
print("The periphery of the graph consists "+ str(len(periphery))+" node(s) and these are :\n")
print(periphery)

print(f"The average shortest path length of the graph is:{nx.average_shortest_path_length(G)}")
print(f"The average node connectivity of the graph is :{nx.average_node_connectivity(G)}")
nx.write_gexf(G, search_word+".gexf")
plt.show()
