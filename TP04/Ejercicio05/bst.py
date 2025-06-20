import pickle
import os
from abc import ABC, abstractmethod

class Serializable(ABC):
    """
    Interfaz abstracta para clases que pueden ser serializadas.
    """
    @abstractmethod
    def save_to_file(self, filename: str):
        pass

    @abstractmethod
    def load_from_file(self, filename: str):
        pass


class Node:
    """
    Clase que representa un nodo en el árbol binario.
    """
    def __init__(self, value: int):
        self.value = value
        self.left = None  # Hijo izquierdo
        self.right = None  # Hijo derecho


class BinarySearchTree(Serializable):
    """
    Implementación de un árbol binario de búsqueda con funcionalidad de persistencia.
    """
    def __init__(self):
        self.root = None

    def insert(self, value: int):
        """
        Inserta un nuevo valor en el árbol.
        """
        if self.root is None:
            self.root = Node(value)
        else:
            self._insert_recursive(self.root, value)

    def _insert_recursive(self, current: Node, value: int):
        """
        Inserción recursiva de un valor en el árbol.
        """
        if value < current.value:
            if current.left is None:
                current.left = Node(value)
            else:
                self._insert_recursive(current.left, value)
        else:  # Valores iguales también van a la derecha
            if current.right is None:
                current.right = Node(value)
            else:
                self._insert_recursive(current.right, value)

    def inorder(self):
        """
        Retorna los valores del árbol en recorrido in-orden.
        """
        return self._inorder_recursive(self.root)

    def _inorder_recursive(self, current: Node):
        if current is None:
            return []
        return self._inorder_recursive(current.left) + [current.value] + self._inorder_recursive(current.right)

    def preorder(self):
        """
        Retorna los valores del árbol en recorrido pre-orden.
        """
        return self._preorder_recursive(self.root)

    def _preorder_recursive(self, current: Node):
        if current is None:
            return []
        return [current.value] + self._preorder_recursive(current.left) + self._preorder_recursive(current.right)

    def postorder(self):
        """
        Retorna los valores del árbol en recorrido post-orden.
        """
        return self._postorder_recursive(self.root)

    def _postorder_recursive(self, current: Node):
        if current is None:
            return []
        return self._postorder_recursive(current.left) + self._postorder_recursive(current.right) + [current.value]

    def find(self, value: int) -> bool:
        """
        Busca un valor en el árbol y retorna True si lo encuentra.
        """
        return self._find_recursive(self.root, value)

    def _find_recursive(self, current: Node, value: int) -> bool:
        if current is None:
            return False
        if value == current.value:
            return True
        elif value < current.value:
            return self._find_recursive(current.left, value)
        else:
            return self._find_recursive(current.right, value)

    def save_to_file(self, filename: str):
        """
        Guarda el árbol actual a un archivo usando pickle.
        """
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load_from_file(filename: str):
        """
        Carga un árbol previamente guardado desde disco.
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(f"No existe el archivo: {filename}")
        with open(filename, 'rb') as f:
            return pickle.load(f)


# ----------------------------- USO / TEST -----------------------------
if __name__ == "__main__":
    tree = BinarySearchTree()

    # Insertar los primeros 1000 números (del 0 al 999) sin importar el orden
    import random
    numeros = list(range(1000))
    random.shuffle(numeros)
    for num in numeros:
        tree.insert(num)

    # Imprimir recorridos
    print("In-orden:", tree.inorder()[:20], "...")  # Solo mostramos los primeros 20 para no saturar
    print("Pre-orden:", tree.preorder()[:20], "...")
    print("Post-orden:", tree.postorder()[:20], "...")

    # Buscar algunos valores
    print("¿Existe el número 500?:", tree.find(500))
    print("¿Existe el número 1001?:", tree.find(1001))

    # Guardar árbol a disco
    tree.save_to_file("arbol.pkl")

    # Cargar árbol desde disco
    loaded_tree = BinarySearchTree.load_from_file("arbol.pkl")
    print("Árbol cargado, ¿existe el número 500?:", loaded_tree.find(500))
