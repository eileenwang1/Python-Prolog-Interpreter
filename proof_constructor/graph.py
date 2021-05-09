# from Data Structures, Spring 2019
class Graph:
    """Representation of a simple graph using an adjacency map."""

    #------------------------- nested Vertex class -------------------------
    class Vertex:
        """Lightweight vertex structure for a graph."""
        # __slots__ = '_element'
    
        def __init__(self, idx, goal=None,proof_tree=None,proof=None):
            """Do not call constructor directly. Use Graph's insert_vertex(x)."""
            self.goal = goal
            self.idx = idx
            self.proof_tree = proof_tree
            self.proof = proof

        # def element(self):
        #     """Return element associated with this vertex."""
        #     return self._element
    
        def __hash__(self):         # will allow vertex to be a map/set key
            return hash(self.idx)

        def __str__(self):
            return "VERTEX ({}, {})".format(self.idx,self.goal)
            # return str(self.goal)

        def __repr__(self):
            return "VERTEX ({}, {})".format(self.idx,self.goal)

        def __ge__(self,v2):
            if not isinstance(v2,type(self)):
                raise ValueError("not a vertex to compare")
            return self.idx >= v2.idx
        
        def __eq__(self,v2):
            if not isinstance(v2,type(self)):
                raise ValueError("not a vertex to compare")
            return self.idx==v2.idx and self.goal==v2.goal and self.proof_tree==v2.proof_tree


            # return str(self.goal)
        
    #------------------------- nested Edge class -------------------------
    class Edge:
        """Lightweight edge structure for a graph."""
        # __slots__ = '_origin', '_destination', '_element'
    
        def __init__(self, u, v, rule_encoding=None,matching_dict=None):
            """Do not call constructor directly. Use Graph's insert_edge(u,v,x)."""
            self._origin = u
            self._destination = v
            self.rule_encoding = rule_encoding
            self.matching_dict = matching_dict
    
        def endpoints(self):
            """Return (u,v) tuple for vertices u and v."""
            return (self._origin, self._destination)
    
        def opposite(self, v):
            """Return the vertex that is opposite v on this edge."""
            if not isinstance(v, Graph.Vertex):
                raise TypeError('v must be a Vertex')
            return self._destination if v is self._origin else self._origin
            raise ValueError('v not incident to edge')
    
        # def element(self):
        #     """Return element associated with this edge."""
        #     return self._element
    
        def __hash__(self):         # will allow edge to be a map/set key
            return hash( (self._origin, self._destination) )

        def __str__(self):
            return '({0},{1},{2},{3})'.format(self._origin,self._destination,self.rule_encoding,self.matching_dict)

        def __repr__(self):
            if self._origin.idx < self._destination.idx:
                u = self._origin
                v = self._destination
            else:
                u = self._destination
                v = self._origin
            return 'EDGE: ({0},{1},{2},{3})'.format(u,v,self.rule_encoding,self.matching_dict)
        
    #------------------------- Graph methods -------------------------
    def __init__(self, directed=False):
        """Create an empty graph (undirected, by default).

        Graph is directed if optional paramter is set to True.
        """
        self._outgoing = {}
        # only create second map for directed graph; use alias for undirected
        self._incoming = {} if directed else self._outgoing

    def __str__(self):
        def edge_key(e):
            if e._origin.idx < e._destination.idx:
                u = e._origin
                v = e._destination
            else:
                u = e._destination
                v = e._origin
            return u.idx
                
        edges = list(self.edges())
        sorted_edges = sorted(edges,key=lambda x:edge_key(x))
        result = []
        for each in sorted_edges:
            result.append(str(each) + "\n")
        return "".join(result)
    
    def size(self):
        return len(self.vertices())
    
    def dfs(self,start_node):
        # retrun an iteration in the dfs order
        def dfs_inner(start_node,visited):
            visited.append(start_node)
            adj_list = list(self._outgoing[start_node].keys())
            for i in range(len(adj_list)):
                has_visited = False
                for j in visited:
                    if j == adj_list[i]:
                        has_visited = True
                        break
                if not has_visited:
                    dfs_inner(adj_list[i],visited)
            return visited

        if len(self._outgoing)==0:
            return []
        to_return = dfs_inner(start_node,[])
        return to_return

    def _validate_vertex(self, v):
        """Verify that v is a Vertex of this graph."""
        if not isinstance(v, self.Vertex):
            raise TypeError('Vertex expected')
        if v not in self._outgoing:
            raise ValueError('Vertex does not belong to this graph.')
        
    def is_directed(self):
        """Return True if this is a directed graph; False if undirected.

        Property is based on the original declaration of the graph, not its contents.
        """
        return self._incoming is not self._outgoing # directed if maps are distinct

    def vertex_count(self):
        """Return the number of vertices in the graph."""
        return len(self._outgoing)

    def vertices(self):
        """Return an iteration of all vertices of the graph."""
        return self._outgoing.keys()

    def edge_count(self):
        """Return the number of edges in the graph."""
        total = sum(len(self._outgoing[v]) for v in self._outgoing)
        # for undirected graphs, make sure not to double-count edges
        return total if self.is_directed() else total // 2

    def edges(self):
        """Return a set of all edges of the graph."""
        result = set()       # avoid double-reporting edges of undirected graph
        for secondary_map in self._outgoing.values():
            result.update(secondary_map.values())    # add edges to resulting set
        return result

    def get_edge(self, u, v):
        """Return the edge from u to v, or None if not adjacent."""
        self._validate_vertex(u)
        self._validate_vertex(v)
        return self._outgoing[u].get(v)        # returns None if v not adjacent

    def degree(self, v, outgoing=True):   
        """Return number of (outgoing) edges incident to vertex v in the graph.

        If graph is directed, optional parameter used to count incoming edges.
        """
        self._validate_vertex(v)
        adj = self._outgoing if outgoing else self._incoming
        return len(adj[v])

    def incident_edges(self, v, outgoing=True):   
        """Return all (outgoing) edges incident to vertex v in the graph.

        If graph is directed, optional parameter used to request incoming edges.
        """
        self._validate_vertex(v)
        adj = self._outgoing if outgoing else self._incoming
        for edge in adj[v].values():
            yield edge

    def insert_vertex(self, x=None):
        """Insert and return a new Vertex with element x."""
        idx = len(self._outgoing)
        v = self.Vertex(idx,x)  #create a new instance in the vertex class
        self._outgoing[v] = {}
        if self.is_directed():
            self._incoming[v] = {}        # need distinct map for incoming edges
        return v
            
    def insert_edge(self, u, v, rule_encoding=None,matching_dict=None):
        """Insert and return a new Edge from u to v with auxiliary element x.

        Raise a ValueError if u and v are not vertices of the graph.
        Raise a ValueError if u and v are already adjacent.
        """
        if self.get_edge(u, v) is not None:      # includes error checking
            raise ValueError('u and v are already adjacent')
        e = self.Edge(u, v, rule_encoding,matching_dict)
        self._outgoing[u][v] = e
        self._incoming[v][u] = e
        return e

    def find_root(self):
        if self.size()==0:
            return None
        return self.idx_to_vertex(0)
    
    def idx_to_vertex(self,idx):
        # input: idx of a vertex
        # return the vertex
        if len(self._outgoing)==0 or idx>=len(self._incoming):
            raise ValueError('vertex DNE')
        for i in self._outgoing.keys():
            if i.idx==idx:
                return i
        return None
        # raise ValueError('vertex DNE')
        
    def goal_to_vertex(self,goal):
        # input: goal of a vertex
        # return the vertex
        if len(self._outgoing)==0:
            print("GOAL: ",goal)
            raise ValueError('vertex DNE')
        for i in self._outgoing.keys():
            if i.goal==goal:
                return i
        return None
        # raise ValueError('vertex DNE')

    def encoding_to_edge(self,rule_encoding):
        # input: encoding of a edge
        # return :the corresponding edge if the edge exists, none otherwise
        edges = list(self.edges())
        for i in range(len(edges)):
            if edges[i].rule_encoding==rule_encoding:
                return edges[i]
        return None
    
    def first_vertex_without_goal(self):
        # return the vertex with the smallest idx that is without goal
        vertices=sorted(self.vertices(), key = lambda u: u.idx)
        for i in range(len(vertices)):
            if vertices[i].goal==None or vertices[i].goal=="":
                return vertices[i]
        return None
    
    def incoming_edge(self,v):
        # find the edge that connects v to a vertex of smaller idx
        incident_edges = self.incident_edges(v)
        incident_edges = list(incident_edges)
        curr_idx = v.idx
        curr_edge = None
        for i in range(len(incident_edges)):
            u,v = incident_edges[i].endpoints()
            if u.idx<=curr_idx and v.idx<=curr_idx:
                curr_edge = incident_edges[i]
                return curr_edge
        return curr_edge

                








