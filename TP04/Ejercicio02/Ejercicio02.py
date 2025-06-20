from abc import ABC, abstractmethod

# ------------------------------------------------------------------------------
# IMPORTANTE:
# La siguiente línea importa dos funciones desde un módulo interno provisto
# por la empresa (NO es una librería estándar de Python).
#
# Este módulo simula o accede a los datos de los paquetes de red recibidos.
#
# Funciones disponibles:
# - get_paquetes() => retorna una lista con todos los paquetes del día.
# - next(lista)    => recibe esa lista y devuelve el siguiente paquete.
#                     Si no hay más, retorna False.
#
# Ejemplo conceptual de los datos retornados por get_paquetes():
# [
#   (1, "192.168.0.1", "2025-06-18", 10, 5),
#   (2, "192.168.0.2", "2025-06-18", 8, 7),
#   ...
# ]
#
# ¡NO modificar ni reemplazar estas funciones!
# ------------------------------------------------------------------------------

from net.network_payload import get_paquetes, next


class Paquete:
    """
    Representa un paquete de red con todos sus atributos relevantes.
    """
    def __init__(self, id_paquete, ip, fecha, frecuencia, duracion):
        self.id = id_paquete
        self.ip = ip
        self.fecha = fecha
        self.frecuencia = frecuencia
        self.duracion = duracion

    def __repr__(self):
        return (f"Paquete(id={self.id}, ip={self.ip}, fecha={self.fecha}, "
                f"frecuencia={self.frecuencia}, duracion={self.duracion})")


class BaseDatos:
    """
    Simula una base de datos en memoria para almacenar y consultar paquetes procesados.
    """
    def __init__(self):
        self.paquetes = []

    def agregar(self, paquete):
        """
        Agrega un paquete al almacenamiento.
        """
        self.paquetes.append(paquete)

    def buscar_por_ip(self, ip):
        """
        Retorna todos los paquetes con la IP especificada.
        """
        return [p for p in self.paquetes if p.ip == ip]

    def buscar_por_fecha(self, fecha):
        """
        Retorna todos los paquetes con la fecha especificada.
        """
        return [p for p in self.paquetes if p.fecha == fecha]

    def buscar_por_frecuencia(self, frecuencia):
        """
        Retorna todos los paquetes con la frecuencia de acceso especificada.
        """
        return [p for p in self.paquetes if p.frecuencia == frecuencia]


class Exportador(ABC):
    """
    Clase abstracta para definir la interfaz de exportación de reportes.
    """
    @abstractmethod
    def exportar(self, reporte):
        pass


class ExportadorConsola(Exportador):
    """
    Exportador que imprime el reporte por consola.
    """
    def exportar(self, reporte):
        print("Reporte generado:")
        for linea in reporte:
            print(linea)


class Reporte:
    """
    Contiene la información procesada del reporte y permite su exportación.
    """
    def __init__(self, base_datos, total_duracion, ip_mas_frecuentes, ip_menor_duracion):
        self.base_datos = base_datos
        self.total_duracion = total_duracion
        self.ip_mas_frecuentes = ip_mas_frecuentes
        self.ip_menor_duracion = ip_menor_duracion

    def imprimir_resumen(self):
        """
        Imprime un resumen con los principales resultados del reporte.
        """
        print("Resumen del Reporte:")
        print(f"- Total duración de todos los paquetes: {self.total_duracion}")
        print(f"- Top 2 IPs con más frecuencia de acceso: {self.ip_mas_frecuentes}")
        print(f"- IP con menor duración: {self.ip_menor_duracion}")

    def exportar(self, exportador):
        """
        Exporta los datos del reporte usando el exportador proporcionado.
        """
        reporte_data = []
        for paquete in self.base_datos.paquetes:
            reporte_data.append({
                'fecha': paquete.fecha,
                'ip': paquete.ip,
                'duracion': paquete.duracion,
                'frecuencia': paquete.frecuencia
            })
        exportador.exportar(reporte_data)


class Procesador:
    """
    Clase principal encargada de procesar los paquetes usando los datos provistos.
    Recorre los datos solo una vez, calcula estadísticas y guarda los paquetes.
    """
    def __init__(self):
        self.base_datos = BaseDatos()
        self.total_duracion = 0
        self.frecuencia_ips = {}
        self.duracion_ips = {}

    def procesar(self):
        """
        Ejecuta el procesamiento de los datos:
        - Recolecta todos los paquetes.
        - Calcula estadísticas necesarias.
        - Devuelve un objeto Reporte.
        """
        paquetes = get_paquetes()

        while True:
            registro = next(paquetes)
            if not registro:
                break

            paquete = Paquete(*registro)
            self.base_datos.agregar(paquete)
            self.total_duracion += paquete.duracion

            # Contabilizamos frecuencia por IP
            self.frecuencia_ips[paquete.ip] = self.frecuencia_ips.get(paquete.ip, 0) + paquete.frecuencia

            # Guardamos la menor duración por IP
            if paquete.ip not in self.duracion_ips or paquete.duracion < self.duracion_ips[paquete.ip]:
                self.duracion_ips[paquete.ip] = paquete.duracion

        # Seleccionamos las dos IPs con más frecuencia
        ip_mas_frecuentes = sorted(self.frecuencia_ips.items(), key=lambda x: x[1], reverse=True)[:2]

        # IP con menor duración acumulada
        ip_menor_duracion = min(self.duracion_ips.items(), key=lambda x: x[1])[0]

        return Reporte(
            base_datos=self.base_datos,
            total_duracion=self.total_duracion,
            ip_mas_frecuentes=ip_mas_frecuentes,
            ip_menor_duracion=ip_menor_duracion
        )
