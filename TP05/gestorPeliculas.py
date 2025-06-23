import json
import os
from datetime import datetime

FILE_PELICULAS = 'peliculas.json'
FILE_USUARIOS = 'usuarios.json'
FILE_REGISTROS = 'registros.json'

class Pelicula:
    def __init__(self, id, titulo, genero, descripcion, fecha, duracion):
        self.__id = id
        self.__titulo = titulo
        self.__genero = genero
        self.__descripcion = descripcion
        self.__fecha = fecha
        self.__duracion = duracion

    @property
    def id(self):
        return self.__id

    @property
    def titulo(self):
        return self.__titulo

    @titulo.setter
    def titulo(self, valor):
        if not valor:
            raise ValueError("El título no puede estar vacío")
        self.__titulo = valor

    @property
    def genero(self):
        return self.__genero

    @genero.setter
    def genero(self, valor):
        if not valor:
            raise ValueError("El género no puede estar vacío")
        self.__genero = valor

    @property
    def descripcion(self):
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor):
        self.__descripcion = valor

    @property
    def fecha(self):
        return self.__fecha

    @fecha.setter
    def fecha(self, valor):
        self.__fecha = valor

    @property
    def duracion(self):
        return self.__duracion

    @duracion.setter
    def duracion(self, valor):
        self.__duracion = valor

    def to_dict(self):
        return {
            'id': self.__id,
            'titulo': self.__titulo,
            'genero': self.__genero,
            'descripcion': self.__descripcion,
            'fecha': self.__fecha,
            'duracion': self.__duracion,
        }

class Usuario:
    def __init__(self, id, usuario, password, edad, ocupacion, genero, rol):
        self.__id = id
        self.__usuario = usuario
        self.__password = password
        self.__edad = edad
        self.__ocupacion = ocupacion
        self.__genero = genero
        self.__rol = rol  # 'admin' o 'usuario'

    @property
    def id(self):
        return self.__id

    @property
    def usuario(self):
        return self.__usuario

    def verificar_password(self, password):
        return self.__password == password

    @property
    def rol(self):
        return self.__rol

    def to_dict(self):
        return {
            'id': self.__id,
            'usuario': self.__usuario,
            'password': self.__password,
            'edad': self.__edad,
            'ocupacion': self.__ocupacion,
            'genero': self.__genero,
            'rol': self.__rol
        }

class RegistroPelicula:
    def __init__(self, id, id_pelicula, popularidad, votos, promedio_votos, ranking, fecha_actualizacion):
        self.__id = id
        self.__id_pelicula = id_pelicula
        self.__popularidad = popularidad
        self.__votos = votos
        self.__promedio_votos = promedio_votos
        self.__ranking = ranking
        self.__fecha_actualizacion = fecha_actualizacion

    @property
    def id(self):
        return self.__id

    @property
    def id_pelicula(self):
        return self.__id_pelicula

    @property
    def popularidad(self):
        return self.__popularidad

    @property
    def votos(self):
        return self.__votos

    @property
    def promedio_votos(self):
        return self.__promedio_votos

    @property
    def ranking(self):
        return self.__ranking

    @property
    def fecha_actualizacion(self):
        return self.__fecha_actualizacion

    def actualizar_voto(self, puntaje):
        if not (1 <= puntaje <= 5):
            raise ValueError("El puntaje debe estar entre 1 y 5.")
        total_votos = self.__votos + 1
        total_puntaje = self.__promedio_votos * self.__votos + puntaje
        promedio = total_puntaje / total_votos

        self.__votos = total_votos
        self.__promedio_votos = round(promedio, 2)
        self.__popularidad = round((self.__promedio_votos * self.__votos) / 10, 2)
        self.__fecha_actualizacion = datetime.now().strftime("%Y-%m-%d")

    def actualizar_ranking(self, nuevo_ranking):
        self.__ranking = nuevo_ranking

    def to_dict(self):
        return {
            'id': self.__id,
            'id_pelicula': self.__id_pelicula,
            'popularidad': self.__popularidad,
            'votos': self.__votos,
            'promedio_votos': self.__promedio_votos,
            'ranking': self.__ranking,
            'fecha_actualizacion': self.__fecha_actualizacion,
        }

class Sistema:
    def __init__(self):
        self.__peliculas = self.__cargar_peliculas()
        self.__usuarios = self.__cargar_usuarios()
        self.__registros = self.__cargar_registros()
        self.__usuario_logueado = None

    def __cargar_json(self, archivo):
        if not os.path.exists(archivo):
            return []
        with open(archivo, 'r', encoding='utf-8') as f:
            return json.load(f)

    def __guardar_json(self, archivo, datos):
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=2, ensure_ascii=False)

    def __cargar_peliculas(self):
        datos = self.__cargar_json(FILE_PELICULAS)
        return [Pelicula(**p) for p in datos]

    def __guardar_peliculas(self):
        datos = [p.to_dict() for p in self.__peliculas]
        datos.sort(key=lambda x: x['id'])
        self.__guardar_json(FILE_PELICULAS, datos)

    def __cargar_usuarios(self):
        datos = self.__cargar_json(FILE_USUARIOS)
        return [Usuario(**u) for u in datos]

    def __guardar_usuarios(self):
        datos = [u.to_dict() for u in self.__usuarios]
        datos.sort(key=lambda x: x['id'])
        self.__guardar_json(FILE_USUARIOS, datos)

    def __cargar_registros(self):
        datos = self.__cargar_json(FILE_REGISTROS)
        return [RegistroPelicula(**r) for r in datos]

    def __guardar_registros(self):
        datos = [r.to_dict() for r in self.__registros]
        datos.sort(key=lambda x: x['ranking'])
        self.__guardar_json(FILE_REGISTROS, datos)

    def login(self, usuario, password):
        for u in self.__usuarios:
            if u.usuario == usuario and u.verificar_password(password):
                self.__usuario_logueado = u
                return True
        return False

    def logout(self):
        self.__usuario_logueado = None

    def __es_admin(self):
        return self.__usuario_logueado and self.__usuario_logueado.rol == 'admin'

    def agregar_usuario(self, usuario, password, edad, ocupacion, genero, rol):
        if not self.__es_admin():
            raise PermissionError("Solo admin puede agregar usuarios.")
        nuevo_id = max([u.id for u in self.__usuarios], default=0) + 1
        nuevo_usuario = Usuario(nuevo_id, usuario, password, edad, ocupacion, genero, rol)
        self.__usuarios.append(nuevo_usuario)
        self.__guardar_usuarios()
        return nuevo_usuario

    def buscar_pelicula(self, nombre):
        return [p for p in self.__peliculas if nombre.lower() in p.titulo.lower()]

    def obtener_top_ten(self):
        # Ordenar registros por ranking ascendente (1 es mejor)
        registros_ordenados = sorted(self.__registros, key=lambda r: r.ranking)
        top_diez = registros_ordenados[:10]
        # Traer las películas relacionadas
        peliculas_top = []
        for reg in top_diez:
            pelicula = next((p for p in self.__peliculas if p.id == reg.id_pelicula), None)
            if pelicula:
                peliculas_top.append({
                    'pelicula': pelicula.to_dict(),
                    'registro': reg.to_dict()
                })
        return peliculas_top

    def agregar_pelicula(self, titulo, genero, descripcion, fecha, duracion):
        if not self.__es_admin():
            raise PermissionError("Solo admin puede agregar películas.")
        nuevo_id = max([p.id for p in self.__peliculas], default=0) + 1
        nueva = Pelicula(nuevo_id, titulo, genero, descripcion, fecha, duracion)
        self.__peliculas.append(nueva)
        self.__guardar_peliculas()

        nuevo_registro_id = max([r.id for r in self.__registros], default=0) + 1
        nuevo_registro = RegistroPelicula(
            nuevo_registro_id,
            nuevo_id,
            popularidad=0.0,
            votos=0,
            promedio_votos=0.0,
            ranking=len(self.__peliculas),
            fecha_actualizacion=datetime.now().strftime("%Y-%m-%d")
        )
        self.__registros.append(nuevo_registro)
        self.__guardar_registros()
        return nueva

    def eliminar_pelicula(self, id_pelicula):
        if not self.__es_admin():
            raise PermissionError("Solo admin puede eliminar películas.")
        self.__peliculas = [p for p in self.__peliculas if p.id != id_pelicula]
        self.__registros = [r for r in self.__registros if r.id_pelicula != id_pelicula]
        self.__guardar_peliculas()
        self.__guardar_registros()

def actualizar_pelicula(self, id_pelicula, **datos):
    if not self.__es_admin():
        raise PermissionError("Solo admin puede actualizar películas.")
    for p in self.__peliculas:
        if p.id == id_pelicula:
            if 'titulo' in datos:
                p.titulo = datos['titulo']
            if 'genero' in datos:
                p.genero = datos['genero']
            if 'descripcion' in datos:
                p._Pelicula__descripcion = datos['descripcion']  # acceso protegido 
            if 'fecha' in datos:
                p._Pelicula__fecha = datos['fecha']
            if 'duracion' in datos:
                p.duracion = datos['duracion']
            self.__guardar_peliculas()
            return p
    raise ValueError(f"No existe película con id {id_pelicula}")