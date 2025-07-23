
# 📦 Reporte de Paquetes de Red

Este proyecto implementa un sistema de procesamiento y generación de reportes para una empresa de mensajería. La solución procesa más de 100,000 paquetes de red diarios, almacenando, consultando y exportando datos clave sobre los mismos.

---

## 🧾 Descripción

Cada paquete contiene los siguientes datos:

- ID del paquete
- Dirección IP
- Fecha
- Frecuencia de acceso
- Duración

El sistema permite:

- Procesar todos los paquetes recorriéndolos **una sola vez**
- Obtener las **2 direcciones IP con mayor frecuencia de acceso**
- Determinar la **IP con menor duración**
- Exportar un reporte detallado con:
  - Fecha
  - Dirección IP
  - Duración
  - Frecuencia de acceso
- Buscar paquetes por:
  - Dirección IP
  - Fecha
  - Frecuencia

---

## ⚙️ Estructura del Proyecto

- `Ejercicio02.py`: Lógica principal del sistema, estructurada con Programación Orientada a Objetos (POO).
- Clases principales:
  - `Paquete`: Representa un paquete de red.
  - `BaseDatos`: Simula una base de datos en memoria.
  - `Procesador`: Ejecuta el procesamiento de los paquetes.
  - `Reporte`: Contiene los resultados procesados.
  - `Exportador`: Interfaz abstracta para exportar.
  - `ExportadorConsola`: Exporta el reporte por consola.

---

## 🛠️ Requisitos

- Python 3.x
- No se requiere instalación de librerías externas.
- Se utiliza únicamente la biblioteca estándar de Python (`abc`).

> ⚠️ El sistema depende del módulo interno de la empresa:
```python
from net.network_payload import get_paquetes, next
````

Este módulo simula el acceso a los paquetes y **debe estar disponible en el entorno donde se ejecuta**.

---

## 🚀 Cómo usar

1. Ejecutar el archivo principal:

```bash
python Ejercicio02.py
```

2. El sistema mostrará:

* Un resumen general del procesamiento.
* El reporte exportado por consola.
* Ejemplos de búsqueda por IP y fecha.

---

## 🔍 Ejemplo de salida

```
Resumen del Reporte:
- Total duración de todos los paquetes: 120948
- Top 2 IPs con más frecuencia de acceso: [('192.168.0.1', 3200), ('10.0.0.4', 3100)]
- IP con menor duración: 192.168.0.254

Buscar por IP '192.168.0.1': [Paquete(...), Paquete(...)]
Buscar por fecha '2025-06-18': [Paquete(...), Paquete(...)]

---

## 🧪 Modo desarrollo / testing local

Si no encontas con el módulo `net.network_payload`, podes crear un mock manual para pruebas:

```python
# simulado_network_payload.py
def get_paquetes():
    return [
        (1, "192.168.0.1", "2025-06-18", 5, 10),
        (2, "192.168.0.2", "2025-06-18", 8, 7),
        ...
    ]

def next(lista):
    if lista:
        return lista.pop(0)
    return False
```

---

## 🏗️ Estructura del Proyecto

Ejercicio02/
│
├── Ejercicio02.py         # Lógica principal del programa
└── README.md         # Este archivo

---

## 📄 Licencia

MIT License © 2025 — Oriana Galíndez 🎓 Universidad de la Marina Mercante
Este proyecto fue desarrollado con fines educativos como parte de un trabajo práctico.