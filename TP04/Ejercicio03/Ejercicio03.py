# ---------------------------------------------------------------------------
# IMPORTACIÓN DE FUNCIONES PROVISTAS POR EL SISTEMA DE LA EMPRESA
# ---------------------------------------------------------------------------
# Estas funciones provienen del módulo interno `agencia.pedidos` y son esenciales
# para operar con los pedidos de la empresa. No se permite el uso de otras librerías
# externas más allá de las estándar o provistas específicamente.

from agencia.pedidos import (
    get_pedidos,       # Función que retorna la lista completa de registros (pedidos).
    next,              # Función que devuelve el siguiente registro a procesar; retorna False si ya no hay más.
    get_type,          # Función que clasifica el registro en uno de los tipos (entrega, calidad, auditoría, o NN).
    send_for_process   # Función que envía un registro para su procesamiento (operación bloqueante).
)

# ---------------------------------------------------------------------------
# LIBRERÍAS ESTÁNDAR PERMITIDAS
# ---------------------------------------------------------------------------

from abc import ABC, abstractmethod      # Para definir clases base abstractas
from datetime import datetime            # Para registrar la fecha/hora en bitácoras
import os                                # Para operaciones de archivo (si se requiriera)
import json                              # Para serializar registros a texto (bitácoras)

# ---------------------------------------------------------------------------
# CLASES DE PROCESAMIENTO
# ---------------------------------------------------------------------------

class Procesador(ABC):
    """
    Clase base abstracta que define la interfaz para todos los tipos de procesamiento.
    Cada clase hija debe implementar los métodos name() y preparar_registro().
    """

    def __init__(self):
        self._total = 0  # Contador de registros procesados
        self._nombre = self.name()
        self._bitacora_path = f"bitacora_{self._nombre}.log"  # Archivo de bitácora

    @abstractmethod
    def name(self):
        """
        Retorna el nombre del tipo de procesamiento.
        """
        pass

    def total_process(self):
        """
        Retorna la cantidad total de registros procesados.
        """
        return self._total

    @abstractmethod
    def preparar_registro(self, registro):
        """
        Prepara el contenido del registro según el tipo de procesamiento.
        Debe ser implementado por cada subclase.
        """
        pass

    def send_for_process(self, registro):
        """
        Prepara el registro, lo envía al sistema y guarda una bitácora del mismo.
        """
        datos = self.preparar_registro(registro)
        datos["type"] = self.name()  # Agrega tipo al registro
        send_for_process(datos)
        self._total += 1
        self._guardar_bitacora(datos)

    def _guardar_bitacora(self, datos):
        """
        Guarda el registro procesado con la fecha actual en un archivo de bitácora.
        """
        with open(self._bitacora_path, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "fecha": datetime.now().isoformat(),
                "registro": datos
            }) + "\n")


class ProcesadorEntrega(Procesador):
    """
    Procesador específico para entregas.
    """

    def name(self):
        return "entrega"

    def preparar_registro(self, registro):
        """
        Extrae los campos necesarios para procesar una entrega.
        """
        return {
            "fecha": registro["fecha"],
            "payload_entrega": registro["payload entrega"],
            "codigo_producto": registro["código de producto"],
            "usuario": registro["usuario"]
        }


class ProcesadorCalidad(Procesador):
    """
    Procesador específico para control de calidad.
    """

    def name(self):
        return "control de calidad"

    def preparar_registro(self, registro):
        """
        Extrae los campos necesarios para procesar control de calidad.
        """
        return {
            "producto": registro["producto"],
            "fecha": registro["fecha"],
            "local": registro["local"],
            "categoria": registro["categoría"]
        }


class ProcesadorAuditoria(Procesador):
    """
    Procesador específico para auditorías.
    """

    def name(self):
        return "auditoria"

    def preparar_registro(self, registro):
        """
        Extrae los campos necesarios para procesar auditoría.
        """
        return {
            "fecha": registro["fecha"],
            "payload_auditoria": registro["payload auditoría"],
            "id_usuario": registro["id usuario"],
            "departamento": registro["departamento"]
        }


class ProcesadorNN(Procesador):
    """
    Procesador para registros sin tipo reconocido ("NN").
    Se envía el contenido completo del registro.
    """

    def name(self):
        return "NN"

    def preparar_registro(self, registro):
        """
        Devuelve el registro completo sin transformación.
        """
        return registro


# ---------------------------------------------------------------------------
# PROCESADOR CENTRAL DE ORQUESTACIÓN
# ---------------------------------------------------------------------------

class ProcesadorCentral:
    """
    Clase central que coordina el procesamiento de todos los registros.
    Mantiene instancias de cada procesador y realiza una única pasada por los datos.
    """

    def __init__(self):
        # Mapa de tipos conocidos a sus respectivos procesadores
        self.procesadores = {
            0: ProcesadorEntrega(),
            1: ProcesadorCalidad(),
            2: ProcesadorAuditoria()
        }
        # Procesador por defecto para tipos no reconocidos
        self.procesador_nn = ProcesadorNN()

    def procesar_todos(self):
        """
        Procesa todos los registros obtenidos, redirigiéndolos al procesador correspondiente.
        Solo realiza una pasada por los datos.
        """
        registros = get_pedidos()
        while True:
            registro = next(registros)
            if not registro:
                break

            tipo = get_type(registro)
            procesador = self.procesadores.get(tipo, self.procesador_nn)
            procesador.send_for_process(registro)

    def resumen(self):
        """
        Devuelve un resumen con la cantidad procesada por cada tipo y el total.
        """
        resumen = {
            "entrega": self.procesadores[0].total_process(),
            "control de calidad": self.procesadores[1].total_process(),
            "auditoria": self.procesadores[2].total_process(),
            "total": sum(p.total_process() for p in self.procesadores.values())
        }
        return resumen


# ---------------------------------------------------------------------------
# PUNTO DE ENTRADA PRINCIPAL
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    central = ProcesadorCentral()
    central.procesar_todos()
    resultados = central.resumen()

    # Muestra de resumen final
    print("Resumen de procesamiento:")
    print(f"Entregas procesadas: {resultados['entrega']}")
    print(f"Control de calidad procesadas: {resultados['control de calidad']}")
    print(f"Auditorías procesadas: {resultados['auditoria']}")
    print(f"Total de registros procesados: {resultados['total']}")
