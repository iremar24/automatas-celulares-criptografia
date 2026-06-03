# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 10:42:55 2026

@author: Irene
"""

import numpy as np
import matplotlib.pyplot as plt

def reglas_automatas(num:int,pasos:int,celdas:int):
    """
    in: num es el entero que da nombre a la regla que queremos representar
        pasos y celdas son los enteros que indican el número de iteraciones a realizar y
        el número de columnas en cada tiempo
        
    out: la matriz resultante de la evolución del autómata
    """
    regla_bin = [int(x) for x in f"{num:08b}"]
    
    # inicializamos el tablero
    tablero=np.zeros((pasos,celdas),dtype=int)
    tablero[0,celdas//2]=1
    for t in range(pasos-1):
        for i in range(celdas):
            izq = str(tablero[t, (i - 1) % celdas])
            cen = str(tablero[t, i])
            der = str(tablero[t, (i + 1) % celdas])
            
            indice=int(izq+cen+der,base=2)
            
            tablero[t+1,i]=regla_bin[7-indice]
            
    return tablero

# ==================================================================================
# CONFIGURACIÓN Y VISUALIZACIÓN
# ==================================================================================
REGLA = 90
PASOS = 100
CELDAS = 200

resultado = reglas_automatas(REGLA, PASOS, CELDAS)

plt.figure(figsize=(10, 6))
plt.imshow(resultado, cmap='binary', interpolation='nearest')
plt.title(f"Autómata Celular - Regla {REGLA}", fontsize=20)
plt.axis('off')
plt.show()

