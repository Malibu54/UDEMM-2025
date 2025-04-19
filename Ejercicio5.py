''''
Este código proporciona una herramienta simple para realizar pruebas A/B en la publicidad de zapatillas, calculando estadísticas relevantes y permitiendo al usuario continuar con más pruebas si es necesario.
'''

import math

# Función para ingresar un número entero válido
def ingresar_entero(mensaje):
    while True:
        try:
            valor = int(input(mensaje))
            return valor
        except ValueError:
            print("Error: Debes ingresar un número entero.")

# Función para calcular sigma
def calcular_sigma(n, N):
    p = n / N
    sigma = math.sqrt(p * (1 - p) / N)
    return sigma

# Función para realizar el test estadístico
def test_estadistico(p1, p2, sigma1, sigma2, N1, N2):
    sigma = math.sqrt(sigma1**2 / N1 + sigma2**2 / N2)
    resultado = (p1 - p2) / sigma
    return resultado

# Función para realizar la aplicación de pruebas A/B
def aplicacion_pruebas_ab():
    errores = 0
    resultados_clicks = []
    resultados_espectadores = []

    # Ingreso de datos y cálculos
    for i in range(2):  # Realizamos dos pruebas A/B
        print(f"\nPrueba A/B {i+1}:")
        while True:
            try:
                clicks = ingresar_entero("Ingrese la cantidad de clicks: ")
                espectadores = ingresar_entero("Ingrese la cantidad de espectadores: ")
                resultados_clicks.append(clicks)
                resultados_espectadores.append(espectadores)
                break
            except:
                errores += 1
                print("Error: Debes ingresar números enteros.")

    # Verificamos que se hayan tomado ambas muestras
    if len(resultados_clicks) == 2:
        # Cálculo de máximos y mínimos
        max_clicks = max(resultados_clicks)
        min_clicks = min(resultados_clicks)
        max_espectadores = max(resultados_espectadores)
        min_espectadores = min(resultados_espectadores)

        print("\nResultados:")
        print("Máximo de clicks:", max_clicks)
        print("Mínimo de clicks:", min_clicks)
        print("Máximo de espectadores:", max_espectadores)
        print("Mínimo de espectadores:", min_espectadores)

        # Cálculo de sigma
        sigma1 = calcular_sigma(resultados_clicks[0], resultados_espectadores[0])
        sigma2 = calcular_sigma(resultados_clicks[1], resultados_espectadores[1])

        # Cálculo de medias
        p1 = sum(resultados_clicks[0])/sum(resultados_espectadores[0])
        p2 = sum(resultados_clicks[1])/sum(resultados_espectadores[1])

        # Test estadístico
        resultado_test = test_estadistico(p1, p2, sigma1, sigma2, sum(resultados_espectadores[0]), sum(resultados_espectadores[1]))
        print("\nResultado del test estadístico:", resultado_test)
    else:
        print("Error: Debes ingresar datos para ambas pruebas A/B.")

    # Mostrar errores y cantidad de muestras
    print("\nTotal de errores:", errores)
    print("Cantidad de muestras tomadas:", len(resultados_clicks))

    # Preguntar si desea continuar
    continuar = input("\n¿Desea continuar? (s/n): ")
    if continuar.lower() == 's':
        aplicacion_pruebas_ab()

# Llamar a la función principal
aplicacion_pruebas_ab()
