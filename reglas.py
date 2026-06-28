# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 10:42:55 2026

@author: Irene
"""

import numpy as np
import matplotlib.pyplot as plt

def reglas_automatas(num:int,pasos:int,celdas:int,v0):
    """
    in: Num es el entero que da nombre a la regla que queremos representar
        pasos y celdas son los enteros que indican el número de iteraciones a realizar y
        el número de columnas en cada tiempo, v0 el el vector con la configuración inicial
        
    out: Matriz resultante de la evolución del autómata
    """
    regla_bin = [int(x) for x in f"{num:08b}"]
    
    # inicializamos el tablero
    tablero=np.zeros((pasos,celdas),dtype=int)
    tablero[0]=v0
    for t in range(pasos-1):
        for i in range(celdas):
            izq =tablero[t, (i - 1) % celdas]
            cen = tablero[t, i]
            der = tablero[t, (i + 1) % celdas]
            
            indice = (izq<<2) | (cen<<1) | der 
            
            tablero[t+1,i]=regla_bin[7-indice]
            
    return tablero

# ==================================================================================
# CONFIGURACIÓN Y VISUALIZACIÓN
# ==================================================================================


regla = 30
pasos = 100
celdas = 200
v0=np.zeros(celdas)
v0[celdas//2]=1


# Para estudiar más a fondo el autómata de la regla 110 para ver su universalidad,
# se ha usado como configuración el vector v0 aleatorio, 200 pasos y 300 celdas

v0_aleatorio = np.random.randint(0, 2, size=celdas)




resultado = reglas_automatas(regla, pasos, celdas,v0)

plt.figure(figsize=(10, 6))
plt.imshow(resultado, cmap='binary', interpolation='nearest')
plt.title(f"Autómata Celular - Regla {regla}", fontsize=20)
plt.axis('off')
plt.show()

