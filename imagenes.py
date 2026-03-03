# -*- coding: utf-8 -*-
"""
Created on Tue Feb  3 19:54:28 2026

@author: Irene
"""

#EN ESTE CÓDIGO SE ALTERA UN POCO EL MÉTODO, EN LA PARTE DE TABLA1
#YA QUE SE FORMA LA MATRIZ UNIDOS UNIENDO LAS DOS ULTIMAS ITERACIONE
# DE S, St+1 y St COMO LOS ALTOS Y LOS BAJOS PARA PODER RECUPERAR AL 
#MENOS UNA PARTE DE LA IMAGEN ORIGINAL E INTENTAR DESENCRIPTAR 

import numpy as np
from PIL import Image
from math import sin 


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






# ==================================================================================
# SECCIÓN 2. ENCRIPTACIÓN DE IMÁGENES 
# ==================================================================================


# -------------------------------------------------------
# Operaciones auxiliares con matrices
# -------------------------------------------------------
  


img=Image.open("beach.jpg").convert("L")
  # Convertir imagen a matriz de números (array)
matriz = np.array(img)

  # Volver a convertir a objeto Pillow
nueva_img = Image.fromarray(matriz)

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
 
def junta2(matriz:list)->list:
    m=len(matriz)
    n=len(matriz[0])
    nueva_matriz=[]
    for i in range(m):
        nueva_fila=[]
        for j in range(0,n,2):
            elem=matriz[i][j]
            elem2=matriz[i][j+1]
            nueva_fila.append(elem+elem2)
        nueva_matriz.append(nueva_fila)
    return nueva_matriz
 
#Para este paso es necesario haber pactado los valores
#iniciales con el receptor, con x0,y0,z0 pertenecientes a (0,1)

# El parámtero u : 0 < u < 3.999

def x_y_z(matriz:list)->list:
    """
    in: Dada una matriz de bin Mx2N
        
    out: Devolverá los valores x, y, z

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
      in: Dados x,y,z
          
      out: Devolverá los x_gorro,y_gorro y z_gorro

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
        
    out: Devolverá la matriz Mx2N resultante de intercambiar de posicion sus celdas

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
    
    out: Devuelve la matriz formada por las columnas pares
    
    Example
    --------
    >>> bitsAltos([[(1,0),(0,1),(10,0),(0,20),(11,1),(12,1)],[(21,2),(22,2),(3,1),(1,3),(4,5),(6,7)]])
        [[1, 0, 10, 0, 11, 1], [21, 2, 3, 1, 4, 5]]
   
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
    >>> bitsBajos([[(1,0),(0,1),(10,0),(0,20),(11,1),(12,1)],[(21,2),(22,2),(3,1),(1,3),(4,5),(6,7)]])
        [[0, 1, 0, 20, 12, 1], [22, 2, 1, 3, 6, 7]]
   
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
                if int(St_vieja[i][j])==0:
                    ind=0
                elif int(St_vieja[i][j])==1:
                    ind=1
                fila_nueva.append(tabla[pos][ind])
            St_nueva.append(fila_nueva)
        S.append(St_nueva)
    #Para poder descifrar después vamos a guardar ambos
    return S[-1],S[-2]




            

def opFinal(matriz:list,z:list,Cini:int)->list:
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


def Fase1y2_2(img:str):
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
    
    #sus elems son str
    
    # Para obtener el S-1 convertiremos z_hat en matriz
    m_nuevo=len(mAltos)
    n_nuevo=len(mAltos[0])
    S_menos1=DesAplana(z_hat,m_nuevo,n_nuevo)
    #Los elementos de S_menos1 son ints
    
    Saltos,Sbajos=tabla1(mAltos,6,S_menos1)
    #Los elementos de S son ints 
    
    #Ahora unimos los bits altos,siendo el valor de St claculado y los bajos
    #para ello tenemos que volver a agrupar cada 4 bits en una sola celda
    union4Altos=une4(Saltos)
    union4Bajos=une4(Sbajos) 
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
                
                
# ==================================================================================
# SECCIÓN 3. DESENCRIPTACIÓN DE IMÁGENES
# ==================================================================================
        
def opFinal_inv(matriz:list,z:list,Cini:int)->list:
    m=len(matriz)
    n=len(matriz[0])
    matriz1D=aplanaMatriz(matriz)
    C=[bin_8(Cini)]+matriz1D
    P=[]
    for i in range(n*m):
        #usamos C[i] para usar el ultimo elem añadido
        nuevop=suma_k(suma_k(C[i],C[i+1]),bin_8(int(z[i]*(10**13))%256))
        P.append(nuevop)
    
    return DesAplana(P,m,n)

def tabla1_inv(matriz:list,tiempo:int,Sf:list):
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
                binario=str(iz)+str(arriba)+str(centro)+str(abajo)+str(dcha)
                #pasamos el num a binario para acceder a su valor en la tabla
                pos=bin_a_num(binario)
                
    
                ind="0"
                if str(St_fut[i][j])==str(tabla[pos][0]):
                    ind="0"
                elif str(St_fut[i][j])==str(tabla[pos][1]):
                    ind="1"
                
                fila_nueva.append(ind)
            St_nueva.append(fila_nueva)
        S.append(St_nueva)
    return S[-2],S[-1]


def permutacion_inv(matriz:list,x_hat,y_hat)->list:
    """
    in: Dada una matriz de bin Mx2N
        
    out: Devolverá la matriz Mx2N resultante de intercambiar de posicion sus celdas

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



def desEncripta_img(img:str):
    #Proceso inverso
    matrizBin=img_a_matrizBin(img)
    m2=separa2(matrizBin)
    x,y,z=x_y_z(m2)
    x_hat,y_hat,z_hat=f_hats(x,y,z,len(m2),len(m2[0]))
   
    P=opFinal_inv(matrizBin,z,168)
    #P=unidos de antes
    P2=separa2(P)
    mAltos=bitsAltos(P2) #string
    mBajos=bitsBajos(P2) #string
    
    
    S0,z2=tabla1_inv(mAltos,6,mBajos) #string
    
    #comprobamos que vamos bien al ser z2==z_hat
    #SO==mAltos1 de antes
    
    union4Altos=une4(S0)
    union4Bajos=une4(mBajos)
    unidos=unionBits(union4Altos,union4Bajos)
    
    unidos2=separa2(unidos)
    
    mp=permutacion_inv(unidos2,x_hat,y_hat)
    
    #ahora hay que juntar
    mpJuntas=junta2(mp)
    
    Cint=imgBin_a_Int(mpJuntas)
    mfinal=np.array(Cint).astype(np.uint8)
    img_final=Image.fromarray(mfinal)
    return img_final