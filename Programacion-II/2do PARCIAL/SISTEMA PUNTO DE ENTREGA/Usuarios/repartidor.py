class Repartidor(Usuario):
    def __init__(self, nombre, apellido, dni, direccion, tipo_vehiculo):
        super().__init__(nombre, apellido, dni, direccion)
        self.tipo_vehiculo = tipo_vehiculo
        self.ordenes_finalizadas = 0

    def finalizar_orden(self, orden):
        if orden.estado == 'en proceso':
            orden.estado = 'finalizado'
            self.ordenes_finalizadas += 1
            return True
        return False

    def cantidad_ordenes_finalizadas(self):
        return self.ordenes_finalizadas
