from proof_tree import ProofTree
from graph import Graph
from html_parser import HtmlParser
import copy

class Rule(object):
    class Clause(object):
        def __init__(functor, arguments=[]):
            self.functor = functor
            self.arguments = arguments

        def __str__(self):
            argument_string = ",".join(self.arguments)
            to_return = "{}({})".format(self.functor,argument_string)
            return to_return

    def __init__(head_clause,tail_clauses=[]):
        self.head = head_clause
        self.tail = tail_clauses

    def __str__(self):
        tail_string_list = [str(i) for i in self.tail]
        tail_string = ", ".join(tail_string_list)
        to_return = "{} :- {}".format(str(self.head),tail_string)
        return to_return

class AddProofTree(object):
    def __init__(self, graph,rules):
        self.graph = graph if isinstance(graph,Graph) else None
        self.proof_tree_added = False
        self.rules = self.parse_rules(rules)

    # def verify_graph(self):
    #     to_return = isinstance(self.graph,Graph)
    #     # print(to_return)
    #     return to_return
    
    def graph_proof_tree(self):
        
        root = self.graph.find_root()
        if root==None:
            return
        node_list = self.graph.dfs(root)
        for i in range(len(node_list)):
            curr_proof_tree = self.node_proof_tree(node_list[i])


        self.proof_tree_added = True

    def root_proof_tree(self,curr_node):
        goal = curr_node.goal_text
        tree = ProofTree()
        tree.add_root(goal)
        tree.root().is_current_vertex = True
        curr_node.proof_tree = tree
        return tree
        
    def node_proof_tree(self,curr_node):
        parent_node = curr_node.parent
        tree = copy.deepcopy(parent_node.proof_tree)

# ----------- parsing -----------
    def parse_rules(self,rules):
        # [String] -> [Rule]
        to_return = []
        for i in rules:
            to_append = self.parse_rule(i)
            to_return.append(to_append)
        return to_return

    def parse_rule(self,rule):
        # String -> Rule
        head_text,tail_text_list = self.split_head_tail(rule)
        head_clause = self.parse_clause(head_text)
        tail_clauses = self.parse_clauses(tail_text_list)
        to_return = Rule(head_clause,tail_clauses)
        return to_return

    def split_head_tail(self,rule):
        # split the head text and the tail texts of a rule text
        # String -> (String,[String])
        cut_idx = rule.find(":-")
        if cut_idx==-1:
            return (rule,[])
        head = rule[:cut_idx].strip()
        tail = rule[cut_idx+2:].strip()
        if tail == "TRUE":
            return(head,[])
        tail_list = []
        pda_counter = 0
        prev_idx = 0
        for i in range(len(tail)):
            if tail[i]=='(':
                pda_counter +=1
            elif tail[i]==')':
                pda_counter -=1
            elif tail[i] == ',' and pda_counter ==0:
                tail_list.append(tail[prev_idx:i])
                prev_idx = i+1
        tail_list.append(tail[prev_idx:])
        tail_list = [i.strip() for i in tail_list]
        return (head,tail_list)
    
    def parse_clauses(self,clause_text_list):
        # [String] (clause text list) -> [Clause]

        to_return = []
        for i in clause_text_list:
            to_append = self.parse_clause(i)
            to_return.append(to_append)
        return to_return

    def parse_clause(self,clause_text):
        # String (clause text) -> Clause
        if clause_text[-1]!=")":
            to_return = Clause(clause_text)
            return to_return
        clause_text = clause_text[:-1]
        cut_idx = clause_text.find("(")
        if cut_idx ==-1:
            raise ValueError("opening parenthesis not found")
        functor = clause_text[:cut_idx].strip()
        arguments = clause_text[cut_idx+1:].split(",")
        arguments = [i.strip() for i in arguments]
        to_return = Clause(functor,arguments)
        return to_return

        

    def variable_substitution(self,input_text,variable_matching):
        # find variable
        VARIABLE_REGEX = r"^[A-Z_][A-Za-z0-9_]*$"
        # re.sub(pattern, repl, string, count=0, flags=0)

        

        

if __name__ == '__main__':
    rules = ["sibling ( A, B )  :- parent_child ( C, A ) , parent_child ( C, B )" , "parent_child ( tom_smith, mary )  :- TRUE", "parent_child ( tom_smith, jack )  :- TRUE"]
    hp = HtmlParser("tests/test1_output")
    g = hp.html_to_graph()
    apt = AddProofTree(g,rules)
    print(apt.rules)
    # print(apt.graph)
    # apt.verify_graph()


