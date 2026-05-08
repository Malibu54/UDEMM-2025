# Primer Parcial — Programación III

## Descripción
<!-- Breve descripción del proyecto o problema a resolver -->

## Estructura del repositorio
```
globerx26/
├── domain/entities.py          ← Entidades puras de negocio
├── adapters/
│   ├── monitor_adapters.py     ← Interfaz + 3 adaptadores concretos
│   ├── adapter_factory.py      ← Fábrica de adaptadores
│   └── monitoring_system.py    ← Orquestador + resiliencia
├── cost/calculators.py         ← Template Method para costos
├── reports/strategies.py       ← Strategy para formatos de reporte
├── config/settings.py          ← Configuración externa
├── tests/test_globerx26.py     ← 36 tests (todos verdes ✅)
└── main.py                     ← Punto de entrada
```

# Patrones aplicados y por qué cada uno
**Adapter** (monitor_adapters.py) — resuelve el problema central: tres APIs incompatibles necesitan presentarse con una interfaz uniforme obtener_estado(). Cada adaptador encapsula la traducción de XML legacy, JSON con auth o REST moderno hacia ServiceStatus. El sistema nunca conoce los detalles de ningún proveedor.
**Factory Method** (adapter_factory.py) — el ADAPTER_REGISTRY mapea strings de configuración a constructores. Agregar un cuarto proveedor es agregar una entrada al diccionario sin tocar create() ni MonitoringSystem. El flag enabled: false en la config desactiva un proveedor sin eliminarlo.
**Template Method** (calculators.py) — el algoritmo de cálculo de costo es fijo en calculate() (Template). Solo regional_factor() es abstracto. Para agregar "Zona Oriente" en el futuro, se crea OrienteCostCalculator(CostCalculator) con su factor; el algoritmo nunca se modifica.
**Strategy** (strategies.py) — el formato del reporte se elige en runtime. ReportGenerator delega a IReportStrategy sin condicionales. set_strategy() permite cambiar el formato en tiempo de ejecución sin reinstanciar nada.

# Principios SOLID aplicados

**SRP**: cada clase tiene una responsabilidad. WebApiAdapter solo traduce XML → ServiceStatus. MonitoringSystem solo orquesta. LatamCostCalculator solo define su factor.
**OCP**: agregar proveedor → registrar en ADAPTER_REGISTRY. Agregar región → crear subclase de CostCalculator. Agregar formato → crear subclase de IReportStrategy. El código existente no se toca.
**LSP**: los tres adaptadores son sustituibles donde se espera IMonitorAdapter. Las calculadoras son sustituibles donde se espera CostCalculator.
**ISP**: IMonitorAdapter define solo obtener_estado() + provider_name. No se fuerza a los adaptadores a implementar métodos que no necesitan.
**DIP**: MonitoringSystem depende de IMonitorAdapter (abstracción), no de WebApiAdapter ni de ningún concreto.

# Resiliencia — doble capa
Cada adaptador captura sus propias excepciones y retorna ServiceStatus(available=False, error=...). MonitoringSystem.collect_all() agrega una segunda capa para errores críticos no anticipados. En ambos casos se registra con logging (configurable externamente) y se continúa con los demás proveedores.


## Autor
- **Nombre:** Oriana Soledad Galindez
- **Materia:** Programación III

## Licencia
Uso académico.