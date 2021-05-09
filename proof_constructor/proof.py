# given a proof tree, construct the proof in this proof tree
# a line of proof consists of a justification (or several justifications), and the truth.
# a truth is a clause
# you also need to state the premises somewhere
class Derivation(object):
    def __init__(self,truth):
        self.truth = truth # a Clause Object
        self.rule_idx = -1
        self.premises = []  # a list of index of derivations

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
        for i in range(len(self.rules)):
            to_append = "{:<5}{:<70}\t{:>5}".format(str(i),str(self.rules[i]),"P",width=80)
            proof_list.append(to_append)
        proof_list.append("{:<5}---------------".format(" "))
        for i in range(len(self.derivations)):
            justification_list = [str(self.derivations[i].rule_idx)] +[str(j) for j in self.derivations[i].premises]
            justification_str = ",".join(justification_list)
            to_append = "{:<5}{:<70}\t{:>5}".format(str(i+len(self.rules)),str(self.derivations[i].truth),justification_str)
            proof_list.append(to_append)
        to_return = "\n".join(proof_list)
        return to_return

    def add_proof(self):
        nodes = list(self.proof_tree.postorder())
        for i in range(len(nodes)):
            if nodes[i].is_true:
                truth = self.proof_tree.get_element(nodes[i])
                derivation = Derivation(truth)
                # search for rule
                if self.proof_tree.is_leaf(nodes[i]):
                    for j in range(len(self.rules)):
                        if self.rules[j].head==truth and self.rules[j].tail==[]:
                            derivation.rule_idx = j
                            break
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
                            to_search = self.proof_tree.get_element(children_list[j])
                            if self.derivations[k].truth==to_search:
                                derivation.premises.append(k+len(self.rules))
                                break
                self.derivations.append(derivation)
        return self.derivations


