import numpy as np
import time
import matplotlib.pyplot as plt
import imageio
import PIL
import pickle

with  open('C:\\Users\\madal\\Downloads\\imge2.py', 'rb') as file:
    imagenCodigo = pickle.load(file)

parm = imagenCodigo[0]
indices = imagenCodigo[len(imagenCodigo) - 1]
bloques = imagenCodigo[1:len(imagenCodigo) - 1]
dic = bloques[0]

n = parm[0]
m = parm[1]
n_b = parm[2]

first = True

bl = 0
block = indices[n_b]

ImagenRecuperada = np.empty((n, m))

for a in range(0, int(n / n_b)):

    for b in range(0, int(m / n_b)):
        if not first:
            bl += 1
            block = indices[bl]
        for i in range(0, n_b):
            for j in range(0, n_b):
                ImagenRecuperada[a * n_b + i][b * n_b + j] = dic[block][i % n_b][j % n_b]
                first = False

fig = plt.figure()
plt.imshow(ImagenRecuperada, cmap=plt.cm.gray, vmin=0, vmax=255)
plt.show()