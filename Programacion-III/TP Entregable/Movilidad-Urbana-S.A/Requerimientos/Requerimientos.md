# Requerimientos del sistema de gestión de estacionamiento


## Requerimientos funcionales

### Acceso y tickets

| ID | Título | Descripción |
|----|--------|-------------|
| RF-01 | Emisión de ticket de ingreso | Al acercarse a la barrera de entrada, el sistema emite automáticamente un ticket impreso con fecha, hora de llegada y código QR/barras que identifica al cliente. |
| RF-02 | Control de barrera de entrada | La barrera se abre tras ser emitido el ticket y se cierra una vez que el vehículo ingresa al predio. |
| RF-03 | Control de barrera de salida | La barrera de salida se abre únicamente luego de que el pago ha sido confirmado correctamente. |

### Gestión de capacidad

| ID | Título | Descripción |
|----|--------|-------------|
| RF-04 | Registro en tiempo real de vehículos | El sistema mantiene un conteo exacto y actualizado de la cantidad de vehículos presentes en el edificio en todo momento. |
| RF-05 | Detección de capacidad máxima | Cuando se alcanza el límite de vehículos, el sistema activa el mensaje de "Estacionamiento lleno" en los paneles de entrada y en las pantallas del piso de acceso. |

### Gestión de espacios

| ID | Título | Descripción |
|----|--------|-------------|
| RF-06 | Gestión de tipos de espacios | El sistema administra espacios diferenciados: compactos, grandes, movilidad reducida, motos, vehículos eléctricos, vehículos autónomos y compartidos. |
| RF-07 | Asignación automática de espacio | El sistema asigna a cada vehículo un espacio acorde a su tipo y dimensiones según las reglas de negocio configuradas. |
| RF-08 | Liberación de espacio al egreso | Al salir el vehículo, el sistema retira la asignación y actualiza la disponibilidad en tiempo real. |

### Pantallas informativas

| ID | Título | Descripción |
|----|--------|-------------|
| RF-09 | Pantalla por piso con disponibilidad | Cada piso muestra en tiempo real la cantidad de espacios disponibles desglosados por tipo de vehículo, visible desde las rampas de acceso. |
| RF-10 | Paneles de entrada/salida | Los paneles de la entrada principal y piso de acceso muestran disponibilidad general, mensajes de lleno y confirmaciones de pago. |

### Tarifas progresivas y pagos

| ID | Título | Descripción |
|----|--------|-------------|
| RF-11 | Cálculo de tarifa progresiva | La tarifa se calcula automáticamente: $6.000 la primera hora, $5.500 la segunda y tercera hora, $1.750 cada hora adicional. |
| RF-12 | Pago en efectivo con asistente | El asistente de estacionamiento puede recibir pagos en efectivo en los puntos de salida, registrando la transacción a nombre del cliente. |
| RF-13 | Pago digital en máquinas automáticas | Los clientes pueden pagar con tarjeta de crédito, débito o billetera virtual en máquinas automáticas de salida. |

### Vehículos eléctricos

| ID | Título | Descripción |
|----|--------|-------------|
| RF-14 | Habilitación de carga eléctrica por ticket | El ticket de ingreso habilita automáticamente la estación de carga eléctrica del espacio asignado. |
| RF-15 | Cobro de energía consumida | El sistema calcula y añade al monto de egreso el costo de la energía eléctrica consumida durante la estadía. |

### Administración del sistema

| ID | Título | Descripción |
|----|--------|-------------|
| RF-16 | Configuración de estructura física | El administrador puede agregar pisos, modificar la cantidad y tipo de espacios por nivel, y gestionar paneles de entrada/salida desde el software. |
| RF-17 | Alta y baja de personal | El administrador puede registrar o eliminar cuentas de asistentes de estacionamiento, controlando el acceso a las funciones operativas. |

### Asistente y operaciones

| ID | Título | Descripción |
|----|--------|-------------|
| RF-18 | Operación en nombre del cliente | El asistente puede realizar todas las acciones que normalmente haría el cliente (recibir pagos, gestionar tickets, aclarar dudas), sin perder trazabilidad de quién ejecutó cada acción. |

### Tipos de vehículos y multimodalidad

| ID | Título | Descripción |
|----|--------|-------------|
| RF-19 | Registro de múltiples tipos de vehículo | El sistema distingue y gestiona automóviles, camiones, furgonetas, motocicletas, vehículos eléctricos, autónomos y de flotas compartidas. |
| RF-20 | Zonas de intercambio modal | El sistema gestiona zonas donde el usuario puede dejar su auto mientras usa taxi, bicicleta o moto, integrando múltiples modos de transporte. |

---

## Requerimientos no funcionales

### Rendimiento

| ID | Título | Descripción |
|----|--------|-------------|
| RNF-01 | Actualización en tiempo real | Las pantallas de disponibilidad por piso y paneles de entrada/salida deben reflejar cambios de ocupación de forma inmediata, sin demoras perceptibles. |
| RNF-10 | Soporte de múltiples entradas simultáneas | El sistema debe procesar el ingreso y egreso de vehículos de forma concurrente a través de las distintas barreras, sin degradar el tiempo de respuesta en horarios pico. |
| RNF-14 | Generación de tickets sin latencia | El tiempo entre la llegada del vehículo a la barrera y la emisión del ticket debe ser mínimo para no generar colas en horas pico. |

### Disponibilidad

| ID | Título | Descripción |
|----|--------|-------------|
| RNF-02 | Alta disponibilidad operativa | El sistema debe operar de forma continua (24/7). Cualquier caída debe recuperarse automáticamente o con mínima intervención. |

### Escalabilidad

| ID | Título | Descripción |
|----|--------|-------------|
| RNF-03 | Soporte para múltiples pisos y espacios | La arquitectura debe permitir incorporar nuevos pisos y categorías de espacios sin rediseño del sistema, acompañando la expansión física del edificio. |

### Seguridad

| ID | Título | Descripción |
|----|--------|-------------|
| RNF-04 | Control de acceso por roles | Cada actor (administrador, asistente, cliente, sistema) debe tener permisos diferenciados. El sistema debe registrar quién realizó cada transacción (trazabilidad). |
| RNF-05 | Protección de datos de pago | Los datos de tarjetas y billeteras virtuales deben manejarse conforme a estándares de seguridad (ej. PCI-DSS), sin almacenamiento local de información sensible. |

### Usabilidad

| ID | Título | Descripción |
|----|--------|-------------|
| RNF-06 | Flujo sin fricción para el cliente | El proceso de ingreso y egreso debe ser simple e intuitivo, evitando largas filas. Las pantallas deben ser legibles desde vehículos en movimiento y desde las rampas. |
| RNF-07 | Accesibilidad | Las interfaces y espacios físicos reservados para personas con movilidad reducida deben cumplir normativas de accesibilidad vigentes. |

### Confiabilidad

| ID | Título | Descripción |
|----|--------|-------------|
| RNF-08 | Integridad del conteo de vehículos | El registro de vehículos presentes no debe desincronizarse ante fallas parciales (cortes de luz, errores de sensor). Debe contemplar mecanismos de reconciliación. |

### Mantenibilidad

| ID | Título | Descripción |
|----|--------|-------------|
| RNF-09 | Configuración sin redeploy | El administrador debe poder modificar la estructura del estacionamiento (pisos, tipos de espacios, tarifas) desde la interfaz sin necesidad de intervención técnica. |

### Integración

| ID | Título | Descripción |
|----|--------|-------------|
| RNF-11 | Compatibilidad con medios de pago digitales | El sistema debe integrarse con procesadores de tarjetas de crédito/débito y billeteras virtuales vigentes en el mercado local. |

### Extensibilidad

| ID | Título | Descripción |
|----|--------|-------------|
| RNF-12 | Base para almacenamiento inteligente futuro | La arquitectura debe contemplar la incorporación futura de IA y sensores para gestión de espacios de bicis y motos sin reescribir el núcleo del sistema. |

### Auditoria
| ID | Título | Descripción |
|----|--------|-------------|
| RNF-13 | Registro de transacciones | Cada operación (ingreso, pago, acción de asistente) debe quedar registrada con usuario, timestamp y detalle, para auditoría y resolución de disputas. |

---

*Total: 20 requerimientos funcionales · 14 requerimientos no funcionales ·*