# -*- coding: utf-8 -*-
"""
Created on Mon Dec  1 18:14:05 2025

TFG

@author: Irene
"""

 # cuidado con caracteres españoles y tildes y cosas q son dos bytes
# cifrar y descifrar a.encode() y a.decode()


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
        it es un entero que será el número de iteraciones que usaremos
        
    out: Devolverá la palabra encriptada en forma de str

    Example
    ------
    >>> encripta('adiós muy buenas',230)
    'anKss*Oõy buedCó'
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
    """
    result=encripta(pal,it)
    return result



        
        
    
    
    


            
        
        
    
    


    
        