'''Realizar un código en Python que permita poder generar un array o lista de
caracteres en orden inverso y la cantidad total de elementos que este contiene. Al
ingresar una cadena de caracteres. No se pueden utilizar funciones ni librerías
extras. Usted debe implementarlas.
Si tengo “la argentina es enorme”
debería retornar:

{
    items: ['e','m','r', 'o', 'n', 'e', ' ','s', 'e', ' ', 'a', 'n', 
'i','t', 'n', 'e', 'g', 'r', 'a', ' ', 'a',  'l'  ]
    length: 22
}
'''

# Función para contar caracteres sin usar len()
def contar_caracteres(cadena):
    contador = 0
    for _ in cadena:
        contador += 1
    return contador

# Función para invertir la cadena sin funciones ni librerías externas
def invertir_cadena(cadena):
    lista_invertida = []
    contador = contar_caracteres(cadena)

    indice = contador - 1
    while indice >= 0:
        lista_invertida += [cadena[indice]]
        indice -= 1

    return {
        "items": lista_invertida,
        "length": contador
    }

# Solicitar entrada al usuario
entrada = input("Ingrese una cadena de texto: ")
resultado = invertir_cadena(entrada)
print(resultado)

