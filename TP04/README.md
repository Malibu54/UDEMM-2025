# UdeMM - Licenciatura en Administración de Sistemas (FAE) 

Trabajo práctico número 
4 del primer cuatrimestre del año 2025.
Los siguientes proyectos fueron desarrollados en Visual Studio Code con lenguaje **Python 3**

# Ejercicio 1 - 

Este proyecto en Python genera una visualización numérica basada en un número entero N ingresado por el usuario. La salida consiste en una serie de líneas que combinan asteriscos (*) y números en orden descendente, siguiendo un patrón específico.

## Requisitos

Usar Python 3.10 o superior si es posible, ya que:

* Tiene mejor rendimiento.
* Incluye mejoras en mensajes de error.
* Es compatible con las últimas herramientas de desarrollo.

## 🔍 Cómo verificar tu versión de Python
En una terminal o consola, escribí:

```bash
python --version
```

o si estás usando python3:

```bash
python3 --version
```

## Instrucciones de Uso

1. Clona este repositorio o descarga el archivo `Ejercicio1.py`.
2. Abrí una terminal o consola de comandos.
3. Ejecuta el script con el siguiente comando: `python3 Ejercicio1.py`.
4. Ingresa un número entre 6 y 19 cuando se te solicite.


## Reglas de Validación

- El número ingresado debe ser un **número entero**.
- El número debe estar en el **rango estricto de 6 a 19** (es decir, `N > 5` y `N < 20`).
- Si el valor ingresado **no es un número entero**, se mostrará un mensaje de error.
- Si el número está **fuera del rango permitido**, también se mostrará un mensaje indicando el error.

## Ejemplo de Ejecución

```
Ingresa un número mayor que 5 y menor que 20: 7
7654321
*654321
**54321
***4321
****321
*****21
******1
```

**Ingrese un número mayor que 5 y menor que 20: 4**  
**El número debe ser mayor que 5 y menor que 20.**

**Ingrese un número mayor que 5 y menor que 20: hola**  
**Por favor, ingresa un número entero válido.**


# Ejercicio 2 Inversión de Cadena y Conteo de Caracteres

Este proyecto en Python permite ingresar una cadena de texto y obtener una lista de sus caracteres en orden inverso, junto con la cantidad total de caracteres. Todo esto se realiza sin utilizar funciones ni librerías externas, como reversed(), len(), list(), etc.

## Requisitos
Usar Python 3.10 o superior si es posible, ya que:

* Tiene mejor rendimiento.
* Incluye mejoras en mensajes de error.
* Es compatible con las últimas herramientas de desarrollo.

## 🔍 Cómo verificar tu versión de Python
En una terminal o consola, escribí:

``` bash
python --version
```

o si estás usando python3:

```bash
python3 --version
```

## Instrucciones de Uso

1. Cloná este repositorio o descargá el archivo `Ejercicio2.py`.
2. Abrí una terminal o consola de comandos.
3. Ejecuta el script con el siguiente comando: `python3 Ejercicio1.py`.

El programa procesará la cadena definida en el código y mostrará el resultado.

## Funcionalidad
El script realiza lo siguiente:

1. Recorre una cadena de texto desde el último carácter al primero.
2. Guarda cada carácter en una lista.
3. Cuenta manualmente la cantidad total de caracteres.
4. Devuelve un diccionario con la lista invertida (items) y el total (length).

## Ejemplo de Ejecución

Para la cadena:

``` python
"la argentina es enorme"
``` 

La salida será:

``` python
{
    'items': ['e', 'm', 'r', 'o', 'n', 'e', ' ', 's', 'e', ' ', 'a', 'n', 'i', 't', 'n', 'e', 'g', 'r', 'a', ' ', 'a', 'l'],
    'length': 22
} 
```

# Ejercicio 3 - Codificador y Decodificador de Texto 

Este programa en Python permite codificar una cadena de texto convirtiendo cada carácter en su representación numérica y también decodificarla para obtener nuevamente el texto original.

## Descripción

El programa ofrece dos funciones principales:

- `encode(texto)`: Convierte cada carácter de un texto en su valor numérico utilizando la función `ord`, y los separa por comas.
- `decode(codificado)`: Convierte una secuencia de números separados por comas en el texto original, utilizando la función `chr`.

Este sistema puede ser útil para representar texto de forma numérica, realizar transformaciones básicas o para comprender mejor la relación entre caracteres y sus códigos Unicode.

## Requisitos

- Python 3.x

## Instalación

No se requiere instalación de bibliotecas externas. Solo necesitas tener Python instalado en tu sistema.

### Ejemplo de Ejecución

1. Ejecuta el programa desde la terminal:

```bash
$ python3 codificador.py
```

2. El programa mostrará el texto original, su versión codificada y el texto decodificado.

## Ejemplo

```text
Texto original: este es un ejemplo
Texto codificado: 101,115,116,101,32,101,115,32,117,110,32,101,106,101,109,112,108,111
Texto decodificado: este es un ejemplo
```

# Ejercicio 5 - Pruebas A/B en Publicidad de Zapatillas

Este proyecto consiste en un programa en Python para realizar pruebas A/B en la publicidad de una marca de zapatillas. Permite ingresar datos como la cantidad de clicks y espectadores involucrados en dos tipos de publicidad, calcular estadísticas relevantes y realizar pruebas estadísticas.

## Requisitos

- Python 3.x instalado en tu sistema.

## Instalación

No se requiere instalación adicional.

## Uso

1. Ejecuta el archivo `Ejercicio5.py` en la terminal.

````
python3 Ejercicio5.py
````

2. Sigue las instrucciones para ingresar los datos de cada prueba A/B.
3. El programa calculará automáticamente los máximos y mínimos valores, así como las estadísticas necesarias.
4. Al finalizar, se mostrarán los resultados en pantalla, incluyendo el test estadístico realizado.


### Autora: [Oriana Galíndez]


## Licencia

[MIT](https://choosealicense.com/licenses/mit/)