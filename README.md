# Autómatas Celulares en la Criptografía

En mi Trabajo de Fin de Grado , quiero implementar distintos algoritmos para encriptar tanto texto como imágenes usando autómatas celulares.


## Encriptación de texto
Usaremos la **Regla 30** , que es una regla de evolución para un autómata celular unidimensional, para encriptar palabras o texto.

La evolución de cada celda se define mediante la siguiente operación lógica:
$$c_i^{(t+1)} = c_{i-1}^{(t)} \oplus (c_i^{(t)} \lor c_{i+1}^{(t)})$$

Donde $\oplus$ representa la operación XOR y $\lor$ la operación OR.

### Metodología de Encriptación
Se parte de una secuencia inicial formada por 0 y un solo 1 en el centro. 
1. Se genera una secuencia binaria a partir de la Regla 30.
2. Se convierte la palabra introducida por el usuario a binario según el código (ASCII).
3. Se aplica una operación **XOR** entre el mensaje dado pasado a binario y la secuencia generada por la Regla 30, y se vuelve a pasar a palabra, para obtener la nueva palabra encriptada.

### Cómo usar el proyecto
1. Asegúrate de tener instalado Python.
2. Abre el archivo principal en Spyder.
3. Ejecuta el script e introduce la palabra que deseas encriptar cuando el programa lo solicite.

### Tecnologías utilizadas
- **Lenguaje:** Python 
- **Entorno:** Spyder
- **Control de versiones:** Git y GitHub

## Encriptación de imágenes
