# Autómatas Celulares en la Criptografía

En mi Trabajo de Fin de Grado , quiero implementar distintos algoritmos para encriptar tanto texto como imágenes usando autómatas celulares.


## Encriptación de texto
Usaremos la **Regla 30** , que es una regla de evolución para un autómata celular unidimensional, para encriptar palabras o texto.

La evolución de cada celda se define mediante la siguiente operación lógica:
$$c_i^{(t+1)} = c_{i-1}^{(t)} \oplus (c_i^{(t)} \lor c_{i+1}^{(t)})$$

Donde $\oplus$ representa la operación XOR y $\lor$ la operación OR.

### Metodología de Encriptación de texto
Se parte de una secuencia inicial formada por 0 y un solo 1 en el centro. 
1. Se genera una secuencia binaria a partir de la Regla 30.
2. Se convierte la palabra introducida por el usuario a binario según el código (ASCII).
3. Se aplica una operación **XOR** entre el mensaje dado pasado a binario y la secuencia generada por la Regla 30, y se vuelve a pasar a palabra, para obtener la nueva palabra encriptada.


### Tecnologías utilizadas
- **Lenguaje:** Python 
- **Entorno:** Spyder
- **Control de versiones:** Git y GitHub

## Encriptación de imágenes
Este proyecto busca encriptar imágenes , usando algoritmos basados en el siguiente artículo:

* **Título del artículo:** "A novel image encryption algorithm using chaos and reversible cellular automata"
* **Autores:** Xingyuan Wang, Dapeng Luan
* **Enlace:** [Haz clic aquí para leer el artículo](https://www.sciencedirect.com/science/article/abs/pii/S1007570413001524?fr=RR-1&ref=cra_js_challenge)

### Metodología de Encriptación de imágenes
Se parte de una imagen inicial, que se convierte en una matriz y sus valores se pasan a binario. La encriptación consta de 2 fases, la Confusión y la Difusión. En la Confusión, a través de un mapa caótico, se permutan los elementos de la matriz. En la fase de Difusión, centrada principalmente en los 4 bits superiores de cada celda, la matriz se modifica siguiendo una tabla que tiene en cuenta varios estados diferentes en diferentes tiempos, y alguna operación auxiliar.

## Cómo usar el proyecto
1. Asegúrate de tener instalado Python.
2. Abre el archivo principal en Spyder.
3. En el caso de encriptar textos:
     Ejecutar el script e introducir la palabra/text que se desee encriptar,seguido de el número de iteraciones (este número tiene que ser suficientemente grande       para poder cubrir el texto/palabra completo). EJ: encripta('hola',100) o des
4. En el caso de las imágenes:
     Se debe ejecutar el script e introducir el nombre de la imágen que se desee encriptar. Esta tiene que estar en la misma ubicación que el programa. Ej:             Fase1y2("beach.jpg").
5. Para
