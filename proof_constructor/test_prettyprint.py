import sys
import os
from prologpy.solver import Solver

def test_prettyprint(filename):
    # read file, get rules text and goal text
    rules_text=""
    goal_text = ""
    is_goal = 0
    f = open(filename, "r")
    line = f.readline()
    while line:
        if line=="\n":
            is_goal = 1
        if is_goal:
            goal_text+=line
        else:
            rules_text+=line
        line = f.readline()
    f.close()
    # output_file = filename+"_output"

    solver = Solver(rules_text)
    rules = solver.database.rules
    to_print = ["{}".format(i) for i in rules]
    print("<rules rules={}>".format(to_print))
    print("</rules>")
    solution = solver.find_solutions(goal_text)
    
test_prettyprint(sys.argv[1])