# -*- coding: utf-8 -*-
"""
Created on Mon Dec  1 18:14:05 2025

TFG

@author: Irene
"""

 # cuidado con caracteres españoles y tildes y cosas q son dos bytes
# cifrar y descifrar a.encode() y a.decode()
# buscar diferencias en este caso o como siempre con clave privada 

import numpy as np
from PIL import Image
from math import sin 

# ==================================================================================
# SECCIÓN 1. ENCRIPTACIÓN DE MENSAJES
# ==================================================================================

def bin_8(n:int)->str:
    """
    in: n es un entero
        
    out: Devolverá el número pasado a binario con 8 digitos en forma de str

    Example
    ------
    >>> bin_8(97)
    '01100001'
    
    """
    result= ""
    while n!=0:
        resto=n%2
        n=n//2
        result+=str(resto)
    result=result[::-1]
    zeros=""
    m=len(result)
    while len(zeros)+m<8:
        zeros+= "0"
    result =zeros+ result
    return result


def bin_a_num(binario:str)->int:
    """
    in: n es un numero de 8 digitos en binario pasado como str
        
    out: Devolverá el entero asociado

    Example
    ------
    >>> bin_a_num('10110100')
        180
    
    """
    result=0
    n=len(binario)
    for i in range(n):
        if int(binario[i])==1:
            result+=2**(n-1-i)
    return result

def bin_a_str(n:str)->str: 
    """
    in: n es un numero de 8 digitos en binario pasado como str
        
    out: Devolverá el caracter asociado a ese numero entero según el código ASCII

    Example
    ------
    >>> bin_a_str('01100001')
    'a'
    
    """
    result=0
    for i in range(8):
        if n[-1]=="1":
           result+=2**i
        n=n[:-1]
   
    return chr(int(result))
       
    


def pal_a_bin(pal:str)->str: 
    """
    in: pal es una palabra en str
        
    out: Devolverá el número binario asociado a cada letra según el código ASCII 

    Example
    ------
    >>> pal_a_bin("HOLA")
    '01001000010011110100110001000001'
    
    """
    result=""
    for elem in pal:
        n=ord(elem)
        binario=bin_8(n)
        result+=binario
    return result


def suma_k(pal:str,k:str)->str:
    """
    in: pal y k son dos numeros binarios en string
        
    out: Devolverá la suma de ambos en binario y en string

    Example
    ------
    >>> suma_k('1001101','0011110')
    '1010011'
    
    """
    result=""
    for i in range(len(pal)):
        if pal[i]==k[i]:
            result+="0"
        else:
            result+="1"
                
    return result

def regla_30(it:int)->str:
    """
    in: it es un entero que indica el número de iteraciones que se repetirá el proceso 
        
    out: Devolverá un número binario en string resultante de aplicarle it veces el algoritmo

    Consideramos configuración circular, cuando estamos en los extremos se tiene que 
      el vecino izq del primer elemento es el último elemento y el vecino derecho del
      último es el primero
      
    Example
    ------
    >>>regla_30(20)
    '00000000000010001000100000001000100010000000100010001000000000000'
    
    """
    #configuración inicial
    r0=[0]*12+[1]+[0]*12
    r1=r0.copy()
    for j in range(it):
        m=len(r0)
        for i in range(m):
            if i==m-1: #si estamos en la ultima pos, consideramos su vecina dcha como la primera
                nueva_dcha=(r0[i-1]+r0[i]+r0[0])%2
            #cuando estamos en la primera, consideramos la vecina izq como el ultimo elemento 
            elif i==0:
                nueva_izda=r1[i]=(r0[-1]+r0[i]+r0[i+1]**2)%2
            else:
                r1[i]=(r0[i-1]+r0[i]+r0[i+1]**2)%2
        r1=[nueva_izda]+r1
        r1.append(nueva_dcha)
        r0=r1.copy()   
        #para que devuelva un str
        resultado=""
        for elem in r0:
            resultado+=str(elem)
            
    return resultado

def encripta(pal: str, it: int) -> str:
    """
    in: pal es un str , que será la palabra/frase que queramos encriptar
        it es un entero que será el número de iteraciones que usaremos.
        Tenemos que asegurarnos que el numero de it sea lo suficientemente grande 
        para cubrir la longitud de la palabra/ frase que queramos encriptar
        
    out: Devolverá la palabra encriptada en forma de str

    Example
    ------
    >>> encripta('adiós muy buenas',230)
    'anKss*Oõy buedCó'
    
    >>> encripta("Hola buenas, Soy María y me gustaría decirte un par de cosas, en Primer lugar soy ESPAÑOLA, no hay duda de eso",1000)
     'Hgdi j}mnas, [gq Eizía y em(g}{|aría lmkiz|m un piz(dm(kosas,(mf Xzamer l}oir({gy ESPIÙGLI$(no haq(luli(de esg'
   
    """
    k=regla_30(it)
    palbin=pal_a_bin(pal)
    m=len(palbin)
    k=k[:m]
    suma=suma_k(palbin,k)
    letras= m//8
    resultado=""
    for i in range(letras):
        ind_0=8*i
        ind_f=8*(i+1)
        pal_trad=suma[ind_0:ind_f]
        traduc=bin_a_str(str(pal_trad))
        resultado+=traduc
    return resultado

def desEncripta(pal:str,it:int)->str:
    """
    in: pal es un str , que será la palabra/frase que queramos desencriptar
        it es un entero que será el número de iteraciones que usaremos
        
    out: Devolverá la palabra desencriptada en forma de str

    Example
    ------
    >>> desEncripta('anKss*Oõy buedCó',230)
    'adiós muy buenas'
    
    >>> desEncripta('Hgdi j}mnas, [gq Eizía y em(g}{|aría lmkiz|m un piz(dm(kosas,(mf Xzamer l}oir({gy ESPIÙGLI$(no haq(luli(de esg',1000)
     'Hola buenas, Soy María y me gustaría decirte un par de cosas, en Primer lugar soy ESPAÑOLA, no hay duda de eso'
    """
    result=encripta(pal,it)
    return result




# ==================================================================================
# SECCIÓN 2. ENCRIPTACIÓN DE IMÁGENES
# ==================================================================================


# -------------------------------------------------------
# Operaciones auxiliares con matrices
# -------------------------------------------------------
  




def img_a_matrizBin(img:str)->list:
    """
    in: Dada una imagen, pasado su nombre en str
        
    out: Devolverá la matriz asociada con sus valores num bin en str

    Example
    ------
    >>> img_a_matrizBin("beach.png")
    [[  '00111000',
      '00110111',
      '00110110'
      ...
      '00110110',
      '00110101',
      '00111000']]
    """

 
    imagen=img=Image.open(img).convert("L")
    #añadimos el convert("L") para que sea en escala de grises
    matriz = np.array(imagen)
    nueva=[]
    for i in range(len(matriz)):
          fila=[]
          for j in range(len(matriz[0])):
              num=matriz[i][j]
              numBin=bin_8(num)
              fila.append(numBin)
          nueva.append(fila)
    return nueva


def imgBin_a_Int(matriz:list)->list:
    """
    
    in : Matriz con sus elementos un bin en str
    
    out: Matriz con sus elementos el int asociado
    
    Example
    --------
    >>> imgBin_a_Int([['00111000', '00110111', '00110110'], ['00110110', '00110101', '00111000']])
        [[56, 55, 54], [54, 53, 56]]
        
    """ 
    m=len(matriz)
    n=len(matriz[0])
    result=[]
    for i in range(m):
        fila=[]
        for j in range(n):
            fila.append(bin_a_num(matriz[i][j]))
        result.append(fila)
    return result


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
    ---------
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


def unionBits(altos:list,bajos:list)->list:
    """
    
    in : Dos matrices
    
    out: Unión de las dos matrices , siendo cada elemento la union de los 4 bits de la primera mas los 4 bits de la segunda
    
    Example: 
    ----------
    >>> unionBits([['0011', '1000'], ['0011', '1000']],[['0011', '0111'], ['0011', '0101']])
        [['00110011', '10000111'], ['00110011', '10000101']]
      
    """
    matriz=[]
    m=len(altos)
    n=len(altos[0])
    for i in range(m):
        fila=[]
        for j in range(n):
            fila.append(str(altos[i][j])+bajos[i][j])
        matriz.append(fila)
    return matriz

def une4(matriz:list)->list:
    """
    
    in: Dada una matriz Mx4N 
    
    out: Devuelve la matriz MxN
    
    Example:
    ----------
    >>> une4([['0', '0', '1', '1', '0', '1', '1', '1'],['0', '0', '1', '1', '0', '1', '0', '1']])
        [['0011', '0111'], ['0011', '0101']]

    """        
    m=len(matriz)
    n=len(matriz[0])
    result=[]
    for i in range(m):
        fila=[]
        for j in range(0,n,4):
            num=str(matriz[i][j])+str(matriz[i][j+1])+str(matriz[i][j+2])+str(matriz[i][j+3])
            fila.append(num)
        result.append(fila)
    return result
            



# -------------------------------------------------------
# FASE 2 : CONFUSIÓN
# -------------------------------------------------------
  
def separa2(matriz:list)->list:
     """
     in: Dada una matriz de bin MxN
         
     out: Devolverá la matriz Mx2N resultante de separar cada numero (8 bits) por la mitad

     Example
     ------
     >>> separa2(m=[['00111001','00111000',],['00110101','00111000']]) 
       [['0011', '1001', '0011', '1000'], ['0011', '0101', '0011', '1000']]
       
     """
     m=len(matriz)
     n=len(matriz[0])
     nueva_matriz=[]
     for i in range(m):
         nueva_fila=[]
         for j in range(n):
             elem=matriz[i][j]
             nueva_fila.append(elem[:4])
             nueva_fila.append(elem[4:])
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
    
    u= 1.5   # 0<u<3.999
    
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
    for l in range(m*n*2): #hacemos *4 porque en la z necesitamos mas elementos
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
      
     for k in range(m*n):
         x_hat.append(int((x[k]*10**13)%m))
         y_hat.append(int((y[k]*10**13)%(n)))
     for k in range(m*2*n):
         z_hat.append(int((z[k]*10**13)%2))
         #de longitud Mx4N
        
     return x_hat,y_hat,z_hat  

def permutacion(matriz:list,x_hat,y_hat)->list:
    """
    in: Dada una matriz de bin Mx2N
        
    out: Devolverá la matriz Mx2N resultante de intercambiar de posición sus celdas
    
    Example:
    ----------
    >>> permutacion([['1010', '1100'], ['0011', '0101']],[1,1,0,0],[1,0,0,1])
        [['1100', '1010'], ['0101', '0011']]
   
    """
    m=len(matriz)
    n=len(matriz[0])
    ind_caos=0
    for i in range(m):
        for j in range(n):
            nueva_i=x_hat[ind_caos]
            nueva_j=y_hat[ind_caos]
            elem_inicial=matriz[i][j]
            matriz[i][j]=matriz[nueva_i][nueva_j]
            matriz[nueva_i][nueva_j]=elem_inicial
            ind_caos+=1
    
    return matriz 

    
# -------------------------------------------------------
# FASE 2 : DIFUSIÓN
# -------------------------------------------------------

#La tabla correspondiente a la tabla1 
tabla=[[1,0]]*4+[[0,1]]*2+[[1,0]]*2+[[0,1]]*4+[[1,0]]*4+[[0,1]]*6+[[1,0]]*2+[[0,1]]*2+[[1,0]]*2+[[0,1]]*4

def bitsAltos(matriz:list)->list:
    """
    
    in: Dada una matriz en forma de lista 
    
    out: Devuelve la matriz formada por las columnas pares, separando cada elem en una columna 
    
    Se llama así ya que en nuestro algoritmo se aplica a una matriz Mx2N donde cada columna son los bits
        altos - bajos alternamente. Al quedarnos solo con los pares nos quedamos con los bits Altos
   
    Example
    --------
    >>> bitsAltos([['0011', '0110', '0011', '0111'], ['0011', '1000', '0011', '1000']])
        [['0', '0', '1', '1', '0', '0', '1', '1'], ['0', '0', '1', '1', '0', '0', '1', '1']]
   
    """
    matrizAlta=[]
    m=len(matriz)
    n=len(matriz[0])
    for i in range(m):
        fila=[]
        for j in range(0,n,2):
            fila+=matriz[i][j]
        matrizAlta.append(fila)
    return matrizAlta


def bitsBajos(matriz:list)->list:
    """
    
    in: Dada una matriz en forma de lista Mx2N
    
    out: Devuelve la matriz formada por las columnas impares con cada bit en una col Mx4N
    
    Example
    --------
    >>> bitsBajos([['0011', '0110', '0011', '0111'], ['0011', '1000', '0011', '1000']])
        [['0', '1', '1', '0', '0', '1', '1', '1'], ['1', '0', '0', '0', '1', '0', '0', '0']]
   
    """
    matrizBaja=[]
    m=len(matriz)
    n=len(matriz[0])
    for i in range(m):
        fila=[]
        for j in range(1,n,2):
            fila+=(matriz[i][j])
        matrizBaja.append(fila)
    return matrizBaja

        
def tabla1(matriz:list,tiempo:int,Sini:list):
    """
    
    in: matriz, tiempo t y un estado inicial Sini con las mismas dimensiones que la matriz
        Ambas matrices de enteros 0 o 1
    
    out: Estado St+1 tras aplicar t veces la tabla 1 con las reglas locales de nuestro 
        Autómata Celular Reversible
    
    Example:
    ----------
    >>>tabla1([[1,0,1,0, 1,1,0,0], [0,0,1,1, 0,1,0,1]],5,[[1,1,0,0, 1,0,1,0], [0,1,0,1, 0,0,1,1]])
        ([[1, 0, 1, 1, 1, 0, 1, 1], [1, 0, 0, 1, 1, 0, 1, 0]])
    
    """
    #la sini sera z_grro
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
                binario=str(iz)+str(arriba)+str(centro)+str(abajo)+str(dcha)
                #pasamos el num a binario para acceder a su valor en la tabla
                pos=bin_a_num(binario)
                
    #Como la tabla 1 guarda segun la combinacion un posible valor segun Sij^(t-1) valga 0 o 1
                ind=0
                if St_vieja[i][j]==0:
                    ind=0
                elif St_vieja[i][j]==1:
                    ind=1
                fila_nueva.append(tabla[pos][ind])
            St_nueva.append(fila_nueva)
        S.append(St_nueva)
    return S[-1]




            

def opFinal(matriz:list,z:list,Cini:int)->list:
    """
    in: matriz de bin en str, z lista de len(m)*len(m[0])*len(m[0][0]), Cini entero dado
   
    out: una matriz m*n 
    
    Example:
    -----------
    matriz=[['00110110', '00110111'], ['00111000', '00111000']]
    z=[0.44188213370884455,0.1269141527519082 , ... , 
      0.6061470652329817, 0.4525983619717273]
    >>> opFinal(matriz,z,168)
        [['10011110', '01110110'], ['11111011', '10101010']]
    
    """
    m=len(matriz)
    n=len(matriz[0])
    matriz1D=aplanaMatriz(matriz)
    C=[bin_8(Cini)]
    for i in range(n*m):
        #usamos C[i] para usar el ultimo elem añadido
        nuevoC=suma_k(suma_k(C[i],matriz1D[i]),bin_8(int(z[i]*(10**13))%256))
        C.append(nuevoC)
        #C tiene m*n+1, descartamos el Cini
    return DesAplana(C[1:],m,n)


# -------------------------------------------------------
# RESULTADO
# -------------------------------------------------------


def Fase1y2(img:str):
    """
    in: Dada una imagen, pasado su nombre en str
        
    out: Devolverá la matriz después de la fase 1 de confusión y la 2 de difusión
    
    """
    # FASE 1 
    matrizBin=img_a_matrizBin(img)
    
    m2=separa2(matrizBin) # da la matriz Mx2N
    
    #calculamos los parametros gorro
    #en la F1 usaremos x e y y en la F2 el z
    x,y,z=x_y_z(m2)
    x_hat,y_hat,z_hat=f_hats(x,y,z,len(m2),len(m2[0]))
    
    m_permutada=permutacion(m2,x_hat,y_hat)
    
    
    #FASE 2
    #vamos a separar la matriz permutada en los bits altos y los bajos
    mAltos=bitsAltos(m_permutada) #Mx4N
    mBajos=bitsBajos(m_permutada) #Mx4N
    #sus elems son str
    
    # Para obtener el S-1 convertiremos z_hat en matriz
    m_nuevo=len(mAltos)
    n_nuevo=len(mAltos[0])
    S_menos1=DesAplana(z_hat,m_nuevo,n_nuevo)
    #Los elementos de S_menos1 son ints
    
    S=tabla1(mAltos,6,S_menos1)
    #Los elementos de S son ints 
    
    #Ahora unimos los bits altos,siendo el valor de St claculado y los bajos
    #para ello tenemos que volver a agrupar cada 4 bits en una sola celda
    union4Altos=une4(S)
    union4Bajos=une4(mBajos) 
    unidos=unionBits(union4Altos,union4Bajos)
    #queremos que en lugar de en cada celda un unico bit, tengamos los 8
    #hemos recuperado las dimensiones originales de la matriz
    
    # Hay que añadir una operación extra por si la informacion se encontrarara en los bits inferiores
    #usaremos Cini=168
    Cini=168
    C=opFinal(unidos,z,Cini)
    #C tiene elementos como binarios en string
    
    Cint=imgBin_a_Int(C)
    #Cint tiene elementos el entero asociado al bin
    
    mfinal=np.array(Cint).astype(np.uint8)
    img_final=Image.fromarray(mfinal)
    return img_final
   
