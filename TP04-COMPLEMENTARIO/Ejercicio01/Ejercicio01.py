from abc import ABC, abstractmethod
from typing import List

class Producto(ABC):
    """
    Clase base abstracta para todos los productos.
    Define la estructura general y obliga a implementar el método calcular_precio().
    """

    def __init__(self, nombre: str, modelo: str, fecha: str, precio: float):
        """
        Inicializa los atributos comunes a todos los productos.
        :param nombre: Nombre del producto
        :param modelo: Modelo del producto
        :param fecha: Fecha de creación o fabricación
        :param precio: Precio base del producto
        """
        self.nombre = nombre
        self.modelo = modelo
        self.fecha = fecha
        self.precio = precio

    @abstractmethod
    def calcular_precio(self) -> float:
        """
        Método abstracto para calcular el precio total del producto.
        Debe ser implementado por cada subclase.
        """
        pass


class ProductoFinal(Producto):
    """
    Clase que representa un producto final vendido directamente a consumidores.
    """

    def __init__(self, nombre: str, modelo: str, fecha: str, precio: float, pais: str):
        """
        Inicializa un producto final.
        :param pais: País donde se fabrica o distribuye el producto
        """
        super().__init__(nombre, modelo, fecha, precio)
        self.pais = pais

    def calcular_precio(self) -> float:
        """
        Calcula el precio del producto final.
        Fórmula: precio + 1.5
        """
        return self.precio + 1.5


class ProductoFabricante(Producto):
    """
    Clase que representa productos vendidos a fabricantes.
    Estos pueden depender de productos finales para su composición.
    """

    def __init__(self, nombre: str, modelo: str, fecha: str, precio: float,
                 cantidad: int, total_para_fabricar: float, dependencias: List[ProductoFinal]):
        """
        Inicializa un producto para fabricantes.
        :param cantidad: Cantidad de unidades vendidas
        :param total_para_fabricar: Costo total estimado para fabricar
        :param dependencias: Lista de productos finales necesarios para componer este producto
        """
        super().__init__(nombre, modelo, fecha, precio)
        self.cantidad = cantidad
        self.total_para_fabricar = total_para_fabricar
        self.dependencias = dependencias

    def calcular_precio(self) -> float:
        """
        Calcula el precio del producto para fabricantes.
        Fórmula: precio * cantidad + 3.5 + suma de los precios de las dependencias
        """
        precio_base = self.precio * self.cantidad + 3.5
        precio_dependencias = sum(dep.calcular_precio() for dep in self.dependencias)
        return precio_base + precio_dependencias


class ProductoMayorista(Producto):
    """
    Clase que representa productos vendidos al por mayor a distribuidores.
    """

    def __init__(self, nombre: str, modelo: str, fecha: str,
                 precio_por_unidad: float, lote: str, cantidad: int, sucursal: str):
        """
        Inicializa un producto mayorista.
        :param precio_por_unidad: Precio unitario del producto
        :param lote: Identificador del lote
        :param cantidad: Cantidad de unidades en el lote
        :param sucursal: Sucursal donde se distribuye
        """
        super().__init__(nombre, modelo, fecha, precio_por_unidad)
        self.lote = lote
        self.cantidad = cantidad
        self.sucursal = sucursal

    def calcular_precio(self) -> float:
        """
        Calcula el precio del producto mayorista.
        Fórmula: precio por unidad * cantidad * 1.7
        """
        return self.precio * self.cantidad * 1.7


# Ejemplo de uso de las clases
if __name__ == "__main__":
    # Crear productos finales
    final1 = ProductoFinal("Producto1", "M1", "2025-06-01", 100, "México")
    final2 = ProductoFinal("Producto2", "M2", "2025-06-05", 150, "Colombia")

    # Crear producto para fabricantes con dependencias
    fabricante = ProductoFabricante(
        nombre="ComponenteA",
        modelo="F1",
        fecha="2025-06-10",
        precio=50,
        cantidad=10,
        total_para_fabricar=500,
        dependencias=[final1, final2]
    )

    # Crear producto mayorista
    mayorista = ProductoMayorista(
        nombre="BulkProduct",
        modelo="B1",
        fecha="2025-06-15",
        precio_por_unidad=20,
        lote="L001",
        cantidad=100,
        sucursal="Sucursal Norte"
    )

    # Calcular y mostrar precios
    print(f"Precio Producto Final: {final1.calcular_precio():.2f}")
    print(f"Precio Producto Fabricante: {fabricante.calcular_precio():.2f}")
    print(f"Precio Producto Mayorista: {mayorista.calcular_precio():.2f}")
