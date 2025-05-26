# UdeMM - Licenciatura en Administración de Sistemas (FAE) 

Trabajo práctico número 2 del primer cuatrimestre del año 2025.
Los siguientes proyectos fueron desarrollados en Visual Studio Code

# Ejercicio 1 - Validador de Disposiciones de Puestos de Trabajo

Este es un proyecto en Python que permite validar si las disposiciones de puestos de trabajo en una oficina son simétricas según ciertas reglas predefinidas. El objetivo es ayudar a garantizar una distribución homogénea y eficiente de los puestos de trabajo.

## Requisitos

- Python 3.x instalado en tu sistema.

## Instrucciones de Uso

1. Clona este repositorio o descarga el archivo `Ejercicio1.py`.
2. Abre una terminal y navega hasta la ubicación del archivo `Ejercicio1.py`.
3. Ejecuta el programa con el comando `python3 Ejercicio1.py`.
4. Sigue las instrucciones en pantalla para ingresar las disposiciones de puestos de trabajo.
5. Ingresa "salir" cuando desees finalizar el programa.

## Reglas de Validación

- La disposición debe tener exactamente 6 caracteres.
- La disposición debe comenzar con 'B' y terminar con 'A'.
- No pueden repetirse 'B' y 'A' en la disposición.
- Los roles válidos son 'B', 'C', 'D', 'E', 'F' y 'A'.

## Ejemplo de Disposición Válida

- BCDEFA
- BCFEFA
- BEFCDA

## Ejemplo de Ejecución

Ingrese la disposición de puestos (B,C,D,E,F,A): BCDEFA
La disposición es válida y simétrica.
Ingrese la disposición de puestos (B,C,D,E,F,A): BCFEGA
La disposición no es válida o no cumple con las reglas.
Ingrese la disposición de puestos (B,C,D,E,F,A): salir
Total de disposiciones simétricas encontradas: 1

 
# Ejercicio 2 y 3 - Validación de Direcciones IP y Codificación Base64

Este es un proyecto de Python que consiste en dos funcionalidades:

1. **Codificación Base64 de Caracteres:**
   - El programa permite al usuario ingresar hasta 25 caracteres en rondas de 7 repeticiones.
   - Los caracteres ingresados son codificados en Base64 y mostrados al usuario en líneas separadas.
   - El usuario puede terminar la entrada ingresando "fin".
   - Al finalizar, se muestra la cantidad de repeticiones ingresadas.

2. **Validación de Direcciones IP y Determinación de VLAN:**
   - El programa valida si las direcciones IP proporcionadas por el usuario son válidas según el estándar IPv4.
   - Determina a qué VLAN pertenecen las direcciones IP, considerando los rangos establecidos por el departamento de redes:
     - Rango A: 10.0.0.0/8 (VLAN 121)
     - Rango B: 172.16.0.0/16 (VLAN 200)
     - Rango C: 192.168.0.0/24 (VLAN 216)
   - Se controla que el usuario ingrese direcciones IP válidas y se informa cualquier error cometido durante la carga.
   - El programa finaliza cuando el usuario decide no continuar la carga.

## Requerimientos

- Python 3.x instalado en el sistema.

## Ejecución

1. Descarga o clona este repositorio en tu máquina local.
2. Abre una terminal y navega al directorio donde se encuentra el archivo `Ejercicio2.py`.
3. Ejecuta el siguiente comando para iniciar el programa:

```
python3 Ejercicio2.py
```
4. Sigue las instrucciones proporcionadas por el programa para utilizar sus funcionalidades.



# Ejercicio 4 - Contador de Etiquetas HTML

Este programa en Python permite contar la cantidad de etiquetas HTML válidas en una página web, así como también identificar etiquetas inválidas.

## Descripción

El programa procesa el contenido HTML de una página web dada por el usuario y cuenta la cantidad de cada etiqueta HTML válida especificada, además de identificar cualquier etiqueta HTML inválida presente en la página. Al final, se genera un reporte completo que incluye la cantidad total de cada etiqueta, la cantidad máxima y mínima de etiquetas encontradas, así como también la cantidad total de etiquetas inválidas.

## Requisitos

- Python 3.x
- Bibliotecas: `requests`, `beautifulsoup4`

## Instalación de Dependencias

Para instalar las dependencias necesarias, ejecuta el siguiente comando en tu terminal por separado:

```
python3 -m pip install beautifulsoup4


python3 -m pip install requests
```


## Uso

1. Ejecuta ` python3 Ejercicio4.py`.
2. Cuando se solicite, ingresa la URL de la página web que deseas procesar.
3. El programa procesará la página web y generará un reporte con la cantidad de cada etiqueta HTML válida encontrada, así como el total de etiquetas, la cantidad máxima y mínima de etiquetas, y la cantidad total de etiquetas inválidas.

## Ejemplo

```
python3 Ejercicio4.py
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