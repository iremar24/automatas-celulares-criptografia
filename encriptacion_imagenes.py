# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 16:41:47 2026

@author: Irene
"""

import numpy as np
from PIL import Image
from math import sin 


# ==================================================================================
# SECCIÓN 1. OPERACIONES AUXILIARES CON MATRICES
# ==================================================================================
  
def aplanaMatriz(matriz:list)->list:
    """
    
    in: Matriz
    
    out: convierte la matriz en una sola lista concatenando sus fila
    
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
    
    in : lista
    
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
    
    in : Dos matrices (sus elementos entre 0 y 15)
    
    out: Unión de las dos matrices , siendo cada elemento la union de los 4 bits de la primera mas los 4 bits de la segunda
    
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


# ==================================================================================
# SECCIÓN 2. FASE 1: CONFUSIÓN
# ==================================================================================
  
def separa2(matriz:list)->list:
     """
     in: Dada una matriz de bin MxN
         
     out: Devolverá la matriz Mx2N resultante de separar cada numero (8 bits) por la mitad

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
    >>> junta2([[0, 1, 7, 11], [2, 13, 112, 48], [2, 2, 8, 11]])
        [[1, 123], [45, 1840], [34, 139]]
         
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
#iniciales con el receptor, con x0,y0,z0 pertenecientes a (0,1)

# El parámtero u : 0 < u < 3.999

def x_y_z(matriz:list)->list:
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
    
   # x0,y0,z0 pertenecientes a (0,1)
   #AQUI METEMOS UNA MATRIZ YA DE LA FORMA Mx2N
    x0=0.36
    y0=0.25
    z0=0.78
    
    u= 1.500000001   # 0<u<3.999
    
    k1= 35.5    #|k1|> 33.5
    k2= 38.2     #|k2|> 37.5
    k3= 36.1    #|k3|> 35.7
    
   # La clave sera : (x0,y0,z0,u,k1,k2,k3)
    #creamos los xn,yn,zn
    x=[x0]
    y=[y0]
    z=[z0]
    m=len(matriz)
    n=len(matriz[0])
    #creamos el mapa caotico
    #para garantizar caos mejor podemos hacer mas iteraciones y quedarnos con las ultimas
    #ej si tenemos M=100x100, la sep=100x200 por tanto
    #n=20000 , podemos hacer 21000 y eliminar los 1000 primeros
    #Asi podemos evitar que se rastreen las semillas originales
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
      
      # si hacemos range(m*2*n + 100) x=x[101:]
      #y=y[101:]
      #z=z[101:]
      x_hat=[]
      y_hat=[]
      z_hat=[]
      
      #en la de imagenes multiplicaba solo z por 2, aqui todas *2 mas ya que
      #la imagen encriptada ocupa el doble que la original
      for k in range(m*n):
         x_hat.append(int((x[k]*10**13)%m))
         y_hat.append(int((y[k]*10**13)%n))
      for k in range(m*n*2):
         z_hat.append(int((z[k]*10**13)%2))
         #de longitud Mx4N
        
      return x_hat,y_hat,z_hat  

def permutacion(matriz:list,x_hat,y_hat)->list:
    """
    in: Dada una matriz de bin Mx2N
        
    out: Devolverá la matriz Mx2N resultante de intercambiar de posición sus celdas
    
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

    
# -------------------------------------------------------
# FASE 2 : DIFUSIÓN
# -------------------------------------------------------

#La tabla correspondiente a la tabla1 
tabla=[[1,0]]*4+[[0,1]]*2+[[1,0]]*2+[[0,1]]*4+[[1,0]]*4+[[0,1]]*6+[[1,0]]*2+[[0,1]]*2+[[1,0]]*2+[[0,1]]*4

def bitsAltos(matriz:list)->list:
    """
    
    in: Dada una matriz 
    
    out: Devuelve la matriz formada por los bits altos
    
    Se llama así ya que en nuestro algoritmo se aplica a una matriz Mx2N donde cada columna son los bits
        altos - bajos alternamente. Al quedarnos solo con los pares nos quedamos con los bits Altos
   
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
    
    in: Dada una matriz en forma de lista Mx2N
    
    out: Devuelve la matriz formada por las columnas impares con cada bit en una col Mx4N
    
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
    
     
"""
def tabla1(matriz:list,tiempo:int,Sini:list):
    
    
    in: matriz, tiempo t y un estado inicial Sini con las mismas dimensiones que la matriz
        Ambas matrices de enteros 
    
    out: Estado St+1, St resultados tras aplicar t veces la tabla 1 con las reglas locales de nuestro 
        Autómata Celular Reversible
    
    Example:
    ----------
    >>> tabla1([[2,14],[3,6]],5,[[4,5],[1,8]])
        ([[5, 14], [3, 14]], [[2, 8], [5, 12]])
    
    
    #la sini sera z_grro
    S=[Sini,matriz]
    m=len(matriz)
    n=len(matriz[0])
    masc1=0b1000
    masc2=0b0100
    masc3=0b0010
    masc4=0b0001
    mascaras=[masc1,masc2,masc3,masc4]
    for t in range(1,tiempo):
        St_nueva=[]
        for i in range(m):
            fila_nueva=[]
            for j in range(n):
                St=S[t]
                St_vieja=S[t-1]
                elem=0b0
                for k in range(4):
                    if k==0:
                        iz=St[i][(j-1)%n] & mascaras[(3-k)]
                        dcha=St[i][j] &mascaras[k+1]
                    if k==3:
                        dcha=St[i][(j+1)%n] & mascaras[3-k]
                        iz=St[i][j] & mascaras[k-1]
                    
                    else:
                        iz=St[i][(j-1)%n] & mascaras[k-1]
                        dcha=St[i][j] &mascaras[k+1]
                    arriba=St[(i-1)%m][j] & mascaras[k]
                    centro=St[i][j] & mascaras[k]
                    abajo=St[(i+1)%m][j] & mascaras[k]
                    
                    valores=[iz,arriba,centro,abajo,dcha]
                    binario=""
                    for v in valores:
                        if v>0:
                            binario+="1"
                        else:
                            binario+="0"
                    
                    #pasamos el num a binario para acceder a su valor en la tabla
                    pos=int(binario,2) #pasamos a int
                
    #Como la tabla 1 guarda segun la combinación de un posible valor segun Sij^(t-1) valga 0 o 1
                    ind=0
                    if St_vieja[i][j] & mascaras[k] ==0:
                        ind=0
                    else:
                        ind=1
                    dato_nuevo=tabla[pos][ind]
                    elem=elem | (dato_nuevo<<(3-k))
                        
                fila_nueva.append(elem)
            St_nueva.append(fila_nueva)
        S.append(St_nueva)
    #Para poder descifrar después vamos a guardar ambos
    return S[-1],S[-2]


"""

def tabla1(matriz:list,tiempo:int,Sini:list):
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
                
    #Como la tabla 1 guarda segun la combinación de un posible valor segun Sij^(t-1) valga 0 o 1
                ind=St_vieja[i][j]
                fila_nueva.append(tabla[pos][ind])
            St_nueva.append(fila_nueva)
        S.append(St_nueva)
    #Para poder descifrar después vamos a guardar ambos
    return S[-1],S[-2]

def union4BitsAltos(matriz:list)->list:
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
    
            

def opFinal(matriz:list,z:list,Cini:int)->list:
    """
    in: matriz de int, z lista de m*n, Cini entero dado
   
    out: una matriz m*n 
    
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


# -------------------------------------------------------
# RESULTADO
# -------------------------------------------------------


def Fase1y2_2(img:str):
    """
    in: Dada una imagen, pasado su nombre en str
        
    out: Devolverá la matriz después de la fase 1 de confusión y la 2 de difusión
    
    """
    # FASE 1 
    imagen=img=Image.open(img).convert("L")
    #añadimos el convert("L") para que sea en escala de grises
    matriz = np.array(imagen)
    
    

    
    m2=separa2(matriz) # da la matriz Mx2N
    
    #calculamos los parametros gorro
    #en la F1 usaremos x e y y en la F2 el z
    x,y,z=x_y_z(m2)
    x_hat,y_hat,z_hat=f_hats(x,y,z,len(m2),len(m2[0]))
    
    m_permutada=permutacion(m2,x_hat,y_hat)
    
    m_juntada=junta2(m_permutada)
    #FASE 2
    #vamos a separar la matriz permutada en los bits altos y los bajos
    mAltos=bitsAltos(m_juntada) 
    mBajos=bitsBajos(m_juntada)
    
    mAltos_sep=separaBits(mAltos)
    mBajos_sep=separaBits(mBajos)
    #sus elems son str
    
    # Para obtener el S-1 convertiremos z_hat en matriz
    m_nuevo=len(mAltos)
    n_nuevo=len(mAltos[0])
    S_menos1=Desaplana4(z_hat,m_nuevo,n_nuevo)
    S_menos1_sep=separaBits(S_menos1)
    #Los elementos de S_menos1 son ints
    
    
    Saltos,Saltos2=tabla1(mAltos_sep,6,S_menos1_sep)
    Sbajos,Sbajos2=tabla1(mBajos_sep,6,S_menos1_sep)
    
    Saltos_uni=union4BitsAltos(Saltos)
    Saltos2_uni=union4BitsAltos(Saltos2)
    
    Sbajos_uni=union4BitsBajos(Sbajos)
    Sbajos2_uni=union4BitsBajos(Sbajos2)
    
    #Los elementos de S son ints 
    
    #Ahora unimos los bits altos,siendo el valor de St claculado y los bajos
    #para ello tenemos que volver a agrupar cada 4 bits en una sola celda 
    unidos=unionBits(Saltos_uni,Sbajos_uni)
    unidos2=unionBits(Saltos2_uni,Sbajos2_uni)
    
    #queremos que en lugar de en cada celda un unico bit, tengamos los 8
    #hemos recuperado las dimensiones originales de la matriz
    
    # Hay que añadir una operación extra por si la informacion se encontrarara en los bits inferiores
    #usaremos Cini=168
    Cini=168
    C=opFinal(unidos,z,Cini)
    
    
    C2=opFinal(unidos2,z,Cini)

    Cf=C+C2
    
    mfinal=np.array(Cf).astype(np.uint8)
    img_final=Image.fromarray(mfinal)
    return img_final
                
                
# ==================================================================================
# SECCIÓN 3. DESENCRIPTACIÓN DE IMÁGENES
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
        La inversa de antes : ESTA DEVUELVE STR
        
    in: matriz, tiempo t y un estado final Sf con las mismas dimensiones que la matriz
        Ambas matrices de enteros 0 o 1
    
    out: Estado St+1, St resultados tras aplicar t veces la tabla 1 con las reglas locales de nuestro 
        Autómata Celular Reversible
    
    Example:
    ----------
    >>>tabla1([[1, 0, 1, 1, 1, 0, 1, 1], [1, 0, 0, 1, 1, 0, 1, 0]],5 ,[[1, 1, 1, 0, 1, 1, 1, 0], [1, 0, 0, 1, 0, 1, 0, 0]])
        ([['1', '0', '1', '0', '1', '1', '0', '0'],
          ['0', '0', '1', '1', '0', '1', '0', '1']],
         [['1', '1', '0', '0', '1', '0', '1', '0'],
          ['0', '1', '0', '1', '0', '0', '1', '1']])
    
    """
    #la sf sera los bits bajos
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

"""
def tabla1_inv(matriz:list,tiempo:int,Sf:list):
    
        
        
    in: matriz, tiempo t y un estado final Sf con las mismas dimensiones que la matriz
        Ambas matrices de enteros 
    
    out: Estado St+1, St resultados tras aplicar t veces la tabla 1 con las reglas locales de nuestro 
        Autómata Celular Reversible
    
    Example:
    ----------
    >>>tabla1([[1, 0, 1, 1, 1, 0, 1, 1], [1, 0, 0, 1, 1, 0, 1, 0]],5 ,[[1, 1, 1, 0, 1, 1, 1, 0], [1, 0, 0, 1, 0, 1, 0, 0]])
        ([['1', '0', '1', '0', '1', '1', '0', '0'],
          ['0', '0', '1', '1', '0', '1', '0', '1']],
         [['1', '1', '0', '0', '1', '0', '1', '0'],
          ['0', '1', '0', '1', '0', '0', '1', '1']])
    
    #la sf sera los bits bajos
    m=len(matriz)
    n=len(matriz[0])
    S=[matriz,Sf]
    masc1=0b1000
    masc2=0b0100
    masc3=0b0010
    masc4=0b0001
    mascaras=[masc1,masc2,masc3,masc4]
    for t in range(1,tiempo):
        St_nueva=[]
        for i in range(m):
            fila_nueva=[]
            for j in range(n):
                St_fut=S[t-1]
                St_pre=S[t]
                elem=0b0
                for k in range(4):
                    if k==0:
                        iz=St_pre[i][(j-1)%n] & mascaras[k]
                        dcha=St_pre[i][(j)%n] & mascaras[k]
                    if k==3:
                        dcha=St_pre[i][(j+1)%n] & mascaras[k]
                        iz=St_pre[i][(j)%n] & mascaras[k]
                    
                    
                    arriba=St_pre[(i-1)%m][j] & mascaras[k]
                    centro=St_pre[i][j] & mascaras[k]
                    abajo=St_pre[(i+1)%m][j] & mascaras[k]
                    
                    valores=[iz,arriba,centro,abajo,dcha]
                    binario=""
                    for v in valores:
                        if v>0:
                            binario+="1"
                        else:
                            binario+="0"
                    
                    #pasamos el num a binario para acceder a su valor en la tabla
                    pos=int(binario,2) #pasamos a int
                
    
                    ind=0
                    if (St_fut[i][j] & mascaras[k] ==0)  and tabla[pos][0]==0:
                        ind=0
                    else:
                        ind=1
                    if ind>0: 
                        elem =  elem | (0b1<<(3-k))
                    else:
                        elem =  elem | (0b0<<(3-k))
                fila_nueva.append(elem)
            St_nueva.append(fila_nueva)
        S.append(St_nueva)
    return S[-2],S[-1]

"""

def permutacion_inv(matriz:list,x_hat,y_hat)->list:
    """
        La permutacion inversa (ceo que esta funcion no hace falta pues la propia permutación es su propia inversa)
    in: Dada una matriz de bin Mx2N
        
    out: Devolverá la matriz Mx2N resultante de intercambiar de posicion sus celdas

    Example:
    ----------
    >> permutacion_inv([['1100', '1010'], ['0101', '0011']],[1,1,0,0],[1,0,0,1])
        [['1010', '1100'], ['0011', '0101']]
   
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
    nueva=[]
    for i in range(len(matriz)):
        fila=[]
        for j in range(len(matriz[0])):
            fila.append(matriz[i][j])
        nueva.append(fila)
    return nueva

def desEncripta_img(img:str):
    """
    in : nombre de la matriz en str
    
    out : devuelve la imagen desencriptada
    
    """
    #Proceso inverso
    imagen=img=Image.open(img).convert("L")
    #añadimos el convert("L") para que sea en escala de grises
    matriz = np.array(imagen)
    
    matriz2=copia_matriz(matriz) # no del tipo img
    
    m=len(matriz2)
    
    mini=matriz2[:m//2][:]
    mini2=matriz2[m//2:][:]
    #mini1==C y mini2==C2 de antes
    
    m2=separa2(mini)
    
    x,y,z=x_y_z(m2)
    x_hat,y_hat,z_hat=f_hats(x,y,z,len(m2),len(m2[0]))
    
    
    
    P1=opFinal_inv(mini,z,168)
    P2=opFinal_inv(mini2,z,168)
    
    #P=unidos de antes
    
    #P_sep=separa2(P1)
    #P_sep2=separa2(P2)
    
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
    
    
    S0alt,z2=tabla1_inv(mAltos_sep,6,mAltos_sep2) 
    S0baj,z22=tabla1_inv(mBajos_sep,6,mBajos_sep2)
    
    S0alt_uni=union4BitsAltos(S0alt)
    S0baj_uni=union4BitsBajos(S0baj)
    
    unidos=unionBits(S0alt_uni,S0baj_uni)
    # igual que la m_juntada
   
    unidos2=separa2(unidos)

    
    mp=permutacion_inv(unidos2,x_hat,y_hat)  
    
    #ahora hay que juntar
    mpJuntas=junta2(mp)
    
    mfinal=np.array(mpJuntas).astype(np.uint8)
    img_final=Image.fromarray(mfinal)
    return img_final