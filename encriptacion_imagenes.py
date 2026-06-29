# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 21:18:31 2026

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

t=6

Cini=168

# Estos parámetros se han elegido así para coincidir con el artículo seguido

# -------------------------------------------------------
#  TABLA NECESARIA PARA FASE 2
# -------------------------------------------------------

# La tabla correspondiente a la tabla1 
tabla=[[1,0]]*4+[[0,1]]*2+[[1,0]]*2+[[0,1]]*4+[[1,0]]*4+[[0,1]]*6+[[1,0]]*2+[[0,1]]*2+[[1,0]]*2+[[0,1]]*4


# ==================================================================================
# SECCIÓN 1. OPERACIONES AUXILIARES CON MATRICES
# ==================================================================================


def desaplana4(lista:np.ndarray,m:int,n:int)->np.ndarray:
    """
    
    in : Lista de 0 y 1 con longitud un múltiplo de 4 ,m y n ints
    
    out: Matriz de mxn donde cada elemento es el entero asociado a cada pack de 4 bits
    
    
    Example:
    ----------
    >>> desaplana4(np.array([0,1,1,0,1,0,1,1,1,0,1,0,0,0,1,1]),2,2) 
        array([[ 6, 11], [10,  3]], dtype=int32)
    """
    elems3=lista[0::4]<<3
    elems2=lista[1::4]<<2
    elems1=lista[2::4]<<1
    elems0=lista[3::4]
    result=elems3 | elems2 | elems1 | elems0
    return result.reshape(m,n)


def unionBits(altos:np.ndarray,bajos:np.ndarray)->np.ndarray:
    """
    
    in : Dos matrices con la misma dimensión
    
    out: Unión de las dos matrices , siendo cada elemento la union de los 4 bits de la primera
        como superiores más los 4 bits de la segunda como inferiores
    
    Example: 
    ----------
    >>> unionBits(np.array([[16, 32, 128], [48, 0, 208]]),np.array([[13, 10, 2], [2, 2, 12]]))
        array([[ 29,  42, 130], [ 50,   2, 220]])
    """
    altos=np.where(altos<=15, altos<<4, altos)
    bajos=np.where(bajos>15 , bajos>>4, bajos)

    return altos|bajos

def union4BitsAltos(matriz:np.ndarray)->np.ndarray:
    """
    
    in : Matriz Mx4N con elementos int 0 o 1 
    
    out : Matriz MxN resultante de agrupar cada 4 bits tomándolos como los 4 bits altos
    
    Example:
    ----------
    >>> union4BitsAltos(np.array([[0,1,1,0,1,0,1,1],[1,0,1,0,0,0,1,1]])) 
        array([[ 96, 176], [160,  48]], dtype=int32)

    """
   
    elems3=matriz[:,0::4]<<3
    elems2=matriz[:,1::4]<<2
    elems1=matriz[:,2::4]<<1
    elems0=matriz[:,3::4]
    nueva_matriz=elems3 | elems2 | elems1 | elems0
    return nueva_matriz<<4

def union4BitsBajos(matriz:np.ndarray)->np.ndarray:
    """
    
    in : Matriz Mx4N con elementos int 0 o 1 
    
    out : Matriz MxN resultante de agrupar cada 4 bits tomándolos como los 4 bits bajos
    
    Example:
    ----------
    >>> union4BitsBajos(np.array([[0,1,1,0,1,0,1,1],[1,0,1,0,0,0,1,1]]))
        array([[ 6, 11], [10,  3]], dtype=int32)

    """
    elems3=matriz[:,0::4]<<3
    elems2=matriz[:,1::4]<<2
    elems1=matriz[:,2::4]<<1
    elems0=matriz[:,3::4]
    nueva_matriz=elems3 | elems2 | elems1 | elems0
    return nueva_matriz


def bitsAltos(matriz:np.ndarray)->np.ndarray:
    """
    
    in: Matriz 
    
    out: Matriz formada por los bits altos
    
   
    Example
    --------
    >>> bitsAltos(np.array([[29,42,130],[50,2,220]]))
        array([[ 16,  32, 128], [ 48,   0, 208]], dtype=int32)
   
    """
    mascaraAltos=0b11110000
    matrizAlta=mascaraAltos & matriz
    
    return matrizAlta




def bitsBajos(matriz:np.ndarray)->np.ndarray:
    """
    
    in: Matriz 
    
    out: Matriz formada por los bits bajos
    
    Example
    --------
    >>>bitsBajos(np.array([[29,42,130],[50,2,220]]))
        array([[13, 10,  2], [ 2,  2, 12]], dtype=int32)
   
    """
    mascaraBajos=0b00001111
    matrizBaja= mascaraBajos & matriz
    return matrizBaja


def separaBits(matriz:np.ndarray)->np.ndarray:
    """
    
    in  : Matriz MxN donde los elementos solo tienen la parte alta o baja de sus bits
    
    out : Matriz Mx4N con cada bit separado (0 ó 1)
        
    Example:
    ---------
    >>> separaBits(np.array([[13, 10, 2], [2, 2, 12]]))
        array([[1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0], [0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0]])
    
    """
    m,n=matriz.shape
    nueva_matriz=matriz.copy()
    
    # Si el elmento es mayor de 15 desplazamos
    nueva_matriz=np.where(nueva_matriz>15,nueva_matriz>>4,nueva_matriz)
    
    bit3 = (nueva_matriz & 0b1000) >>3  # Los valores del bit 4 de cada elemento
    bit2 = (nueva_matriz & 0b0100) >> 2
    bit1 = (nueva_matriz & 0b0010) >> 1
    bit0 = (nueva_matriz & 0b0001) 
    
    result=np.zeros((m,4*n),dtype=int)
    result[:,0::4]=bit3
    result[:,1::4]=bit2
    result[:,2::4]=bit1
    result[:,3::4]=bit0
    
    
    return result
    

# ==================================================================================
# SECCIÓN 2. FASE 1: CONFUSIÓN
# ==================================================================================
  
def separa2(matriz:np.ndarray)->np.ndarray:
     """
     in: Matriz de bin MxN
         
     out: Matriz Mx2N resultante de separar cada número (8 bits) por la mitad
          cada mitad estará en una columna distinta

     Example
     ------
     >>> separa2(np.array([[139,23,12],[43,159,138]]))
         array([[128,  11,  16,   7,   0,  12],  [ 32,  11, 144,  15, 128,  10]])
     """
     m,n=matriz.shape
     mascaraAltos=0b11110000
     mascaraBajos=0b00001111
     
     altos= matriz & mascaraAltos
     bajos=matriz & mascaraBajos
     
     nueva_matriz=np.zeros((m,2*n),dtype=int)
     nueva_matriz[:,0::2] = altos
     nueva_matriz[:,1::2]=bajos
     return nueva_matriz
 
 
def junta2(matriz:np.ndarray)->np.ndarray:
    """
    
    in: Matriz Mx2N
    
    out : Matriz MxN donde se han unido cada par de elementos
    
    Example:
    ----------
    >>> junta2([[128, 11, 16, 7, 0, 12], [32, 11, 144, 15, 128, 10]])
        [[139, 23, 12], [43, 159, 138]]
         
    """
    m,n=matriz.shape
    nueva_matriz=np.zeros((m,n//2),dtype=int)
    elem1 = matriz[:, 0::2]
    elem2 = matriz[:, 1::2]
    
    # Aseguramos que los de elem1 sean bits altos (>15) y los de elem2 <=15
    elem1 = np.where(elem1 <= 15, elem1 << 4, elem1)

    elem2 = np.where(elem2 > 15, elem2 >> 4, elem2)
    
    nueva_matriz[:, :] = elem1 | elem2

    return nueva_matriz
 
# Para este paso es necesario haber pactado los valores
# iniciales con el receptor, x0,y0,z0,u,k1,k2 y k3

def x_y_z(matriz:np.ndarray,x0:float,y0:float,z0:float,u:float,k1:float,k2:float,k3:float)->tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    in: Matriz 
        
    out: Valores x, y, z asociados al mapa caótico
    
    Example:
    ----------
    >>> x_y_z(np.array([[29,31], [201, 5]]),x0,y0,z0,u,k1,k2,k3)

        (array([0.3       , 0.95511034, 0.45895285, 0.96547472, 0.72625317,
                0.3828777 , 0.563686  , 0.71908364]),
         array([0.04059633, 0.55725113, 0.03532237, 0.51452091, 0.99291588,
                0.68697043, 0.1136488 , 0.56388592]),
         array([0.44188213, 0.12691415, 0.94781041, 0.7803214 , 0.90912454,
                0.9886267 , 0.07859908, 0.40286414]))

    """
    
   # La clave sera : (x0,y0,z0,u,k1,k2,k3)
    #creamos los xn,yn,zn
 
    m,n=matriz.shape
    x=np.zeros(m*n*2+1,dtype=float)
    y=np.zeros(m*n*2+1,dtype=float)
    z=np.zeros(m*n*2+1,dtype=float)
    x[0],y[0],z[0]=x0,y0,z0
   
    
    xl,yl,zl=x0,y0,z0
    #creamos el mapa caotico
    for l in range(m*n*2): 
        # guardamos las variables para evitar tener que acceder a la matriz
        xl_sig=(u*k1*yl*(1-xl)+zl)%1
        yl_sig=(u*k2*yl+zl*1/(1+xl_sig**2))% 1
        zl_sig=(u*(xl_sig+yl_sig + k3)*sin(zl))%1
        
        x[l+1],y[l+1],z[l+1]=xl_sig,yl_sig,zl_sig
        
        xl,yl,zl=xl_sig,yl_sig,zl_sig
    #vamos desde el uno para no usar los valores x0,y0,z0
    return x[1:],y[1:],z[1:]



def f_hats(x:np.ndarray,y:np.ndarray,z:np.ndarray,m:int,n:int)->tuple[np.ndarray, np.ndarray, np.ndarray]:
      """
      in: Dados x,y,z y las dimensiones m,n 
          
      out: x_gorro,y_gorro y z_gorro discretizando las secuencias del mapa caótico

      Example:
      ----------
      >>> f_hats(x,y,z,2,2) (siendo los x,y,z del resultado anterior)
          (array([0, 1, 1, 1]), array([0, 1, 1, 1]), array([0, 1, 1, 1, 0, 1, 0, 0]))
      """
      x_hat=np.zeros(m*n,dtype=int)
      y_hat=np.zeros(m*n,dtype=int)
      z_hat=np.zeros(m*n*2,dtype=int)
      
      x_hat[:]=(x[:m*n]*10**13)%m
      y_hat[:]=(y[:m*n]*10**13)%n
       # z_hat tiene mayor longitud ya que después se necesitará 
      z_hat[:]=(z[:m*n*2]*10**13)%2
        
      return x_hat,y_hat,z_hat  




def permutacion(matriz:np.ndarray,x_hat,y_hat)->np.ndarray:
    """
    in: Matriz
        
    out: Matriz resultante de intercambiar de posición sus celdas
         intercambiando la pos i,j por la x_hat_i,y_hat_j de la matriz
    
    Example:
    ----------
    >>> permutacion(np.array([[4,7,2],[2,6,8]]),np.array([0,1,1,0,0,1]),np.array([2,1,0,2,2,1]))
        array([[2, 6, 7], [2, 8, 4]])
   

    """
    
    m,n=matriz.shape
    resultado=matriz.copy()
    ind_caos=0
    for i in range(m):
          for j in range(n):
              nueva_i=x_hat[ind_caos]
              nueva_j=y_hat[ind_caos]
              resultado[i,j],resultado[nueva_i,nueva_j]=resultado[nueva_i,nueva_j],resultado[i,j]
          
              ind_caos+=1
      
    return resultado


    
# ==================================================================================
# SECCIÓN 3. FASE 2: DIFUSIÓN
# ==================================================================================


def tabla1(matriz:np.ndarray,tiempo:int,Sini:np.ndarray)->tuple[np.ndarray, np.ndarray]:
    """
    in: Matriz, tiempo t y un estado inicial Sini con las mismas dimensiones que la matriz
        Ambas matrices de 0 o 1 
    
    out: Estados St+1 y St tras aplicar t veces la tabla 1 con las reglas locales de nuestro 
        Autómata Celular Reversible
    
    Example:
    ----------
    >>> tabla1(np.array([[0, 0, 1, 0, 1, 1, 1, 0], [0, 0, 1, 1, 0, 1, 1, 0]]) , 6 , np.array([[0, 1, 0, 0, 0, 1, 0, 1], [0, 0, 0, 1, 1, 0, 0, 0]]))
        (array([[0, 0, 1, 0, 0, 1, 1, 0], [1, 0, 1, 1, 1, 0, 0, 0]]),
         array([[0, 1, 0, 1, 0, 0, 1, 0], [0, 0, 1, 1, 0, 1, 0, 1]]))
    """
    m,n=matriz.shape
    S=[Sini,matriz]

    St=matriz
    St_vieja=Sini
    
    for t in range(1,tiempo):
        St_nueva=np.zeros((m,n),dtype=int)
        for i in range(m):
            for j in range(n):
                St=S[t]
                St_vieja=S[t-1]
                iz=St[i,(j-1)%n]
                arriba=St[(i-1)%m,j]
                centro=St[i,j]
                abajo=St[(i+1)%m,j]
                dcha=St[i,(j+1)%n]
                
                pos=(iz << 4) | (arriba << 3) | (centro << 2) | (abajo << 1) | dcha
                
                ind = St_vieja[i,j]
                St_nueva[i,j]=tabla[pos][ind]
        St=St_nueva
        
        S.append(St_nueva)
        
    # Para poder descifrar después vamos a guardar ambos
    return S[-1],S[-2]
            


def opFinal(matriz:np.ndarray,z:np.ndarray,Cini:int)->np.ndarray:
    """
    in: Matriz de int mxn, z lista de longitud m*n, Cini entero dado
   
    out: Matriz mxn resultante de aplicar una fase de difusión final en
         cascada para garantizar la encriptación de los 4 bits bajos
    
    Example:
    -----------
    z=np.array([0.44188213370884455, 0.1269141527519082, 0.9478104122549009, 0.7803213978473096,0.9091245400766681,
      0.9886267010853445, 0.07859908416606487, 0.4028641393942234, 0.04441778045339362])
    
    >>> opFinal(np.array([[28,140,88],[3,126,39]]),z,168)
        array([[180, 231,  10],[ 96, 160, 162]])
    
    """
    m,n=matriz.shape
    matriz1D=matriz.flatten()
    C=np.zeros(n*m+1,dtype=int)
    C[0]=Cini
    for i in range(n*m):
        # Usamos C[i] para usar el ultimo elem añadido
        nuevoC=C[i] ^ matriz1D[i] ^ int(z[i]*(10**13))%256
        C[i+1]=nuevoC
        #C tiene m*n+1, descartamos el Cini
    
    return C[1:].reshape(m,n)


# ==================================================================================
# SECCIÓN 4. FUNCIÓN FINAL DEL ALGORITMO DE ENCRIPTACIÓN DE IMÁGENES
# ==================================================================================


def encripta_img(img:str,x0:int,y0:int,z0:int,u:int,k1:int,k2:int,k3:int,tiempo:int,Cini:int):
    """
    in: Imagen pasado su nombre en str y los valores de la clave
        
    out: Matriz después de la fase 1 de confusión y la 2 de difusión
    
    Example:
    ---------
    >>> Encripta_img("p1.png",x0,y0,z0,u,k1,k2,k3,6)
    
    """
    # FASE 1 
    imagen=img=Image.open(img).convert("L")
    # Añadimos el convert("L") para que sea en escala de grises
    matriz = np.array(imagen)
    
    
    m2=separa2(matriz) # Da la matriz Mx2N
    
    # Calculamos los parametros y sus parametros gorro correspondientes
    # En la Fase 1 usaremos x e y , en la Fase 2 el z
    x,y,z=x_y_z(m2,x0,y0,z0,u,k1,k2,k3)
    x_hat,y_hat,z_hat=f_hats(x,y,z,len(m2),len(m2[0]))
    
    m_permutada=permutacion(m2,x_hat,y_hat)
    
    m_juntada=junta2(m_permutada)
    
    
    # FASE 2
    # Vamos a separar la matriz permutada en los bits altos y los bajos
    mAltos=bitsAltos(m_juntada) 
    mBajos=bitsBajos(m_juntada)
    
    # Separamos en cada bit para poder aplicar la tabla 1
    mAltos_sep=separaBits(mAltos) 
    mBajos_sep=separaBits(mBajos)
    # Sus elementos son 0 o 1
    
    # Para obtener el S-1 convertiremos z_hat en matriz
    m_nuevo,n_nuevo=mAltos.shape
    S_menos1=desaplana4(z_hat,m_nuevo,n_nuevo)
    S_menos1_sep=separaBits(S_menos1)
    # Los elementos de S_menos1 son 0 o 1
    
    
    # Guardamos los dos ultimos estados para poder desencriptar bien y no perder información 
    Saltos,Saltos2=tabla1(mAltos_sep,tiempo,S_menos1_sep)
    Sbajos,Sbajos2=tabla1(mBajos_sep,tiempo,S_menos1_sep)
    
    Saltos_uni=union4BitsAltos(Saltos)
    Saltos2_uni=union4BitsAltos(Saltos2)
    
    Sbajos_uni=union4BitsBajos(Sbajos)
    Sbajos2_uni=union4BitsBajos(Sbajos2)
    # Ahora las 4 matrices unidas son de enteros, agrupando cada 4 bits , no solo de 0 y 1
    

    unidos=unionBits(Saltos_uni,Sbajos_uni)
    unidos2=unionBits(Saltos2_uni,Sbajos2_uni)
    # Para poder desencriptar al completo después, devolveremos una matriz con el doble de filas 
    # que la original, para poder revertir las operaciones y tener la información suficiente
    
    # Hay que añadir una operación extra por si la información se encontrarara en los bits inferiores
    
    C=opFinal(unidos,z,Cini)
    
    
    C2=opFinal(unidos2,z,Cini)

    Cf = np.vstack((C, C2)) # Una encima de la otra
    
    mfinal=np.array(Cf).astype(np.uint8)
    img_final=Image.fromarray(mfinal)
    return img_final
                
                
# ==================================================================================
# SECCIÓN 5. DESENCRIPTACIÓN DE IMÁGENES
# ==================================================================================
 
      
def opFinal_inv(matriz:np.ndarray, z:np.ndarray, Cini:int)->np.ndarray:
    """
        La inversa de OpFinal anterior
    
    in: Matriz int, z lista de m*n, Cini entero dado
   
    out: Matriz m*n 
    
    Example:
    -----------
    z=np.array([0.44188213370884455, 0.1269141527519082, 0.9478104122549009, 0.7803213978473096,0.9091245400766681,
                0.9886267010853445, 0.07859908416606487, 0.4028641393942234, 0.04441778045339362])
    
    >>> opFinal_inv(np.array([[180, 231, 10],[96, 160, 162]]), z , 168)
        array([[28, 140, 88], [3, 126, 39]])
    
    """
    m,n=matriz.shape
    matriz1D=matriz.flatten()
    C=np.concatenate((np.array([Cini]),matriz1D))
    P=np.zeros(n*m,dtype=int)
    for i in range(n*m):
        nuevop=C[i] ^ C[i+1] ^ int(z[i]*(10**13))%256
        P[i]=nuevop
    
    return P.reshape(m,n)


def tabla1_inv(matriz:np.ndarray,tiempo:int,Sf:np.ndarray)->np.ndarray:
    """
        La inversa de tabla1
        
    in: Matriz, tiempo t y un estado final Sf con las mismas dimensiones que la matriz
        Ambas matrices de enteros 0 o 1
    
    out: Estados St+1, St resultantes tras aplicar t veces la tabla 1 con las reglas locales de nuestro 
        Autómata Celular Reversible
    
    Example:
    ----------
    >>>tabla1_inv(np.array([[0, 0, 1, 0, 0, 1, 1, 0], [1, 0, 1, 1, 1, 0, 0, 0]]),6, np.array([[0, 1, 0, 1, 0, 0, 1, 0], [0, 0, 1, 1, 0, 1, 0, 1]])) 
        (array([[0, 1, 0, 1, 0, 0, 1, 0], [0, 0, 1, 1, 0, 1, 0, 1]]),
         array([[0, 0, 1, 0, 0, 1, 1, 0],[1, 0, 1, 1, 1, 0, 0, 0]]))
    
    """
    # Sf sera los bits bajos por como encriptamos
    m,n=matriz.shape
    S=[matriz,Sf]
    for t in range(1,tiempo):
        St_nueva=np.zeros((m,n),dtype=int)
        for i in range(m):
            for j in range(n):
                St_fut=S[t-1]
                St_pre=S[t]
                
                iz=St_pre[i,(j-1)%n]
                arriba=St_pre[(i-1)%m,j]
                centro=St_pre[i,j]
                abajo=St_pre[(i+1)%m,j]
                dcha=St_pre[i,(j+1)%n]
                
                pos=(iz << 4) | (arriba << 3) | (centro << 2) | (abajo << 1) | dcha
                
    
                ind=0
                if St_fut[i,j]==tabla[pos][0]:
                    ind=0
                elif St_fut[i,j]==tabla[pos][1]:
                    ind=1
                
                
                St_nueva[i,j]=ind
        S.append(St_nueva)
    return S[-2],S[-1]

  


def permutacion_inv(matriz:list,x_hat,y_hat)->list:
    """
        La permutacion inversa 
        
    in: Matriz
        
    out: Matriz resultante de intercambiar de posición sus celdas

    Example:
    ----------
    >>> permutacion_inv(np.array([[2, 6, 7],[2,8,4]]),np.array([0,1,1,0,0,1]),np.array([2,1,0,2,2,1]))
        array([[4, 7, 2], [2, 6, 8]])
   
    """
    
    m,n=matriz.shape
    resultado=matriz
    ind_caos=m*n-1
    for i in range(m-1,-1,-1):
        for j in range(n-1,-1,-1):
            nueva_i=x_hat[ind_caos]
            nueva_j=y_hat[ind_caos]
            resultado[i,j],resultado[nueva_i,nueva_j]=resultado[nueva_i,nueva_j],resultado[i,j]
            ind_caos-=1
    
    return matriz 



def desEncripta_img(img:str,x0:int,y0:int,z0:int,u:int,k1:int,k2:int,k3:int,tiempo:int,Cini:int):
    """
    in : Nombre de la matriz en str y los valores correctos de la clave
    
    out : Imagen desencriptada
    
    Example:
    ---------
    >>> desEncripta_img("p1_encriptada.png",x0,y0,z0,u,k1,k2,k3,6)
    """
    # Proceso inverso
    imagen=img=Image.open(img).convert("L")
    # Añadimos el convert("L") para que sea en escala de grises
    matriz = np.array(imagen)
    

    
    m,n=matriz.shape
    
    mini=matriz[:m//2,:]
    mini2=matriz[m//2:,:]
    # mini1==C y mini2==C2 de antes
    
    m2=separa2(mini)
    
    x,y,z=x_y_z(m2,x0,y0,z0,u,k1,k2,k3)
    x_hat,y_hat,z_hat=f_hats(x,y,z,len(m2),len(m2[0]))
    
    P1=opFinal_inv(mini,z,Cini)
    P2=opFinal_inv(mini2,z,Cini)
    
    
    mAltos=bitsAltos(P1) 
    mBajos=bitsBajos(P1) 
    
    # Los mBajos coinciden con los Sbajos_uni de antes
    # Los mAltos coinciden con los Saltos_uni
    
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
