# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 11:21:52 2026

@author: Irene
"""


# ==================================================================================
#   ENCRIPTACIÓN DE MENSAJES
# ==================================================================================

# Valores iniciales
r0=[0]*12+[1]+[0]*12
r1=[0]*11 + [1] + [0]*13

def junta_bits(lista:list):
    """
    
    in: Lista de 8 elementos, 0 o 1, cada uno indica un bit
    
    out: Devuelve el entero asociado a juntar los 8 bits 
    
    Example:
    ----------
    >>> junta_bits([0,1,1,1,0,1,0,1])
        117   (bin(117)='0b1110101')
        
    """
    unido="".join(str(x) for x in lista)
    return int(unido,2)

def separaBitsPal(palabra:str)->list:
    """
    
    in: Dada una palabra 
    
    out: Devuelve la lista separando cada byte de cada letra de cada palabra en
            8 bits siguiendo la codificación latin-1
    Example:
    ---------
    >>> separaBitsPal('España')
        [0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 0,
         0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1]

    """
    result=[]
    lista_bin=list(palabra.encode('iso8859_15'))
    for num in lista_bin:
        result+=[int(x) for x in f"{num:08b}"]
    return result

def regla_30(r0:list[int],it:int)->list[int]:
    """
    in: r0 es la configuración inicial, it es un entero que indica el número de iteraciones que se repetirá el proceso. 
        
    out: Devolverá una lista de números binarios de longitud it, resultante de aplicarle it veces el algoritmo
         e ir almacenando el elemento del medio.

    Consideramos configuración circular, cuando estamos en los extremos se tiene que 
      el vecino izq del primer elemento es el último elemento y el vecino derecho del
      último es el primero.
      
    Example
    ------
    r0=[0]*12+[1]+[0]*12
    >>> regla_30(r0,20)
        [1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0]
    
    """
    
    rs=[r0]
    result=[]
    medio=len(r0)//2 
    m=len(r0)
    for j in range(1,it+1):
        r_nueva=[]
        r_ant=rs[j-1]
        
        
        for i in range(m):
            izq = r_ant[(i-1)%m] 
            centro = r_ant[i]
            der = r_ant[(i+1)%m] 
            r_nueva.append(izq ^ (centro | der))
       
        rs.append(r_nueva)
        result.append(r_nueva[medio])
            
    return result

    
 #-----------------------------------------------------------------------------------
 #   Encriptado y desEncriptado usando sistema latin
 #-----------------------------------------------------------------------------------

# Al ser la operación XOR su propia inversa, la operación de cifrar es también su propia inversa. Por tanto,
# para descifrar habría que aplicar la operación encripta al criptograma recibido, con la misma clave inicial.


def encripta(texto: str,clave_inicial:list) -> str:
    """
    in: texto es un str, que será el mensaje a cifrar/descifrar.
        clave_inicial es el estado inicial del que partirá la regla_30.

        
    out: Devolverá el mensaje cifrado/descifrado en sistema latin-1.

    Example
    ------
    r0=[0]*12+[1]+[0]*12
    >>> encripta('María es Española',r0)
       'ôêUP\x1b±\x15>Ò\x0c\t\x95/\x06£Æ\x83'
       
    >>> encripta('ôêUP\x1b±\x15>Ò\x0c\t\x95/\x06£Æ\x83',r0)
        'María es Española'
       
    Si probamos con una clave errónea al desencriptar obtendríamos un resultado incorrecto:
    r1=[0]*11 + [1] + [0]*13
    
    >>> encripta('ôêUP\x1b±\x15>Ò\x0c\t\x95/\x06£Æ\x83',r1)
        ']\x928;\x19ÁBúÔ×\x0bÉj\x83ædÍ'
   
    """
    
    
    pal_bin=separaBitsPal(texto)
    
    it= len(pal_bin) #número de iteraciones
    
    # Clave con la regla 30 con la misma longitud que el texto
    clave=regla_30(clave_inicial,it) 

    
    #Operación XOR bit a bit
    result=[]
    for i in range(len(pal_bin)):
        result.append(clave[i] ^ pal_bin[i])
    

    # Agrupamos en bytes de 8 bits
    bytes_encriptados=bytearray()
    for j in range(0,len(result),8):
        entero=junta_bits(result[j:j+8])
        bytes_encriptados.append(entero)
     
    
    return bytes_encriptados.decode('iso8859_15')