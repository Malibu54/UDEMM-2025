from abc import ABC, abstractmethod

class EstadoProducto(ABC):
    @abstractmethod
    def get_costo(self, precio: float) -> float:
        pass

    @abstractmethod
    def nombre(self) -> str:
        pass


class Fabricacion(EstadoProducto):
    def get_costo(self, precio: float) -> float:
        return 0.0

    def nombre(self) -> str:
        return "fabricacion"

class Ready(EstadoProducto):
    def get_costo(self, precio: float) -> float:
        return precio

    def nombre(self) -> str:
        return "ready"

class EstadoContenedor(ABC):
    @abstractmethod
    def acepta_productos(self) -> bool:
        pass

    @abstractmethod
    def es_activo(self) -> bool:
        pass

    @abstractmethod
    def nombre(self) -> str:
        pass


class Almacenaje(EstadoContenedor):
    def acepta_productos(self) -> bool: return True
    def es_activo(self) -> bool: return False
    def nombre(self) -> str: return "almacenaje"


class Viaje(EstadoContenedor):
    def acepta_productos(self) -> bool: return False
    def es_activo(self) -> bool: return True
    def nombre(self) -> str: return "viaje"


class Vacio(EstadoContenedor):
    def acepta_productos(self) -> bool: return False
    def es_activo(self) -> bool: return False
    def nombre(self) -> str: return "vacio"


class Lleno(EstadoContenedor):
    def acepta_productos(self) -> bool: return False
    def es_activo(self) -> bool: return False
    def nombre(self) -> str: return "lleno"


class Reparacion(EstadoContenedor):
    def acepta_productos(self) -> bool: return False
    def es_activo(self) -> bool: return False
    def nombre(self) -> str: return "reparacion"


class Destino(EstadoContenedor):
    def acepta_productos(self) -> bool: return False
    def es_activo(self) -> bool: return True
    def nombre(self) -> str: return "destino"

class Producto:
    def __init__(self, nombre: str, peso: float, tipo: str, costo: float):
        self._nombre = nombre
        self._peso = peso
        self._tipo = tipo
        self._costo = costo
        self._estado: EstadoProducto = Fabricacion()

    def setEstado(self, estado: EstadoProducto):
        self._estado = estado

    def get_costo(self) -> float:
        return self._estado.get_costo(self._costo)

    def get_info(self) -> dict:
        return {
            "nombre": self._nombre,
            "peso": self._peso,
            "tipo": self._tipo,
            "estado": self._estado.nombre(),
            "costo": self.get_costo(),
        }

class Contenedor:
    def __init__(self, peso: float, porcentaje_costo: float, cantidad_max: int):
        self._peso = peso
        self._porcentaje_costo = porcentaje_costo
        self._cantidad_max = cantidad_max
        self._productos: list[Producto] = []
        self._estado: EstadoContenedor = Vacio()

    def setEstado(self, estado: EstadoContenedor):
        self._estado = estado

    def add(self, producto: Producto):
        # Solo acepta productos en modo Almacenaje
        if not self._estado.acepta_productos():
            return
        if producto is self:
            return
        if len(self._productos) < self._cantidad_max:
            self._productos.append(producto)

    def get_productos(self) -> int:
        return len(self._productos)

    def get_costo(self) -> float:
        if not self._estado.es_activo():
            return 0.0
        costo_productos = sum(p.get_costo() for p in self._productos)
        return self._porcentaje_costo + costo_productos

    def get_info(self) -> dict:
        return {
            "cantidad_productos": self.get_productos(),
            "estado": self._estado.nombre(),
            "peso": self._peso,
            "porcentaje_costo": self._porcentaje_costo,
        }

class Gestion:
    def __init__(self):
        self._contenedores: list[Contenedor] = []

    def addContenedor(self, contenedor: Contenedor):
        self._contenedores.append(contenedor)

    def get_container(self) -> int | Contenedor:

        if len(self._contenedores) == 1:
            return self._contenedores[0]
        return len(self._contenedores)

    def get_costo_total(self) -> float:
        return sum(c.get_costo() for c in self._contenedores)


class Problema4:
    pass


#Test

from src.app import (Producto, Contenedor, Gestion,Fabricacion, Ready, Almacenaje, Viaje,Destino)

def test_check_producto_contenedor():
    e1 = Gestion()

    p1 = Producto("A", 100, "T1", 100)
    p2 = Producto("B", 102, "T1", 3300)
    p3 = Producto("C", 302, "T1", 200)

    p1.setEstado(Fabricacion())
    p2.setEstado(Fabricacion())
    p3.setEstado(Fabricacion())

    assert p1.get_costo() == 0
    assert p2.get_costo() == 0
    assert p3.get_costo() == 0

    c1 = Contenedor(1000, 0.75, 100)

    p1.setEstado(Ready())
    p2.setEstado(Ready())
    p3.setEstado(Ready())

    assert p1.get_costo() == 100
    assert p2.get_costo() == 3300
    assert p3.get_costo() == 200

    c1.setEstado(Almacenaje())
    c1.add(p1)
    c1.add(p2)
    c1.add(p3)
    c1.add(c1)                          

    c1.setEstado(Viaje())
    c1.add(Producto("D", 100, "Z1", 1111))  
    assert c1.get_productos() == 3

    e1.addContenedor(c1)               
    assert e1.get_container() == c1  

    c1.setEstado(Destino())

    assert c1.get_productos() == 3
    assert e1.get_costo_total() == (0.75 + (100 + 3300 + 200))