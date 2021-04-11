from igraph import *
g = Graph()
g.add_vertices(6)
g.add_edges([(0,1)])
g.add_edges([(2,3)])
print(g)
g.vs['name'] = [i for i in range(10,16)]
g.es['label'] = [i for i in 'ab']
edge_idx = -1
for i in range(len(g.es)):
    if g.es[i]['label']=='b':
        edge_idx = i
        break
print(edge_idx)
u,v = g.get_edgelist()[edge_idx]
print("u: {}, v: {}".format(u,v))
# print(g.degree())
# # layout = g.layout_circle()
# # layout = g.layout("rt", [2])
# # layout = g.layout_reingold_tilford(root=[2])
# layout = g.layout("rt")
# g.vs["label"] = g.vs["name"]
# plot(g,layout=layout)