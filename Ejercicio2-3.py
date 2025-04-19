'''
Este código solicita al usuario ingresar hasta 25 caracteres en cada repetición y los almacena. 
Cuando se han ingresado 7 repeticiones, muestra los caracteres codificados en base64 en líneas separadas. 
El programa termina cuando el usuario ingresa "fin" y muestra la cantidad total de repeticiones ingresadas.
'''
import re
import base64

def validar_direccion_ip(ip):
    # Expresión regular para validar la dirección IP IPv4
    patron_ip = r'^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$'
    if re.match(patron_ip, ip):
        return True
    else:
        return False

def determinar_vlan(ip):
    if ip.startswith("10."):
        return "VLAN 121"
    elif ip.startswith("172.16."):
        return "VLAN 200"
    elif ip.startswith("192.168."):
        return "VLAN 216"
    else:
        return "No se pudo determinar la VLAN"

def main():
    caracteres = []
    repeticiones = 0
    intentos_erroneos = 0

    while True:
        entrada = input("Ingrese hasta 25 caracteres o 'fin' para terminar: ")

        if entrada == 'fin':
            break

        if len(entrada) != 25:
            print("La entrada debe tener exactamente 25 caracteres.")
            intentos_erroneos += 1
            continue

        caracteres.append(entrada)
        repeticiones += 1

        if repeticiones % 7 == 0:
            mostrar_caracteres_base64(caracteres)
            caracteres = []

    if repeticiones % 7 != 0:
        print("La cantidad de repeticiones ingresada no es un múltiplo de 7.")
        intentos_erroneos += 1

    print("Cantidad de repeticiones ingresadas:", repeticiones)

    while True:
        direccion_ip = input("Ingrese una dirección IP (o 'fin' para salir): ")

        if direccion_ip == 'fin':
            break

        if not validar_direccion_ip(direccion_ip):
            print("Dirección IP inválida. Por favor, ingrese una dirección IP válida en formato IPv4.")
            intentos_erroneos += 1
            continue

        vlan = determinar_vlan(direccion_ip)
        if vlan != "No se pudo determinar la VLAN":
            print(f"La dirección IP {direccion_ip} pertenece a la {vlan}.")
        else:
            print("No se pudo determinar la VLAN para la dirección IP proporcionada.")
            intentos_erroneos += 1

    print(f"Total de intentos erróneos: {intentos_erroneos}")


def mostrar_caracteres_base64(caracteres):
    for caracter in caracteres:
        codificado = base64.b64encode(caracter.encode()).decode()
        print(codificado)


if __name__ == "__main__":
    main()
