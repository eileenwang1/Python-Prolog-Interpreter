# import Solver
from prologpy.solver import Solver
import sys

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
    solver = Solver(rules_text)
    rules = solver.database.rules
    print(rules)
    solution = solver.find_solutions(goal_text)
    



if __name__ == '__main__':
    filename = sys.argv[1]
    test_prettyprint(filename)