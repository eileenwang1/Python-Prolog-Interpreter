# represent html as using a PDA
# nested query calls is the and stack
# for loops are the or-stack
# the output should be stored globally, but how to store the sources of output?
import re
from graph import Graph 

class HtmlParser(object):
    def __init__(self, src_filename):
        self.graph = Graph()
        self.src_filename = src_filename
        self.rule_texts = ""
    
    def output_to_html(self):
        dst_filename = self.src_filename+".html"
        to_write = []
        src_file = open(self.src_filename, "r")
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
        return dst_filename
    
    def html_to_graph(self):
        html_filename = self.output_to_html()
        and_stack = []
        or_stack=[]
        output_dict={} 

        # a dictionary
        # key: (string of numbers) encoding of the OR-stack, 
        # value: dict of variable matching
        
        html_file = open(html_filename,'r')
        to_parse = html_file.readlines()
        html_file.close()
        counter = 0
        for curr_line in to_parse:
            curr_line = curr_line.strip()
            if curr_line == "\n":
                continue
            counter += 1
            # todo: parse rules
            if curr_line[:6]=="<rules":
                self.rule_texts = extract_rules(curr_line[6:])
            elif curr_line[:7]=="<query ":
                goal = extract_goal(curr_line[7:])
                and_stack.append(goal)
                if counter == 3:
                    self.graph.insert_vertex(goal)
                # else:
                #     # find first vertex without goal
                #     v = self.graph.first_vertex_without_goal()
                #     v.goal = goal
                #     print("first_vertex without goal: ",v)


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
                if self.graph.encoding_to_edge(encoding)==None:
                    if "-" in encoding:
                        prev_encoding = get_prev_encoding(encoding)
                        if prev_encoding==None:
                            raise ValueError("can't find prev_encoding")
                        prev_edge = self.graph.encoding_to_edge(prev_encoding)
                        if prev_edge==None:
                            raise ValueError("can't find prev_edge")
                        u,v = prev_edge.endpoints()
                        if u.idx>v.idx:
                            curr_vertex = u
                        else:
                            curr_vertex = v 
                        if curr_vertex.goal==None:
                            curr_vertex.goal = and_stack[-1]
                                  
                    else:
                        curr_goal = and_stack[-1]
                        curr_vertex = self.graph.goal_to_vertex(curr_goal)
                    new_vertex = self.graph.insert_vertex()
                    curr_edge = self.graph.insert_edge(curr_vertex,new_vertex,encoding,matching_dict)
                # if edge exists, add matching to the edge
                else:
                    if self.graph.encoding_to_edge(encoding).matching_dict!=None and self.graph.encoding_to_edge(encoding).matching_dict!={}:
                        for k in matching_dict.keys():
                            value = self.graph.encoding_to_edge(encoding).matching_dict.get(k)
                            if value!=None and value != matching_dict[k]:
                                raise ValueError("matching_dict value error")
                    g.encoding_to_edge(encoding).matching_dict = matching_dict
                # modification of output_dict (to be commented out)     
                if output_dict.get(encoding)==None:
                    output_dict[encoding] = matching_dict
                else:
                    for k in matching_dict.keys():
                        if output_dict.get(k)!=None and output_dict.get(k)!=matching_dict[k]:
                            raise ValueError("ERROR adding to output dict")
                        output_dict[encoding][k] = matching_dict[k]

            # elif curr_line.find("<yield output=")!=-1:
            #     yield_value = extract_yield_value(curr_line)

            # print("CURR_LINE: ",curr_line)
            # # print("AND_STACK:\n",and_stack)
            # # print("OR_STACK:\n",or_stack)
            # # print("OUTPUT_DICT:\n",output_dict)
            # print(g)
        return self.graph

    

# input: a string in the form of 'index="0" rule="sibling ( X, Y )  :- parent_child ( Z, X ) , parent_child ( Z, Y ) ">'
# output: (char) index of the rule
def extract_rules(raw_rule_text):
    raw_rule_text = raw_rule_text.strip()
    raw_rule_text = raw_rule_text[7:-2]
    # print(raw_rule_text)
    raw_rules = raw_rule_text.split("'")
    rule_texts = []
    for i in range(len(raw_rules)):
        curr_rule = raw_rules[i].strip()
        if curr_rule != "" and curr_rule != ",":
            rule_texts.append(curr_rule)
    return rule_texts
        

    # print(raw_rule_text)
def extract_rule_number(rule):
    p = re.compile(r'\d+')
    rule_idx = p.findall(rule)[0]
    return rule_idx

def extract_key_value_pair(matching_str):
    if matching_str[0]=='{' and matching_str[-3:]=='}\">':
        matching_str = matching_str[1:]
        matching_str = matching_str[:-3]
    else:
        raise ValueError("ERROR parsing matching_str")
        # return
    matching_list = matching_str.split(",")
    matching_dict = {}
    for i in range(len(matching_list)):
        if matching_list[i] =="":
            continue
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

def get_prev_encoding(encoding):
    i = -1
    while i!= 0-len(encoding):
        if encoding[i]=='-':
            return encoding[:i]
        i -= 1

    # for i in range(-len(encoding),0):
    #     if encoding[i]=='-':
    #         return encoding[:i]
    return None

if __name__ == '__main__':
    hp = HtmlParser("tests/test3_output")
    g = hp.html_to_graph()
    start_node = g.idx_to_vertex(0)
    from_dfs = g.dfs(start_node)
    for i in from_dfs:
        print(i)
    
    # print(to_print)
    # output_to_html("tests/test3_output")
    # html_parser("tests/test3_output.html")