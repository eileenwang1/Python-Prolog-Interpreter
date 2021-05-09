from graph import Graph
from proof import Proof
class AddProof(object):
    def __init__(self,graph,rules):
        self.graph = graph if isinstance(graph,Graph) else None
        self.rules = rules
    
    def add_proofs(self):
        root = self.graph.find_root()
        if root is None:
            return
        vertex_list = self.graph.dfs(root)
        for i in range(len(vertex_list)):
            new_proof = Proof(vertex_list[i].proof_tree,self.rules)
            new_proof.add_proof()
            vertex_list[i].proof = new_proof

    def print_proofs(self):
        root = self.graph.find_root()
        if root is None:
            return
        vertex_list = self.graph.dfs(root)
        for i in range(len(vertex_list)):
            print("NODE {}".format(str(i)))
            print(vertex_list[i].proof)


   