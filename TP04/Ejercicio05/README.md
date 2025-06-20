# 🌳 Árbol Binario de Búsqueda con Persistencia en Disco

Este proyecto implementa un **Árbol Binario de Búsqueda (BST)** en Python usando **Programación Orientada a Objetos (OOP)**. Además, incluye funcionalidades para **persistir el árbol a disco** utilizando `pickle`.

---

## 🏗️ Estructura del Proyecto

Ejercicio05/
│
├── Ejercicio05.py         # Lógica principal del programa
└── README.md         # Este archivo

---

## ⚙️ Requisitos

- 🐍 Python 3.x
- 📦 No se requieren instalaciones adicionales

---

## ▶️ Ejecución

Para ejecutar el proyecto:

```bash
python Ejercicio05.py
````

👨‍💻 Esto realizará:

* Inserción aleatoria de los 1000 números
* Impresión parcial de los recorridos
* Búsqueda de valores
* Guardado del árbol en `arbol.pkl`

---

## 🧱 Estructura de Clases

* 🧩 `Serializable`: Interfaz abstracta para guardar/cargar estructuras
* 🌿 `Node`: Representa cada nodo del árbol
* 🌲 `BinarySearchTree`: Contiene lógica de inserción, búsqueda, recorridos y persistencia

---

## ❓ Preguntas Clave

### 📈 ¿Qué pasa si los números se insertan en orden?

🔴 El árbol se vuelve **degenerado** (como una lista enlazada), y las operaciones se vuelven **lentas** (O(n)).

### 🔁 ¿Y si se insertan en orden inverso?

🔴 Mismo problema: el árbol crece en una sola dirección, perdiendo eficiencia.

### ✅ ¿Solución?

⚖️ Insertar los valores en **orden aleatorio** (usando `random.shuffle`) para obtener un árbol **más balanceado** y eficiente.

---

## 💾 Persistencia

Guardar el árbol:

`
tree.save_to_file("arbol.pkl")
`

Cargar el árbol:

`
loaded_tree = BinarySearchTree.load_from_file("arbol.pkl")
`

---

## 📄 Licencia

MIT License © 2025 — Oriana Galíndez 🎓 Universidad de la Marina Mercante
Este proyecto fue desarrollado con fines educativos como parte de un trabajo práctico.