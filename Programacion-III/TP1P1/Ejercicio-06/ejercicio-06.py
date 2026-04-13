# ── ¿Cómo lo haría teniendo en cuenta que solo puede existir una sola instancia?
"""
EN este caso, como Singleton solo tiene una instancia y aca necesiramos potencialmente conexion por motores podemos tomar dos puntos:

1- Singleton Multiton con un registro interno 'dict' donde la clave sea el nombre del motor y por cada motor exista su propia instancia única

_instances = {
    "postgresql": <instancia>,
    "mysql":      <instancia>,
    "mssql":      <instancia>,
}
2- Singleton con motor de configuración donde exisre solo una instancia que recibe el motor como parametro en la configuracion, es decir, una conexión por vez siendo esta opcíón más restrictiva.
"""

# ── ¿Qué consideraciones evaluaría a la hora de implementarlo?
"""
A la hora de implementarlo se evaluaria si la conexión se abre al crear una instancia, quien es el responsable de cerrarla y si se necesita reconexión al servidor por timeout de forma inmediata
En cuanto a la concurrencia tendria en cuenta usar connection pool y no una conexión directa encapsulando el pool y no la conexión individual.
Y por último, teniedo en cuenta los motores, como cada motor tiene su propio driver, el diseño debe abstraer esto mediante interfaz común.
"""

# ── ¿Qué consecuencias cree que tendría tener varias instancias de la DB?
"""
Las consecuencias que tendría tener varias instancia de la DB podrian ser
 -Saturación de conexiones al servidor
 -overhead de memoria y CPU cuando cada instancia mantiene su propio estado, buffers y metadatos de conexión
"""

# ── ¿Qué pasa con las conexiones TCP?
"""
Con las conexiones TCp es que en cada instancia el gestor abre conexiones TCP hacia el servidor. Si no aplicamos Singleton pasaria:
-En cada unstancia consume file descriptor del sistema operativo
-El servidor de BD lanza un proceso'hilo por conexión y Postges hace fork()por cada uno de ellos
-Con instancias accidentales se puede llegar al limite del servidor sin que la aplicación lo requiera

"""