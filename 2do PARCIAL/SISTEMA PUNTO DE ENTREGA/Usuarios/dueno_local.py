class DuenoLocal(Usuario):
    def __init__(self, nombre, apellido, dni, direccion):
        super().__init__(nombre, apellido, dni, direccion)
        self.locales = []  # lista de locales (ej: nombre, dimensiones)
        self.ordenes = []  # órdenes del dueño

    def agregar_local(self, nombre_local, dimensiones):
        self.locales.append({'nombre': nombre_local, 'dimensiones': dimensiones})

    def cantidad_locales(self):
        total = 0
        for _ in self.locales:
            total += 1
        return total

    def agregar_orden(self, orden):
        self.ordenes.append(orden)

    def cantidad_ordenes_en_proceso(self):
        total = 0
        for orden in self.ordenes:
            if orden.estado != 'bloqueado' and orden.estado == 'en proceso':
                total += 1
        return total

    def cantidad_ordenes_finalizadas(self):
        total = 0
        for orden in self.ordenes:
            if orden.estado == 'finalizado':
                total += 1
        return total

    def actualizar_estado_orden(self, codigo, nuevo_estado):
        for orden in self.ordenes:
            if orden.codigo == codigo:
                orden.estado = nuevo_estado
                return True
        return False
