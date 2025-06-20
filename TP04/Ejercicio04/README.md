
# 📊 Sistema de Clasificación y Top 10 de Ventas

Este proyecto en Python implementa un sistema orientado a objetos para clasificar registros de ventas almacenados en una tabla de dimensiones `N x M`, y obtener el **Top 10 de ventas con mayor valor**.

## ✅ Objetivos

- Utilizar **Programación Orientada a Objetos (OOP)**.
- No usar librerías externas (excepto `abc`, `random`, `datetime`).
- Clasificar las filas de ventas en **tres listas** basadas en la cantidad de ventas.
- Generar un **Top 10** de ventas con mayor valor.

---

## 🧩 Estructura del Proyecto

- `VentaBase`: Clase abstracta que define la interfaz de una venta.
- `Venta`: Representa una venta con `id`, `valor` y `fecha`.
- `TablaVentas`: Genera y almacena una tabla de objetos `Venta`.
- `GestorVentas`: Clasifica las filas de la tabla en listas y extrae el Top 10 de mayor valor.

---

## 📦 Criterios de Clasificación

Cada fila se asigna a una lista según la **cantidad de ventas (columnas)** que contiene:

- **Lista 1**: si ventas `≥ 100` y `≤ 150`
- **Lista 2**: si ventas `≥ 50` y `< 100`
- **Lista 3**: si ventas `≥ 0` y `< 50`

---

## 🚀 Cómo Ejecutar el Programa

1. Asegúrate de tener Python 3 instalado.
2. Clona este repositorio.
3. Ejecuta el archivo principal:

```bash
python top-ten.py
```
Puedes modificar los valores de `N` (filas) y `M` (ventas por fila) en el bloque `if __name__ == "__main__"` para probar distintas configuraciones.

---

## 📌 Ejemplo de Salida

```
Top 10 Ventas de Mayor Valor:
Venta(ID: 45, Valor: 998.23, Fecha: 2025-06-20)
Venta(ID: 12, Valor: 985.75, Fecha: 2025-06-20)
...
```

---

## 📚 Dependencias Permitidas

* `abc` – para clases abstractas.
* `random` – para simular valores de ventas.
* `datetime` – para asignar fechas.

---

## 🏗️ Estructura del Proyecto

Ejercicio04/
│
├── top-ten.py         # Lógica principal del programa
└── README.md          # Este archivo

---

## 📄 Licencia

MIT License © 2025 — Oriana Galíndez 🎓 Universidad de la Marina Mercante
Este proyecto fue desarrollado con fines educativos como parte de un trabajo práctico.

