from html_parser import HtmlParser
from add_proof_tree import AddProofTree
from plot_trees import PlotTrees
from add_proof_from_tree import AddProof
def main():
    # test5
    # rules_text =["great_grand_parent ( A, D )  :- parent ( A, B ) , grand_parent ( B, D )" , "grand_parent ( A, C )  :- parent ( A, B ) , parent ( B, C )" , "parent ( alice, bob )  :- TRUE", "parent ( bob, charlie )  :- TRUE", "parent ( charlie, daisy )  :- TRUE"]
    # test3
    # rules_text =["grand_parent ( X, Y )  :- parent_child ( X, Z ) , parent_child ( Z, Y )" , "parent_child ( alice, bob )  :- TRUE", "parent_child ( alice, bertie )  :- TRUE", "parent_child ( charlie, daisy )  :- TRUE", "parent_child ( bertie, chuck )  :- TRUE", "parent_child ( bob, charlie )  :- TRUE", "parent_child ( chuck, david )  :- TRUE"]

    # rules_text = ["sibling ( A, B )  :- parent_child ( C, A ) , parent_child ( C, B )" , "parent_child ( tom_smith, mary )  :- TRUE", "parent_child ( tom_smith, jack )  :- TRUE"]
    # parse_rule = ParseRule(rules_text)
    # rules = parse_rule.rules

    hp = HtmlParser("tests/test5_output")
    g = hp.html_to_graph()
    rule_texts = hp.rule_texts
    apt = AddProofTree(g,rule_texts)
    apt.graph_proof_tree()
    tree_plotter = PlotTrees(apt.graph)
    rules = apt.rules
    add_proof = AddProof(g,rules)
    add_proof.add_proofs()
    add_proof.print_proofs()

    # # test for add proof
    # proof_tree = g.idx_to_vertex(5).proof_tree
    # add_proof = TreetoProof(proof_tree,rules)
    # add_proof.add_proof()
    # print(add_proof)

    # vis_tree = tree_plotter.plot_trees()

main()