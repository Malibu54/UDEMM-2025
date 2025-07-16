from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum

# --- Clases de Entidades ---

## Clases Base Abstractas
# ---
class Persona(ABC):
    """
    Clase base abstracta para entidades que comparten información personal común.
    Promueve la reutilización de código y asegura la consistencia.
    """
    def __init__(self, dni: str, codigo: str, nombre: str, direccion: str, telefono: str):
        if not all([dni, codigo, nombre, direccion, telefono]):
            raise ValueError("Todos los atributos de Persona deben tener un valor.")
        self._dni = dni
        self._codigo = codigo
        self._nombre = nombre
        self._direccion = direccion
        self._telefono = telefono

    @property
    def dni(self) -> str:
        return self._dni

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def direccion(self) -> str:
        return self._direccion

    @property
    def telefono(self) -> str:
        return self._telefono

    def mostrar_informacion(self) -> str:
        return (f"Código: {self._codigo}, Nombre: {self._nombre}, DNI: {self._dni}, "
                f"Dirección: {self._direccion}, Teléfono: {self._telefono}")

# ---
class Publicidad(ABC):
    """
    Clase base abstracta para todos los tipos de publicidad.
    Define una interfaz común para calcular costos.
    """
    def __init__(self, nombre: str, descripcion: str, monto_base: float):
        if not all([nombre, descripcion]) or monto_base <= 0:
            raise ValueError("Nombre, descripción y monto base son obligatorios y monto base debe ser positivo.")
        self._nombre = nombre
        self._descripcion = descripcion
        self._monto_base = monto_base
        self._monto_capital = monto_base * 1.15 # 15% más que el monto base

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @property
    def monto_base(self) -> float:
        return self._monto_base

    @property
    def monto_capital(self) -> float:
        return self._monto_capital

    @abstractmethod
    def calcular_costo(self) -> float:
        """Método abstracto para calcular el costo específico de cada tipo de publicidad."""
        pass

    def obtener_monto_final(self) -> float:
        """Devuelve el monto final de la publicidad."""
        return self.calcular_costo()

# ---
class MetodoPago(ABC):
    """
    Clase base abstracta para diferentes tipos de pago.
    Define una interfaz común para la validación.
    """
    def __init__(self, monto: float):
        if monto <= 0:
            raise ValueError("El monto del método de pago debe ser positivo.")
        self._monto = monto

    @property
    def monto(self) -> float:
        return self._monto

    @abstractmethod
    def es_valido(self) -> bool:
        """Método abstracto para verificar la validez específica de cada tipo de pago."""
        pass

## Subclases Concretas

# ---
class Cliente(Persona):
    """
    Representa un cliente de la agencia, hereda de Persona.
    """
    def __init__(self, dni: str, codigo: str, nombre: str, direccion: str, telefono: str, esta_activo: bool = True):
        super().__init__(dni, codigo, nombre, direccion, telefono)
        self._esta_activo = esta_activo
        self._metodos_pago = [] # Lista de objetos MetodoPago

    @property
    def esta_activo(self) -> bool:
        return self._esta_activo

    @esta_activo.setter
    def esta_activo(self, valor: bool):
        if not isinstance(valor, bool):
            raise TypeError("El estado 'esta_activo' debe ser booleano.")
        self._esta_activo = valor

    def agregar_metodo_pago(self, metodo_pago: MetodoPago):
        """Agrega un método de pago a la lista del cliente."""
        if not isinstance(metodo_pago, MetodoPago):
            raise TypeError("El objeto agregado debe ser una instancia de MetodoPago.")
        self._metodos_pago.append(metodo_pago)

    def es_valido(self) -> bool:
        """Verifica si el cliente está activo."""
        return self._esta_activo

    def obtener_metodos_pago(self) -> list:
        """Devuelve la lista de métodos de pago del cliente."""
        return list(self._metodos_pago) # Devuelve una copia para no romper encapsulación

# ---
class Vendedor(Persona):
    """
    Representa un vendedor de la agencia, hereda de Persona.
    """
    def __init__(self, dni: str, codigo: str, nombre: str, direccion: str, telefono: str, max_proyectos_sin_terminar: int = 3):
        super().__init__(dni, codigo, nombre, direccion, telefono)
        if max_proyectos_sin_terminar <= 0:
            raise ValueError("El máximo de proyectos sin terminar debe ser un número positivo.")
        self._proyectos = [] # Lista de objetos Proyecto
        self._max_proyectos_sin_terminar = max_proyectos_sin_terminar

    @property
    def proyectos(self) -> list:
        return list(self._proyectos)

    @property
    def max_proyectos_sin_terminar(self) -> int:
        return self._max_proyectos_sin_terminar

    def agregar_proyecto(self, proyecto): # Tipo Proyecto circular, se maneja en el método
        """Agrega un proyecto a la lista del vendedor."""
        # Se verifica la instancia dentro del método para evitar importaciones circulares en el encabezado.
        if not isinstance(proyecto, Proyecto):
            raise TypeError("El objeto agregado debe ser una instancia de Proyecto.")
        self._proyectos.append(proyecto)

    def obtener_cantidad_proyectos_sin_terminar(self) -> int:
        """Calcula y devuelve la cantidad de proyectos sin terminar del vendedor."""
        cantidad_sin_terminar = 0
        for p in self._proyectos:
            if p.estado != EstadoProyecto.TERMINADO:
                cantidad_sin_terminar += 1
        return cantidad_sin_terminar

    def esta_disponible(self) -> bool:
        """
        Verifica si el vendedor está disponible (no tiene más de `max_proyectos_sin_terminar` proyectos sin terminar).
        No verifica asignaciones directas, ya que eso sería responsabilidad de la clase Asignacion.
        """
        return self.obtener_cantidad_proyectos_sin_terminar() < self._max_proyectos_sin_terminar

    def obtener_costo_proyecto(self, codigo_proyecto: str) -> float:
        """Obtiene el costo total de un proyecto específico del vendedor."""
        for proyecto in self._proyectos:
            if proyecto.codigo == codigo_proyecto:
                return proyecto.obtener_monto_total_publicidad()
        return 0.0 # Retorna 0.0 si el proyecto no se encuentra

    def obtener_proyecto_mas_caro_terminado(self): # Retorna objeto Proyecto o None
        """Encuentra y devuelve el proyecto terminado más caro del vendedor."""
        proyecto_mas_caro = None
        monto_maximo = 0.0
        for proyecto in self._proyectos:
            if proyecto.estado == EstadoProyecto.TERMINADO:
                costo_actual = proyecto.obtener_monto_total_publicidad()
                if costo_actual > monto_maximo:
                    monto_maximo = costo_actual
                    proyecto_mas_caro = proyecto
        return proyecto_mas_caro

    def obtener_proyecto_mas_economico_terminado(self): # Retorna objeto Proyecto o None
        """Encuentra y devuelve el proyecto terminado más económico del vendedor."""
        proyecto_mas_economico = None
        monto_minimo = float('inf') # Inicializar con un valor muy alto
        for proyecto in self._proyectos:
            if proyecto.estado == EstadoProyecto.TERMINADO:
                costo_actual = proyecto.obtener_monto_total_publicidad()
                if costo_actual < monto_minimo:
                    monto_minimo = costo_actual
                    proyecto_mas_economico = proyecto
        return proyecto_mas_economico

    def aplicar_descuento_a_proyecto(self, codigo_proyecto: str, porcentaje_descuento: float) -> bool:
        """Aplica un descuento a un proyecto específico del vendedor."""
        if not (0 < porcentaje_descuento < 100):
            raise ValueError("El porcentaje de descuento debe estar entre 0 y 100.")
        for proyecto in self._proyectos:
            if proyecto.codigo == codigo_proyecto:
                proyecto.aplicar_descuento(porcentaje_descuento)
                return True
        return False

# ---
class Tecnico(Persona):
    """
    Representa un técnico que trabaja en las asignaciones, hereda de Persona.
    """
    def __init__(self, dni: str, codigo: str, nombre: str, direccion: str, telefono: str, categoria: str, horas_a_trabajar: int):
        super().__init__(dni, codigo, nombre, direccion, telefono)
        if not categoria or horas_a_trabajar <= 0:
            raise ValueError("Categoría y horas a trabajar son obligatorias y positivas.")
        self._categoria = categoria
        self._horas_a_trabajar = horas_a_trabajar
        self._esta_asignado = False # Indica si ya está trabajando en una asignación

    @property
    def categoria(self) -> str:
        return self._categoria

    @property
    def horas_a_trabajar(self) -> int:
        return self._horas_a_trabajar

    @property
    def esta_asignado(self) -> bool:
        return self._esta_asignado

    @esta_asignado.setter
    def esta_asignado(self, valor: bool):
        if not isinstance(valor, bool):
            raise TypeError("El estado 'esta_asignado' debe ser booleano.")
        self._esta_asignado = valor

# ---
class EstadoProyecto(Enum):
    """Enumeración para el estado de un proyecto."""
    EN_PROCESO = "en_proceso"
    TERMINADO = "terminado"
    BLOQUEADO = "bloqueado"

# ---
class Proyecto:
    """
    Representa un proyecto de marketing realizado para un cliente.
    """
    def __init__(self, codigo: str, fecha_inicio: datetime, fecha_fin: datetime, monto: float, descripcion: str, estado: EstadoProyecto = EstadoProyecto.EN_PROCESO):
        if not all([codigo, descripcion]) or monto <= 0:
            raise ValueError("Código, descripción y monto son obligatorios y monto debe ser positivo.")
        if not isinstance(fecha_inicio, datetime) or not isinstance(fecha_fin, datetime):
            raise TypeError("Fecha de inicio y fin deben ser objetos datetime.")
        if fecha_inicio >= fecha_fin:
            raise ValueError("La fecha de inicio debe ser anterior a la fecha de fin.")
        if not isinstance(estado, EstadoProyecto):
            raise TypeError("El estado debe ser un miembro de EstadoProyecto Enum.")

        self._codigo = codigo
        self._fecha_inicio = fecha_inicio
        self._fecha_fin = fecha_fin
        self._estado = estado
        self._monto = monto # Monto estimado inicial
        self._descripcion = descripcion
        self._publicidades = [] # Lista de objetos Publicidad

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def fecha_inicio(self) -> datetime:
        return self._fecha_inicio

    @property
    def fecha_fin(self) -> datetime:
        return self._fecha_fin

    @property
    def estado(self) -> EstadoProyecto:
        return self._estado

    @property
    def monto(self) -> float:
        return self._monto

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @property
    def publicidades(self) -> list:
        return list(self._publicidades)

    def establecer_estado(self, nuevo_estado: EstadoProyecto):
        """Establece un nuevo estado para el proyecto."""
        if not isinstance(nuevo_estado, EstadoProyecto):
            raise TypeError("El nuevo estado debe ser un miembro de EstadoProyecto Enum.")
        self._estado = nuevo_estado

    def agregar_publicidad(self, publicidad: Publicidad):
        """Agrega un objeto Publicidad a la lista de publicidades del proyecto."""
        if not isinstance(publicidad, Publicidad):
            raise TypeError("El objeto agregado debe ser una instancia de Publicidad.")
        self._publicidades.append(publicidad)

    def es_viable(self) -> bool:
        """Verifica si el proyecto tiene al menos un tipo de publicidad."""
        return len(self._publicidades) > 0

    def obtener_cantidad_total_publicidades(self) -> int:
        """Devuelve la cantidad total de publicidades en el proyecto."""
        return len(self._publicidades)

    def obtener_monto_total_publicidad(self) -> float:
        """Calcula el monto total sumando los costos de todas las publicidades."""
        total = 0.0
        for pub in self._publicidades:
            total += pub.calcular_costo()
        return total

    def aplicar_descuento(self, porcentaje: float):
        """Aplica un descuento al monto inicial del proyecto."""
        if not (0 < porcentaje < 100):
            raise ValueError("El porcentaje de descuento debe estar entre 0 y 100.")
        self._monto -= self._monto * (porcentaje / 100)

## Subclases de Publicidad

# ---
class PublicidadRevista(Publicidad):
    """
    Tipo específico de publicidad para revistas físicas.
    """
    def __init__(self, nombre: str, descripcion: str, monto_base: float, tiene_convenio: bool = False):
        super().__init__(nombre, descripcion, monto_base)
        self._tiene_convenio = tiene_convenio

    @property
    def tiene_convenio(self) -> bool:
        return self._tiene_convenio

    def calcular_costo(self) -> float:
        costo = self.monto_base * 1.25 # monto_base + 25%
        if self._tiene_convenio:
            costo *= 0.90 # -10% si tiene convenio
        return costo

# ---
class PublicidadDigital(Publicidad, ABC): # También abstracta para definir la base de digitales
    """
    Clase base para las publicidades digitales.
    """
    def __init__(self, nombre: str, descripcion: str, monto_base: float):
        super().__init__(nombre, descripcion, monto_base)

    def calcular_costo(self) -> float:
        return self.monto_base * 1.07 # monto_base + 7% de costo fijo

# ---
class PublicidadWebSEO(PublicidadDigital):
    """
    Publicidad digital enfocada en SEO web.
    """
    def __init__(self, nombre: str, descripcion: str, monto_base: float, cantidad_paginas: int, tiene_convenio: bool = False):
        super().__init__(nombre, descripcion, monto_base)
        if cantidad_paginas <= 0:
            raise ValueError("La cantidad de páginas debe ser positiva.")
        self._cantidad_paginas = cantidad_paginas
        self._tiene_convenio = tiene_convenio

    @property
    def cantidad_paginas(self) -> int:
        return self._cantidad_paginas

    @property
    def tiene_convenio(self) -> bool:
        return self._tiene_convenio

    def calcular_costo(self) -> float:
        costo = super().calcular_costo() # Costo de PublicidadDigital (monto_base + 7%)
        costo += self.monto_base * 0.12 # + 12% del monto base digital

        if self._cantidad_paginas > 20:
            costo += costo * 0.20 # 20% adicional si cantidad_paginas > 20

        if self._tiene_convenio:
            costo *= 0.82 # Descuento del 18%
        return costo

# ---
class PublicidadRedesSociales(PublicidadDigital):
    """
    Publicidad digital para redes sociales.
    """
    def __init__(self, nombre: str, descripcion: str, monto_base: float, es_local: bool, redes_sociales_usadas: list[str]):
        super().__init__(nombre, descripcion, monto_base)
        if not redes_sociales_usadas:
            raise ValueError("Debe especificar al menos una red social usada.")
        self._es_local = es_local
        self._redes_sociales_usadas = [rs.lower() for rs in redes_sociales_usadas] # Normalizar a minúsculas

    @property
    def es_local(self) -> bool:
        return self._es_local

    @property
    def redes_sociales_usadas(self) -> list[str]:
        return list(self._redes_sociales_usadas) # Devuelve una copia

    def calcular_costo(self) -> float:
        costo = super().calcular_costo() # Costo de PublicidadDigital (monto_base + 7%)
        costo += self.monto_base * 0.07 # + 7% de costo fijo

        if self._es_local:
            costo *= 0.90 # -10% de descuento si es local

        # Costo fijo basado en el número de redes sociales clásicas usadas
        num_redes = len(self._redes_sociales_usadas)
        if num_redes >= 3:
            costo += 21000
        elif num_redes == 2:
            costo += 14000
        elif num_redes == 1:
            costo += 7000
        return costo

    def aplicar_descuento_extra(self, porcentaje: float):
        """
        Aplica un descuento extra al monto base de la publicidad de redes sociales.
        Este método podría ser para promociones específicas.
        """
        if not (0 < porcentaje < 100):
            raise ValueError("El porcentaje de descuento debe estar entre 0 y 100.")
        self._monto_base -= self._monto_base * (porcentaje / 100)

## Subclases de MetodoPago

# ---
class PagoEfectivo(MetodoPago):
    """
    Pago realizado en efectivo.
    """
    def __init__(self, monto: float, cantidad_billetes: int):
        super().__init__(monto)
        if cantidad_billetes <= 0:
            raise ValueError("La cantidad de billetes debe ser positiva.")
        self._cantidad_billetes = cantidad_billetes

    @property
    def cantidad_billetes(self) -> int:
        return self._cantidad_billetes

    def es_valido(self) -> bool:
        """Siempre válido para pago en efectivo."""
        return True

# ---
class PagoCheque(MetodoPago):
    """
    Pago realizado con un cheque.
    """
    def __init__(self, monto: float, tiene_fondos: bool, esta_autorizado: bool, fecha: datetime, nombre_banco: str):
        super().__init__(monto)
        if not isinstance(fecha, datetime):
            raise TypeError("La fecha debe ser un objeto datetime.")
        if not nombre_banco:
            raise ValueError("El nombre del banco es obligatorio.")
        self._tiene_fondos = tiene_fondos
        self._esta_autorizado = esta_autorizado
        self._fecha = fecha
        self._nombre_banco = nombre_banco

    @property
    def tiene_fondos(self) -> bool:
        return self._tiene_fondos

    @property
    def esta_autorizado(self) -> bool:
        return self._esta_autorizado

    @property
    def fecha(self) -> datetime:
        return self._fecha

    @property
    def nombre_banco(self) -> str:
        return self._nombre_banco

    def es_valido(self) -> bool:
        """Verifica si el cheque tiene fondos y está autorizado."""
        return self._tiene_fondos and self._esta_autorizado

# ---
class PagoTransferencia(MetodoPago):
    """
    Pago realizado mediante transferencia bancaria.
    """
    def __init__(self, monto: float, esta_autorizada: bool, fecha: datetime, nombre_banco: str):
        super().__init__(monto)
        if not isinstance(fecha, datetime):
            raise TypeError("La fecha debe ser un objeto datetime.")
        if not nombre_banco:
            raise ValueError("El nombre del banco es obligatorio.")
        self._esta_autorizada = esta_autorizada
        self._fecha = fecha
        self._nombre_banco = nombre_banco

    @property
    def esta_autorizada(self) -> bool:
        return self._esta_autorizada

    @property
    def fecha(self) -> datetime:
        return self._fecha

    @property
    def nombre_banco(self) -> str:
        return self._nombre_banco

    def es_valido(self) -> bool:
        """Verifica si la transferencia está autorizada."""
        return self._esta_autorizada

# ---
class Asignacion:
    """
    Representa una asignación de trabajo que vincula un cliente, vendedores y técnicos a un proyecto.
    """
    def __init__(self, codigo: str, descripcion: str, fecha: datetime, cliente: Cliente, proyecto: Proyecto):
        if not all([codigo, descripcion]) or not isinstance(fecha, datetime):
            raise ValueError("Código, descripción y fecha son obligatorios.")
        if not isinstance(cliente, Cliente) or not isinstance(proyecto, Proyecto):
            raise TypeError("Cliente y Proyecto deben ser instancias de sus respectivas clases.")

        self._codigo = codigo
        self._descripcion = descripcion
        self._fecha = fecha
        self._cliente = cliente
        self._proyecto = proyecto
        self._vendedores = [] # Lista de objetos Vendedor - máximo 2
        self._tecnicos = [] # Lista de objetos Tecnico - al menos 1
        self._esta_bloqueada = False
        self._presupuesto = proyecto.obtener_monto_total_publicidad() # Presupuesto basado en el proyecto

    @property
    def codigo(self) -> str:
        return self._codigo

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @property
    def fecha(self) -> datetime:
        return self._fecha

    @property
    def cliente(self) -> Cliente:
        return self._cliente

    @property
    def proyecto(self) -> Proyecto:
        return self._proyecto

    @property
    def vendedores(self) -> list:
        return list(self._vendedores)

    @property
    def tecnicos(self) -> list:
        return list(self._tecnicos)

    @property
    def esta_bloqueada(self) -> bool:
        return self._esta_bloqueada

    @property
    def presupuesto(self) -> float:
        return self._presupuesto

    def agregar_vendedor(self, vendedor: Vendedor):
        """Agrega un vendedor a la asignación, con un máximo de 2."""
        if not isinstance(vendedor, Vendedor):
            raise TypeError("El objeto agregado debe ser una instancia de Vendedor.")
        if len(self._vendedores) >= 2:
            raise ValueError("Una asignación no puede tener más de 2 vendedores.")
        if not vendedor.esta_disponible():
            raise ValueError(f"El vendedor {vendedor.nombre} no está disponible (tiene demasiados proyectos sin terminar).")
        self._vendedores.append(vendedor)

    def agregar_tecnico(self, tecnico: Tecnico):
        """Agrega un técnico a la asignación."""
        if not isinstance(tecnico, Tecnico):
            raise TypeError("El objeto agregado debe ser una instancia de Tecnico.")
        if tecnico.esta_asignado:
            raise ValueError(f"El técnico {tecnico.nombre} ya está asignado a otra tarea.")
        self._tecnicos.append(tecnico)
        tecnico.esta_asignado = True # Marcar al técnico como asignado

    def bloquear_asignacion(self):
        """Bloquea la asignación, impidiendo futuras modificaciones."""
        self._esta_bloqueada = True

    def es_valida(self) -> bool:
        """
        Verifica la validez de la asignación:
        - Cliente válido (activo).
        - Vendedores disponibles y no superan el límite de proyectos sin terminar.
        - Al menos 1 técnico asignado.
        """
        if not self._cliente.es_valido():
            return False
        if not self._vendedores: # Debe haber al menos un vendedor
            return False
        for vendedor in self._vendedores:
            # Se asume que la disponibilidad del vendedor ya se verifica al agregarlo.
            # Aquí se verifica que los que ya están agregados sigan siendo válidos.
            if not vendedor.esta_disponible():
                return False
        if not self._tecnicos: # Debe haber al menos un técnico
            return False
        return True

# ---
class Agencia:
    """
    Representa la propia agencia de marketing, gestionando las operaciones generales.
    """
    def __init__(self, nombre: str):
        self._nombre = nombre
        self._clientes = []
        self._vendedores = []
        self._tecnicos = []
        self._proyectos = []
        self._asignaciones = []

    @property
    def nombre(self) -> str:
        return self._nombre

    def agregar_cliente(self, cliente: Cliente):
        """Agrega un cliente a la agencia."""
        if not isinstance(cliente, Cliente):
            raise TypeError("El objeto agregado debe ser una instancia de Cliente.")
        if any(c.dni == cliente.dni for c in self._clientes): # Verifica DNI duplicado
            raise ValueError(f"Ya existe un cliente con DNI {cliente.dni}.")
        self._clientes.append(cliente)

    def agregar_vendedor(self, vendedor: Vendedor):
        """Agrega un vendedor a la agencia."""
        if not isinstance(vendedor, Vendedor):
            raise TypeError("El objeto agregado debe ser una instancia de Vendedor.")
        if any(v.dni == vendedor.dni for v in self._vendedores): # Verifica DNI duplicado
            raise ValueError(f"Ya existe un vendedor con DNI {vendedor.dni}.")
        self._vendedores.append(vendedor)

    def agregar_tecnico(self, tecnico: Tecnico):
        """Agrega un técnico a la agencia."""
        if not isinstance(tecnico, Tecnico):
            raise TypeError("El objeto agregado debe ser una instancia de Tecnico.")
        if any(t.dni == tecnico.dni for t in self._tecnicos): # Verifica DNI duplicado
            raise ValueError(f"Ya existe un técnico con DNI {tecnico.dni}.")
        self._tecnicos.append(tecnico)

    def agregar_proyecto(self, proyecto: Proyecto):
        """Agrega un proyecto a la agencia."""
        if not isinstance(proyecto, Proyecto):
            raise TypeError("El objeto agregado debe ser una instancia de Proyecto.")
        if any(p.codigo == proyecto.codigo for p in self._proyectos): # Verifica código duplicado
            raise ValueError(f"Ya existe un proyecto con código {proyecto.codigo}.")
        self._proyectos.append(proyecto)

    def crear_asignacion(self, codigo: str, descripcion: str, fecha: datetime, cliente_codigo: str, proyecto_codigo: str, vendedores_codigos: list[str], tecnicos_codigos: list[str]) -> Asignacion:
        """
        Crea y agrega una asignación, vinculando entidades existentes.
        Realiza validaciones antes de crear la asignación.
        """
        cliente_obj = None
        for c in self._clientes:
            if c.codigo == cliente_codigo:
                cliente_obj = c
                break
        if not cliente_obj:
            raise ValueError(f"Cliente con código {cliente_codigo} no encontrado.")

        proyecto_obj = None
        for p in self._proyectos:
            if p.codigo == proyecto_codigo:
                proyecto_obj = p
                break
        if not proyecto_obj:
            raise ValueError(f"Proyecto con código {proyecto_codigo} no encontrado.")

        vendedores_obj = []
        for vend_code in vendedores_codigos:
            vendedor_encontrado = None
            for v in self._vendedores:
                if v.codigo == vend_code:
                    vendedor_encontrado = v
                    break
            if not vendedor_encontrado:
                raise ValueError(f"Vendedor con código {vend_code} no encontrado.")
            vendedores_obj.append(vendedor_encontrado)

        tecnicos_obj = []
        for tecn_code in tecnicos_codigos:
            tecnico_encontrado = None
            for t in self._tecnicos:
                if t.codigo == tecn_code:
                    tecnico_encontrado = t
                    break
            if not tecnico_encontrado:
                raise ValueError(f"Técnico con código {tecn_code} no encontrado.")
            tecnicos_obj.append(tecnico_encontrado)

        if not vendedores_obj:
            raise ValueError("Debe asignar al menos un vendedor.")
        if len(vendedores_obj) > 2:
            raise ValueError("No se pueden asignar más de 2 vendedores a una asignación.")
        if not tecnicos_obj:
            raise ValueError("Debe asignar al menos un técnico.")


        # Instanciar la asignación y agregar vendedores/técnicos
        nueva_asignacion = Asignacion(codigo, descripcion, fecha, cliente_obj, proyecto_obj)

        for vendedor in vendedores_obj:
            nueva_asignacion.agregar_vendedor(vendedor)

        for tecnico in tecnicos_obj:
            nueva_asignacion.agregar_tecnico(tecnico)

        if not nueva_asignacion.es_valida():
            raise ValueError("La asignación no es válida según las reglas de negocio.")

        self._asignaciones.append(nueva_asignacion)
        return nueva_asignacion

    def obtener_clientes_activos(self) -> list[Cliente]:
        """Devuelve una lista de clientes que están activos."""
        activos = []
        for cliente in self._clientes:
            if cliente.es_valido(): # Usa el método es_valido() del cliente
                activos.append(cliente)
        return activos

    def obtener_vendedores_disponibles(self) -> list[Vendedor]:
        """Devuelve una lista de vendedores que están disponibles."""
        disponibles = []
        for vendedor in self._vendedores:
            if vendedor.esta_disponible():
                disponibles.append(vendedor)
        return disponibles

    def obtener_proyectos_por_estado(self, estado: EstadoProyecto) -> list[Proyecto]:
        """Devuelve una lista de proyectos con un estado específico."""
        proyectos_filtrados = []
        for proyecto in self._proyectos:
            if proyecto.estado == estado:
                proyectos_filtrados.append(proyecto)
        return proyectos_filtrados

    def obtener_asignaciones_por_cliente(self, cliente_codigo: str) -> list[Asignacion]:
        """Devuelve una lista de asignaciones para un cliente específico."""
        asignaciones_cliente = []
        for asignacion in self._asignaciones:
            if asignacion.cliente.codigo == cliente_codigo:
                asignaciones_cliente.append(asignacion)
        return asignaciones_cliente


# --- Ejemplo de Uso ---
if __name__ == "__main__":
    print("--- Demostración del Algoritmo ---")

    # 1. Crear la Agencia
    agencia_digital = Agencia("Marketing Total S.A.")
    print(f"\nAgencia creada: {agencia_digital.nombre}")

    # 2. Crear Personas (Clientes, Vendedores, Técnicos)
    cliente1 = Cliente("11223344", "CL001", "Juan Pérez", "Calle Falsa 123", "555-1111", True)
    cliente2 = Cliente("55667788", "CL002", "Ana Gómez", "Av. Siempre Viva 456", "555-2222", False) # Cliente inactivo
    agencia_digital.agregar_cliente(cliente1)
    agencia_digital.agregar_cliente(cliente2)
    print("\n--- Clientes ---")
    print(cliente1.mostrar_informacion())
    print(cliente2.mostrar_informacion())
    print(f"Cliente 1 activo: {cliente1.es_valido()}")
    print(f"Cliente 2 activo: {cliente2.es_valido()}")

    vendedor1 = Vendedor("99887766", "VEND001", "María López", "Ruta 66", "555-3333", 2)
    vendedor2 = Vendedor("12345678", "VEND002", "Pedro Giménez", "Elm Street", "555-4444") # Default 3 proyectos
    agencia_digital.agregar_vendedor(vendedor1)
    agencia_digital.agregar_vendedor(vendedor2)
    print("\n--- Vendedores ---")
    print(vendedor1.mostrar_informacion())
    print(vendedor2.mostrar_informacion())

    tecnico1 = Tecnico("87654321", "TEC001", "Laura Fernández", "Tech Avenue", "555-5555", "marketing digital", 40)
    tecnico2 = Tecnico("23456789", "TEC002", "Carlos Ruiz", "Data Center", "555-6666", "informático", 30)
    agencia_digital.agregar_tecnico(tecnico1)
    agencia_digital.agregar_tecnico(tecnico2)
    print("\n--- Técnicos ---")
    print(tecnico1.mostrar_informacion())
    print(tecnico2.mostrar_informacion())

    # 3. Crear Publicidades
    pub_revista_promo = PublicidadRevista("Revista Gamer", "Publicidad en revista especializada.", 50000.0, True)
    pub_digital_base = PublicidadDigital("Banner Genérico", "Banner para sitios web.", 10000.0)
    pub_web_seo_grande = PublicidadWebSEO("SEO Avanzado", "Optimización SEO para sitio grande.", 70000.0, 25, False)
    pub_redes_loc = PublicidadRedesSociales("Campaña Local FB", "Campaña en Facebook para negocio local.", 30000.0, True, ["facebook"])
    pub_redes_global = PublicidadRedesSociales("Campaña Global Multi", "Campaña en varias redes para alcance global.", 60000.0, False, ["facebook", "instagram", "linkedin"])

    print("\n--- Costos de Publicidad ---")
    print(f"Costo Revista (con convenio): ${pub_revista_promo.calcular_costo():.2f}")
    print(f"Costo Digital Base: ${pub_digital_base.calcular_costo():.2f}")
    print(f"Costo Web SEO (25 páginas, sin convenio): ${pub_web_seo_grande.calcular_costo():.2f}")
    print(f"Costo Redes Sociales (Local, 1 red): ${pub_redes_loc.calcular_costo():.2f}")
    print(f"Costo Redes Sociales (Global, 3 redes): ${pub_redes_global.calcular_costo():.2f}")

    # 4. Crear Proyectos
    proyecto1 = Proyecto("PROY001", datetime(2025, 7, 1), datetime(2025, 9, 30), 100000.0, "Campaña de lanzamiento producto X")
    proyecto1.agregar_publicidad(pub_revista_promo)
    proyecto1.agregar_publicidad(pub_web_seo_grande)
    proyecto1.agregar_publicidad(pub_redes_global)
    agencia_digital.agregar_proyecto(proyecto1)

    proyecto2 = Proyecto("PROY002", datetime(2025, 8, 1), datetime(2025, 8, 31), 50000.0, "Campaña de verano")
    proyecto2.agregar_publicidad(pub_digital_base)
    proyecto2.agregar_publicidad(pub_redes_loc)
    agencia_digital.agregar_proyecto(proyecto2)

    vendedor1.agregar_proyecto(proyecto1)
    vendedor1.agregar_proyecto(proyecto2) # Vendedor1 ahora tiene 2 proyectos sin terminar

    print("\n--- Proyectos ---")
    print(f"Proyecto 1 - Código: {proyecto1.codigo}, Descripción: {proyecto1.descripcion}")
    print(f"Monto total publicidades Proyecto 1: ${proyecto1.obtener_monto_total_publicidad():.2f}")
    print(f"Proyecto 1 es viable: {proyecto1.es_viable()}")
    print(f"Vendedor 1 tiene {vendedor1.obtener_cantidad_proyectos_sin_terminar()} proyectos sin terminar.")
    print(f"Vendedor 1 disponible: {vendedor1.esta_disponible()}")

    # 5. Crear Asignaciones
    print("\n--- Asignaciones ---")
    try:
        # Asignación válida
        asignacion1 = agencia_digital.crear_asignacion(
            "ASIG001", "Asignación inicial para campaña X", datetime.now(),
            cliente1.codigo, proyecto1.codigo,
            [vendedor1.codigo], [tecnico1.codigo]
        )
        print(f"Asignación 1 creada con éxito. Cliente: {asignacion1.cliente.nombre}, Proyecto: {asignacion1.proyecto.descripcion}")
        print(f"Asignación 1 es válida: {asignacion1.es_valida()}")
        print(f"Técnico 1 asignado: {tecnico1.esta_asignado}")

        # Intentar agregar un segundo vendedor a la asignación 1
        asignacion1.agregar_vendedor(vendedor2)
        print(f"Vendedor 2 agregado a Asignación 1. Vendedores en Asignación 1: {[v.nombre for v in asignacion1.vendedores]}")

        # Intentar agregar un tercer vendedor (debería fallar)
        # vendedor3 = Vendedor("00000000", "VEND003", "Lucas Blanco", "Fake St", "555-7777")
        # agencia_digital.agregar_vendedor(vendedor3)
        # asignacion1.agregar_vendedor(vendedor3) # Esto lanzará un ValueError

    except ValueError as e:
        print(f"Error al crear/modificar asignación: {e}")
    except TypeError as e:
        print(f"Error de tipo: {e}")

    # Demostrar la limitación de proyectos por vendedor
    print(f"\nVendedor 1 tiene {vendedor1.obtener_cantidad_proyectos_sin_terminar()} proyectos sin terminar (max: {vendedor1.max_proyectos_sin_terminar}).")
    vendedor1.agregar_proyecto(Proyecto("PROY003", datetime(2025, 7, 1), datetime(2025, 9, 30), 20000.0, "Campaña adicional"))
    print(f"Vendedor 1 ahora tiene {vendedor1.obtener_cantidad_proyectos_sin_terminar()} proyectos sin terminar.")
    print(f"Vendedor 1 disponible: {vendedor1.esta_disponible()}") # Debería ser False si max_proyectos_sin_terminar es 3 y tiene 3 proyectos sin terminar

    # 6. Métodos de MetodoPago
    pago_efectivo = PagoEfectivo(5000.0, 10)
    pago_cheque = PagoCheque(15000.0, True, True, datetime.now(), "Banco Central")
    pago_transferencia = PagoTransferencia(25000.0, False, datetime.now(), "Banco Nación")

    cliente1.agregar_metodo_pago(pago_efectivo)
    cliente1.agregar_metodo_pago(pago_cheque)
    cliente1.agregar_metodo_pago(pago_transferencia)

    print("\n--- Métodos de Pago del Cliente 1 ---")
    for metodo in cliente1.obtener_metodos_pago():
        print(f"Método de pago: {type(metodo).__name__}, Monto: ${metodo.monto:.2f}, Válido: {metodo.es_valido()}")

    # 7. Operaciones de Agencia
    print("\n--- Operaciones de Agencia ---")
    print("Clientes Activos:")
    for c in agencia_digital.obtener_clientes_activos():
        print(f"- {c.nombre}")

    print("\nVendedores Disponibles:")
    for v in agencia_digital.obtener_vendedores_disponibles():
        print(f"- {v.nombre}")

    proyecto1.establecer_estado(EstadoProyecto.TERMINADO)
    print("\nProyectos Terminados:")
    for p in agencia_digital.obtener_proyectos_por_estado(EstadoProyecto.TERMINADO):
        print(f"- {p.descripcion}")

    print("\nProyectos en Proceso:")
    for p in agencia_digital.obtener_proyectos_por_estado(EstadoProyecto.EN_PROCESO):
        print(f"- {p.descripcion}")

    # Demostrar obtener proyecto más caro/económico (sin sorted, min, max)
    print("\n--- Proyectos de Vendedor 1 ---")
    proyecto_caro = vendedor1.obtener_proyecto_mas_caro_terminado()
    if proyecto_caro:
        print(f"Proyecto TERMINADO más caro de {vendedor1.nombre}: {proyecto_caro.descripcion} (Costo: ${proyecto_caro.obtener_monto_total_publicidad():.2f})")
    else:
        print(f"{vendedor1.nombre} no tiene proyectos terminados.")

    proyecto_eco = vendedor1.obtener_proyecto_mas_economico_terminado()
    if proyecto_eco:
        print(f"Proyecto TERMINADO más económico de {vendedor1.nombre}: {proyecto_eco.descripcion} (Costo: ${proyecto_eco.obtener_monto_total_publicidad():.2f})")
    else:
        print(f"{vendedor1.nombre} no tiene proyectos terminados.")

    # Aplicar descuento a un proyecto
    print(f"\nMonto inicial Proyecto 1 (estimado): ${proyecto1.monto:.2f}")
    vendedor1.aplicar_descuento_a_proyecto(proyecto1.codigo, 10.0)
    print(f"Monto Proyecto 1 (después de 10% descuento): ${proyecto1.monto:.2f}")

    # Intento de acceso directo a atributo privado (no permitido o no recomendado)
    try:
        # Esto generaría un AttributeError si se intenta acceder a _dni directamente desde fuera de la clase
        # print(cliente1.__dni)
        pass
    except AttributeError:
        print("\nIntento de acceso directo a atributo privado bloqueado (AttributeError esperado).")