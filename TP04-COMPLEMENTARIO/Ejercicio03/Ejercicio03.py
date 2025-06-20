from abc import ABC, abstractmethod

# ======================
# Clase base abstracta
# ======================
class Empleado(ABC):
    """
    Clase abstracta que representa un empleado genérico.
    """
    def __init__(self, id, nombre, cuil, direccion, salario_basico):
        """
        Inicializa los atributos comunes de todos los empleados.
        """
        self.id = id
        self.nombre = nombre
        self.cuil = cuil
        self.direccion = direccion
        self.salario_basico = salario_basico

    @abstractmethod
    def calcular_pago(self):
        """
        Método abstracto para calcular el pago. 
        Debe ser implementado por las subclases.
        """
        pass


# ======================
# Empleado Operario
# ======================
class Operario(Empleado):
    """
    Representa a un empleado del tipo operario.
    """
    def __init__(self, id, nombre, cuil, direccion, salario_basico, horas):
        super().__init__(id, nombre, cuil, direccion, salario_basico)
        self.horas = horas

    def calcular_pago(self):
        """
        Calcula el pago para un operario:
        salario_basico * 24 + 250000
        """
        return self.salario_basico * 24 + 250000


# ======================
# Empleado Administrador
# ======================
class Administrador(Empleado):
    """
    Representa a un administrador.
    """
    def __init__(self, id, nombre, cuil, direccion, salario_basico, plus, subordinados):
        super().__init__(id, nombre, cuil, direccion, salario_basico)
        self.plus = plus
        self.subordinados = subordinados  # Lista de empleados administrativos

    def calcular_pago(self):
        """
        Calcula el pago para un administrador:
        salario_basico + plus + 805500
        """
        return self.salario_basico + self.plus + 805500


# ======================
# Empleado Administrativo
# ======================
class Administrativo(Empleado):
    """
    Representa a un empleado administrativo.
    """
    def __init__(self, id, nombre, cuil, direccion, salario_basico, jefe, sucursal, horas):
        super().__init__(id, nombre, cuil, direccion, salario_basico)
        self.jefe = jefe
        self.sucursal = sucursal
        self.horas = horas

    def calcular_pago(self):
        """
        Calcula el pago para un administrativo:
        salario_basico * horas + 1500
        """
        return self.salario_basico * self.horas + 1500


# ======================
# Obra Social
# ======================
class ObraSocial:
    """
    Representa una obra social que puede tener convenio.
    """
    def __init__(self, id, fecha, nombre, valor, sucursal, con_convenio):
        self.id = id
        self.fecha = fecha
        self.nombre = nombre
        self.valor = valor
        self.sucursal = sucursal
        self.con_convenio = con_convenio

    def get_precio(self):
        """
        Devuelve el precio de la obra social.
        Si tiene convenio, se aplica un descuento del 35%.
        """
        if self.con_convenio:
            return self.valor * 0.65
        return self.valor


# ======================
# Base Empleados Foráneos
# ======================
class EmpleadoForaneo(Empleado):
    """
    Clase base para empleados foráneos.
    """
    def __init__(self, id, nombre, cuil, direccion, salario_basico,
                 fecha_inicio, fecha_fin, horas, certificaciones, obra_social):
        super().__init__(id, nombre, cuil, direccion, salario_basico)
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.horas = horas
        self.certificaciones = certificaciones  # Lista de certificaciones
        self.obra_social = obra_social


# ======================
# Contrato Fijo
# ======================
class EmpleadoContratoFijo(EmpleadoForaneo):
    """
    Empleado foráneo con contrato fijo.
    """
    def __init__(self, id, nombre, cuil, direccion, salario_basico,
                 fecha_inicio, fecha_fin, horas, certificaciones,
                 grado_estudio, obra_social):
        super().__init__(id, nombre, cuil, direccion, salario_basico,
                         fecha_inicio, fecha_fin, horas, certificaciones,
                         obra_social)
        self.grado_estudio = grado_estudio

    def calcular_pago(self):
        """
        Cálculo de pago:
        salario_basico + obra_social.get_precio() + 900000 + 
        (certificaciones * 800) + 250000 si tiene grado_estudio
        """
        pago = self.salario_basico + self.obra_social.get_precio() + 900000 + len(self.certificaciones) * 800
        if self.grado_estudio:
            pago += 250000
        return pago


# ======================
# Contrato Temporal
# ======================
class EmpleadoContratoTemporal(EmpleadoForaneo):
    """
    Empleado foráneo con contrato temporal.
    """
    def calcular_pago(self):
        """
        Cálculo de pago:
        salario_basico + obra_social.get_precio() + 50000 + 
        (certificaciones * 400)
        """
        return self.salario_basico + self.obra_social.get_precio() + 50000 + len(self.certificaciones) * 400
