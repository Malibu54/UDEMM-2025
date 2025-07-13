class Administrador(Usuario):
    def __init__(self, nombre, apellido, dni, direccion):
        super().__init__(nombre, apellido, dni, direccion)
        self.ordenes = []  # Lista de órdenes

    def agregar_orden(self, orden):
        self.ordenes.append(orden)

    def total_ordenes_procesadas(self):
        total = 0
        for orden in self.ordenes:
            if orden.estado == 'finalizado':
                total += 1
        return total

    def bloquear_orden(self, codigo):
        for orden in self.ordenes:
            if orden.codigo == codigo:
                orden.estado = 'bloqueado'
                return True
        return False

    def total_items_orden(self, codigo):
        for orden in self.ordenes:
            if orden.codigo == codigo:
                total_items = 0
                for _, cantidad in orden.detalles:
                    total_items += cantidad
                return total_items
        return 0

    def max_duracion(self):
        max_dur = None
        for orden in self.ordenes:
            if max_dur is None or orden.duracion > max_dur:
                max_dur = orden.duracion
        return max_dur

    def min_duracion(self):
        min_dur = None
        for orden in self.ordenes:
            if min_dur is None or orden.duracion < min_dur:
                min_dur = orden.duracion
        return min_dur

    def top_ten_max_duracion(self):
        # Copiar lista de duraciones y códigos
        duraciones = []
        for orden in self.ordenes:
            duraciones.append((orden.duracion, orden.codigo))
        # Ordenar desc sin sorted ni max
        for i in range(len(duraciones)):
            for j in range(0, len(duraciones) - i - 1):
                if duraciones[j][0] < duraciones[j + 1][0]:
                    duraciones[j], duraciones[j + 1] = duraciones[j + 1], duraciones[j]
        return duraciones[:10]
