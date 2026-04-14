from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
import textwrap


# ──────────────────────────────────────────────────────────────────────────────
# Dominio
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class Producto:
    nombre: str
    precio: float
    categoria: str          
    stock: int = 5

    def __str__(self) -> str:
        return f"{self.nombre} (${self.precio:.2f}) [{self.categoria}]"


class OperacionNoPermitidaError(Exception):
    ...


# ──────────────────────────────────────────────────────────────────────────────
# Contrato abstracto: EstadoBase
# ──────────────────────────────────────────────────────────────────────────────

class EstadoBase(ABC):


    def __init__(self, maquina: "VendingMachine") -> None:
        self._maquina = maquina

    # ── Operaciones que cada estado implementa según corresponda ──────────────

    def insertar_dinero(self, monto: float) -> None:
        raise OperacionNoPermitidaError(
            f"[{self.__class__.__name__}] No se puede insertar dinero en este estado."
        )

    def seleccionar_producto(self, codigo: str) -> None:
        raise OperacionNoPermitidaError(
            f"[{self.__class__.__name__}] No se puede seleccionar producto en este estado."
        )

    def confirmar(self) -> None:
        raise OperacionNoPermitidaError(
            f"[{self.__class__.__name__}] No se puede confirmar en este estado."
        )

    def cancelar(self) -> None:
        raise OperacionNoPermitidaError(
            f"[{self.__class__.__name__}] No se puede cancelar en este estado."
        )

    def manejar_error(self, mensaje: str) -> None:
        """Transición al estado de error. Disponible desde cualquier estado."""
        print(f"  ⚠  ERROR detectado: {mensaje}")
        self._maquina.cambiar_estado(ErrorState(self._maquina, mensaje))

    @property
    def nombre(self) -> str:
        return self.__class__.__name__.replace("State", "")

    def __str__(self) -> str:
        return self.nombre


# ──────────────────────────────────────────────────────────────────────────────
# Contexto: VendingMachine
# ──────────────────────────────────────────────────────────────────────────────

class VendingMachine:

    def __init__(self, nombre: str = "BioMenu") -> None:
        self.nombre = nombre
        self._saldo: float = 0.0
        self._seleccion: Optional[Producto] = None
        self._ventas: list[str] = []
        self._inventario: dict[str, Producto] = {}

        # El estado inicial siempre es SinDinero
        self._estado: EstadoBase = SinDineroState(self)
        self._cargar_menu_demo()
        self._banner()

    # ── Menú de demostración ──────────────────────────────────────────────────

    def _cargar_menu_demo(self) -> None:
        productos = [
            # Almuerzos saludables
            Producto("Bowl de quinoa y verduras", 8.50,  "almuerzo"),
            Producto("Wrap de pollo y palta",     7.90,  "almuerzo"),
            Producto("Ensalada mediterránea",     6.50,  "almuerzo"),
            # Snacks saludables
            Producto("Mix de frutos secos",       3.20,  "snack"),
            Producto("Yogur griego con granola",  4.00,  "snack"),
            Producto("Banana deshidratada",       2.50,  "snack"),
            Producto("Barra de dátiles y cacao",  3.00,  "snack"),
            # Bebidas saludables
            Producto("Jugo verde detox",          4.50,  "bebida"),
            Producto("Agua de coco",              3.50,  "bebida"),
            Producto("Café de especialidad",      2.80,  "bebida"),
            Producto("Kombucha de jengibre",      3.90,  "bebida"),
        ]
        for idx, p in enumerate(productos, start=1):
            self._inventario[f"A{idx:02d}"] = p

    def _banner(self) -> None:
        print("=" * 60)
        print(f"  🥗  {self.nombre} — Alimentación sana en tu oficina")
        print("=" * 60)
        self._mostrar_estado()

    # ── API pública (delega al estado) ────────────────────────────────────────

    def insertar_dinero(self, monto: float) -> None:
        print(f"\n[ACCIÓN] Insertar dinero: ${monto:.2f}")
        self._estado.insertar_dinero(monto)

    def seleccionar_producto(self, codigo: str) -> None:
        print(f"\n[ACCIÓN] Seleccionar producto: {codigo}")
        self._estado.seleccionar_producto(codigo)

    def confirmar(self) -> None:
        print("\n[ACCIÓN] Confirmar compra")
        self._estado.confirmar()

    def cancelar(self) -> None:
        print("\n[ACCIÓN] Cancelar operación")
        self._estado.cancelar()

    def mostrar_menu(self) -> None:
        print("\n── Menú BioMenu ──")
        for codigo, p in self._inventario.items():
            disponible = "✓" if p.stock > 0 else "✗"
            print(f"  {disponible} [{codigo}] {p}")

    # ── Gestión de estado (usada por los estados concretos) ───────────────────

    def cambiar_estado(self, nuevo: EstadoBase) -> None:
        print(f"  → Transición: {self._estado.nombre}  →  {nuevo.nombre}")
        self._estado = nuevo
        self._mostrar_estado()

    def _mostrar_estado(self) -> None:
        print(f"  Estado actual : {self._estado.nombre}")
        print(f"  Saldo         : ${self._saldo:.2f}")

    # ── Accesores para los estados ────────────────────────────────────────────

    @property
    def saldo(self) -> float:
        return self._saldo

    @saldo.setter
    def saldo(self, valor: float) -> None:
        self._saldo = max(0.0, valor)

    @property
    def seleccion(self) -> Optional[Producto]:
        return self._seleccion

    @seleccion.setter
    def seleccion(self, producto: Optional[Producto]) -> None:
        self._seleccion = producto

    def buscar_producto(self, codigo: str) -> Optional[Producto]:
        return self._inventario.get(codigo.upper())

    def registrar_venta(self, descripcion: str) -> None:
        self._ventas.append(descripcion)

    def reporte_ventas(self) -> None:
        print("\n── Reporte de ventas ──")
        if not self._ventas:
            print("  Sin ventas registradas.")
            return
        for v in self._ventas:
            print(f"  • {v}")
        print(f"  Total transacciones: {len(self._ventas)}")


# ──────────────────────────────────────────────────────────────────────────────
# Estado 1: SinDineroState
# ──────────────────────────────────────────────────────────────────────────────

class SinDineroState(EstadoBase):

    def insertar_dinero(self, monto: float) -> None:
        if monto <= 0:
            self.manejar_error(f"Monto inválido: ${monto:.2f}")
            return
        self._maquina.saldo += monto
        print(f"  ✓  ${monto:.2f} aceptados. Saldo: ${self._maquina.saldo:.2f}")
        self._maquina.cambiar_estado(DineroInsertadoState(self._maquina))


# ──────────────────────────────────────────────────────────────────────────────
# Estado 2: DineroInsertadoState
# ──────────────────────────────────────────────────────────────────────────────

class DineroInsertadoState(EstadoBase):


    def insertar_dinero(self, monto: float) -> None:
        if monto <= 0:
            self.manejar_error(f"Monto inválido: ${monto:.2f}")
            return
        self._maquina.saldo += monto
        print(f"  ✓  ${monto:.2f} agregados. Saldo total: ${self._maquina.saldo:.2f}")

    def seleccionar_producto(self, codigo: str) -> None:
        producto = self._maquina.buscar_producto(codigo)
        if producto is None:
            print(f"  ✗  Código '{codigo}' no existe.")
            return
        if producto.stock == 0:
            print(f"  ✗  '{producto.nombre}' sin stock.")
            return
        self._maquina.seleccion = producto
        print(f"  ✓  Seleccionado: {producto.nombre}")
        self._maquina.cambiar_estado(SeleccionandoProductoState(self._maquina))

    def cancelar(self) -> None:
        devolucion = self._maquina.saldo
        self._maquina.saldo = 0
        print(f"  ✓  Operación cancelada. Devolviendo ${devolucion:.2f}")
        self._maquina.cambiar_estado(SinDineroState(self._maquina))


# ──────────────────────────────────────────────────────────────────────────────
# Estado 3: SeleccionandoProductoState
# ──────────────────────────────────────────────────────────────────────────────

class SeleccionandoProductoState(EstadoBase):


    def confirmar(self) -> None:
        producto = self._maquina.seleccion
        if producto is None:
            self.manejar_error("Confirmación sin producto seleccionado.")
            return
        if self._maquina.saldo < producto.precio:
            faltante = producto.precio - self._maquina.saldo
            print(f"  ✗  Saldo insuficiente. Faltan ${faltante:.2f}.")
            print("     Puede insertar más dinero o cancelar.")
            self._maquina.cambiar_estado(DineroInsertadoState(self._maquina))
            return
        entregando = EntregandoProductoState(self._maquina)
        self._maquina.cambiar_estado(entregando)
        entregando.dispensar()

    def cancelar(self) -> None:
        print(f"  ✓  Selección cancelada. Volviendo con saldo ${self._maquina.saldo:.2f}.")
        self._maquina.seleccion = None
        self._maquina.cambiar_estado(DineroInsertadoState(self._maquina))


# ──────────────────────────────────────────────────────────────────────────────
# Estado 4: EntregandoProductoState
# ──────────────────────────────────────────────────────────────────────────────

class EntregandoProductoState(EstadoBase):

    def dispensar(self) -> None:
        producto = self._maquina.seleccion
        if producto is None:
            self.manejar_error("Sin producto al intentar dispensar.")
            return

        # Simular posible fallo de hardware (descomentar para probar)
        # raise RuntimeError("Fallo en motor dispensador")

        try:
            vuelto = self._maquina.saldo - producto.precio
            self._maquina.saldo = 0
            producto.stock -= 1

            print(f"\n  🎉  ¡Aquí está tu {producto.nombre}!")
            print(f"  💰  Vuelto: ${vuelto:.2f}")

            self._maquina.registrar_venta(
                f"{producto.nombre} — ${producto.precio:.2f}"
            )
            self._maquina.seleccion = None
            self._maquina.cambiar_estado(SinDineroState(self._maquina))

        except Exception as exc:
            self.manejar_error(f"Fallo al dispensar: {exc}")


# ──────────────────────────────────────────────────────────────────────────────
# Estado 5: ErrorState
# ──────────────────────────────────────────────────────────────────────────────

class ErrorState(EstadoBase):


    def __init__(self, maquina: VendingMachine, mensaje: str) -> None:
        super().__init__(maquina)
        self._mensaje = mensaje
        print(f"\n  🔴  MÁQUINA EN ERROR: {mensaje}")
        print("      Llame a soporte técnico o presione RESET.")

    def insertar_dinero(self, monto: float) -> None:
        print("  ✗  Máquina fuera de servicio. No se aceptan pagos.")

    def seleccionar_producto(self, codigo: str) -> None:
        print("  ✗  Máquina fuera de servicio.")

    def confirmar(self) -> None:
        print("  ✗  Máquina fuera de servicio.")

    def cancelar(self) -> None:
        """Devuelve el saldo y reinicia."""
        self._reset()

    def reset(self) -> None:
        """Restablece la máquina desde código (ej. técnico remoto)."""
        self._reset()

    def _reset(self) -> None:
        if self._maquina.saldo > 0:
            print(f"  ✓  Devolviendo saldo: ${self._maquina.saldo:.2f}")
            self._maquina.saldo = 0
        self._maquina.seleccion = None
        print("  ✓  Máquina reiniciada. Volviendo a estado seguro.")
        self._maquina.cambiar_estado(SinDineroState(self._maquina))


# ──────────────────────────────────────────────────────────────────────────────
# Escenarios de demostración
# ──────────────────────────────────────────────────────────────────────────────

def separador(titulo: str) -> None:
    print(f"\n{'─'*60}")
    print(f"  ESCENARIO: {titulo}")
    print('─'*60)


def demo_compra_exitosa() -> None:
    separador("Compra exitosa — almuerzo completo")
    maquina = VendingMachine()
    maquina.mostrar_menu()
    maquina.insertar_dinero(10.00)
    maquina.seleccionar_producto("A01")   # Bowl de quinoa $8.50
    maquina.confirmar()
    maquina.reporte_ventas()


def demo_armar_menu() -> None:
    separador("Armar menú — snack + bebida (dos transacciones)")
    maquina = VendingMachine()
    # Compra 1: snack
    maquina.insertar_dinero(5.00)
    maquina.seleccionar_producto("A04")   # Mix de frutos secos $3.20
    maquina.confirmar()
    # Compra 2: bebida
    maquina.insertar_dinero(5.00)
    maquina.seleccionar_producto("A08")   # Jugo verde detox $4.50
    maquina.confirmar()
    maquina.reporte_ventas()


def demo_cancelacion() -> None:
    separador("Cancelación con devolución")
    maquina = VendingMachine()
    maquina.insertar_dinero(8.00)
    maquina.seleccionar_producto("A02")   # Wrap $7.90
    maquina.cancelar()                    # Vuelve a DineroInsertado
    maquina.cancelar()                    # Devuelve el dinero → SinDinero


def demo_saldo_insuficiente() -> None:
    separador("Saldo insuficiente → agregar dinero → confirmar")
    maquina = VendingMachine()
    maquina.insertar_dinero(3.00)         # Bowl cuesta $8.50
    maquina.seleccionar_producto("A01")
    maquina.confirmar()                   # Detecta faltante, vuelve a DineroInsertado
    maquina.insertar_dinero(6.00)         # Ahora sí alcanza
    maquina.seleccionar_producto("A01")
    maquina.confirmar()


def demo_condicion_error() -> None:
    separador("Condición de error y recuperación (RESET)")
    maquina = VendingMachine()
    maquina.insertar_dinero(10.00)
    # Simulamos un error de hardware
    maquina._estado.manejar_error("Sensor de temperatura fuera de rango")
    # Intentos bloqueados
    maquina.insertar_dinero(5.00)
    maquina.seleccionar_producto("A08")
    # Técnico presiona RESET
    if isinstance(maquina._estado, ErrorState):
        maquina._estado.reset()
    # Máquina vuelve a funcionar
    maquina.insertar_dinero(4.00)
    maquina.seleccionar_producto("A10")   # Café $2.80
    maquina.confirmar()


def demo_accion_invalida() -> None:
    separador("Acción inválida en estado incorrecto (OperacionNoPermitidaError)")
    maquina = VendingMachine()
    try:
        maquina.confirmar()               # Sin dinero ni selección
    except OperacionNoPermitidaError as e:
        print(f"  ✗  Error capturado correctamente: {e}")
    try:
        maquina.seleccionar_producto("A01")  # Sin dinero
    except OperacionNoPermitidaError as e:
        print(f"  ✗  Error capturado correctamente: {e}")


# ──────────────────────────────────────────────────────────────────────────────
# Punto de entrada
# ──────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    demo_compra_exitosa()
    demo_armar_menu()
    demo_cancelacion()
    demo_saldo_insuficiente()
    demo_condicion_error()
    demo_accion_invalida()