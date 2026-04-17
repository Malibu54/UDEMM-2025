"""
Movilidad Urbana S.A
Sistema de Gestión de Estacionamiento
Persistencia: en memoria
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Optional
import uuid


# ─────────────────────────────────────────────
#  Enumeraciones
# ─────────────────────────────────────────────

class TipoEspacio(Enum):
    COMPACTO  = "Compacto"
    GRANDE    = "Grande"
    PMR       = "Movilidad reducida"
    MOTO      = "Moto"
    ELECTRICO = "Eléctrico"


class TipoVehiculo(Enum):
    AUTO      = "Auto"
    MOTO      = "Moto"
    CAMION    = "Camión"
    FURGONETA = "Furgoneta"
    OTRO      = "Otro"


class EstadoTicket(Enum):
    ACTIVO   = "Activo"
    PAGADO   = "Pagado"
    CANCELADO = "Cancelado"


class MetodoPago(Enum):
    EFECTIVO          = "Efectivo"
    TARJETA           = "Tarjeta"
    BILLETERA_VIRTUAL = "Billetera virtual"


class TipoPanel(Enum):
    ENTRADA = "Entrada"
    PISO    = "Piso"
    SALIDA  = "Salida"


# ─────────────────────────────────────────────
#  Cálculo de tarifas
# ─────────────────────────────────────────────

class CalculadoraTarifa:
    TARIFA_H1    = 6_000   # primera hora
    TARIFA_H2H3  = 5_500   # segunda y tercera hora (c/u)
    TARIFA_EXTRA = 1_750   # horas adicionales (c/u)
    TARIFA_KWH   = 150     # costo por kWh cargado

    @staticmethod
    def calcular(horas: float, kwh: float = 0.0) -> float:

        import math
        horas_enteras = max(1, math.ceil(horas))

        monto = 0.0
        for h in range(1, horas_enteras + 1):
            if h == 1:
                monto += CalculadoraTarifa.TARIFA_H1
            elif h <= 3:
                monto += CalculadoraTarifa.TARIFA_H2H3
            else:
                monto += CalculadoraTarifa.TARIFA_EXTRA

        monto += kwh * CalculadoraTarifa.TARIFA_KWH
        return monto


# ─────────────────────────────────────────────
#  Dominio: Panel
# ─────────────────────────────────────────────

@dataclass
class Panel:
    tipo: TipoPanel
    mensaje: str = ""

    def mostrar(self) -> str:
        return f"[Panel {self.tipo.value}] {self.mensaje}"


# ─────────────────────────────────────────────
#  Dominio: Espacio
# ─────────────────────────────────────────────

@dataclass
class Espacio:
    id_espacio: str
    tipo: TipoEspacio
    tiene_carga_electrica: bool = False
    disponible: bool = True
    _ticket_activo: Optional["Ticket"] = field(default=None, repr=False)

    def ocupar(self, ticket: "Ticket") -> None:
        if not self.disponible:
            raise ValueError(f"El espacio {self.id_espacio} ya está ocupado.")
        self.disponible = False
        self._ticket_activo = ticket

    def liberar(self) -> None:
        self.disponible = True
        self._ticket_activo = None

    def __str__(self) -> str:
        estado = "libre" if self.disponible else "ocupado"
        carga  = " + carga" if self.tiene_carga_electrica else ""
        return f"Espacio {self.id_espacio} [{self.tipo.value}{carga}] — {estado}"


# ─────────────────────────────────────────────
#  Dominio: Piso
# ─────────────────────────────────────────────

@dataclass
class Piso:
    numero: int
    descripcion: str = ""
    espacios: list[Espacio] = field(default_factory=list)
    panel: Panel = field(default_factory=lambda: Panel(TipoPanel.PISO))

    def agregar_espacio(self, espacio: Espacio) -> None:
        self.espacios.append(espacio)
        self._actualizar_panel()

    def disponibles_por_tipo(self) -> dict[TipoEspacio, int]:
        conteo: dict[TipoEspacio, int] = {t: 0 for t in TipoEspacio}
        for e in self.espacios:
            if e.disponible:
                conteo[e.tipo] += 1
        return conteo

    def buscar_espacio_disponible(self, tipo: TipoEspacio) -> Optional[Espacio]:
        for e in self.espacios:
            if e.tipo == tipo and e.disponible:
                return e
        return None

    def _actualizar_panel(self) -> None:
        partes = [
            f"{t.value}: {n}"
            for t, n in self.disponibles_por_tipo().items()
            if n > 0
        ]
        self.panel.mensaje = f"Piso {self.numero} — " + " | ".join(partes) if partes else f"Piso {self.numero} — SIN ESPACIOS"

    def __str__(self) -> str:
        self._actualizar_panel()
        return self.panel.mostrar()


# ─────────────────────────────────────────────
#  Dominio: Vehículo y subtipos
# ─────────────────────────────────────────────

@dataclass
class Vehiculo:
    patente: str
    tipo: TipoVehiculo
    es_electrico: bool = False
    kwh_cargados: float = 0.0

    def tipo_espacio_requerido(self) -> TipoEspacio:
        if self.es_electrico:
            return TipoEspacio.ELECTRICO
        mapping = {
            TipoVehiculo.MOTO:      TipoEspacio.MOTO,
            TipoVehiculo.CAMION:    TipoEspacio.GRANDE,
            TipoVehiculo.FURGONETA: TipoEspacio.GRANDE,
            TipoVehiculo.AUTO:      TipoEspacio.COMPACTO,
            TipoVehiculo.OTRO:      TipoEspacio.COMPACTO,
        }
        return mapping[self.tipo]

    def __str__(self) -> str:
        elec = " (eléctrico)" if self.es_electrico else ""
        return f"Vehículo {self.patente} [{self.tipo.value}{elec}]"


class Auto(Vehiculo):
    def __init__(self, patente: str, es_electrico: bool = False):
        super().__init__(patente, TipoVehiculo.AUTO, es_electrico)


class Moto(Vehiculo):
    def __init__(self, patente: str):
        super().__init__(patente, TipoVehiculo.MOTO)


class Camion(Vehiculo):
    def __init__(self, patente: str):
        super().__init__(patente, TipoVehiculo.CAMION)


class Furgoneta(Vehiculo):
    def __init__(self, patente: str):
        super().__init__(patente, TipoVehiculo.FURGONETA)


# ─────────────────────────────────────────────
#  Dominio: Pago
# ─────────────────────────────────────────────

@dataclass
class Pago:
    monto: float
    metodo: MetodoPago
    timestamp: datetime = field(default_factory=datetime.now)
    realizado_por: Optional[str] = None   # id del asistente si aplica

    def __str__(self) -> str:
        agente = f" (asistido por {self.realizado_por})" if self.realizado_por else ""
        return (
            f"Pago ${self.monto:,.0f} — {self.metodo.value}"
            f" — {self.timestamp:%H:%M:%S}{agente}"
        )


# ─────────────────────────────────────────────
#  Dominio: Ticket
# ─────────────────────────────────────────────

@dataclass
class Ticket:
    codigo: str = field(default_factory=lambda: str(uuid.uuid4())[:8].upper())
    vehiculo: Optional[Vehiculo] = None
    espacio: Optional[Espacio] = None
    fecha_hora_entrada: datetime = field(default_factory=datetime.now)
    fecha_hora_salida: Optional[datetime] = None
    estado: EstadoTicket = EstadoTicket.ACTIVO
    pago: Optional[Pago] = None
    kwh_consumidos: float = 0.0

    def horas_transcurridas(self) -> float:
        fin = self.fecha_hora_salida or datetime.now()
        delta = fin - self.fecha_hora_entrada
        return delta.total_seconds() / 3600

    def calcular_monto(self) -> float:
        return CalculadoraTarifa.calcular(self.horas_transcurridas(), self.kwh_consumidos)

    def cerrar(self, metodo: MetodoPago, realizado_por: Optional[str] = None) -> Pago:
        if self.estado != EstadoTicket.ACTIVO:
            raise ValueError("El ticket no está activo.")
        self.fecha_hora_salida = datetime.now()
        monto = self.calcular_monto()
        self.pago = Pago(monto, metodo, realizado_por=realizado_por)
        self.estado = EstadoTicket.PAGADO
        return self.pago

    def __str__(self) -> str:
        entrada = self.fecha_hora_entrada.strftime("%d/%m/%Y %H:%M")
        veh = str(self.vehiculo) if self.vehiculo else "—"
        esp = self.espacio.id_espacio if self.espacio else "—"
        return (
            f"Ticket {self.codigo} | {veh} | Espacio {esp} | "
            f"Entrada: {entrada} | Estado: {self.estado.value}"
        )


# ─────────────────────────────────────────────
#  Dominio: Usuarios
# ─────────────────────────────────────────────

@dataclass
class Usuario:
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:6].upper())
    nombre: str = ""
    activo: bool = True

    def __str__(self) -> str:
        return f"{self.__class__.__name__} {self.nombre} (id={self.id})"


class Administrador(Usuario):
    pass


class Asistente(Usuario):
    pass


# ─────────────────────────────────────────────
#  Dominio: Estacionamiento (raíz del agregado)
# ─────────────────────────────────────────────

@dataclass
class Estacionamiento:
    nombre: str
    capacidad_total: int
    pisos: list[Piso] = field(default_factory=list)
    _tickets: dict[str, Ticket] = field(default_factory=dict, repr=False)
    _usuarios: dict[str, Usuario] = field(default_factory=dict, repr=False)
    panel_entrada: Panel = field(default_factory=lambda: Panel(TipoPanel.ENTRADA))
    panel_salida:  Panel = field(default_factory=lambda: Panel(TipoPanel.SALIDA))

    # ── Propiedades ──────────────────────────

    @property
    def vehiculos_adentro(self) -> int:
        return sum(
            1 for t in self._tickets.values()
            if t.estado == EstadoTicket.ACTIVO
        )

    @property
    def esta_lleno(self) -> bool:
        return self.vehiculos_adentro >= self.capacidad_total

    # ── Administración de estructura ─────────

    def agregar_piso(self, numero: int, descripcion: str = "") -> Piso:
        if any(p.numero == numero for p in self.pisos):
            raise ValueError(f"Ya existe el piso {numero}.")
        piso = Piso(numero, descripcion)
        self.pisos.append(piso)
        self.pisos.sort(key=lambda p: p.numero)
        return piso

    def agregar_espacio(
        self,
        numero_piso: int,
        tipo: TipoEspacio,
        cantidad: int = 1,
        con_carga: bool = False,
    ) -> list[Espacio]:
        piso = self._piso_o_error(numero_piso)
        nuevos = []
        for _ in range(cantidad):
            idx = len(piso.espacios) + 1
            eid = f"P{numero_piso}-{tipo.name[:1]}{idx:03d}"
            esp = Espacio(eid, tipo, tiene_carga_electrica=con_carga or tipo == TipoEspacio.ELECTRICO)
            piso.agregar_espacio(esp)
            nuevos.append(esp)
        return nuevos

    # ── Gestión de personal ──────────────────

    def dar_alta_usuario(self, usuario: Usuario) -> None:
        self._usuarios[usuario.id] = usuario

    def dar_baja_usuario(self, id_usuario: str) -> None:
        u = self._usuarios.get(id_usuario)
        if not u:
            raise ValueError(f"Usuario {id_usuario} no encontrado.")
        u.activo = False

    def listar_personal(self) -> list[Usuario]:
        return [u for u in self._usuarios.values() if u.activo]

    # ── Flujo de ingreso ─────────────────────

    def ingresar_vehiculo(self, vehiculo: Vehiculo) -> Ticket:

        if self.esta_lleno:
            raise RuntimeError("Estacionamiento lleno. No se puede ingresar.")

        tipo_req = vehiculo.tipo_espacio_requerido()
        espacio  = self._buscar_espacio(tipo_req)
        if not espacio:
            raise RuntimeError(
                f"No hay espacios disponibles para el tipo {tipo_req.value}."
            )

        ticket = Ticket(vehiculo=vehiculo, espacio=espacio)
        espacio.ocupar(ticket)
        self._tickets[ticket.codigo] = ticket
        self._actualizar_panel_entrada()
        return ticket

    # ── Flujo de egreso ──────────────────────

    def egresar_vehiculo(
        self,
        codigo_ticket: str,
        metodo: MetodoPago,
        asistente_id: Optional[str] = None,
    ) -> Pago:

        ticket = self._ticket_activo_o_error(codigo_ticket)

        asistente = None
        if asistente_id:
            asistente = self._usuarios.get(asistente_id)
            if not asistente or not asistente.activo:
                raise ValueError(f"Asistente {asistente_id} no válido.")

        kwh = ticket.vehiculo.kwh_cargados if ticket.vehiculo else 0.0
        ticket.kwh_consumidos = kwh

        pago = ticket.cerrar(
            metodo,
            realizado_por=asistente.nombre if asistente else None,
        )

        if ticket.espacio:
            ticket.espacio.liberar()

        self._actualizar_panel_entrada()
        self._actualizar_panel_salida(ticket, pago)
        return pago

    # ── Paneles ──────────────────────────────

    def _actualizar_panel_entrada(self) -> None:
        if self.esta_lleno:
            self.panel_entrada.mensaje = "⛔ ESTACIONAMIENTO LLENO"
        else:
            libre = self.capacidad_total - self.vehiculos_adentro
            self.panel_entrada.mensaje = f"Espacios disponibles: {libre}/{self.capacidad_total}"

    def _actualizar_panel_salida(self, ticket: Ticket, pago: Pago) -> None:
        horas = ticket.horas_transcurridas()
        self.panel_salida.mensaje = (
            f"Ticket {ticket.codigo} — {horas:.1f}h — "
            f"Total: ${pago.monto:,.0f} — {pago.metodo.value} — GRACIAS"
        )

    def mostrar_paneles_pisos(self) -> None:
        for piso in self.pisos:
            piso._actualizar_panel()
            print(piso.panel.mostrar())

    # ── Consultas ────────────────────────────

    def disponibilidad_total(self) -> dict[TipoEspacio, int]:
        conteo: dict[TipoEspacio, int] = {t: 0 for t in TipoEspacio}
        for piso in self.pisos:
            for tipo, n in piso.disponibles_por_tipo().items():
                conteo[tipo] += n
        return conteo

    def historial_tickets(self) -> list[Ticket]:
        return list(self._tickets.values())

    # ── Helpers privados ─────────────────────

    def _piso_o_error(self, numero: int) -> Piso:
        for p in self.pisos:
            if p.numero == numero:
                return p
        raise ValueError(f"Piso {numero} no encontrado.")

    def _ticket_activo_o_error(self, codigo: str) -> Ticket:
        t = self._tickets.get(codigo)
        if not t or t.estado != EstadoTicket.ACTIVO:
            raise ValueError(f"Ticket {codigo} no existe o no está activo.")
        return t

    def _buscar_espacio(self, tipo: TipoEspacio) -> Optional[Espacio]:
        for piso in self.pisos:
            esp = piso.buscar_espacio_disponible(tipo)
            if esp:
                return esp
        return None


# ─────────────────────────────────────────────
#  Demo
# ─────────────────────────────────────────────

def demo() -> None:
    print("=" * 60)
    print("  SISTEMA DE ESTACIONAMIENTO INTELIGENTE  —  Demo")
    print("=" * 60)

    # 1. Configurar estructura
    park = Estacionamiento("ParkMultimodal Centro", capacidad_total=20)

    park.agregar_piso(1, "Planta baja")
    park.agregar_espacio(1, TipoEspacio.COMPACTO,  cantidad=4)
    park.agregar_espacio(1, TipoEspacio.GRANDE,    cantidad=2)
    park.agregar_espacio(1, TipoEspacio.ELECTRICO, cantidad=2)

    park.agregar_piso(2, "Primer nivel")
    park.agregar_espacio(2, TipoEspacio.MOTO,      cantidad=5)
    park.agregar_espacio(2, TipoEspacio.PMR,       cantidad=2)
    park.agregar_espacio(2, TipoEspacio.COMPACTO,  cantidad=3)

    # 2. Dar de alta personal
    admin = Administrador(nombre="Carlos Ruiz")
    asist = Asistente(nombre="Lucía Gómez")
    park.dar_alta_usuario(admin)
    park.dar_alta_usuario(asist)

    print("\n── Personal activo ──")
    for u in park.listar_personal():
        print(f"  {u}")

    # 3. Ingresar vehículos
    print("\n── Ingreso de vehículos ──")
    v1 = Auto("ABC123")
    v2 = Auto("DEF456", es_electrico=True)
    v3 = Moto("MN001")
    v4 = Camion("TRK99")

    t1 = park.ingresar_vehiculo(v1)
    t2 = park.ingresar_vehiculo(v2)
    t3 = park.ingresar_vehiculo(v3)
    t4 = park.ingresar_vehiculo(v4)

    for t in [t1, t2, t3, t4]:
        print(f"  {t}")

    print(f"\n  {park.panel_entrada.mostrar()}")

    # 4. Paneles por piso
    print("\n── Disponibilidad por piso ──")
    park.mostrar_paneles_pisos()

    # 5. Simular carga eléctrica
    v2.kwh_cargados = 18.5
    print(f"\n  {v2} cargó {v2.kwh_cargados} kWh")

    # 6. Egresar vehículos
    print("\n── Egreso y pagos ──")

    # Simular 2.5 horas para t1
    from datetime import timedelta
    t1.fecha_hora_entrada -= timedelta(hours=2, minutes=30)
    pago1 = park.egresar_vehiculo(t1.codigo, MetodoPago.TARJETA)
    print(f"  {pago1}")
    print(f"  {park.panel_salida.mostrar()}")

    # Asistente cobra en efectivo para t3
    t3.fecha_hora_entrada -= timedelta(hours=1)
    pago3 = park.egresar_vehiculo(t3.codigo, MetodoPago.EFECTIVO, asistente_id=asist.id)
    print(f"  {pago3}")

    # Vehículo eléctrico — 4 horas
    t2.fecha_hora_entrada -= timedelta(hours=4)
    pago2 = park.egresar_vehiculo(t2.codigo, MetodoPago.BILLETERA_VIRTUAL)
    print(f"  {pago2}")

    # 7. Estado final
    print("\n── Estado final ──")
    print(f"  Vehículos adentro: {park.vehiculos_adentro}")
    print(f"  {park.panel_entrada.mostrar()}")

    print("\n── Disponibilidad total ──")
    for tipo, n in park.disponibilidad_total().items():
        if n > 0:
            print(f"  {tipo.value}: {n} libres")

    # 8. Tarifas ejemplo
    print("\n── Ejemplos de tarifas ──")
    for h in [1, 2, 3, 5, 8]:
        monto = CalculadoraTarifa.calcular(h)
        print(f"  {h}h → ${monto:,.0f}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    demo()