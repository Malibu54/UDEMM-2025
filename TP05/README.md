# UdeMM - Licenciatura en Administración de Sistemas (FAE) 

Trabajo práctico número 05 ¡Perfecto! Aquí te dejo un README con emojis y comentarios más amigables, reflejando el propósito del proyecto según el enunciado que me pasaste:


## 🎬 Sistema de Gestión de Películas

### 🚀 Descripción

Este proyecto nace para **mejorar la gestión actual de películas**, que hasta ahora se hacía de forma manual y con Excel. El objetivo es tener una **aplicación backend robusta y escalable**, que permita manejar miles de registros, varios usuarios con distintos roles, y facilite futuras integraciones con sistemas web y aplicaciones de machine learning.  

Actualmente, la gestión de películas, usuarios y sus votos se realiza manualmente, lo que genera lentitud y errores. Este sistema automatiza el proceso, agiliza las búsquedas, ABM de películas y usuarios, y permite procesar lotes de datos estadísticos (popularidad, votos, ranking) de forma dinámica y ordenada.  

---

### 🛠 Funcionalidades principales

- 📁 **Migración de Excel a JSON** para manejar la información de forma más dinámica.
- 🔐 **Autenticación y roles**: admin y usuario normal.
- 🎥 **ABM de películas**: agregar, modificar, eliminar y buscar.
- 🔝 **Top 10 películas** según ranking y votos.
- 👥 **Gestión de usuarios** con diferentes permisos.
- 🗳️ **Votación colaborativa**: usuarios pueden votar y actualizar el puntaje.
- 📥 **Procesamiento de lotes** para importar registros de popularidad y votos.
- 🔄 **Preparado para interoperabilidad futura** con servicios web y machine learning.

---

### 📂 Estructura del proyecto

- `peliculas.json`: datos de películas.
- `usuarios.json`: datos de usuarios y roles.
- `registros.json`: registros estadísticos de cada película.
- `gestorPeliculas.py`: lógica backend con clases y métodos para la gestión.

---

### 🎯 Modelo de Dominio

- **Pelicula**: datos básicos y atributos de cada película.
- **Usuario**: información personal y rol para control de acceso.
- **RegistroPelicula**: popularidad, votos y ranking que acompañan a cada película.
- **Sistema**: coordina todas las operaciones y guarda los datos en archivos JSON.

---

### ⚙️ Requisitos

- Python 3.7+
- Solo módulos estándar de Python (sin librerías externas).

---

### 🧑‍💻 Cómo usar

1. Colocar los archivos JSON (`peliculas.json`, `usuarios.json`, `registros.json`) en la carpeta del script.
2. Ejecutar el script principal (por ejemplo, importar y usar la clase `Sistema`).
3. Autenticarse con un usuario registrado.
4. Usar métodos para:
   - Buscar películas por nombre.
   - Obtener el Top 10 de películas.
   - Agregar, modificar o eliminar películas.
   - Agregar usuarios (solo admin).
   - Votar películas.
   - Importar lotes de datos estadísticos.

---

## 💡 Notas importantes

- Las variables de instancia están protegidas para mantener la integridad y evitar accesos directos.
- La solución es extensible, pensada para crecer e integrarse con sistemas futuros.
- El backend está desacoplado del frontend, por lo que puede adaptarse a cualquier tipo de interfaz gráfica o entorno operativo.

---


## 📄 Licencia

[MIT](https://choosealicense.com/licenses/mit/) © 2025 — Oriana Galíndez 🎓 Universidad de la Marina Mercante
Este proyecto fue desarrollado con fines educativos como parte de un trabajo práctico.