# Autómatas Celulares en la Criptografía

En mi Trabajo de Fin de Grado , quiero implementar distintos algoritmos para encriptar tanto texto como imágenes usando autómatas celulares.


## Encriptación de texto
Usaremos la **Regla 30** , que es una regla de evolución para un autómata celular unidimensional, para encriptar palabras o texto.

La evolución de cada celda se define mediante la siguiente operación lógica:
$$c_i^{(t+1)} = c_{i-1}^{(t)} \oplus (c_i^{(t)} \lor c_{i+1}^{(t)})$$

Donde $\oplus$ representa la operación XOR y $\lor$ la operación OR.

### Metodología de Encriptación de texto
Se parte de una secuencia inicial dada. 
1. Se genera una secuencia binaria a partir de la Regla 30.
2. Se convierte la palabra introducida por el usuario a binario según el código (ASCII).
3. Se aplica una operación **XOR** entre el mensaje dado pasado a binario y la secuencia generada por la Regla 30, y se vuelve a pasar a palabra, usando el sistema hexadecimal (para evitar problemas con símbolos como 'ñ' o 'à'), para obtener la nueva palabra encriptada.

Este algoritmo de encriptación de mensajes usando la regla 30 está inspirado en el siguiente artículo:
* **Título del artículo:** "Descripción y Aplicaciones de los Autómatas Celulares"
* **Autor:** David Alejandro Reyes Gómez
* **Enlace:** [Haz clic aquí para leer el artículo](https://www.comunidad.escom.ipn.mx/genaro/Papers/Veranos_McIntosh_files/Articulo%20Verano%20De%20Investigacion%202011.pdf)


## Encriptación de imágenes
### Metodología de Encriptación de imágenes
Se parte de una imagen inicial.
1. Se convierte en una matriz.
2. La encriptación consta de 2 fases, la Confusión y la Difusión.
3. En la Confusión, a través de un mapa caótico, se permutan los elementos de la matriz.
4. En la fase de Difusión, la matriz se modifica siguiendo la tabla de reglas locales, que consideran los vecinos de cada célula y su estado anterior para poder asegurar su reversibilidad:
   #### Reglas Locales del Autómata Reversible (RCA)
   
     ![Reglas Locales del RCA](tabla1_reglasACR.png)
   
6. Finalmente se realiza una operación auxiliar:
   $$c_i = c_{i-1} \oplus p'_i \oplus \text{mod}(\lfloor z_i \cdot 10^{13} \rfloor, 256)$$ .

Este proyecto busca encriptar imágenes , usando algoritmos basados en el siguiente artículo:

* **Título del artículo:** "A novel image encryption algorithm using chaos and reversible cellular automata"
* **Autores:** Xingyuan Wang, Dapeng Luan
* **Enlace:** [Haz clic aquí para leer el artículo](https://www.sciencedirect.com/science/article/abs/pii/S1007570413001524?fr=RR-1&ref=cra_js_challenge)


## Cómo usar el proyecto
1. Se debe tener instalado Python.
2. Abrir el archivo principal en Spyder.
3. En el caso de encriptar textos:
     Ejecutar el script regla30.py e introducir la palabra/texto que se desee encriptar, seguido del estado inicial del que partirá el Autómata para la regla 30, y  del número de iteraciones (este número tiene que ser suficientemente grande para poder cubrir el texto/palabra completo). Por ejemplo, sea r0=[0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0] , encripta('hola',r0,100) o desEncripta('hgäa',r0,100) si se quiere desencriptar. El estado inicial tiene que ser el mismo en ambos casos.
4. En el caso de las imágenes:
     Se debe ejecutar el script encriptacion_imagenes.py o encriptacion_imagenes_listas.py (ambos realizan lo mismo pero de diferentes formas) e introducir el nombre de la imágen que se desee encriptar. Esta tiene que estar en la misma ubicación que el programa. Ej: encripta_img $$("p1.png", x_0, y_0, z_0, u, k_1, k_2, k_3,t)$$, para unos parámetros $x_0,y_0,z_0,u,k_1,k_2,k_3,t$ seleccionados para que cumplan unos requisitos dados. En el archivo del programa ya se han inicializado unos valores, por lo que para ejecutarlo bastaría usar su nombre.
5. Para poder desencriptar, en el archivo imagenes.py ejecutar la encriptación y guardar el resultado. A continuación, hacer                                  desEncripta_img $$("resultado.png",x0,y0,z0,u,k1,k2,k3,t)$$, usando los mismos parámetros que al encriptar.



### Tecnologías utilizadas
- **Lenguaje:** Python 
- **Entorno:** Spyder
- **Control de versiones:** Git y GitHub
