import sys
import os
from proof_constructor.html_parser import HtmlParser
from proof_constructor.add_proof_tree import AddProofTree
from proof_constructor.add_proof_from_tree import AddProof
from proof_constructor.plot_graph import PlotGraph
from proof_constructor.plot_trees import PlotTrees
TEST_DIR = "tests/"
PLOT_DIR = "plotting/"
SRC_DIR = "proof_constructor/"
def main():
    
    if len(sys.argv) != 2:
        raise ValueError('wrong number of inputs.')
    test_case_filename = sys.argv[1]
    if not os.path.isfile(test_case_filename):
        raise ValueError('input file does not exist')

    # set absolute path for future imports
    os.system("export PYTHONPATH=$PYTHONPATH:$(pwd)")
    
    # manage filenames
    test_output_filename = test_case_filename + "_output"
    proof_file_name = test_case_filename+"_proof"
    # for plotting filenames
    cut_idx = test_case_filename.find(TEST_DIR)+len(TEST_DIR)
    atom_filename = test_case_filename[cut_idx:]
    plot_child_dir = "{}f{}/".format(PLOT_DIR,atom_filename)
    if not os.path.isdir(plot_child_dir):
        try:
            os.mkdir(plot_child_dir) 
        except OSError as error: 
            print(error)  
    graph_filename = "{}{}_plot.png".format(plot_child_dir,atom_filename)
    
    # pretty-print the states of the python interpreter
    cmd_str = "python3 {}test_prettyprint.py {} > {}".format(SRC_DIR,test_case_filename,test_output_filename)
    os.system(cmd_str)
    
    # post-process and parse pretty-printed output
    hp = HtmlParser(test_output_filename)   # parser object
    # the search graph
    g = hp.html_to_graph()  # graph object
    rule_texts = hp.rule_texts  # list of rule texts (str)
   
    # add proof tree to each vertex in the graph
    apt = AddProofTree(g,rule_texts)    
    apt.graph_proof_tree()
    rules = apt.rules   # list of Rule objects
    
    # add proof to each vertex from proof tree
    add_proof = AddProof(g,rules)
    add_proof.add_proofs()
    add_proof.print_proofs(proof_file_name)
    
    # plot graph
    graph_plotter = PlotGraph(g,graph_filename)
    graph_plotter.show()

    # plot tree
    tree_plotter = PlotTrees(apt.graph,plot_child_dir)
    vis_tree = tree_plotter.plot_trees()

main()