from abc import ABC, abstractmethod

VARIANTES = {"A": 0.10, "C": 0.25, "D": 0.35, "E": 0.45}

def _aplicar_variantes(base: float, *codigos: str) -> float:
    """Suma al base el porcentaje de cada variante solicitada."""
    total = base
    for codigo in codigos:
        total += base * VARIANTES.get(codigo, 0)
    return total

class CategoriaBase(ABC):
    @abstractmethod
    def calcular(self) -> float:
        pass


class Estudiante(CategoriaBase):
    BONUS = 0.15

    def __init__(self, base: float, *variantes: str):
        self._base = base
        self._variantes = variantes

    def calcular(self) -> float:
        subtotal = _aplicar_variantes(self._base, *self._variantes)
        return subtotal + subtotal * self.BONUS


class Administrativo(CategoriaBase):
    def __init__(self, base: float, *variantes: str):
        self._base = base
        self._variantes = variantes

    def calcular(self) -> float:
        return _aplicar_variantes(self._base, *self._variantes)


class Especial(CategoriaBase):
    def __init__(self):
        self._categorias: list[CategoriaBase] = []

    def add(self, categoria: CategoriaBase):
        self._categorias.append(categoria)

    def calcular(self) -> float:
        return sum(c.calcular() for c in self._categorias)


class Empleado:
    def __init__(self):
        self.categoria: CategoriaBase | None = None

    def liquidar(self) -> float:
        if self.categoria is None:
            return 0.0
        return self.categoria.calcular()


class Gestion:
    def __init__(self):
        self._empleados: list[Empleado] = []

    def addEmpleado(self, empleado: Empleado):
        self._empleados.append(empleado)

    def getEmpleados(self) -> int:
        return len(self._empleados)

    def liquidar(self) -> float:
        return sum(e.liquidar() for e in self._empleados)


class Problema3:
    pass


#Test

from src.app import Problema3, Empleado, Estudiante, Administrativo, Especial, Gestion

def test_check_calculo_base():
    e1 = Empleado()
    e1.categoria = Estudiante(800, "A", "B")   
    e2.categoria = Administrativo(1500, "A", "B", "C", "D")

    s1 = Gestion()
    s1.addEmpleado(e1)
    s1.addEmpleado(e2)

    assert s1.getEmpleados() == 2
    assert s1.liquidar() > 0

def test_check_calculo_base_extra():
    e1 = Empleado()
    e1.categoria = Estudiante(800, "A", "B")

    e2 = Empleado()
    e2.categoria = Administrativo(1500, "A", "B", "C", "D")

    e3 = Empleado()
    e3.categoria = Especial()
    e3.categoria.add(Estudiante(200, "A", "B"))
    e3.categoria.add(Administrativo(100, "A", "B", "C", "D"))

    s1 = Gestion()
    s1.addEmpleado(e1)
    s1.addEmpleado(e2)
    s1.addEmpleado(e3)

    assert s1.getEmpleados() == 3
    assert s1.liquidar() > 0