# represent html as using a PDA
# nested query calls is the and stack
# for loops are the or-stack
# the output should be stored globally, but how to store the sources of output?
import re
from graph import Graph 

class HtmlParser(object):
    def __init__(self, src_filename):
        pass

def output_to_html(src_filename):
    dst_filename = src_filename+".html"
    to_write = []
    src_file = open(src_filename, "r")
    src_line = src_file.readline()
    while src_line:
        src_line = src_line.lstrip()
        if src_line[0]=='<':
            to_write.append(src_line)
        src_line = src_file.readline()
    src_file.close()

    dst_file = open(dst_filename,"w")
    dst_file.writelines(to_write)
    dst_file.close()
    
def html_parser(html_filename):
    and_stack = []
    or_stack=[]
    output_dict={} 
    # node_list = []
    g = Graph()

    # a dictionary
    # key: (string of numbers) encoding of the OR-stack, 
    # value: dict of variable matching
    
    html_file = open(html_filename,'r')
    to_parse = html_file.readlines()
    html_file.close()
    counter = 0
    for curr_line in to_parse:
        curr_line = curr_line.strip()
        counter += 1

        if curr_line[:7]=="<query ":
            goal = extract_goal(curr_line[7:])
            and_stack.append(goal)
            if counter == 1:
                g.insert_vertex(goal)
            else:
                # find first vertex without goal
                try:
                    g.first_vertex_without_goal().goal = goal
                except Exception:
                    print(Exception)

            # # add new vertex in the graph (with current goal)
            # curr_vertex = g.insert_vertex(goal)
            # # check whether there is edge that leads to the goal
            # if len(output_dict)!=0:

            # # modification of node_list
            # new_node = Node(len(node_list))
            # new_node.goal = goal
            # node_list.append(new_node)

        elif curr_line == "</query>":
            try:
                and_stack.pop()
            except Exception:
                print(Exception)
                return
        elif curr_line.find("<forloop ")!=-1:
            start_idx = curr_line.find("<forloop ")+len("<forloop ")
            rule = curr_line[start_idx:].strip()
            to_append = extract_rule_number(rule)
            or_stack.append(to_append)
        elif curr_line=="</forloop>":
            try:
                or_stack.pop()
            except Exception:
                print(Exception)
                return

        elif curr_line.find("<matching_head matchinghead=\"")!=-1:
            start_idx = curr_line.find("<matching_head matchinghead=\"")+len("<matching_head matchinghead=\"")
            matching_str = curr_line[start_idx:]
            matching_str = matching_str.strip()
            matching_dict = extract_key_value_pair(matching_str)
            encoding = "-".join(or_stack)
            if len(and_stack)==0:
                raise ValueError("and-stack empty")
            # if edge does not exist, add edge and the matching
            if g.encoding_to_edge(encoding)==None:
                curr_goal = and_stack[-1]
                curr_vertex = g.goal_to_vertex(curr_goal)
                new_vertex = g.insert_vertex()
                curr_edge = g.insert_edge(curr_vertex,new_vertex,encoding,matching_dict)
            # if edge exists, add matching to the edge
            else:
                if g.encoding_to_edge(encoding).matching_dict!=None and g.encoding_to_edge(encoding).matching_dict!={}:
                    for k in matching_dict.keys():
                        value = g.encoding_to_edge(encoding).matching_dict.get(k)
                        if value!=None and value != matching_dict[k]:
                            raise ValueError("matching_dict value error")
                g.encoding_to_edge(encoding).matching_dict = matching_dict
            # modification of output_dict (to be commented out)     
            if output_dict.get(encoding)==None:
                output_dict[encoding] = matching_dict
            else:
                for k in matching_dict.keys():
                    if output_dict.get(k)!=None and output_dict.get(k)!=matching_dict[k]:
                        print("ERROR adding to output dict")
                        return
                    output_dict[encoding][k] = matching_dict[k]

        elif curr_line.find("<yield output=")!=-1:
            yield_value = extract_yield_value(curr_line)
            if len(and_stack)==0:
                print("ERROR: and_stack empty when yield")
                return
            first_goal = and_stack[0]

            curr_node=None
            for i in range(len(node_list)):
                if node_list[i].goal==curr_goal:
                    curr_node = node_list[i]
                    break
            if curr_node==None:
                print("ERROR: no corresponding node for yield output")
                return
            curr_node.yield_value = yield_value
        # else:
        #     continue
        #     # no modification
        print("CURR_LINE: ",curr_line)
        # print("AND_STACK:\n",and_stack)
        # print("OR_STACK:\n",or_stack)
        # print("OUTPUT_DICT:\n",output_dict)
        print(g)
        # for i in node_list:
        #     print(i)
        # print("\n")
    

# input: a string in the form of 'index="0" rule="sibling ( X, Y )  :- parent_child ( Z, X ) , parent_child ( Z, Y ) ">'
# output: (char) index of the rule
def extract_rule_number(rule):
    p = re.compile(r'\d+')
    rule_idx = p.findall(rule)[0]
    return rule_idx

def extract_key_value_pair(matching_str):
    if matching_str[0]=='{' and matching_str[-3:]=='}\">':
        matching_str = matching_str[1:]
        matching_str = matching_str[:-3]
    else:
        print("ERROR parsing matching_str")
        return
    matching_list = matching_str.split(",")
    matching_dict = {}
    for i in range(len(matching_list)):
        matching_list[i] = matching_list[i].split(":")
        key = matching_list[i][0].strip()
        value = matching_list[i][1].strip()
        matching_dict[key] = value
    return matching_dict

def extract_goal(goal_text):
    # 'goal="sibling ( mary, A ) ">'
    goal_text = goal_text.strip()
    to_return = goal_text[6:-2]
    to_return = to_return.strip()
    return to_return

def extract_yield_value(yield_text):
    yield_text = yield_text.strip()
    to_return = yield_text[15:-2]
    to_return = to_return.strip()
    return to_return

if __name__ == '__main__':
    # output_to_html("tests/test1_output")
    html_parser("tests/test1_output.html")