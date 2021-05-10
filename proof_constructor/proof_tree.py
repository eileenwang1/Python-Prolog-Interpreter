
import copy
class ProofTree:
    class TreeNode:
        def __init__(self, idx,element="", children=[],parent = None):
            self._parent = parent
            self._element = element # clauses
            self.idx = idx
            self.children = children
            self.is_true = False

    #-------------------------- binary tree constructor --------------------------
    def __init__(self):
        """Create an initially empty binary tree."""
        self._root = None
        self._size = 0

    #-------------------------- public accessors ---------------------------------
    def __len__(self):
        """Return the total number of elements in the tree."""
        return self._size

    def is_root(self, node):
        """Return True if a given node represents the root of the tree."""
        return self._root == node

    def is_leaf(self, node):
        """Return True if a given node does not have any children."""
        return self.num_children(node) == 0

    def is_empty(self):
        """Return True if the tree is empty."""
        return len(self) == 0
    
    def is_true(self):
        # return true if every tree node is true
        node_list = list(self.nodes())
        for node in node_list:
            if not node.is_true:
                return False
        return True

    def __iter__(self):
        """Generate an iteration of the tree's elements."""
        for node in self.nodes():                        # use same order as nodes()
            yield node                               # but yield each element

    def nodes(self):
        """Generate an iteration of the tree's nodes."""
        return self.preorder()                            # return entire preorder iteration

    def preorder(self):
        """Generate a preorder iteration of nodes in the tree."""
        if not self.is_empty():
            for node in self._subtree_preorder(self._root):  # start recursion
                yield node

    def _subtree_preorder(self, node):
        """Generate a preorder iteration of nodes in subtree rooted at node."""
        yield node                                           # visit node before its subtrees
        for c in self.children(node):                        # for each child c
            for other in self._subtree_preorder(c):         # do preorder of c's subtree
                yield other                                   # yielding each to our caller

    def postorder(self):
        """Generate a postorder iteration of nodes in the tree."""
        if not self.is_empty():
            for node in self._subtree_postorder(self._root):  # start recursion
                yield node

    def _subtree_postorder(self, node):
        """Generate a postorder iteration of nodes in subtree rooted at node."""
        for c in self.children(node):                        # for each child c
            for other in self._subtree_postorder(c):        # do postorder of c's subtree
                yield other                                   # yielding each to our caller
        yield node                                           # visit node after its subtrees
    def inorder(self):
        """Generate an inorder iteration of positions in the tree."""
        if not self.is_empty():
          for node in self._subtree_inorder(self._root):
            yield node

    def _subtree_inorder(self, node):
        """Generate an inorder iteration of positions in subtree rooted at p."""
        if node._left is not None:          # if left child exists, traverse its subtree
          for other in self._subtree_inorder(node._left):
            yield other
        yield node                               # visit p between its subtrees
        if node._right is not None:         # if right child exists, traverse its subtree
          for other in self._subtree_inorder(node._right):
            yield other


    # def breadthfirst(self):
    #     """Generate a breadth-first iteration of the nodes of the tree."""
    #     if not self.is_empty():
    #         fringe = LinkedQueue()             # known nodes not yet yielded
    #         fringe.enqueue(self._root)        # starting with the root
    #         while not fringe.is_empty():
    #             node = fringe.dequeue()             # remove from front of the queue
    #             yield node                          # report this node
    #             for c in self.children(node):
    #                 fringe.enqueue(c)              # add children to back of queue


    def root(self):
        """Return the root of the tree (or None if tree is empty)."""
        return self._root

    def parent(self, node):
        """Return node's parent (or None if node is the root)."""
        return node._parent

    def children(self, node):
        """Generate an iteration of nodes representing node's children."""
        return node.children

    def num_children(self, node):
        """Return the number of children of a given node."""
        return len(node.children)

    def get_element(self,node):
        return node._element

    def set_element(self,node,new_element):
        node._element = new_element
    
    # def set_true(self):
    #     node_list = list(self.postorder())
        
    #     for i in range(len(node_list)):
    #         if node_list[i].is_true:
    #             continue
    #         clause = self.get_element(node_list[i])
    #         if clause.has_variable() is False:
    #             if self.is_leaf(node_list[i]):
    #                 node_list[i].is_true = True
    #             else:
    #                 subtree_list = list(self._subtree_postorder(node_list[i]))
    #                 subtree_list = subtree_list[:-1]
    #                 for j in range(len(subtree_list)):
    #                     if subtree_list[j].is_true ==False:
    #                         return
    #                 node_list[i].is_true = True
                    
                    

    #-------------------------- nonpublic mutators --------------------------
    def add_root(self, e=None):
        """Place element e at the root of an empty tree and return the root node.

        Raise ValueError if tree nonempty.
        """
        if self._root is not None:
            raise ValueError('Root exists')
        self._size = 1
        self._root = self.TreeNode(idx = 0,element=e)
        return self._root

    def add_children(self,node,element_list):
        for i in range(len(element_list)):
            idx = self._size
            self._size += 1
            new_node = self.TreeNode(idx=idx,element=element_list[i],parent=node)
            node.children.append(copy.deepcopy(new_node))

    def _replace(self, node, e):
        """Replace the element at given node with e, and return the old element."""
        old = node._element
        node._element = e
        return old

    # def _delete(self, node):
    #     """Delete the given node, and replace it with its child, if any.

    #     Return the element that had been stored at the given node.
    #     Raise ValueError if node has two children.
    #     """
    #     if self.num_children(node) == 2:
    #         raise ValueError('Position has two children')
    #     child = node._left if node._left else node._right  # might be None
    #     if child is not None:
    #         child._parent = node._parent     # child's grandparent becomes parent
    #     if node is self._root:
    #         self._root = child             # child becomes root
    #     else:
    #         parent = node._parent
    #         if node is parent._left:
    #             parent._left = child
    #         else:
    #             parent._right = child
    #     self._size -= 1
    #     return node._element



    # def _attach(self, node, t1, t2):
    #     """Attach trees t1 and t2, respectively, as the left and right subtrees of the external node.

    #     As a side effect, set t1 and t2 to empty.
    #     Raise TypeError if trees t1 and t2 do not match type of this tree.
    #     Raise ValueError if node already has a child. (This operation requires a leaf node!)
    #     """
    #     if not self.is_leaf(node):
    #         raise ValueError('position must be leaf')
    #     if not type(self) is type(t1) is type(t2):    # all 3 trees must be same type
    #         raise TypeError('Tree types must match')
    #     self._size += len(t1) + len(t2)
    #     if not t1.is_empty():         # attached t1 as left subtree of node
    #         t1._root._parent = node
    #         node._left = t1._root
    #         t1._root = None             # set t1 instance to empty
    #         t1._size = 0
    #     if not t2.is_empty():         # attached t2 as right subtree of node
    #         t2._root._parent = node
    #         node._right = t2._root
    #         t2._root = None             # set t2 instance to empty
    #         t2._size = 0

    def preorderPrint(self,node):
        if node is not None:
            print("from PreorderPrint:",node._element)
        for i in node.children:
            self.preorderPrint(i)
        # if node._left is not None:
        #     self.preorderPrint(node._left)
        # if node._right is not None:
        #     self.preorderPrint(node._right)

    # def postorderPrint(self,node):
    #     if node._left is not None:
    #         self.postorderPrint(node._left)
    #     if node._right is not None:
    #         self.postorderPrint(node._right)
    #     if node is not None:
    #         print("from PostorderPrint:",node._element)

    # def inorderPrint(self,node):
    #     if node._left is not None:
    #         self.inorderPrint(node._left)
    #     if node is not None:
    #         print("from InorderPrint:",node._element)
    #     if node._right is not None:
    #         self.inorderPrint(node._right)

    # def levelorderPrint(self, node):
    #     '''
    #     @node: a given TreeNode.

    #     Prints all the elements with level order traversal, starting at the given node.

    #     @return: nothing.
    #     '''
    #     q = LinkedQueue()
    #     q.enqueue(node)
    #     while not q.is_empty():
    #         temp = q.dequeue()
    #         print(temp._element)

    #         if temp._left is not None:
    #             q.enqueue(temp._left)

    #         if temp._right is not None:
    #             q.enqueue(temp._right)




    def height(self, node = None):
        '''
        @node: a given TreeNode.

        Return the height of the subtree rooted at a given node.
        If node is None, return the height of the entire tree.

        @return: height of subtree, integer.
        '''

        #special case: if node is none

        if node is None:
            node = self._root
            print(node._element)
        return self.inner_fun(node)

    def inner_fun(self, node):
        if node is None:
            return -1
        else:
            #an induction case: you check every node, run time: O(n)
            return 1 + max(self.inner_fun(node._left), self.inner_fun(node._right)) #take the larger one


    def depth(self, node):
        '''
        @node: a given TreeNode.

        Return the number of levels separating a given node from the root.
        
        @return: depth of a node, integer
        '''
        to_return = 0
        temp = node
        while temp._parent is not None:
            to_return += 1
            temp = temp._parent
        return to_return






def pretty_print(tree):
    # ----------------------- Need to enter height to work -----------------
    levels = tree.height() + 1  
    print("Levels:", levels)   
    print_internal([tree._root], 1, levels)

def print_internal(this_level_nodes, current_level, max_level):
    if (len(this_level_nodes) == 0 or all_elements_are_None(this_level_nodes)):
        return  # Base case of recursion: out of nodes, or only None left

    floor = max_level - current_level;
    endgeLines = 2 ** max(floor - 1, 0);
    firstSpaces = 2 ** floor - 1;
    betweenSpaces = 2 ** (floor + 1) - 1;
    print_spaces(firstSpaces)
    next_level_nodes = []
    for node in this_level_nodes:
        if (node is not None):
            print(node._element, end = "")
            next_level_nodes.append(node._left)
            next_level_nodes.append(node._right)
        else:
            next_level_nodes.append(None)
            next_level_nodes.append(None)
            print_spaces(1)

        print_spaces(betweenSpaces)
    print()
    for i in range(1, endgeLines + 1):
        for j in range(0, len(this_level_nodes)):
            print_spaces(firstSpaces - i)
            if (this_level_nodes[j] == None):
                    print_spaces(endgeLines + endgeLines + i + 1);
                    continue
            if (this_level_nodes[j]._left != None):
                    print("/", end = "")
            else:
                    print_spaces(1)
            print_spaces(i + i - 1)
            if (this_level_nodes[j]._right != None):
                    print("\\", end = "")
            else:
                    print_spaces(1)
            print_spaces(endgeLines + endgeLines - i)
        print()

    print_internal(next_level_nodes, current_level + 1, max_level)

def all_elements_are_None(list_of_nodes):
    for each in list_of_nodes:
        if each is not None:
            return False
    return True

def print_spaces(number):
    for i in range(number):
        print(" ", end = "")




def main():
    ''' The following code will construct this tree:
               -               
              / \       
             /   \      
            /     \     
           /       \    
           *       +       
          / \     / \   
         /   \   /   \  
         +   4   -   2   
        / \     / \     
        3 1     9 5   
    ''' 
    t = Tree()
    a = t.add_root("-")
    b = t.add_left(a, "*")
    c = t.add_right(a, "+")
    d = t.add_left(b, "+")
    e = t.add_right(b, 4)
    t.add_left(d, 3)
    t.add_right(d, 1)
    f = t.add_left(c, "-")
    t.add_right(c, 2)
    t.add_left(f, 9)
    k = t.add_right(f, 5)
    #pretty_print(t)

    ''' The following code will construct this tree:
               1               
              / \       
             /   \      
            /     \     
           /       \    
           2       3       
          / \           
         /   \          
         4   5           
        / \             
        6 7 
    ''' 
         
    t2 = Tree()
    a2 = t2.add_root(1)
    b2 = t2.add_left(a2, 2)
    c2 = t2.add_right(a2, 3)
    d2 = t2.add_left(b2, 4)
    e2 = t2.add_right(b2, 5)
    f2 = t2.add_left(d2, 6)
    g2 = t2.add_right(d2, 7)
    #pretty_print(t2)




    print("-------------------Testing task 1 preorder--------------------")
    t.preorderPrint(a)  # a is the root
    print("-------------------Testing task 2 inorder--------------------")
    t.inorderPrint(a) # a is the root
    print("-------------------Testing task 3 postorder--------------------")
    t.postorderPrint(a)  # a is the root
    print("-------------------Testing task 4 levelorderPrint--------------------")
    t.levelorderPrint(a)  # a is the root
    print("-------------------Testing task 5 height--------------------")
    print("Height of Tree 1: Expected: 3;   Your answer:", t.height())
    print("Height of Tree 2: Expected: 3;   Your answer:", t2.height())
    print("-------------------Testing task 6 depth--------------------")
    print("Depth of '*' in Tree 1: Expected: 1;    Your answer:", t.depth(b))
    print("Depth of root in Tree 1: Expected: 0;    Your answer:", t.depth(a))
    print("Depth of leaf in Tree 1: Expected: 3;    Your answer:", t.depth(k))
    print("-------------------Testing task 7 return_max--------------------")
    print("Max value within Tree 2: Expected: 7;    Your answer:", t2.return_max())
    print("-------------------Testing task 8 flip_node--------------------")
    print("Tree 2 before flip_node:")
    #pretty_print(t2)
    t2.flip_node(t2._root)
    print("Tree 2 after flip_node:")
    #pretty_print(t2)
    print("-------------------Testing task 9 flip_tree--------------------")
    print("Tree 1 before flip_tree:")
    t.flip_tree(t._root)
    #pretty_print(t)
    print("Tree 1 after flip_tree:")
    #pretty_print(t)

# main()






