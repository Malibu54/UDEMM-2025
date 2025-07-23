from abc import ABC, abstractmethod

# Clase abstracta base para todas las estrategias de persistencia
class Persistencia(ABC):
    """
    Clase base abstracta que define la interfaz común para cualquier tipo de persistencia de datos.
    """

    def __init__(self, origen, destino):
        """
        Inicializa los atributos comunes de persistencia.
        :param origen: Fuente de datos.
        :param destino: Destino donde se almacenarán los datos.
        """
        self.origen = origen
        self.destino = destino

    @abstractmethod
    def get_datos(self):
        """
        Método abstracto que debe retornar los datos almacenados.
        """
        pass

    @abstractmethod
    def save(self, datos):
        """
        Método abstracto que debe guardar los datos. Es la interfaz estándar.
        """
        pass

# Persistencia en memoria RAM
class Memoria(Persistencia):
    """
    Implementación de persistencia en memoria RAM.
    """

    def __init__(self, origen="mem_interna", destino="mem_externa", cant_bytes=0):
        """
        Inicializa los datos para memoria RAM.
        :param cant_bytes: Cantidad de bytes a almacenar.
        """
        super().__init__(origen, destino)
        self.cant_bytes = cant_bytes
        self.datos = ""

    def get_datos(self):
        """
        Retorna los datos almacenados en memoria.
        """
        return self.datos

    def save(self, datos):
        """
        Guarda datos en memoria RAM simulada.
        """
        print(f"[RAM] Guardando {len(datos)} bytes desde {self.origen} a {self.destino}")
        self.datos = datos

# Persistencia mediante archivos en disco
class Archivo(Persistencia):
    """
    Implementación de persistencia usando archivos con soporte para journaling.
    """

    def __init__(self, nombre, path_fisico, journal_enabled=False, origen="archivo_in", destino="archivo_out"):
        """
        Inicializa la persistencia por archivo.
        :param nombre: Nombre del archivo.
        :param path_fisico: Ruta física del archivo.
        :param journal_enabled: Habilita o no journaling.
        """
        super().__init__(origen, destino)
        self.path_fisico = path_fisico
        self.journal_enabled = journal_enabled
        self.nombre = nombre

    def get_datos(self):
        """
        Lee y retorna los datos del archivo, si existe.
        """
        try:
            with open(f"{self.path_fisico}/{self.nombre}", "r") as f:
                return f.read()
        except FileNotFoundError:
            return ""

    def save_archivo(self, nombre, origen, datos):
        """
        Guarda los datos en archivo, incluyendo journaling si está habilitado.
        """
        if self.journal_enabled:
            print(f"[Archivo] Guardando journal para {nombre}")
        with open(f"{self.path_fisico}/{nombre}", "w") as f:
            f.write(datos)
        print(f"[Archivo] Datos guardados en {self.path_fisico}/{nombre}")

    def save(self, datos):
        """
        Implementa la interfaz común usando el método interno save_archivo.
        """
        self.save_archivo(self.nombre, self.origen, datos)

# Persistencia con cifrado
class Cifrado(Persistencia):
    """
    Implementación de persistencia usando cifrado de datos básico.
    """

    def __init__(self, nombre, path_original, path_cifrado, origen="cif_in", destino="cif_out", cant_bytes_originales=0):
        """
        Inicializa la persistencia cifrada.
        :param nombre: Nombre del archivo.
        :param path_original: Ruta del archivo sin cifrar.
        :param path_cifrado: Ruta donde se guarda el archivo cifrado.
        """
        super().__init__(origen, destino)
        self.nombre = nombre
        self.path_original = path_original
        self.path_cifrado = path_cifrado
        self.cant_bytes_originales = cant_bytes_originales

    def get_datos(self):
        """
        Lee y descifra los datos almacenados en el archivo cifrado.
        """
        try:
            with open(f"{self.path_cifrado}/{self.nombre}", "r") as f:
                contenido = f.read()
            return self._descifrar(contenido)
        except FileNotFoundError:
            return ""

    def _cifrar(self, datos):
        """
        Aplica un cifrado simple (Caesar +1) a los datos.
        """
        return "".join(chr(ord(c) + 1) for c in datos)

    def _descifrar(self, datos):
        """
        Descifra los datos previamente cifrados.
        """
        return "".join(chr(ord(c) - 1) for c in datos)

    def save_cifrado(self, nombre, path_original, datos):
        """
        Cifra los datos y los guarda en la ruta de archivo cifrada.
        """
        datos_cifrados = self._cifrar(datos)
        with open(f"{self.path_cifrado}/{nombre}", "w") as f:
            f.write(datos_cifrados)
        print(f"[Cifrado] Datos cifrados guardados en {self.path_cifrado}/{nombre}")

    def save(self, datos):
        """
        Implementa la interfaz estándar usando el método save_cifrado.
        """
        self.save_cifrado(self.nombre, self.path_original, datos)
