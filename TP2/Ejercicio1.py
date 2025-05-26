''''
Este código solicitará al usuario que ingrese disposiciones de puestos y luego verificará si son válidas y simétricas según las reglas dadas. 
El programa continuará ejecutándose hasta que el usuario ingrese "salir".
Al final, mostrará la cantidad de disposiciones simétricas encontradas.
'''

def validar_disposicion(disposicion):
    if len(disposicion) != 6:
        return False
    if disposicion[0] != 'B' or disposicion[-1] != 'A':
        return False
    if len(set(disposicion)) != len(disposicion):  # Verificar que no se repitan B y A
        return False
    valid_roles = {'B', 'C', 'D', 'E', 'F', 'A'}
    if not set(disposicion).issubset(valid_roles):
        return False
    return True

def main():
    disposiciones_afirmativas = 0
    while True:
        disposicion = input("Ingrese la disposición de puestos (B,C,D,E,F,A): ").strip().upper()
        if disposicion.lower() == 'salir':
            break
        if validar_disposicion(disposicion):
            print("La disposición es válida y simétrica.")
            disposiciones_afirmativas += 1
        else:
            print("La disposición no es válida o no cumple con las reglas.")

    print(f"Total de disposiciones simétricas encontradas: {disposiciones_afirmativas}")

if __name__ == "__main__":
    main()

