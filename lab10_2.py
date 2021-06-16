import numpy,random
import lab10
from lab10_1 import huffman

# arguments:
#   encoded_message -- numpy array of 0's and 1's
#   huffman_tree -- instance of Tree, root of Huffman tree
# return:
#   sequence of decoded symbols
def decode(huffman_tree,encoded_message):
    result = []

    # Use successive bits from encoded_message to guide
    # traversal of huffman_tree until a leaf is reached.
    # The value of the left slot will be the next symbol
    # to be appended to result.  Repeat until all the
    # bits of encoded_message have been consumed.

    next_node = tree;
    current = [];
    for bit in encoded_message:
        if bit:
            next_node = next_node.right
        else:
            next_node = next_node.left;
        current.append(bit);
        if next_node.isLeaf():
            for el in cdict:
                if cdict[el] == current:
                    result.append(el)
                    current = [];
            next_node = tree;

    # return the result sequence
    return result;

if __name__ == '__main__':
    # start by building Huffman tree from probabilities
    plist = ((0.34,'A'),(0.5,'B'),(0.08,'C'),(0.08,'D'))
    cdict,tree = huffman(plist)

    # test case 1: decode a simple message
    message = ['A', 'B', 'C', 'D']
    encoded_message = lab10.encode(cdict,message)
    decoded_message = decode(tree,encoded_message)
    assert message == decoded_message, \
           "Decoding failed: expected %s, got %s" % \
           (message,decoded_message)

    # test case 2: construct a random message and encode it
    message = [random.choice('ABCD') for i in range(100)]
    encoded_message = lab10.encode(cdict,message)
    decoded_message = decode(tree,encoded_message)
    assert message == decoded_message, \
           "Decoding failed: expected %s, got %s" % \
           (message,decoded_message)

    # when your code is ready to be submitted, enable the
    # call to lab10.checkoff.
    #lab10.checkoff((decode,cdict,tree),'L10_2')
    print(lab10.verify_task2(decode,cdict,tree))
