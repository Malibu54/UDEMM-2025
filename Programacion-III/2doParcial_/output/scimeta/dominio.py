from datetime import date

class Autor:
    
    def __init__(self, id_autor, nombre, apellido, afiliacion,
                 fecha_registro, activo=True, bloqueado=False,
                 publicaciones_count=0):
        self.__id = id_autor
        self.__nombre = nombre
        self.__apellido = apellido
        self.__afiliacion = afiliacion
        self.__activo = activo
        self.__bloqueado = bloqueado
        self.__publicaciones_count = publicaciones_count
        self.__fecha_registro = fecha_registro

    @property
    def id(self):
        return self.__id

    @property
    def nombre(self):
        return self.__nombre

    @property
    def apellido(self):
        return self.__apellido

    @property
    def afiliacion(self):
        return self.__afiliacion

    @property
    def activo(self):
        return self.__activo

    @property
    def bloqueado(self):
        return self.__bloqueado

    @property
    def publicaciones_count(self):
        return self.__publicaciones_count

    @property
    def fecha_registro(self):
        return self.__fecha_registro

    def activar(self):
        if self.__bloqueado:
            raise ValueError(
                "No se puede activar un autor bloqueado.")
        self.__activo = True

    def desactivar(self):
        self.__activo = False

    def bloquear(self):
        self.__bloqueado = True
        self.__activo = False

    def desbloquear(self):
        self.__bloqueado = False

    def nombre_completo(self):
        return f"{self.__nombre} {self.__apellido}".strip()

    def antiguedad_en_anios(self, fecha_actual=None):
        if fecha_actual is None:
            fecha_actual = date.today()
        anios = fecha_actual.year - self.__fecha_registro.year
        aniversario_pendiente = (
            (fecha_actual.month, fecha_actual.day) <
            (self.__fecha_registro.month, self.__fecha_registro.day)
        )
        if aniversario_pendiente:
            anios -= 1
        return max(anios, 0)

    def incrementar_publicaciones(self):

        self.__publicaciones_count += 1

    def __repr__(self):
        return f"Autor({self.nombre_completo()!r})"

class DocumentoCientifico:

    def __init__(self, id_documento, titulo, resumen,
                 fecha_publicacion, path_documento, nombre_documento,
                 likes=0, activo=True, autores=None):
        self.__id = id_documento
        self.__titulo = titulo
        self.__resumen = resumen
        self.__fecha_publicacion = fecha_publicacion
        self.__path_documento = path_documento
        self.__nombre_documento = nombre_documento
        self.__likes = likes
        self.__activo = activo
        self.__autores = list(autores) if autores else []

    @property
    def id(self):
        return self.__id

    @property
    def titulo(self):
        return self.__titulo

    @property
    def resumen(self):
        return self.__resumen

    @property
    def fecha_publicacion(self):
        return self.__fecha_publicacion

    @property
    def path_documento(self):
        return self.__path_documento

    @property
    def nombre_documento(self):
        return self.__nombre_documento

    @property
    def likes(self):
        return self.__likes

    @property
    def autores(self):
        # Se devuelve una copia para no exponer la lista interna.
        return list(self.__autores)

    # --- Comportamiento propio de la entidad ---

    def esta_activo(self):
        return self.__activo

    def activar(self):
        self.__activo = True

    def desactivar(self):
        self.__activo = False

    def agregar_autor(self, autor):

        if any(autor_actual.id == autor.id
               for autor_actual in self.__autores):
            return
        self.__autores.append(autor)

    def agregar_autores(self, autores):

        for autor in autores:
            self.agregar_autor(autor)

    def obtener_extension(self):

        if "." not in self.__nombre_documento:
            return ""
        partes = self.__nombre_documento.rsplit(".", 1)
        return "." + partes[-1].lower()

    def tiene_atributos_completos(self):

        atributos_obligatorios = [
            self.__id, self.__titulo, self.__resumen,
            self.__fecha_publicacion, self.__path_documento,
            self.__nombre_documento,
        ]
        todos_presentes = all(
            atributo is not None and str(atributo).strip() != ""
            for atributo in atributos_obligatorios
        )
        return todos_presentes and len(self.__autores) > 0

    def sumar_like(self):
        self.__likes += 1

    def __repr__(self):
        return (f"DocumentoCientifico(id={self.__id}, "
                f"titulo={self.__titulo!r})")