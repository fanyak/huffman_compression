# REF: http://web.mit.edu/6.02/www/s2010/handouts/labs/lab10.shtml
# template file for Lab #10, Task 1
import heapq
import lab10

# an object representing a node in a Huffman tree.
class Tree:
    def __init__(self,p,left,right=None):
        self.p = p          # probability associated with node
        self.left = left    # left child (any Python value if leaf)
        self.right = right  # right child (None if leaf)
        # depth ensures the algorithm prefers to combine shallow
        # trees when selected items of equal probability
        self.depth = 1 if right is None \
                     else 1 + max(self.left.depth,self.right.depth)

    # compare two tree nodes, sorting first by probability then
    # by depth of tree.  This is the low-level function called
    # by min or the less-than operator when the arguments are
    # instances of Tree.
    def __lt__(self,other):
        return self.p < other.p or \
               (self.p == other.p and self.depth < other.depth)

    # return True if this instance is a leaf of the tree
    def isLeaf(self):
        return self.depth == 1

    # recursive procedure to construct encoding dictionary
    # by walking the tree to find all the leaf nodes.
    def walk(self,encode_dict,prefix):
        if self.isLeaf():
            encode_dict[self.left] = prefix
        else:
            self.left.walk(encode_dict,prefix+[0])# add 0 if we move to the left
            self.right.walk(encode_dict,prefix+[1]) # add 1 if we move to the right

# arguments:
#   plist -- sequence of (probability,object) tuples
# return:
#   (dict,tree) where
#     dict is a dictionary mapping object -> binary encoding
#     tree is the Huffman tree built by the algorithm.
def huffman(plist):
    # initialize set of tree nodes as leaves of the tree
    tlist = [Tree(p,obj) for p,obj in plist]

    # Build Huffman tree by processing tlist until there is only a
    # single tree object left in the list (ie, the root of the
    # Huffman tree).  Consider using the heapq module.  You can
    # make a new node in the Huffman tree by calling
    #     Tree(probability,left_child,right_child).

    # your code here...
    # get the number of existing nodes
    n = len(tlist);
    ## use the heapq module to create a priority queue
    heapq.heapify(tlist);
    for i in range(n-1):
        # remove the nodes from the minimum probability from the heap
        left_child = heapq.heappop(tlist); # left node
        right_child = heapq.heappop(tlist); # right node
        propability = left_child.p + right_child.p
        # create a new node with 2 children (left,right) and key the sum of their probabilities
        newNode = Tree(propability,left_child,right_child) 
        # add the new child to the heap
        heapq.heappush(tlist,newNode);

    # walk the Huffman tree, adding an entry to the encoding
    # dictionary each time we find a leaf
    root = tlist[0]
    encoding_dict = {}
    root.walk(encoding_dict,[])

    # return (encoding dictionary,huffman tree)
    return (encoding_dict,root)

if __name__ == '__main__':
    # test case 1: four symbols with equal probability
    lab10.test_huffman(huffman,
                       # symbol probabilities
                       ((0.25,'A'),(0.25,'B'),(0.25,'C'),
                        (0.25,'D')),
                       # expected encoding lengths
                       ((2,'A'),(2,'B'),(2,'C'),(2,'D')))

    # test case 2: example from section 22.3 in notes
    lab10.test_huffman(huffman,
                       # symbol probabilities
                       ((0.34,'A'),(0.5,'B'),(0.08,'C'),
                        (0.08,'D')),
                       # expected encoding lengths
                       ((2,'A'),(1,'B'),(3,'C'),(3,'D')))

    # test case 3: example from Exercise 5 in notes
    lab10.test_huffman(huffman,
                       # symbol probabilities
                       ((0.07,'I'),(0.23,'II'),(0.07,'III'),
                        (0.38,'VI'),(0.13,'X'),(0.12,'XVI')),
                       # expected encoding lengths
                       ((4,'I'),(3,'II'),(4,'III'),
                        (1,'VI'),(3,'X'),(3,'XVI')))

    # test case 4: 3 flips of unfair coin
    phead = 0.9
    plist = []
    for flip1 in ('H','T'):
        p1 = phead if flip1 == 'H' else 1-phead
        for flip2 in ('H','T'):
            p2 = phead if flip2 == 'H' else 1-phead
            for flip3 in ('H','T'):
                p3 = phead if flip3 == 'H' else 1-phead
                plist.append((p1*p2*p3,flip1+flip2+flip3))
    expected_sizes = ((1,'HHH'),(3,'HTH'),(5,'TTT'))
    lab10.test_huffman(huffman,plist,expected_sizes)

    # when your code is ready to be submitted, enable the
    # call to lab10.checkoff.
    #lab10.checkoff(huffman,'L10_1')
    
    lab10.verify_task1(huffman)
