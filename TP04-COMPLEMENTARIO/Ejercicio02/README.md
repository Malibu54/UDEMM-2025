# 💾 Persistencia de Datos para Dispositivos IoT - POO en Python

Este proyecto implementa una solución orientada a objetos en Python para gestionar diferentes tipos de persistencia de datos en dispositivos IoT. La solución permite almacenar información de forma persistente en memoria RAM, archivos con journaling y archivos cifrados, manteniendo una interfaz común y simple (`save(datos)`), facilitando la extensión a otros tipos de persistencia en el futuro (flash, remota, etc.).

---

## 🏗️ Estructura del Proyecto

```plaintext
Ejercicio02/
│
├── Ejercicio02.py         # Lógica principal del programa
└── README.md              # Este archivo
```

---

## 📚 Requisitos

* Python 3.x
* No se requieren librerías externas

---

## 🚀 Uso básico

Ejemplo de cómo cambiar dinámicamente el tipo de persistencia sin modificar la interfaz:

```python
from Ejercicio02 import Memoria, Archivo, Cifrado

# Persistencia en RAM
persistencia = Memoria()
persistencia.save("Datos en RAM")

# Cambiar a persistencia por archivo
persistencia = Archivo(nombre="datos.txt", path_fisico=".", journal_enabled=True)
persistencia.save("Datos en archivo")

# Cambiar a persistencia cifrada
persistencia = Cifrado(nombre="datos_cif.txt", path_original=".", path_cifrado=".")
persistencia.save("Datos confidenciales")
```

---

## 📝 Descripción de Clases

* `Persistencia`: Clase abstracta que define la interfaz común `save(datos)` y `get_datos()`.
* `Memoria`: Persistencia en RAM simulada.
* `Archivo`: Persistencia en archivo con soporte para journaling.
* `Cifrado`: Persistencia en archivo con cifrado simple.

---

## 📄 Licencia

MIT License © 2025 — Oriana Galíndez 🎓 Universidad de la Marina Mercante
Este proyecto fue desarrollado con fines educativos como parte de un trabajo práctico.

