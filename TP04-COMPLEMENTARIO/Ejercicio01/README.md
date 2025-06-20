# 🏭 Sistema de Gestión de Productos - POO en Python

Este proyecto implementa un sistema de gestión para una empresa manufacturera que transforma materias primas en productos elaborados, utilizando **Programación Orientada a Objetos (POO)** en Python.

Se contemplan tres tipos de productos:

* **Producto Final**: Vendido directamente al consumidor.
* **Producto Fabricante**: Vendido a otras empresas para su integración en productos más complejos. Puede incluir productos finales como dependencias.
* **Producto Mayorista**: Vendido en grandes cantidades a sucursales o distribuidores externos.

---

## 🏗️ Estructura del Proyecto

```plaintext
Ejercicio01/
│
├── Ejercicio01.py         # Lógica principal del programa
└── README.md              # Este archivo
```

---

## 📚 Requisitos

* Python 3.x
* No se requieren librerías externas

---

## 🚀 Ejecución

Ejecuta el archivo principal desde la línea de comandos:

```bash
python Ejercicio01.py
```

Se mostrarán en consola los cálculos de precios para diferentes tipos de productos utilizando ejemplos integrados.

---

## 🧠 Lógica del Cálculo de Precios

| Tipo de Producto    | Fórmula del Precio                                          |
| ------------------- | ----------------------------------------------------------- |
| Producto Final      | `precio + 1.5`                                              |
| Producto Fabricante | `precio * cantidad + 3.5 + suma de precios de dependencias` |
| Producto Mayorista  | `precio por unidad * cantidad * 1.7`                        |

---

## 📦 Clases Principales

* `Producto`: Clase base abstracta con el método `calcular_precio()`.
* `ProductoFinal`: Hereda de `Producto`. Representa productos de consumo directo.
* `ProductoFabricante`: Hereda de `Producto`. Puede tener dependencias de tipo `ProductoFinal`.
* `ProductoMayorista`: Hereda de `Producto`. Representa productos en lote para sucursales.

---

## ✅ Ejemplo de Salida Esperada

```plaintext
Precio Producto Final: 101.5
Precio Producto Fabricante: 1218.5
Precio Producto Mayorista: 3400.0
```

---

## 📄 Licencia

MIT License © 2025 — Oriana Galíndez 🎓 Universidad de la Marina Mercante
Este proyecto fue desarrollado con fines educativos como parte de un trabajo práctico.

---


