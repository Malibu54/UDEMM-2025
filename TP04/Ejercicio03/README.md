# 📦 Sistema de Procesamiento de Pedidos – Empresa de Logística

El sistema permite clasificar, enviar y contabilizar registros según su tipo: **Entrega**, **Control de Calidad**, **Auditoría** o **NN (no clasificado)**.

---

## 📌 Requisitos

* Python 3.x
* El entorno debe incluir el módulo interno `agencia.pedidos`, que provee:

```python
from agencia.pedidos import get_pedidos, next, get_type, send_for_process
```

> 📎 Nota: Estas funciones son proporcionadas por el sistema de la empresa. Este repositorio asume su existencia.

---

## 🚀 Ejecución

```bash
python delivery.py
```

Al ejecutarse:

* Se procesan todos los registros provistos por `get_pedidos()`.
* Cada registro se envía a su procesador correspondiente.
* Se crean archivos `bitacora_<tipo>.log` con los datos procesados.
* Se imprime en consola un resumen total del procesamiento.

---

## 📊 Ejemplo de salida

```text
Resumen de procesamiento:
Entregas procesadas: 3521
Control de calidad procesadas: 2850
Auditorías procesadas: 1170
Total de registros procesados: 7541
```

---

## 🏗️ Estructura del Proyecto

Ejercicio03/
│
├── delivery.py         # Lógica principal del programa
└── README.md         # Este archivo

---

## 📄 Licencia

MIT License © 2025 — Oriana Galíndez 🎓 Universidad de la Marina Mercante
Este proyecto fue desarrollado con fines educativos como parte de un trabajo práctico.