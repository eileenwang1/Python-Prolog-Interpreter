# https://bor0.wordpress.com/2015/10/04/prolog-proof-search-trees/
class node(object):
    def __init__(self, value, children = []):
        self.value = value
        self.children = children

    def contains(self, value):
        for x in self.children:
            if x.value == value:
                return True

        return False

    def __repr__(self, level=0):
        ret = "  "*level+repr(self.value)+"\n"
        for child in self.children:
            ret += child.__repr__(level+1)
        return ret

# The relation tree to work with
tree = node("bigger", [
    node("cat", [node("mouse"), node("bug")]),
    node("mouse", [node("bug")]),
])

# This function would attempt to find a correct proof for the given task
# It parses the tree
def find_proof(tree, A, B):
    if tree.value == A and tree.contains(B):
        return True

    for node in tree.children:
        if find_proof(node, A, B):
            return True

    return False

# Try to find proof
print(find_proof(tree, 'cat', 'mouse'))
print(find_proof(tree, 'mouse', 'bug'))
print(find_proof(tree, 'cat', 'bug'))