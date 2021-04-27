import igraph
from html_parser import HtmlParser


class PlotGraph(object):
    def __init__(self,to_plot):
        self.to_plot = to_plot
        self.plotted = igraph.Graph()
    
    def plot(self):
        # prepare vertices
        vertices=sorted(self.to_plot.vertices(), key = lambda u: u.idx)
        # vertex_idx_list = []
        vertex_goal_list = []
        for i in vertices:
            # vertex_idx_list.append(i.idx)
            vertex_goal_list.append(i.goal)
        self.plotted.add_vertices(len(vertices))
        # self.plotted.vs['idx'] = vertex_idx_list
        self.plotted.vs['goal'] = vertex_goal_list

        # prepare edges
        edges = list(self.to_plot.edges())
        edge_list = []
        edge_rule_encoding_list = []
        edge_matching_dict_list = []
        for e in edges:
            u,v = e.endpoints()
            edge_list.append((u.idx,v.idx))
            edge_rule_encoding_list.append(e.rule_encoding)
            edge_matching_dict_list.append(e.matching_dict)
        self.plotted.add_edges(edge_list)
        self.plotted.es['rule_encoding'] = edge_rule_encoding_list
        self.plotted.es['matching_dict'] = edge_matching_dict_list

    def show(self):
        self.plot()
        layout = self.plotted.layout("rt_circular")

        vertex_label_list = []
        for i in range(len(self.plotted.vs)):
            to_append = "{}:{}".format(i,self.plotted.vs[i]['goal'])
            vertex_label_list.append(to_append)
        self.plotted.vs['label'] = vertex_label_list
        edge_label_list = []
        for e in self.plotted.es:
            to_append = "{}:{}".format(e['rule_encoding'][-1],e['matching_dict'])
            edge_label_list.append(to_append)
        self.plotted.es["label"] = edge_label_list

        visual_style = {}
        visual_style["vertex_size"] = 40
        # visual_style["vertex_color"] = [color_dict[gender] for gender in g.vs["gender"]]
        visual_style["vertex_label"] = self.plotted.vs['label']
        # visual_style["edge_width"] = [1 + 2 * int(is_formal) for is_formal in g.es["is_formal"]]
        visual_style["layout"] = layout
        visual_style["bbox"] = (1000, 1000)
        visual_style["margin"] = 50
        visual_style["order"] = [0,1,2,3].sort()
        
        # >>> plot(g, **visual_style)
        

        # for i in range(len(key_tuple)):
        #     to_append = "{}: {}".format(key_tuple[i],output_dict[key_tuple[i]])
        #     edge_label_list.append(to_append)
        # g.es["label"] = edge_label_list
        # todo: label of vertives is subject to change
        # g.vs['label'] = [i for i in range(len(g.vs))]
        # plot(g, "social_network.pdf", **visual_style)
        igraph.plot(self.plotted,"test3_plot.png",**visual_style)

if __name__ == '__main__':
    hp = HtmlParser("tests/test3_output")
    to_plot = hp.html_to_graph()
    # print(to_plot)
    pg = PlotGraph(to_plot)
    # pg.plot1()
    # print(pg.plotted)
    pg.show()





