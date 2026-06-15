# CU-01: Crear Nota de Inteligencia de Mercado
## Actor Principal

Analista

## Descripción

Permite a un analista registrar una nueva nota de inteligencia de mercado en el sistema.

## Flujo Principal
1. El analista accede al sistema.
2. Selecciona la opción "Crear Nota".
3. Ingresa título, contenido y categoría.
4. El sistema valida la información.
5. El sistema almacena la nota.
6. La nota queda disponible para consulta.


# CU-02: Revisar Nota
## Actor Principal

Gerente

## Descripción

Permite a un gerente revisar una nota creada por un analista.

## Flujo Principal
1. El gerente visualiza las notas pendientes.
2. Selecciona una nota.
3. Revisa el contenido.
4. Marca la nota como revisada.
5. El sistema registra la revisión.


# CU-03: Marcar Nota como DEPRECATED
## Actor Principal

Administrador

## Precondición

La nota debe haber sido revisada por un gerente.

## Descripción

Permite cambiar el estado de una nota a DEPRECATED cuando la información ya no es válida o relevante.

## Flujo Principal
1. El administrador selecciona una nota.
2. Solicita marcarla como DEPRECATED.
3. El sistema verifica que la nota haya sido revisada por un gerente.
4. El sistema actualiza la categoría.

## Flujo Alternativo

3a. La nota no fue revisada.

El sistema rechaza la operación.
Muestra mensaje de error.


# CU-04: Consultar y Filtrar Notas
## Actor Principal

Gerente

## Descripción

Permite buscar notas utilizando diferentes criterios de filtrado.

## Flujo Principal
1. El gerente accede a la consulta de notas.
2. Selecciona filtros.
3. El sistema aplica los criterios.
4. Se muestran los resultados.


# CU-05: Exportar Información
## Actor Principal

Gerente

## Descripción

Permite exportar los resultados de una consulta en distintos formatos.

## Flujo Principal
1. El gerente realiza una búsqueda.
2. Selecciona el formato de exportación.
3. El sistema genera el archivo.
4. El usuario descarga el resultado.

Formatos
PDF
CSV
JSON


# CU-06: Notificar Nota Emergente
## Actor Principal

Sistema

## Descripción

Cuando una nota es clasificada como EMERGENTE, el sistema debe notificar automáticamente a los gerentes.

## Flujo Principal
1. Un analista registra una nota EMERGENTE.
2. El sistema detecta la categoría.
3. Se activan las notificaciones.
4. Los gerentes reciben el aviso.
