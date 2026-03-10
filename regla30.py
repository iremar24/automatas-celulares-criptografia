# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 15:19:56 2026

@author: Irene
"""

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
   
    return f"{n:08b}"


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


def XOR(pal1:str,pal2:str)->str:
    """
    in: pal1 y pal2 son dos palabras en string
        
    out: Devolverá una lista con los int correspondientes a aplicar XOR a cada uno de sus elementos

    Example
    ------
    >>> XOR("hola","vale")
         [30, 14, 0, 4]
    
    """
    palabra_xor=bytearray()
    pal1_bytes=pal1.encode('utf-8')
    pal2_bytes=pal2.encode('utf-8')
    i=len(pal1_bytes)
    j=len(pal2_bytes)
    
    if i>=j:
        for k in range(0,i):
            letra_xor=pal1_bytes[k] ^ pal2_bytes[k%j]
            palabra_xor.append(letra_xor)
            
    else:
        for k in range(0,j):
            letra_xor=pal1_bytes[k%i] ^ pal2_bytes[k]
            palabra_xor.append(letra_xor)
           
        
    return list(palabra_xor)


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
    r0=0b0000000000001000000000000
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



