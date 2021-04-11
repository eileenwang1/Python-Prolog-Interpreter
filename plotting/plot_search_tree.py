from igraph import *
# test3
# output_dict={'0': {'X': 'X', 'Y': 'Y'}, '0-1': {'X': 'alice', 'Z': 'bob'}, '0-1-5': {'Y': 'charlie'}, '0-2': {'X': 'alice', 'Z': 'bertie'}, '0-2-4': {'Y': 'chuck'}, '0-3': {'X': 'charlie', 'Z': 'daisy'}, '0-4': {'X': 'bertie', 'Z': 'chuck'}, '0-4-6': {'Y': 'david'}, '0-5': {'X': 'bob', 'Z': 'charlie'}, '0-5-3': {'Y': 'daisy'}, '0-6': {'X': 'chuck', 'Z': 'david'}}
# test1
output_dict = {'0': {'X': 'mary', 'Y': 'X'}, '0-1': {'Z': 'tom_smith'}, '0-1-1': {'X': 'mary'}, '0-1-2': {'X': 'jack'}}

key_list = list(output_dict.keys())
key_list.sort()
key_tuple = tuple(key_list)
g = Graph()
vertice_num = len(key_tuple)+1
g.add_vertices(vertice_num)
if len(key_tuple)>0:
    curr_vertex = 1
    curr_parent = 0
    curr_path_len = 0
    for i in range(len(key_tuple)):
        curr_path_list = key_tuple[i].split('-')
        if len(curr_path_list) == curr_path_len + 1:
            curr_parent = curr_vertex-1
            g.add_edges([(curr_parent,curr_vertex)])

        elif (len(curr_path_list))==curr_path_len:
            g.add_edges([(curr_parent,curr_vertex)])
        
        elif (len(curr_path_list)<curr_path_len):
            curr_parent = -1
            parent_path = "-".join(curr_path_list[:-1])
            edge_idx = g.es.find(rule_path=parent_path).index
            u,v = g.get_edgelist()[edge_idx]
            curr_parent = max(u,v)
            g.add_edges([(curr_parent,curr_vertex)])
        else:
            print("error in adding edges")
            exit()
            
        g.es[-1]['rule_path'] = key_tuple[i]
        g.es[-1]['matching'] = output_dict[key_tuple[i]]
        print("edge added: ({}, {})".format(curr_parent,curr_vertex))
        curr_vertex += 1
        curr_path_len = len(curr_path_list)

    # for test1
    # g.add_edges([(0,1),(1,2),(2,3),(2,4)])
    layout = g.layout("rt_circular")
    edge_label_list = []
    for i in range(len(key_tuple)):
        to_append = "{}: {}".format(key_tuple[i],output_dict[key_tuple[i]])
        edge_label_list.append(to_append)
    g.es["label"] = edge_label_list
    # todo: label of vertives is subject to change
    g.vs['label'] = [i for i in range(len(g.vs))]
    # plot(g, "social_network.pdf", **visual_style)
    plot(g,"test1_plot.png",layout=layout)
