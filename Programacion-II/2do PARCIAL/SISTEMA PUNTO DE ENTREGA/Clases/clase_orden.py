class Orden:
    def __init__(self, codigo, fecha, estado, duracion):
        self.codigo = codigo
        self.fecha = fecha
        self.estado = estado  # 'en proceso', 'finalizado', 'pausado', 'bloqueado'
        self.duracion = duracion  # en minutos
        self.detalles = []  # lista de (DetalleOrden, cantidad)
        self.pago = None

    def agregar_detalle(self, detalle, cantidad=1):
        if detalle.hay_stock(cantidad):
            detalle.descontar_stock(cantidad)
            for i, (det, cant) in enumerate(self.detalles):
                if det.nombre == detalle.nombre:
                    self.detalles[i] = (det, cant + cantidad)
                    return True
            self.detalles.append((detalle, cantidad))
            return True
        else:
            print(f"Producto {detalle.nombre} no está activo o no tiene stock suficiente.")
            return False

    def calcular_peso_total(self):
        peso_total = 0
        for detalle, cantidad in self.detalles:
            peso_total += detalle.peso * cantidad
        return peso_total

    def calcular_total_precio(self):
        total = 0
        for detalle, cantidad in self.detalles:
            total += detalle.precio_unitario * cantidad
        return total

    def calcular_iva(self):
        total_iva = 0
        for detalle, cantidad in self.detalles:
            total_iva += (detalle.precio_unitario * cantidad) * (detalle.impuesto / 100)
        return total_iva

    def ordenar_detalles_por_peso(self):
        n = len(self.detalles)
        for i in range(n):
            for j in range(0, n - i - 1):
                if self.detalles[j][0].peso > self.detalles[j + 1][0].peso:
                    self.detalles[j], self.detalles[j + 1] = self.detalles[j + 1], self.detalles[j]

    def ordenar_detalles_por_precio(self):
        n = len(self.detalles)
        for i in range(n):
            for j in range(0, n - i - 1):
                if self.detalles[j][0].precio_unitario > self.detalles[j + 1][0].precio_unitario:
                    self.detalles[j], self.detalles[j + 1] = self.detalles[j + 1], self.detalles[j]

    def asignar_pago(self, pago):
        self.pago = pago
