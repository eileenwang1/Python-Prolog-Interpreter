# represent html as using a PDA
# nested query calls is the and stack
# for loops are the or-stack
# the output should be stored globally, but how to store the sources of output?
import re
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
    # a dictionary
    # key: (string of numbers) encoding of the OR-stack, 
    # value: dict of variable matching
    
    html_file = open(html_filename,'r')
    to_parse = html_file.readlines()
    html_file.close()

    for curr_line in to_parse:
        curr_line = curr_line.strip()

        if curr_line[:7]=="<query ":
            and_stack.append(curr_line[7:])
        elif curr_line == "</query>":
            try:
                and_stack.pop()
            except Exception:
                print(Exception)
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
        elif curr_line.find("<matching_head matchinghead=\"")!=-1:
            start_idx = curr_line.find("<matching_head matchinghead=\"")+len("<matching_head matchinghead=\"")
            matching_str = curr_line[start_idx:]
            matching_str = matching_str.strip()
            matching_dict = extract_key_value_pair(matching_str)
            encoding = "-".join(or_stack)
            if output_dict.get(encoding)==None:
                output_dict[encoding] = matching_dict
            else:
                for k in matching_dict.keys():
                    if output_dict.get(k)!=None and output_dict.get(k)!=matching_dict[k]:
                        print("ERROR adding to output dict")
                        return
                    output_dict[encoding][k] = matching_dict[k]


            
        print("CURR_LINE: ",curr_line)
        print("AND_STACK:\n",and_stack)
        print("OR_STACK:\n",or_stack)
        print("OUTPUT_STACK:\n",output_dict)

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




        



if __name__ == '__main__':
    output_to_html("tests/test3_output")
    html_parser("tests/test3_output.html")