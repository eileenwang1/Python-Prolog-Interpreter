# represent html as using a PDA
# nested query calls is the and stack
# for loops are the or-stack
# the output should be stored globally, but how to store the sources of output?

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
    output_stack=[] # todo: what do you want to store in the output?
    
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
        elif curr_line[:9]=="<forloop ":
            or_stack.append(curr_line[9:])
        elif curr_line=="</forloop>":
            or_stack.pop()
        else:
            output_stack.append(curr_line)
        print("CURR_LINE: ",curr_line)
        print("AND_STACK:\n",and_stack)
        print("OR_STACK:\n",or_stack)
        print("OUTPUT_STACK:\n",output_stack)


        



if __name__ == '__main__':
    # output_to_html("tests/test3_output")
    html_parser("tests/test1_output.html")