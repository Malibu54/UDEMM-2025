def encode(texto):
    """
    Codifica un texto convirtiendo cada carácter a su valor numérico (usando ord),
    y los separa con comas.
    """
    return ','.join(str(ord(c)) for c in texto)

def decode(codificado):
    """
    Decodifica un texto codificado con números separados por comas,
    convirtiendo cada número a su carácter original (usando chr).
    """
    return ''.join(chr(int(numero)) for numero in codificado.split(','))

# Ejemplo de uso
if __name__ == "__main__":
    texto_original = "este es un ejemplo"
    codificado = encode(texto_original)

    print("Texto original:", texto_original)
    print("Texto codificado:", codificado)
    print("Texto decodificado:", decode(codificado))
