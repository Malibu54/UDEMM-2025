''''
Este programa solicita al usuario ingresar una dirección IP IPv4. 
Luego valida si la dirección IP ingresada cumple con el formato IPv4 válido y si pertenece a alguno de los rangos especificados. 
Si es válida, muestra a qué VLAN pertenece. 
Si no es válida, muestra un mensaje de error y registra un intento erróneo. 
El programa termina cuando el usuario ingresa "fin" y luego muestra la cantidad total de intentos erróneos.
'''

import requests
from bs4 import BeautifulSoup

# Conjunto de etiquetas válidas
etiquetas_validas = {'html', 'body', 'title', 'script', 'head', 'meta', 'span', 'href', 'link', 'div', 'application', 'json'}

def procesar_pagina(url):
    # Realizar la solicitud GET a la página web
    response = requests.get(url)
    
    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Obtener el contenido HTML de la página
        html = response.text
        
        # Analizar el contenido HTML utilizando BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        # Inicializar contadores
        conteo_etiquetas = {}
        etiquetas_invalidas = 0
        
        # Contabilizar etiquetas válidas
        for etiqueta in etiquetas_validas:
            conteo_etiquetas[etiqueta] = len(soup.find_all(etiqueta))
        
        # Contabilizar etiquetas inválidas
        for etiqueta in soup.find_all():
            if etiqueta.name not in etiquetas_validas:
                etiquetas_invalidas += 1
        
        # Imprimir el reporte completo
        print("Reporte completo:")
        print("-----------------")
        for etiqueta, cantidad in conteo_etiquetas.items():
            print(f"{etiqueta}: {cantidad}")
        
        # Imprimir total de etiquetas encontradas
        total_etiquetas = sum(conteo_etiquetas.values())
        print(f"Total de etiquetas encontradas: {total_etiquetas}")
        
        # Imprimir cantidad máxima de etiquetas
        max_etiquetas = max(conteo_etiquetas.values())
        print(f"Cantidad máxima de etiquetas encontradas: {max_etiquetas}")
        
        # Imprimir cantidad mínima de etiquetas
        min_etiquetas = min(conteo_etiquetas.values())
        print(f"Cantidad mínima de etiquetas encontradas: {min_etiquetas}")
        
        # Imprimir cantidad total de etiquetas inválidas
        print(f"Total de etiquetas inválidas: {etiquetas_invalidas}")
    else:
        print("Error: No se pudo acceder a la página web.")

# Ejemplo de uso
if __name__ == "__main__":
    url = input("Ingrese la URL de la página web a procesar: ")
    procesar_pagina(url)
