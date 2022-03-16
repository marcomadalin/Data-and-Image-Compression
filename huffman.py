import heapq
from binarytree import Node

def mergeNodes(n1, n2):
    n3 = Node(n1.value + n2.value)
    if (n1.value <= n2.value):
        n3.right = n2
        n3.left = n1
    else:
        n3.right = n1
        n3.left = n2
    return n3

def huffmanTree(p):
    for i in range(len(p)): p[i] = Node(p[i])
    heapq.heapify(p)

    while len(p) > 1:
        n1 = heapq.heappop(p)
        n2 = heapq.heappop(p)
        heapq.heappush(p,mergeNodes(n1,n2))

    return heapq.heappop(p)

def computeSumOfLengths(tree,sum,codeLength):
    if (tree):
        if (not tree.right and not tree.left): sum[0] += codeLength
        else:
            if (tree.right): computeSumOfLengths(tree.right,sum,codeLength+1)
            if (tree.left): computeSumOfLengths(tree.left,sum,codeLength+1)
    return

def averageCodeLength(tree,chars):
    sum = [0]
    codeLength = 0
    computeSumOfLengths(tree,sum,codeLength)
    return sum[0]/chars

def getFrequencies(msg):
    codeFreq = {}
    for i in range(len(msg)):
        val = codeFreq.get(msg[i],-1)
        if (val == -1): val = 1
        else: val = val + 1
        codeFreq.update({msg[i]:val})
    freq = []
    for v in codeFreq.values(): freq.append(v)
    return freq


def averageLengthFromCodeString(code):
    sum = 0
    num = 1
    i = 0
    while (i < len(code)):
        if (code[i] == '0' or code[i] == '1'): sum += 1
        elif (code[i] == ','): num += 1
        i = i+1
    return sum/num


freq = [0.0129, 0.0355, 0.0138, 0.0103, 0.0416, 0.0244, 0.0401, 0.0149, 0.0192, 0.0083, 0.0036, 0.0052, 0.0277, 0.0052, 0.0134, 0.0121, 0.7118]
tree = huffmanTree(list.copy(freq))
print ("Average Length = ", averageCodeLength(tree,len(freq)))

code1 = "['010101', '0010', '00111', '011110', '0100', '01011', '0110', '00110', '01110', '000010', '0111111', '0111110', '0001', '000011', '00000', '010100', '1']"
print("Average code 1 length = ", averageLengthFromCodeString(code1))

