'''Realizar un código en Python que permita poder visualizar la siguiente composición
de números:
Así se ve hasta el número 5
# 54321
# *4321
# **321
# ***21
# ****1
Realizar un código en Python que permita poder realizar la misma visualización teniendo en
cuenta que debe ser ingresado como parámetro un N que debe ser >5 y < 20. Por lo tanto,
debe poder graficar números entre 1 al 20 en el formato que se ve en el ejemplo.'''

def mostrar_composicion(N):
    if N <= 5 or N >= 20:
        print("El número debe ser mayor que 5 y menor que 20.")
        return

    for i in range(N):
        # Imprimir asteriscos
        print('*' * i, end='')

        # Imprimir números descendentes desde N - i hasta 1
        for j in range(N - i, 0, -1):
            print(j, end='')

        print()  # Nueva línea al final de cada fila

# Ejemplo de uso:
try:
    N = int(input("Ingresa un número mayor que 5 y menor que 20: "))
    mostrar_composicion(N)
except ValueError:
    print("Por favor, ingresa un número entero válido.")
