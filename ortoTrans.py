
import numpy as np

import pickle


A = np.array([[0.09754516100806412, 0.4157348061512726, 0.4903926402016152, 0.2777851165098011, -0.09754516100806418, -0.4157348061512726, -0.4903926402016152, -0.2777851165098011],
[0.1913417161825449, 0.46193976625564337, -0.19134171618254484, -0.4619397662556433, 0.19134171618254497, 0.46193976625564337, -0.19134171618254492, -0.46193976625564337],
[0.2777851165098011, 0.0975451610080643, -0.41573480615127273, 0.49039264020161527, -0.2777851165098016, -0.09754516100806404, 0.41573480615127284, -0.49039264020161505],
[0.35355339059327373, -0.35355339059327373, 0.3535533905932737, -0.35355339059327395, 0.3535533905932739, -0.35355339059327384, 0.3535533905932738, -0.3535533905932738],
[0.4157348061512726, -0.4903926402016152, 0.27778511650980114, 0.09754516100806443, -0.4157348061512725, 0.4903926402016152, -0.2777851165098007, -0.097545161008065],
[0.46193976625564337, -0.1913417161825452, -0.4619397662556432, 0.19134171618254456, 0.4619397662556438, -0.19134171618254472, -0.4619397662556431, 0.19134171618254653],
[0.4903926402016152, 0.2777851165098009, -0.09754516100806404, -0.4157348061512719, -0.4903926402016154, -0.2777851165098013, 0.09754516100806272, 0.4157348061512731],
[0.35355339059327373, 0.35355339059327373, 0.35355339059327373, 0.35355339059327373, 0.35355339059327373, 0.35355339059327373, 0.35355339059327373, 0.35355339059327373]])


x =  [0.729, 0.404, 0.804, 0.493, -0.493, -0.804, -0.404, -0.729]
A1 = np.linalg.inv(A)

y = np.matmul(A,x)

n = 3;

for i in range(len(y)):
    if i >= n: y[i] = 0

print(y)
x2 = np.matmul(A1,y)

ini = np.linalg.norm(x)
res = np.linalg.norm(x2)

prop = (res**2)/(ini**2)

print(prop*100)

print("NOW OTHER:")

import numpy as np
import matplotlib.pyplot as plt

from math import sqrt

from math import log2
def H_WH(N):
    def h(k):
        if k == 0:
            return np.array([1])
        if k == 1:
            return np.array([[1, 1], [1, -1]])
        return np.kron(h(1), h(k - 1))
    def arrange(M):
        def count_sign_changes(r):
            current_sign = 1
            counter = 0
            for x in r:
                if x != current_sign:
                    counter += 1
                    current_sign = x
            return counter
        R = np.zeros(M.shape)
        for row in M:
            i = count_sign_changes(row)
            R[i] = row
        return R
    H = h(log2(N))
    W = arrange(H) * 1/sqrt(N)
    return W


with  open('C:\\Users\\madal\\Downloads\\image.py', 'rb') as file:
    imagenCodigo = pickle.load(file)

imagenCodigo.pop(len(imagenCodigo) - 1)

parm = imagenCodigo[0]
n = parm[0]
m = parm[1]
print(n, m)
n_b = parm[2]
C = parm[3]

M = imagenCodigo[1:]

for k in range(1, len(imagenCodigo)):
    bc = imagenCodigo[k]

    a = np.zeros(shape=(n_b, n_b))
    h = 0
    for i in range(0, n_b):
        for j in range(0, n_b):
            if i + j < C:
                a[i][j] = bc[h]
                h += 1
    M[k - 1] = a

H = H_WH(n_b)
HT = np.transpose(H)

for i in range(0, len(M)):
    M[i] = np.dot(HT, M[i])
    M[i] = np.dot(M[i], H)
    M[i] = M[i] + 128

ImagenRecuperada = np.empty((n, m))

first = True

block = 0
ip = 0
jp = 0

for a in range(0, int(n / n_b)):

    for b in range(0, int(m / n_b)):
        if not first: block += 1
        for i in range(0, n_b):
            for j in range(0, n_b):
                ImagenRecuperada[a * n_b + i][b * n_b + j] = M[block][i % n_b][j % n_b]
                first = False

fig = plt.figure()
plt.imshow(ImagenRecuperada, cmap=plt.cm.gray, vmin=0, vmax=255)
plt.show()


