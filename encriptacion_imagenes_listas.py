# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 16:41:47 2026

@author: Irene
"""

import numpy as np
from PIL import Image
from math import sin 


# ==================================================================================
# SECCIÓN 0. VALORES INICIALES
# ==================================================================================

# -------------------------------------------------------
#  VALORES DE LA CLAVE 
# -------------------------------------------------------

# Estos parámetros determinan la clave y tienen que ser 
# conocidos por el emisor y el receptor 

x0=0.36
y0=0.25     # x0,y0,z0 pertenecientes a (0,1)
z0=0.78

u= 1.5      # 0<u<3.999
 
k1= 35.5    #|k1|> 33.5
k2= 38.2    #|k2|> 37.5
k3= 36.1    #|k3|> 35.7


# -------------------------------------------------------
#  TABLA NECESARIA PARA FASE 2
# -------------------------------------------------------

#La tabla correspondiente a la tabla1 
tabla=[[1,0]]*4+[[0,1]]*2+[[1,0]]*2+[[0,1]]*4+[[1,0]]*4+[[0,1]]*6+[[1,0]]*2+[[0,1]]*2+[[1,0]]*2+[[0,1]]*4


# ==================================================================================
# SECCIÓN 1. OPERACIONES AUXILIARES CON MATRICES
# ==================================================================================
  
def aplanaMatriz(matriz:list)->list:
    """
    
    in: Matriz
    
    out: convierte la matriz en una sola lista concatenando sus filas
    
    Example:
    ----------
    >>> aplanaMatriz([[1,2,3],[4,5,6],[7,8,9]])
        [1, 2, 3, 4, 5, 6, 7, 8, 9]
        
    """
    result=[]
    for fila in matriz:
        result+=fila
    return result


def DesAplana(lista:list,m:int,n:int)->list:
    """
    
    in : lista, m y n enteros 
    
    out: Matriz MxN transformada de la lista 
    
    Example:
    ----------
    >>> DesAplana([1, 2, 3, 4, 5, 6, 7, 8, 9],3,3)
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        
    """
    result=[]
    ind=0
    for i in range(m):
        fila=[]
        for j in range(n):
            fila.append(lista[ind])
            ind+=1
        result.append(fila)
    return result


def Desaplana4(lista:list,m:int,n:int)->list:
    """
    
    in : lista de 0 y 1 con longitud un múltiplo de 4 ,m y n ints
    
    out: matriz de mxn donde cada elemento es el entero asociado a cada pack de 4 bits
    
    Example:
    ----------
    >>> Desaplana4([0,1,1,0,1,0,1,1,1,0,1,0,0,0,1,1],2,2)
        [[6, 11], [10, 3]]
    """
    result=[]
    ind=0
    for i in range(m):
        fila=[]
        for j in range(n):
            elem=lista[ind]<<3 | lista[ind+1]<<2 | lista[ind+2]<<1 | lista[ind+3]
            fila.append(elem)
            ind+=4
        result.append(fila)
    return result


def unionBits(altos:list,bajos:list)->list:
    """
    
    in : Dos matrices
    
    out: Unión de las dos matrices , siendo cada elemento la union de los 4 bits de la primera
    como superiores mas los 4 bits de la segunda como inferiores
    
    Example: 
    ----------
    >>> unionBits([[16, 32, 128], [48, 0, 208]],[[13, 10, 2], [2, 2, 12]])
        [[29, 42, 130], [50, 2, 220]]
         
    """
    matriz=[]
    m=len(altos)
    n=len(altos[0])
    for i in range(m):
        fila=[]
        for j in range(n):
            elem1=altos[i][j]
            elem2=bajos[i][j]
            if elem1<=15:
                elem1=elem1<<4
            if elem2>15:
                elem2=elem2>> 4
                
            fila.append(elem1 | elem2 )
        matriz.append(fila)
    return matriz

def union4BitsAltos(matriz:list)->list:
    """
    
    in : matriz Mx4N con elementos int 0 o 1 
    
    out : matriz MxN resultante de agrupar cada 4 bits tomándolos como los 4 bits altos
    
    Example:
    ----------
    >>> union4BitsAltos([[0,1,1,0,1,0,1,1],[1,0,1,0,0,0,1,1]])
        [[96, 176], [160, 48]]   (bin(96)=0110 0000)

    """
    m=len(matriz)
    n=len(matriz[0])
    nueva_matriz=[]
    for i in range(m):
        fila=[]
        for j in range(0,n,4):
            elem=matriz[i][j]<<3 | matriz[i][j+1] <<2 |matriz[i][j+2]<<1 | matriz[i][j+3]
            fila.append(elem<<4)
        nueva_matriz.append(fila)
    return nueva_matriz

def union4BitsBajos(matriz:list)->list:
    """
    
    in : matriz Mx4N con elementos int 0 o 1 
    
    out : matriz MxN resultante de agrupar cada 4 bits tomándolos como los 4 bits bajos
    
    Example:
    ----------
    >>> union4BitsBajos([[0,1,1,0,1,0,1,1],[1,0,1,0,0,0,1,1]])
        [[6, 11], [10, 3]]    (bin(6)=0000 0110)

    """
    m=len(matriz)
    n=len(matriz[0])
    nueva_matriz=[]
    for i in range(m):
        fila=[]
        for j in range(0,n,4):
            elem=matriz[i][j]<<3 | matriz[i][j+1] <<2 |matriz[i][j+2]<<1 | matriz[i][j+3]
            fila.append(elem)
        nueva_matriz.append(fila)
    return nueva_matriz


def bitsAltos(matriz:list)->list:
    """
    
    in: Dada una matriz 
    
    out: Devuelve la matriz formada por los bits altos
    
   
    Example
    --------
    >>> bitsAltos([[29,42,130],[50,2,220]])
        [[16, 32, 128], [48, 0, 208]]
   
    """
    matrizAlta=[]
    m=len(matriz)
    n=len(matriz[0])
    mascaraAltos=0b11110000
    for i in range(m):
        fila=[]
        for j in range(n):
            fila.append(mascaraAltos & matriz[i][j])
        matrizAlta.append(fila)
    return matrizAlta




def bitsBajos(matriz:list)->list:
    """
    
    in: Dada una matriz 
    
    out: Devuelve la matriz formada por los bits bajos
    
    Example
    --------
    >>> bitsBajos([[29,42,130],[50,2,220]])
        [[13, 10, 2], [2, 2, 12]]
   
    """
    matrizBaja=[]
    m=len(matriz)
    n=len(matriz[0])
    mascaraBajos=0b00001111
    for i in range(m):
        fila=[]
        for j in range(n):
            fila.append(mascaraBajos & matriz[i][j])
        matrizBaja.append(fila)
    return matrizBaja


def separaBits(matriz:list)->list:
    """
    
    in  : Dada una matriz MxN donde los elementos solo tienen la parte alta o baja de sus bits
    
    out : Devuelve matriz Mx4N con cada bit separado (0 ó 1)
        
    Example:
    ---------
    >>> separaBits([[13, 10, 2], [2, 2, 12]])
        [[1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0], [0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0]]
    
    """
    
    nueva_matriz=[]
    m=len(matriz)
    n=len(matriz[0])
    masc1=0b1000
    masc2=0b0100
    masc3=0b0010
    masc4=0b0001
    mascaras=[masc1,masc2,masc3,masc4]
    for i in range(m):
        fila=[]
        for j in range(n):
            elem=matriz[i][j]
            if elem>15:
                elem=elem>>4
            for k in range(4):
                if elem & mascaras[k]>0:
                    fila.append(1)
                else:
                    fila.append(0)
        nueva_matriz.append(fila)
    return nueva_matriz
    

# ==================================================================================
# SECCIÓN 2. FASE 1: CONFUSIÓN
# ==================================================================================
  
def separa2(matriz:list)->list:
     """
     in: Dada una matriz de bin MxN
         
     out: Devolverá la matriz Mx2N resultante de separar cada número (8 bits) por la mitad
          cada mitad estará en una columna distinta

     Example
     ------
     >>> separa2([[139,23,12],[43,159,138]])
         [[128, 11, 16, 7, 0, 12], [32, 11, 144, 15, 128, 10]]
     """
     m=len(matriz)
     n=len(matriz[0])
     mascaraAltos=0b11110000
     mascaraBajos=0b00001111
     
     nueva_matriz=[]
     for i in range(m):
         nueva_fila=[]
         for j in range(n):
             elem=matriz[i][j]
             nueva_fila.append(elem & mascaraAltos)
             nueva_fila.append(elem & mascaraBajos)
         nueva_matriz.append(nueva_fila)
     return nueva_matriz
 
 
def junta2(matriz:list)->list:
    """
    
    in: Matriz Mx2N
    
    out : Matriz MxN donde se han unido cada par de elementos
    
    Example:
    ----------
    >>> junta2([[128, 11, 16, 7, 0, 12], [32, 11, 144, 15, 128, 10]])
        [[139, 23, 12], [43, 159, 138]]
         
    """
    m=len(matriz)
    n=len(matriz[0])
    nueva_matriz=[]
    for i in range(m):
        nueva_fila=[]
        for j in range(0,n,2):
            elem=matriz[i][j]
            elem2=matriz[i][j+1]
            if elem<=15: # está en la parte baja, hay  que desplazar a la alta
                elem=elem<<4
            if elem2>15 : #esta en la parte alta, hay que desplazar a la baja
                elem2 = elem2>>4
            nueva_fila.append(elem| elem2)
        nueva_matriz.append(nueva_fila)
    return nueva_matriz
 
#Para este paso es necesario haber pactado los valores
#iniciales con el receptor, x0,y0,z0,u,k1,k2 y k3

def x_y_z(matriz:list,x0:float,y0:float,z0:float,u:float,k1:float,k2:float,k3:float)->list:
    """
    in: Dada una matriz de bin 
        
    out: Devolverá los valores x, y, z asociados al mapa caótico
    
    Example:
    ----------
    x_y_z([['00111000', '00110111'], ['00110110', '00111000']])
     
    ([0.29999999999999893, 0.95511034471805, 0.4589528513769614, 0.9654747230881349,
     0.726253173680864, 0.38287769637623903, 0.5636860010224893, 0.7190836419857214],
     [0.04059633027523013, 0.5572511324639962, 0.03532236870436378, 0.5145209133675017,
      0.9929158802135127, 0.6869704321108756, 0.11364880471931116, 0.5638859190396097],
     [0.44188213370884455, 0.1269141527519082, 0.9478104122549009, 0.7803213978473096,
      0.9091245400766681, 0.9886267010853445, 0.07859908416606487, 0.4028641393942234])

    """
    
   # La clave sera : (x0,y0,z0,u,k1,k2,k3)
    #creamos los xn,yn,zn
    x=[x0]
    y=[y0]
    z=[z0]
    m=len(matriz)
    n=len(matriz[0])
    #creamos el mapa caotico
    for l in range(m*n*2): 
        x.append((u*k1*y[l]*(1-x[l])+z[l])%1)
        y.append((u*k2*y[l]+z[l]*1/(1+(x[l+1])**2))% 1)
        z.append((u*(x[l+1]+y[l+1] + k3)*sin(z[l]))%1)
        
    #vamos desde el uno para no usar los valores x0,y0,z0
    return x[1:],y[1:],z[1:]



def f_hats(x:list,y:list,z:list,m:int,n:int)->list:
      """
      in: Dados x,y,z y las dimensiones m,n 
          
      out: Devolverá los x_gorro,y_gorro y z_gorro discretizando las secuencias del mapa caótico

      Example:
      ----------
      >>> f_hats(x,y,z,2,2) (siendo los x,y,z del resultado anterior)
          ([1, 0, 1, 1], [0, 1, 1, 1], [0, 1, 1, 1, 0, 1, 0, 0])
      """
      x_hat=[]
      y_hat=[]
      z_hat=[]
      
      for k in range(m*n):
         x_hat.append(int((x[k]*10**13)%m))
         y_hat.append(int((y[k]*10**13)%n))
      for k in range(m*n*2): #z_hat vale más pues después se necesitará 
         z_hat.append(int((z[k]*10**13)%2))
        
      return x_hat,y_hat,z_hat  



def permutacion(matriz:list,x_hat,y_hat)->list:
    """
    in: Dada una matriz
        
    out: Devolverá la matriz resultante de intercambiar de posición sus celdas
         intercambiando la pos M i,j por la M x_hat_i,y_hat_j
    
    Example:
    ----------
    >>> permutacion([[4,7,2],[2,6,8]],[0,1,1,0,0,1],[2,1,0,2,2,1])
        [[2, 6, 7], [2, 8, 4]]
   
    """
    resultado=[fila.copy() for fila in matriz]
    m=len(resultado)
    n=len(resultado[0])
    ind_caos=0
    for i in range(m):
        for j in range(n):
            nueva_i=x_hat[ind_caos]
            nueva_j=y_hat[ind_caos]
            elem_inicial=resultado[i][j]
            resultado[i][j]=resultado[nueva_i][nueva_j]
            resultado[nueva_i][nueva_j]=elem_inicial
            ind_caos+=1
    
    return resultado

    
# ==================================================================================
# SECCIÓN 3. FASE 2: DIFUSIÓN
# ==================================================================================


def tabla1(matriz:list,tiempo:int,Sini:list):
    """
    in: matriz, tiempo t y un estado inicial Sini con las mismas dimensiones que la matriz
        Ambas matrices de 0 o 1 
    
    out: Estados St+1 y St tras aplicar t veces la tabla 1 con las reglas locales de nuestro 
        Autómata Celular Reversible
    
    Example:
    ----------
    >>> tabla1([[0, 0, 1, 0, 1, 1, 1, 0], [0, 0, 1, 1, 0, 1, 1, 0]] , 6 , [[0, 1, 0, 0, 0, 1, 0, 1], [0, 0, 0, 1, 1, 0, 0, 0]])
        ([[0, 0, 1, 0, 0, 1, 1, 0], [1, 0, 1, 1, 1, 0, 0, 0]],
         [[0, 1, 0, 1, 0, 0, 1, 0], [0, 0, 1, 1, 0, 1, 0, 1]])
    """
    S=[Sini,matriz]
    m=len(matriz)
    n=len(matriz[0])
    for t in range(1,tiempo):
        St_nueva=[]
        for i in range(m):
            fila_nueva=[]
            for j in range(n):
                St=S[t]
                St_vieja=S[t-1]
                iz=St[i][(j-1)%n]
                arriba=St[(i-1)%m][j]
                centro=St[i][j]
                abajo=St[(i+1)%m][j]
                dcha=St[i][(j+1)%n]
                
                pos=(iz << 4) | (arriba << 3) | (centro << 2) | (abajo << 1) | dcha
                
                ind = St_vieja[i][j]
                fila_nueva.append(tabla[pos][ind])
            St_nueva.append(fila_nueva)
        S.append(St_nueva)
        
    #Para poder descifrar después vamos a guardar ambos
    return S[-1],S[-2]
            

def opFinal(matriz:list,z:list,Cini:int)->list:
    """
    in: matriz de int mxn, z lista de longitud m*n, Cini entero dado
   
    out: una matriz mxn resultante de aplicar una fase de difusión final en
         cascada para garantizar la encriptación de los 4 bits bajos
    
    Example:
    -----------
    z=[0.44188213370884455, 0.1269141527519082, 0.9478104122549009, 0.7803213978473096,0.9091245400766681,
      0.9886267010853445, 0.07859908416606487, 0.4028641393942234, 0.04441778045339362]
    
    >>> opFinal([[28,140,88],[3,126,39]],z,168)
        [[180, 231, 10], [96, 160, 162]]
    
    """
    m=len(matriz)
    n=len(matriz[0])
    matriz1D=aplanaMatriz(matriz)
    C=[Cini]
    for i in range(n*m):
        #usamos C[i] para usar el ultimo elem añadido
        nuevoC=C[i] ^ matriz1D[i] ^ int(z[i]*(10**13))%256
        C.append(nuevoC)
        #C tiene m*n+1, descartamos el Cini
    return DesAplana(C[1:],m,n)


# ==================================================================================
# SECCIÓN 4. FUNCIÓN FINAL DEL ALGORITMO DE ENCRIPTACIÓN DE IMÁGENES
# ==================================================================================


def encripta_img(img:str,x0:int,y0:int,z0:int,u:int,k1:int,k2:int,k3:int,tiempo:int):
    """
    in: Dada una imagen, pasado su nombre en str, y los valores de las claves
        
    out: Devolverá la matriz después de la fase 1 de confusión y la 2 de difusión
    
    Example:
    ---------
    >>> Encripta_img("p1.png",x0,y0,z0,u,k1,k2,k3,6)
    
    """
    # FASE 1 
    imagen=img=Image.open(img).convert("L")
    #añadimos el convert("L") para que sea en escala de grises
    matriz = np.array(imagen)
    
    
    m2=separa2(matriz) # da la matriz Mx2N
    
    #calculamos los parametros gorro
    #en la Fase 1 usaremos x e y , en la Fase 2 el z
    x,y,z=x_y_z(m2,x0,y0,z0,u,k1,k2,k3)
    x_hat,y_hat,z_hat=f_hats(x,y,z,len(m2),len(m2[0]))
    
    m_permutada=permutacion(m2,x_hat,y_hat)
    
    m_juntada=junta2(m_permutada)
    
    
    #FASE 2
    #vamos a separar la matriz permutada en los bits altos y los bajos
    mAltos=bitsAltos(m_juntada) 
    mBajos=bitsBajos(m_juntada)
    
    #separamos en cada bit para poder aplicar la tabla 1
    mAltos_sep=separaBits(mAltos) 
    mBajos_sep=separaBits(mBajos)
    #sus elementos son 0 o 1
    
    # Para obtener el S-1 convertiremos z_hat en matriz
    m_nuevo=len(mAltos)
    n_nuevo=len(mAltos[0])
    S_menos1=Desaplana4(z_hat,m_nuevo,n_nuevo)
    S_menos1_sep=separaBits(S_menos1)
    #Los elementos de S_menos1 son 0 o 1
    
    
    #guardamos los dos ultimos estados para poder desencriptar bien y no perder información 
    Saltos,Saltos2=tabla1(mAltos_sep,tiempo,S_menos1_sep)
    Sbajos,Sbajos2=tabla1(mBajos_sep,tiempo,S_menos1_sep)
    
    Saltos_uni=union4BitsAltos(Saltos)
    Saltos2_uni=union4BitsAltos(Saltos2)
    
    Sbajos_uni=union4BitsBajos(Sbajos)
    Sbajos2_uni=union4BitsBajos(Sbajos2)
    #ahora las 4 matrices unidas son de enteros, agrupando cada 4 bits , no solo de 0 y 1
    

    unidos=unionBits(Saltos_uni,Sbajos_uni)
    unidos2=unionBits(Saltos2_uni,Sbajos2_uni)
    # Para poder desencriptar al completo después, devolveremos una matriz con el doble de filas 
    # que la original, para poder revertir las operaciones y tener la información suficiente
    
    # Hay que añadir una operación extra por si la información se encontrarara en los bits inferiores
    #usaremos Cini=168
    Cini=168
    C=opFinal(unidos,z,Cini)
    
    
    C2=opFinal(unidos2,z,Cini)

    Cf=C+C2
    
    mfinal=np.array(Cf).astype(np.uint8)
    img_final=Image.fromarray(mfinal)
    return img_final
                
                
# ==================================================================================
# SECCIÓN 5. DESENCRIPTACIÓN DE IMÁGENES
# ==================================================================================
        
def opFinal_inv(matriz:list,z:list,Cini:int)->list:
    """
        La inversa de OpFinal anterior
    
    in: matriz int, z lista de m*n, Cini entero dado
   
    out: una matriz m*n 
    
    Example:
    -----------
    z=[0.44188213370884455, 0.1269141527519082, 0.9478104122549009, 0.7803213978473096,0.9091245400766681,
       0.9886267010853445, 0.07859908416606487, 0.4028641393942234, 0.04441778045339362]
    >>> opFinal_inv([[180, 231, 10], [96, 160, 162]], z ,168)
        [[28, 140, 88], [3, 126, 39]]

    
    """
    m=len(matriz)
    n=len(matriz[0])
    matriz1D=aplanaMatriz(matriz)
    C=[Cini]+matriz1D
    P=[]
    for i in range(n*m):
        #usamos C[i] para usar el ultimo elem añadido
        nuevop=C[i] ^ C[i+1] ^ int(z[i]*(10**13))%256
        P.append(nuevop)
    
    return DesAplana(P,m,n)


def tabla1_inv(matriz:list,tiempo:int,Sf:list):
    """
        La inversa de tabla1
        
    in: matriz, tiempo t y un estado final Sf con las mismas dimensiones que la matriz
        Ambas matrices de enteros 0 o 1
    
    out: Estado St+1, St resultados tras aplicar t veces la tabla 1 con las reglas locales de nuestro 
        Autómata Celular Reversible
    
    Example:
    ----------
    >>>tabla1_inv([[1, 0, 1, 1, 1, 0, 1, 1], [1, 0, 0, 1, 1, 0, 1, 0]],5 ,[[1, 1, 1, 0, 1, 1, 1, 0], [1, 0, 0, 1, 0, 1, 0, 0]])
        ([[1, 0, 1, 0, 1, 1, 0, 0], [0, 0, 1, 1, 0, 1, 0, 1]],
         [[1, 1, 0, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 0, 1, 1]])
    
    """
    #la sf sera los bits bajos por como encriptamos
    m=len(matriz)
    n=len(matriz[0])
    S=[matriz,Sf]
    for t in range(1,tiempo):
        St_nueva=[]
        for i in range(m):
            fila_nueva=[]
            for j in range(n):
                St_fut=S[t-1]
                St_pre=S[t]
                
                iz=St_pre[i][(j-1)%n]
                arriba=St_pre[(i-1)%m][j]
                centro=St_pre[i][j]
                abajo=St_pre[(i+1)%m][j]
                dcha=St_pre[i][(j+1)%n]
                
                pos=(iz << 4) | (arriba << 3) | (centro << 2) | (abajo << 1) | dcha
                
    
                ind=0
                if St_fut[i][j]==tabla[pos][0]:
                    ind=0
                elif St_fut[i][j]==tabla[pos][1]:
                    ind=1
                
                fila_nueva.append(ind)
            St_nueva.append(fila_nueva)
        S.append(St_nueva)
    return S[-2],S[-1]


def permutacion_inv(matriz:list,x_hat,y_hat)->list:
    """
        La permutacion inversa 
    in: Dada una matriz
        
    out: Devolverá la matriz resultante de intercambiar de posición sus celdas

    Example:
    ----------
    >> permutacion_inv([[2, 6, 7], [2, 8, 4]],[0,1,1,0,0,1],[2,1,0,2,2,1])
        [[4, 7, 2], [2, 6, 8]]
   
    """
    
    m=len(matriz)
    n=len(matriz[0])
    ind_caos=m*n-1
    for i in range(m-1,-1,-1):
        for j in range(n-1,-1,-1):
            nueva_i=x_hat[ind_caos]
            nueva_j=y_hat[ind_caos]
            elem_inicial=matriz[i][j]
            matriz[i][j]=matriz[nueva_i][nueva_j]
            matriz[nueva_i][nueva_j]=elem_inicial
            ind_caos-=1
    
    return matriz 


def copia_matriz(matriz)->list:
    """
    in : dada una matriz (en nuestro caso un array de la imagen )
    
    out : una matriz (lista de listas) copia de la dada
    
    Example:
    ---------
    m=array([[140, 139, 139, ...,  96,  95,  96],
        [125, 124, 125, ...,  83,  83,  83]], dtype=uint8)
    
    >>> copia_matriz(m)
        ([[140, 139, 139, ..., 96, 95, 96],[125, 124, 125, ..., 83, 83, 83]])
    """
    
    nueva=[]
    for i in range(len(matriz)):
        fila=[]
        for j in range(len(matriz[0])):
            fila.append(matriz[i][j])
        nueva.append(fila)
    return nueva

def desEncripta_img(img:str,x0:int,y0:int,z0:int,u:int,k1:int,k2:int,k3:int,tiempo:int):
    """
    in : nombre de la matriz en str y los valores correctos de la clave
    
    out : devuelve la imagen desencriptada
    
    Example:
    ---------
    >>> desEncripta_img("p1_encriptada.png",x0,y0,z0,u,k1,k2,k3,6)
    """
    #Proceso inverso
    imagen=img=Image.open(img).convert("L")
    #añadimos el convert("L") para que sea en escala de grises
    matriz = np.array(imagen)
    
    matriz2=copia_matriz(matriz) # no del tipo (array dtype=uint8)
    
    m=len(matriz2)
    
    mini=matriz2[:m//2][:]
    mini2=matriz2[m//2:][:]
    #mini1==C y mini2==C2 de antes
    
    m2=separa2(mini)
    
    x,y,z=x_y_z(m2,x0,y0,z0,u,k1,k2,k3)
    x_hat,y_hat,z_hat=f_hats(x,y,z,len(m2),len(m2[0]))
    
    P1=opFinal_inv(mini,z,168)
    P2=opFinal_inv(mini2,z,168)
    
    
    mAltos=bitsAltos(P1) 
    mBajos=bitsBajos(P1) 
    
    #los mBajos coinciden con los Sbajos_uni de antes
    #los mAltos coinciden con los Saltos_uni
    
    mAltos2=bitsAltos(P2) 
    mBajos2=bitsBajos(P2) 
    
    mAltos_sep=separaBits(mAltos)
    mBajos_sep=separaBits(mBajos)
    
    mAltos_sep2=separaBits(mAltos2)
    mBajos_sep2=separaBits(mBajos2)
    
    S0alt,z2=tabla1_inv(mAltos_sep,tiempo,mAltos_sep2) 
    S0baj,z22=tabla1_inv(mBajos_sep,tiempo,mBajos_sep2)
    
    S0alt_uni=union4BitsAltos(S0alt)
    S0baj_uni=union4BitsBajos(S0baj)
    
    unidos=unionBits(S0alt_uni,S0baj_uni)
 
   
    unidos2=separa2(unidos)

    
    mp=permutacion_inv(unidos2,x_hat,y_hat)  
    
    mpJuntas=junta2(mp)
    
    mfinal=np.array(mpJuntas).astype(np.uint8)
    img_final=Image.fromarray(mfinal)
    return img_final