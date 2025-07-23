# Crear detalles de productos
d1 = DetalleOrden("ProdA", "Producto A", 100, stock=5, impuesto=10, activo=True, peso=2.5)
d2 = DetalleOrden("ProdB", "Producto B", 200, stock=10, impuesto=5, activo=True, peso=1.0)
d3 = DetalleOrden("ProdC", "Producto C", 150, stock=2, impuesto=10, activo=True, peso=3.0)

# Crear orden y agregar detalles
orden1 = Orden("O123", "2025-07-02", "en proceso", 45)
orden1.agregar_detalle(d1, 3)
orden1.agregar_detalle(d2, 1)

orden2 = Orden("O124", "2025-07-03", "finalizado", 30)
orden2.agregar_detalle(d3, 2)

# Asignar pagos
pago1 = PagoEfectivo(500)
orden1.asignar_pago(pago1)

pago2 = PagoTarjeta(300, banco="Banco X", fecha="2025-07-02", autorizada=True, tipo_tarjeta="crédito")
orden2.asignar_pago(pago2)

# Crear usuarios
admin = Administrador("Admin", "Principal", "12345678", "Calle Falsa 123")
admin.agregar_orden(orden1)
admin.agregar_orden(orden2)

dueno = DuenoLocal("Juan", "Perez", "87654321", "Av Siempre Viva 742")
dueno.agregar_local("Local1", "100m2")
dueno.agregar_orden(orden1)
dueno.agregar_orden(orden2)

repartidor = Repartidor("Carlos", "Lopez", "11223344", "Calle Real 456", tipo_vehiculo="moto")
repartidor.finalizar_orden(orden1)

# Reportes
print("Total ordenes procesadas por admin:", admin.total_ordenes_procesadas())
print("Max duración orden:", admin.max_duracion())
print("Top ten duraciones:", admin.top_ten_max_duracion())
print("Cantidad locales dueño:", dueno.cantidad_locales())
print("Ordenes en proceso dueño:", dueno.cantidad_ordenes_en_proceso())
print("Ordenes finalizadas dueño:", dueno.cantidad_ordenes_finalizadas())
print("Ordenes finalizadas repartidor:", repartidor.cantidad_ordenes_finalizadas())
