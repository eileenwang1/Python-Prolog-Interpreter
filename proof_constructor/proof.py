# given a proof tree, construct the proof in this proof tree
# a line of proof consists of a justification (or several justifications), and the truth.
# a truth is a clause
# you also need to state the premises somewhere
import copy
from proof_constructor.add_proof_tree import Rule
UNIVERSAL_INSTANTIATION = "UI"
CONJUNCTION_INTRODUCTION = "∧ Intro"
CONDITONAL_ELIMINATION = "-> Elim"
class Derivation(object):
    def __init__(self,truth):
        self.truth = truth # a list of clauses, or a rule
        self.rule_idx = None
        self.premises = []  # a list of index of derivations
        self.justification = None

    def __str__(self):
        to_return = "by rule {0}, derivation {1}, {2}".format(self.rule_idx,[i for i in self.premises], self.truth)
        return to_return

class Proof(object):
    # given a proof tree and a list of rules, construct proofs
    def __init__(self,proof_tree,rules):
        self.proof_tree = proof_tree
        self.rules = rules
        self.derivations = []    # premises: rule object, derivations: proof object

    def __str__(self):
        proof_list = []
        # premises
        for i in range(len(self.rules)):
            to_append = "{:<5}{:<65}\t{:>5}".format(str(i),self.conditional_rule(self.rules[i]),"P")
            proof_list.append(to_append)
        proof_list.append("{:<5}---------------".format(" "))
        # derivations and conclusions
        for i in range(len(self.derivations)):
            justification_list = []
            if isinstance(self.derivations[i].rule_idx,int):
                justification_list.append(str(self.derivations[i].rule_idx))
            if self.derivations[i].premises!=[]:
                for k in self.derivations[i].premises:
                    to_append = copy.deepcopy(k)
                    justification_list.append(str(to_append))
            justification_str = ",".join(justification_list)
            if self.derivations[i].justification!=None:
                justification_str = justification_str + " " + self.derivations[i].justification
            if isinstance(self.derivations[i].truth,Rule):
                truth_str = self.conditional_rule(self.derivations[i].truth)
            else:
                clause_list = [str(j) for j in self.derivations[i].truth]
                truth_str = " ∧ ".join(clause_list)
            to_append = "{:<5}{:<65}\t{:>5}".format(str(i+len(self.rules)),truth_str,justification_str)
            proof_list.append(to_append)
        to_return = "\n".join(proof_list)
        return to_return

    def conditional_rule(self,rule):
        # return a string in the form a - > b
        if not isinstance(rule,Rule):
            raise ValueError("input not a rule: {}".format(type(rule)))
        if rule.tail == []:
            return str(rule)
        else:
            tail_string_list = [str(i) for i in rule.tail]
            if len(tail_string_list)>1:
                tail_string ="( "+ " ∧ ".join(tail_string_list)+" )"
            else:
                tail_string = tail_string_list[0]
            to_return = "{} -> {}".format(tail_string,str(rule.head))
            return to_return

    def add_proof(self):
        nodes = list(self.proof_tree.postorder())
        for i in range(len(nodes)):
            if nodes[i].is_true:
                truth = self.proof_tree.get_element(nodes[i])
                derivation = Derivation([truth])
                # case 1: is leaf
                if self.proof_tree.is_leaf(nodes[i]):
                    # search for rule
                    for j in range(len(self.rules)):
                        if self.rules[j].head==truth and self.rules[j].tail==[]:
                            derivation.rule_idx = j
                            break
                    self.derivations.append(derivation)
                # case 2: inner tree nodes
                else:
                    # search for rule
                    for j in range(len(self.rules)):
                        to_match = self.rules[j].head
                        if to_match.match_functor(truth):
                            derivation.rule_idx = j
                            break
                    # search for premises
                    children_list = nodes[i].children
                    for j in range(len(children_list)):
                        if not children_list[j].is_true:
                            raise ValueError("child {} not true".format(children_list[j]._element))
                        for k in range(len(self.derivations)):
                            to_search = [self.proof_tree.get_element(children_list[j])]
                            if isinstance(self.derivations[k],Rule):
                                continue
                            if self.derivations[k].truth==to_search:
                                derivation.premises.append(k+len(self.rules))
                                break
                    self.rigorous_subproof(derivation)
                    
        return self.derivations

    def rigorous_subproof(self,derivation):
        # make the proof more rigorous
        # step 1 conjunction intro
        truth1 = [self.derivations[j-len(self.rules)].truth[0] for j in copy.deepcopy(derivation.premises)]
        derivation1 = Derivation(truth1)
        derivation1.premises = copy.deepcopy(derivation.premises)
        derivation1.justification = CONJUNCTION_INTRODUCTION
        self.derivations.append(derivation1)
        
        # step 2 universal instantiation
        curr_rule = copy.deepcopy(self.rules[derivation.rule_idx])
        if len(curr_rule.tail)!= len(truth1):
            raise ValueError("number of premises does not match")
        for j in range(len(truth1)):
            if not truth1[j].match_functor(curr_rule.tail[j]):
                raise ValueError("functor not match")
        matching_dict = {}
        for j in range(len(truth1)):
            sub_matching = curr_rule.tail[j].get_variable_matching(truth1[j])
            matching_dict = self.merge_dict(matching_dict,sub_matching)
        for j in range(len(curr_rule.tail)):
            curr_rule.tail[j].variable_substitution(matching_dict)
        curr_rule.head.variable_substitution(matching_dict)
        derivation2 = Derivation(curr_rule)
        derivation2.premises = copy.deepcopy([derivation.rule_idx])
        derivation2.justification = UNIVERSAL_INSTANTIATION
        self.derivations.append(derivation2)

        # step 3 conditional elimination
        truth3 = copy.deepcopy(derivation.truth)
        derivation3 = Derivation(truth3)
        idx1 = copy.copy(len(self.rules)+len(self.derivations)-1)
        derivation3.premises = [idx1-1,idx1]
        derivation3.justification = CONDITONAL_ELIMINATION
        self.derivations.append(derivation3)



    def merge_dict(self,d1,d2):
        # add key-value pairs from d2 to d1
        for key in d2.keys():
            value = d2[key]
            if d1.get(key)!=None and d1.get(key)!=value:
                raise ValueError("inconsistent matching")
            d1[key] = copy.deepcopy(value)
        return d1


