# 🧮 Generador de Matriz Identidad en Python (POO)

Este proyecto implementa un generador de **matrices identidad** utilizando **Programación Orientada a Objetos (POO)** en Python. Se hace uso de clases abstractas para definir una interfaz base para las matrices, y una clase concreta que construye la matriz identidad de tamaño `n x n`.

---

## 🏗️ Estructura del Proyecto

Ejercicio06/
│
├── Ejercicio06.py         # Lógica principal del programa
└── README.md         # Este archivo

---

## 📚 Requisitos

- Python 3.x
- No se requieren librerías externas

---

## ⚙️ Uso

Podes ejecutar el programa directamente desde la terminal:

```bash
python Ejercicio06.py
````

El programa construirá una matriz identidad del tamaño indicado (podes modificar el valor en el código).

---

## 📌 Ejemplo de salida (n = 4)

[1, 0, 0, 0]
[0, 1, 0, 0]
[0, 0, 1, 0]
[0, 0, 0, 1]

---

## 🧱 Detalles de implementación

* `Matriz` es una **clase abstracta** que define los métodos `construir()` y `mostrar()`.
* `MatrizIdentidad` hereda de `Matriz` y genera correctamente la matriz identidad.
* Toda la lógica está en un solo archivo para simplicidad y cumplimiento de requisitos académicos.

---

## 📄 Licencia

MIT License © 2025 — Oriana Galíndez 🎓 Universidad de la Marina Mercante
Este proyecto fue desarrollado con fines educativos como parte de un trabajo práctico.


