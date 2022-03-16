# -*- coding: utf-8 -*-
"""
@author: martinez
Jordi Armengol, Bruno Tamborero.
"""

import math
# ¿Se tenía que usar random? Estaba importado en el enunciado
# import random

from itertools import accumulate

# %%
"""
Dado un mensaje y su alfabeto con sus frecuencias dar el código 
que representa el mensaje utilizando precisión infinita (reescalado)
El intervalo de trabajo será: [0,R), R=2**k, k menor entero tal que R>4T
T: suma total de frecuencias
"""


# Basado en https://people.cs.nctu.edu.tw/~cmliu/Courses/Compression/chap4.pdf

def bitfield(n):
    return [int(digit) for digit in bin(n)[2:]]


def bitfield_to_dec(bit_array):
    dec = 0
    for i in range(len(bit_array)):
        dec += bit_array[-(i + 1)] * 2 ** i
    return dec


# Most significant bit equal
def equal_msb(a, b):
    return a[0] == b[0]


def get_bitfields_lower_upper(lower_bound, upper_bound, nbits):
    lower = bitfield(lower_bound)
    upper = bitfield(upper_bound)
    return (nbits - len(lower)) * [0] + lower, (nbits - len(upper)) * [0] + upper  # para que tengan nbits


def shift_left_and_set_lsb(bfield, bit):
    length = len(bfield)
    for i in range(1, len(bfield)):
        bfield[i - 1] = bfield[i]
    bfield[length - 1] = bit
    return bfield


def e3(lower, upper):
    return lower[0:2] == [0, 1] and upper[0:2] == [1, 0]


def IntegerArithmeticCode(mensaje, alfabeto, frecuencias):
    codigo = ''
    T = sum(frecuencias)
    acumuladas = [0] + list(accumulate(frecuencias))
    indices = dict(zip(alfabeto, range(len(frecuencias))))
    k = int(math.log2(4 * T)) + 1
    R = 2 ** k
    lower, upper = get_bitfields_lower_upper(0, R - 1, k)
    e3_counter = 0
    for c in mensaje:
        decimal_lower_bound = bitfield_to_dec(lower)
        decimal_upper_bound = bitfield_to_dec(upper)
        indice = indices[c]
        lower_c = acumuladas[indice]
        upper_c = acumuladas[indice + 1]
        new_lower = decimal_lower_bound + ((decimal_upper_bound - decimal_lower_bound + 1) * lower_c) // T
        new_upper = decimal_lower_bound + ((decimal_upper_bound - decimal_lower_bound + 1) * upper_c) // T - 1
        lower, upper = get_bitfields_lower_upper(new_lower, new_upper, k)
        while equal_msb(lower, upper) or e3(lower, upper):
            if equal_msb(lower, upper):  # escalado e1, e2
                b = lower[0]
                codigo += str(b) + e3_counter * str(1 - b)  # send b (+ los esperados por e3)
                lower = shift_left_and_set_lsb(lower, 0)
                upper = shift_left_and_set_lsb(upper, 1)
                e3_counter = 0
            if e3(lower, upper):  # escalado e3
                lower = shift_left_and_set_lsb(lower, 0)
                upper = shift_left_and_set_lsb(upper, 1)
                # complement
                lower[0] = 1 - lower[0]
                upper[0] = 1 - upper[0]
                e3_counter += 1
    for e in lower:
        codigo += str(e) + e3_counter * str(1 - e)
        if e3_counter > 0:
            e3_counter = 0
    return codigo


# %%


"""
Dada la representación binaria del número que representa un mensaje, la
longitud del mensaje y el alfabeto con sus frecuencias 
dar el mensaje original
"""


def IntegerArithmeticDecode(codigo, tamanyo_mensaje, alfabeto, frecuencias):
    mensaje = ''
    T = sum(frecuencias)
    k = int(math.log2(4 * T)) + 1
    R = 2 ** k
    acumuladas = list(accumulate(frecuencias))
    lower = [0] * k
    upper = [1] * k
    c_k = k
    t = []
    for i in range(c_k):
        t.append(int(codigo[i]))
    while len(mensaje) < tamanyo_mensaje:
        decimal_t = bitfield_to_dec(t)
        decimal_lower_bound = bitfield_to_dec(lower)
        decimal_upper_bound = bitfield_to_dec(upper)
        j = 0
        frec_acum = int(
            ((decimal_t - decimal_lower_bound + 1) * T - 1) / (decimal_upper_bound - decimal_lower_bound + 1))
        while acumuladas[j] <= frec_acum:
            j += 1
        mensaje += alfabeto[j]
        lower_c = 0 if j <= 0 else acumuladas[j - 1]
        upper_c = acumuladas[j]
        new_lower = decimal_lower_bound + ((decimal_upper_bound - decimal_lower_bound + 1) * lower_c) // T
        new_upper = decimal_lower_bound + ((decimal_upper_bound - decimal_lower_bound + 1) * upper_c) // T - 1
        lower, upper = get_bitfields_lower_upper(new_lower, new_upper, k)
        while equal_msb(lower, upper) or e3(lower, upper):
            if equal_msb(lower, upper):
                lower = shift_left_and_set_lsb(lower, 0)
                upper = shift_left_and_set_lsb(upper, 1)
                t = shift_left_and_set_lsb(t, int(codigo[c_k]))
                c_k += 1
            if e3(lower, upper):
                lower = shift_left_and_set_lsb(lower, 0)
                upper = shift_left_and_set_lsb(upper, 1)
                t = shift_left_and_set_lsb(t, int(codigo[c_k]))
                c_k += 1
                # complement
                lower[0] = 1 - lower[0]
                upper[0] = 1 - upper[0]
                t[0] = 1 - t[0]
    return mensaje


# %%


# %%
'''
Definir una función que codifique un mensaje utilizando codificación aritmética con precisión infinita
obtenido a partir de las frecuencias de los caracteres del mensaje.
Definir otra función que decodifique los mensajes codificados con la función 
anterior.
'''


def EncodeArithmetic(mensaje_a_codificar):
    fuente = {}
    for c in mensaje_a_codificar:
        if c not in fuente:
            fuente[c] = 1
        else:
            fuente[c] += 1
    alfabeto, frecuencias = list(fuente.keys()), list(fuente.values())
    mensaje_codificado = IntegerArithmeticCode(mensaje_a_codificar, alfabeto, frecuencias)
    return mensaje_codificado, alfabeto, frecuencias


def DecodeArithmetic(mensaje_codificado, tamanyo_mensaje, alfabeto, frecuencias):
    mensaje_decodificado = IntegerArithmeticDecode(mensaje_codificado, tamanyo_mensaje, alfabeto, frecuencias)
    return mensaje_decodificado


def firstXChars(msg, x):
    code = []
    for i in range(x): code.append(msg[i])
    return code


import math

def IntegerArithmeticCode(msg, alph, frq, R):
    m = 0
    M = R
    for i in range(len(msg)):
        j = 0
        while (alph[j] != msg[i]):
            j += 1
        ac_freq = 0
        for k in range(j): ac_freq += frq[k]
        diff = M - m
        m_aux = m
        m = m_aux + diff*ac_freq
        M = m_aux + diff*(ac_freq+frq[j])
    diff = M - m
    t = math.floor(math.log2(1/diff))
    val = math.pow(2,t)
    x = math.ceil(m*val)
    print ("m = ", m, "M = ", M, "X = ", x/val)
    return bin(x)


def dec2bin(x,nb=100):
	ans=''
	interv= 1.0
	while nb >= len(ans) and x != 0:
		interv/=2
		if x >= interv:
			ans+= '1'
			x-=interv
		else :
			ans+= '0'
	return ans


alph = ['a','b','c','d']
frq = [1,3,0.5,2]
length = 5
msg = dec2bin(0.46664)

print(msg)

code = DecodeArithmetic(msg, length, alph,frq)
print(code)
