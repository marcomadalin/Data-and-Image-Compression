
import numpy as np
import time
import matplotlib.pyplot as plt
import imageio
import PIL
import pickle

with  open('C:\\Users\\madal\\Downloads\\imge.py', 'rb') as file:
    imagenCodigo = pickle.load(file)

parm = imagenCodigo[0]
bloques = imagenCodigo[1:]

n = parm[0]
m = parm[1]
n_b = parm[2]
bit = parm[3]
levels = 2 ** bit

ImagenRecuperada = np.empty((n, m))

for k in range(0, len(bloques)):
    b = bloques[k]
    min = b[0][0]
    M = b[0][1] + 1
    # print(min,M)
    step = (M - min) / levels
    limits = []
    act = min
    for i in range(0, levels + 1):
        limits.append(act + i * step)

    bl = b[1]

    # print("////// inicial: " )
    # print(bl)

    # print("////// limits: ")
    # print(limits)

    for i in range(0, n_b):
        for j in range(0, n_b):
            elm = bl[i][j]
            Min = limits[elm - 1]
            Max = limits[elm]
            new_elm = (Max + Min) / 2
            bl[i][j] = new_elm

            # print("elm ini = ", elm," // Min = ", Min, " // Max = ", Max," // elm fin = ", new_elm)
    # print("////// final: " )
    # print(bl)
    bloques[k] = bl

n_bloq = 0
first = True

for a in range(0, int(n / n_b)):

    for b in range(0, int(m / n_b)):

        if not first: n_bloq += 1
        for i in range(0, n_b):
            for j in range(0, n_b):
                ImagenRecuperada[a * n_b + i][b * n_b + j] = bloques[n_bloq][i % n_b][j % n_b]

                first = False

fig = plt.figure()
plt.imshow(ImagenRecuperada, cmap=plt.cm.gray, vmin=0, vmax=255)
plt.show()