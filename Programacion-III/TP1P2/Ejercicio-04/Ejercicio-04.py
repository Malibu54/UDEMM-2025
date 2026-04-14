from abc import ABC, abstractmethod
from datetime import date


# ─────────────────────────────────────────────────────────
# Clase abstracta — define el esqueleto del algoritmo
# ─────────────────────────────────────────────────────────

class ReporteFinanciero(ABC):

    # ── Template Method ────────────────────────────────────
    def generate(self) -> None:
        """Esqueleto del algoritmo. Secuencia inmutable."""
        print(f"\n{'=' * 50}")
        print(f"  Generando: {self.__class__.__name__}  [{date.today()}]")
        print(f"{'=' * 50}")
        self.loadData()
        self.customFilter()       # hook — puede no hacer nada
        self.processData()
        self.formatReport()
        self.exportReport()
        print(f"{'─' * 50}")
        print(f"  Reporte finalizado.\n")

    # ── Pasos abstractos (obligatorio implementar) ─────────
    @abstractmethod
    def loadData(self) -> None:
        """Carga los datos de la fuente correspondiente."""

    @abstractmethod
    def processData(self) -> None:
        """Aplica los cálculos propios de la periodicidad."""

    @abstractmethod
    def formatReport(self) -> None:
        """Formatea la salida según el tipo de reporte."""

    @abstractmethod
    def exportReport(self) -> None:
        """Exporta/distribuye el reporte generado."""

    # ── Hook (opcional, no obliga a sobreescribir) ─────────
    def customFilter(self) -> None:
        """
        Hook vacío. Las subclases pueden sobreescribirlo para
        aplicar filtros personalizados antes del procesamiento.
        Por defecto no hace nada.
        """
        pass


# ─────────────────────────────────────────────────────────
# Subclases concretas
# ─────────────────────────────────────────────────────────

class ReporteSemanal(ReporteFinanciero):

    def loadData(self) -> None:
        print("  [Semanal] Cargando transacciones de los últimos 7 días...")

    def customFilter(self) -> None:
        print("  [Semanal] Filtrando fines de semana y días feriados...")

    def processData(self) -> None:
        print("  [Semanal] Calculando variación diaria y promedio de 7 días...")

    def formatReport(self) -> None:
        print("  [Semanal] Formateando tabla con columnas por día de la semana...")

    def exportReport(self) -> None:
        print("  [Semanal] Enviando por e-mail al equipo operativo...")


class ReporteQuincenal(ReporteFinanciero):

    def loadData(self) -> None:
        print("  [Quincenal] Cargando datos de los últimos 15 días...")

    def customFilter(self) -> None:
        print("  [Quincenal] Separando quincena 1 (1-15) y quincena 2 (16-fin)...")

    def processData(self) -> None:
        print("  [Quincenal] Comparando totales entre ambas quincenas...")

    def formatReport(self) -> None:
        print("  [Quincenal] Formateando con sección por quincena + delta %...")

    def exportReport(self) -> None:
        print("  [Quincenal] Exportando a PDF y subiendo al portal interno...")


class ReporteMensual(ReporteFinanciero):

    def loadData(self) -> None:
        print("  [Mensual] Cargando registros del mes completo...")

    def processData(self) -> None:
        print("  [Mensual] Calculando promedio diario y totales por categoría...")

    def formatReport(self) -> None:
        print("  [Mensual] Formateando con cabecera de mes y resumen ejecutivo...")

    def exportReport(self) -> None:
        print("  [Mensual] Generando Excel y distribuyendo a gerencia...")


class ReporteTrimestral(ReporteFinanciero):

    def loadData(self) -> None:
        print("  [Trimestral] Cargando datos de los 3 meses del trimestre...")

    def customFilter(self) -> None:
        print("  [Trimestral] Excluyendo ajustes contables extraordinarios...")

    def processData(self) -> None:
        print("  [Trimestral] Calculando totales por mes y tendencia lineal...")

    def formatReport(self) -> None:
        print("  [Trimestral] Formateando con gráfico de barras y tabla comparativa...")

    def exportReport(self) -> None:
        print("  [Trimestral] Publicando en el sistema de BI y notificando al CFO...")


class ReporteAnual(ReporteFinanciero):

    def loadData(self) -> None:
        print("  [Anual] Cargando todo el ejercicio fiscal...")

    def customFilter(self) -> None:
        print("  [Anual] Normalizando por inflación y excluyendo partidas no recurrentes...")

    def processData(self) -> None:
        print("  [Anual] Calculando acumulados YTD, CAGR y proyección del cierre...")

    def formatReport(self) -> None:
        print("  [Anual] Formateando memoria anual con portada, índice y anexos...")

    def exportReport(self) -> None:
        print("  [Anual] Archivando en repositorio regulatorio y enviando al directorio...")
