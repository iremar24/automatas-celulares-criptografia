# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 15:19:56 2026

@author: Irene
"""


# ==================================================================================
#   ENCRIPTACIÓN DE MENSAJES
# ==================================================================================


#-----------------------------------------------------------------------------------
#   Operaciones auxiliares
#-----------------------------------------------------------------------------------

def junta_bits(lista:list):
    """
    
    in: lista de 8 elementos, 0 o 1, cada uno indica un byte
    
    out: Devuelve el entero asociado a juntar los 8 bits 
    
    Example:
    ----------
    >>> junta_bits([0,1,1,1,0,1,0,1])
        117   (bin(117)='0b1110101')
        
    """
    elem=0b0
    n=len(lista)
    for i in range(n):
        elem=lista[i]<<(n-i-1) | elem
    return elem


def separaBits(num:int)->list:
    """
    
    in  : Dado un número entero
    
    out : Devuelve una lista de 8 elementos con cada bit del número
        
    Example:
    ---------
    >>> separaBits(117)
        [0, 1, 1, 1, 0, 1, 0, 1]
    
    """
    result=[]
    n=len(bin(num))-2
    mascaras=[2**i for i in range(n)]
    for masc in mascaras:
        elem=num & masc
        if elem>0:
            result.append(1)
        else: 
            result.append(0)
    
    result.reverse()
    while len(result)<8:
        result=[0]+result
    return result

def separaBitsPal(palabra:str)->list:
    """
    
    in: Dada una palabra 
    
    out: Devuelve la lista separando cada bit de cada palabra 
            8 bits o 16 si son caracteres especiales (ñ,á,...)
    Example:
    ---------
    >>> separaBitsPal('España')
        [0,1,0,0,0,1,0,1, 0,1,1,1,0,0,1,1, 0,1,1,1,0,0,0,0, 0,1,1,0,
         0,0,0,1, 1,1,0,0,0,0,1,1,1,0,1,1,0,0,0,1, 0,1,1,0,0,0,0,1]
                  -------------------------------
                   16 bytes correspondientes a ñ
    """
    result=[]
    lista_bin=list(palabra.encode('utf-8'))
    for num in lista_bin:
        result+=separaBits(num)
    return result

def regla_30(r0:list,it:int)->str:
    """
    in: r0 es la configuración inicial, it es un entero que indica el número de iteraciones que se repetirá el proceso 
        
    out: Devolverá un número binario en string resultante de aplicarle it veces el algoritmo
         e ir almacenando el elemento del medio

    Consideramos configuración circular, cuando estamos en los extremos se tiene que 
      el vecino izq del primer elemento es el último elemento y el vecino derecho del
      último es el primero
      
    Example
    ------
    r0=[0]*12+[1]+[0]*12
    >>> regla_30(r0,20)
        [1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0]
    
    """
    #configuración inicial del ejemplo
    #r0=0b0000000000001000000000000 
    
    rs=[r0]
    result=[]
    medio=len(r0)//2
    for j in range(1,it+1):
        r_nueva=[]
        r_ant=rs[j-1]
        
        m=len(r_ant)
        for i in range(m):
            izq = r_ant[(i-1)%m] 
            centro = r_ant[i]
            der = r_ant[(i+1)%m] 
            r_nueva.append(izq ^ (centro | der))
       
        rs.append(r_nueva)
        result.append(r_nueva[medio])
            
    return result


#-----------------------------------------------------------------------------------
#   Ejemplo como el del artículo, sin usar sistema hexadecimal
#-----------------------------------------------------------------------------------
def encripta_articulo(pal: str,clave_inicial:list, it: int) -> str:
    """
    in: pal es un str , que será la palabra/frase que queramos encriptar
        it es un entero que será el número de iteraciones que usaremos.
        Tenemos que asegurarnos que el numero de it sea lo suficientemente grande 
        para cubrir la longitud de la palabra/ frase que queramos encriptar
        
    out: Devolverá la palabra encriptada en forma de str

    Example
    ------
    r0=[0]*12+[1]+[0]*12
    >>> encripta_articulo('SECRETO',r0,100)
        'êÎdï?Å?'
        
    >>> encripta_articulo('María es Española',r0,200)
        'ôêU~×ðP(\x81i?\x96>\x96\x0f\x1b\x8d\x85×'
    """
    
    clave=regla_30(clave_inicial,it)
    pal_bin=separaBitsPal(pal)
    
    result=[]
    for i in range(len(pal_bin)):
        result.append(clave[i] ^ pal_bin[i])

    palabra_encriptada=''
    for j in range(0,len(result),8):
        entero=junta_bits(result[j:j+8])
        palabra_encriptada+=chr(entero)
      
    return palabra_encriptada



#-----------------------------------------------------------------------------------
#   Encriptado y desEncriptado usando sistema hexadecimal
#-----------------------------------------------------------------------------------
def encripta(pal: str,clave_inicial:list, it: int) -> str:
    """
    in: Pal es un str , que será la palabra/frase que queramos encriptar.
        Clave_inicial es el estado inicial del que partirá la regla_30
        it es un entero que será el número de iteraciones que usaremos.
        Tenemos que asegurarnos que el numero de it sea lo suficientemente grande 
        para cubrir la longitud de la palabra/ frase que queramos encriptar
        
    out: Devolverá la palabra encriptada en sistema hexadecimal

    Example
    ------
    r0=[0]*12+[1]+[0]*12
    >>> encripta('María es Española',r0,200)
        'f4ea557ed7f0502881693f963e960f1b8d85d7'
   
    """
    clave=regla_30(clave_inicial,it)
    
    pal_bin=separaBitsPal(pal)
    
    result=[]
    for i in range(len(pal_bin)):
        result.append(clave[i] ^ pal_bin[i])
   

    bytes_encriptados=bytearray()
    for j in range(0,len(result),8):
        entero=junta_bits(result[j:j+8])
        bytes_encriptados.append(entero)
     
    
    return bytes_encriptados.hex()



def desEncripta(pal:str,clave_inicial:list,it:int)->str:
    """
    in: Pal es un str en hexadecimal , que será la palabra/frase que queramos desencriptar.
        Clave_inicial es el estado inicial del que parterá la regla_30.
            (tiene que ser la misma que se usó al encriptar)
        It es un entero que será el número de iteraciones que usaremos 
        
    out: Devolverá la palabra desencriptada en forma de str

    Example
    ------
    r0=[0]*12+[1]+[0]*12
    r02=[0]*12 + [1]+[1]+[0]*11
    
    >>> desEncripta('f4ea557ed7f0502881693f963e960f1b8d85d7',r0,200)
        'María es Española'
        
    si metemos una clave inicial diferente a la que se usó all encriptar:
        
    >>> desEncripta('f4ea557ed7f0502881693f963e960f1b8d85d7',r02,200)
        'Mas���\x1e\x08�c\x06\x07Ճ���̉'
    """
    bytes_unidos=bytes.fromhex(pal)
    enteros_sep=[]
    for elem in bytes_unidos:
        enteros_sep+=separaBits(elem)
    
    #así hemos recuperado los enteros
    
    clave=regla_30(clave_inicial,it)
    
    result=[]
    for i in range(len(enteros_sep)):
        result.append(clave[i] ^ enteros_sep[i])
   

    bytes_desencriptados=bytearray()
    for j in range(0,len(result),8):
        entero=junta_bits(result[j:j+8])
        bytes_desencriptados.append(entero)
    #en este punto tendríamos algo como por ejemplo
    # bytearray(b'Mar\xc3\xada es Espa\xc3\xb1ola')
    
    
    # Usamos errors='replace' para que ponga el símbolo  cuando el byte sea inválido
    # para que si cambiamos la clave inicial nos devuelva un mensaje y no un error
    return bytes_desencriptados.decode('utf-8', errors='replace')
    
     
    


