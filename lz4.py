# input [token1,token2,extra]
def getSizeByToken(t):
    size = 0
    for i in range(0,len(t)):
        if i != 1:
            size += int(str(t[i]), 2)
    return size

# input [ofsset1,offset2]
def getOffset(off):
    total = off[1] + off[0]
    return int(str(total), 2)

# input [token2,extra]
def getMatchLengthByToken(t):
    length = 0
    length += 4 + int(str(t[0]), 2)
    for i in range(1,len(t)):
        length += int(str(t[i]), 2)
    return length

# output array de bytes
def getInputFile(fileName):
    f = open("C:\\Users\\madal\\Downloads\\" + fileName, mode = 'rb')
    bytes = []
    while(byte := f.read(1)): bytes.append('{0:08b}'.format(ord(byte)))
    return bytes


bytes = getInputFile("YeMi.dna.lz4")

i = 0

acabar = False
blocks = []

while i < len(bytes):

    token = [bytes[i][:4], bytes[i][4:]]
    literalLength = []
    L = 0

    if token[0] == '1111':
        i += 8
        while bytes[i:i+8] == '11111111':
            literalLength.append(bytes[i:i+8])
            i += 8
        literalLength.append(bytes[i:i+8])

    L = getSizeByToken(token+literalLength)
    literals = []
    i += 8
    for k in range(0,L):
        literals.append(bytes[i:i+8])
        i += 8

    offset = []
    offset.append(bytes[i:i+8])
    i += 8
    offset.append(bytes[i:i+8])
    i += 8
    matchLength = []
    if token[1] == '1111':
        while bytes[i:i+8] == '11111111':
            matchLength.append(bytes[i:i+8])
            i += 8
        matchLength.append(bytes[i:i+8])

    blocks.append([token,literalLength,literals,offset,matchLength])

print(blocks)
