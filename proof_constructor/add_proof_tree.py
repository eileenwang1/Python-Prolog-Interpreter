from proof_constructor.proof_tree import ProofTree
from proof_constructor.graph import Graph
import copy
import re

VARIABLE_REGEX = r"^[A-Z_][A-Za-z0-9_]*$"

class Clause(object):
    def __init__(self,functor, arguments=[]):
        self.functor = functor.strip()
        self.arguments = [i.strip() for i in arguments]

    def __str__(self):
        argument_string = ",".join(self.arguments)
        to_return = "{}({})".format(self.functor,argument_string)
        return to_return

    def __eq__(self,c2):
        if not isinstance(c2,Clause):
            raise ValueError("input not a clause")
        self.strip()
        c2.strip()
        return self.functor==c2.functor and self.arguments==c2.arguments
   
    def strip(self):
        self.functor = self.functor.strip()
        self.arguments = [i.strip() for i in self.arguments]
    
    def match_functor(self,clause2):
        # Clause -> Clause -> Bool12
        if not isinstance(clause2,Clause):
            raise ValueError("input not a clause")
        return self.functor==clause2.functor and len(self.arguments) == len(clause2.arguments)

    def variable_substitution(self,variable_matching):
        # find variable
        for i in range(len(self.arguments)):
            if re.match(VARIABLE_REGEX,self.arguments[i])!=None:
                to_substitute = variable_matching.get(self.arguments[i])
                if to_substitute!=None:
                    self.arguments[i] = to_substitute.strip()
    
    def get_variable_matching(self,c2):
        matching_dict = {}
        if not self.match_functor(c2):
            raise ValueError("functor not match")
        l1 = copy.deepcopy(self.arguments)
        l2 = copy.deepcopy(c2.arguments)
        for i in range(len(l1)):
            if re.match(VARIABLE_REGEX,l1[i])!=None and re.match(VARIABLE_REGEX,l2[i])==None:
                if matching_dict.get(l1[i])!=None and matching_dict.get(l1[i])!=l2[i]:
                    raise ValueError("inconsistent matching,{} to {} and {}".format(l1[i],matching_dict[l1[i]],l2[i]))
                matching_dict[l1[i]] = l2[i]
            elif re.match(VARIABLE_REGEX,l2[i])!=None and re.match(VARIABLE_REGEX,l1[i])==None:
                if matching_dict.get(l2[i])!=None and matching_dict.get(l2[i])!=l1[i]:
                    raise ValueError("inconsistent matching,{} to {} and {}".format(l2[i],matching_dict[l2[i]],l1[i]))
                matching_dict[l2[i]] = l1[i]
        return matching_dict
                

    def test_substitution(self,variable_matching):
        print(self.variable_substitution(variable_matching))

    def has_variable(self):
        for i in self.arguments:
            if re.match(VARIABLE_REGEX,i)!=None:
                return True
        return False


class Rule(object):
    def __init__(self,head_clause,tail_clauses=[]):
        self.head = head_clause
        self.tail = tail_clauses

    def __str__(self):
        if self.tail==[]:
            return str(self.head)
        tail_string_list = [str(i) for i in self.tail]
        tail_string = ", ".join(tail_string_list)
        to_return = "{} :- {}".format(str(self.head),tail_string)
        return to_return

class ParseRule(object):
    def __init__(self,rule_texts):
        self.rules = self.parse_rules(rule_texts)

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
        return [ParseClause(i).clause for i in clause_text_list]
    #     to_return = []
    #     for i in clause_text_list:
    #         to_append = self.parse_clause(i)
    #         to_return.append(to_append)
    #     return to_return
    def parse_clause(self,clause_text):
        clause_parser = ParseClause(clause_text)
        return clause_parser.clause

class ParseClause(object):
    def __init__(self,clause_text):
        self.clause = self.parse_clause(clause_text)

    def parse_clause(self,clause_text):
        # String (clause text) -> Clause
        if clause_text==None:
            return None
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


class AddProofTree(object):
    def __init__(self, graph,rule_texts):
        self.graph = graph if isinstance(graph,Graph) else None
        self.proof_tree_added = False
        self.rules = ParseRule(rule_texts).rules
    
    def graph_proof_tree(self):
        root = self.graph.find_root()
        if root is None:
            return
        self.root_proof_tree(root)
        vertex_list = self.graph.dfs(root)
        for i in range(1,len(vertex_list)):
            # print("vertex: ",vertex_list[i])
            to_print = self.vertex_proof_tree(vertex_list[i])
            # to_print.preorderPrint(to_print._root)
            # for j in to_print:
            #     print(j._element,"\t",j.is_true)


        # self.node_proof_tree(node_list[1])
        # new_tree = self.root_proof_tree(root)
        # print(new_tree.root())
        # print(new_tree._size)
        # for i in range(len(node_list)):
        #     curr_proof_tree = self.node_proof_tree(node_list[i])

    def root_proof_tree(self,curr_vertex):
        # curr_vertex = self.graph.idx_to_vertex(vertex_idx)
        goal = curr_vertex.goal
        goal_clause = ParseClause(goal).clause
        tree = ProofTree()
        root_node = tree.add_root(goal_clause)
        curr_vertex.proof_tree = copy.deepcopy(tree)
        return curr_vertex.proof_tree
        
    def vertex_proof_tree(self,curr_vertex):
        # find incoming edge in the graph 
        curr_edge = self.graph.incoming_edge(curr_vertex)
        if curr_edge is None:
            raise ValueError("no incoming edge found")
        # find current rule
        curr_rule_idx = int(curr_edge.rule_encoding.strip()[-1])
        curr_rule = self.rules[curr_rule_idx]
        # find matching_dict
        matching_dict = curr_edge.matching_dict
        # find current goal
        goal = curr_vertex.goal
        goal_clause = ParseClause(goal).clause

        prev_vertex = curr_edge.opposite(curr_vertex)
        # copy parent tree
        tree = copy.deepcopy(prev_vertex.proof_tree)
        
        # the tree grows
        if curr_rule.tail!=[]:
            tail_clauses = copy.deepcopy(curr_rule.tail)

            # find a children-less node that matches the functor
            curr_node = None
            node_list = list(tree.postorder())
            for i in range(len(node_list)):
                if tree.is_leaf(node_list[i]):
                    if curr_rule.head.match_functor(tree.get_element(node_list[i])):
                        curr_node = node_list[i]
                        break
            if curr_node is None:
                raise ValueError("curr node not found")
            tree.add_children(curr_node,tail_clauses)
  
        # substitution
        node_list = list(tree.postorder())
        for i in range(len(node_list)):
            curr_clause = tree.get_element(node_list[i])
            curr_clause.variable_substitution(matching_dict)
            tree.set_element(node_list[i],curr_clause)
        # check truth value
        self.set_true(tree)
        curr_vertex.proof_tree = copy.deepcopy(tree)
        return curr_vertex.proof_tree
    
    def set_true(self,proof_tree):
        node_list = list(proof_tree.postorder())
        
        for i in range(len(node_list)):
            if node_list[i].is_true:
                continue
            clause = proof_tree.get_element(node_list[i])
            if clause.has_variable() is False:
                if proof_tree.is_leaf(node_list[i]):
                    for j in self.rules:
                        if j.head==clause and j.tail==[]:
                            node_list[i].is_true = True
                            break

                    
                else:
                    subtree_list = list(proof_tree._subtree_postorder(node_list[i]))
                    subtree_list = subtree_list[:-1]
                    for j in range(len(subtree_list)):
                        if subtree_list[j].is_true ==False:
                            return
                    node_list[i].is_true = True
        return proof_tree
        # change is also in-place
                

if __name__ == '__main__':
    pass
    # # test5
    # # rules_text =["great_grand_parent ( A, D )  :- parent ( A, B ) , grand_parent ( B, D )" , "grand_parent ( A, C )  :- parent ( A, B ) , parent ( B, C )" , "parent ( alice, bob )  :- TRUE", "parent ( bob, charlie )  :- TRUE", "parent ( charlie, daisy )  :- TRUE"]
    # # test3
    # rules_text =["grand_parent ( X, Y )  :- parent_child ( X, Z ) , parent_child ( Z, Y )" , "parent_child ( alice, bob )  :- TRUE", "parent_child ( alice, bertie )  :- TRUE", "parent_child ( charlie, daisy )  :- TRUE", "parent_child ( bertie, chuck )  :- TRUE", "parent_child ( bob, charlie )  :- TRUE", "parent_child ( chuck, david )  :- TRUE"]

    # # rules_text = ["sibling ( A, B )  :- parent_child ( C, A ) , parent_child ( C, B )" , "parent_child ( tom_smith, mary )  :- TRUE", "parent_child ( tom_smith, jack )  :- TRUE"]
    # parse_rule = ParseRule(rules_text)
    # rules = parse_rule.rules

    # hp = HtmlParser("tests/test3_output")
    # g = hp.html_to_graph()
    # apt = AddProofTree(g,rules)
    # apt.graph_proof_tree()
    # tree_plotter = PlotTrees(apt.graph)
    # # vis_tree = tree_plotter.plot_tree(3)
    # # tree_plotter.show_tree(vis_tree,3)


    # vis_tree = tree_plotter.plot_trees()




