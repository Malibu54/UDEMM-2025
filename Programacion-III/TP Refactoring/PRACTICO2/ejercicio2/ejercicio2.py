from abc import ABC, abstractmethod
import unittest

class LogisticsComponent(ABC):


    def __init__(self, name: str):
        self._name = name

    def get_name(self) -> str:
        return self._name

    @abstractmethod
    def get_weight(self) -> float:
        

    @abstractmethod
    def get_price(self) -> float:
        

    @abstractmethod
    def describe(self, indent: int = 0) -> str:
       


class Package(LogisticsComponent):

    def __init__(self, name: str, weight: float, price: float):
        super().__init__(name)
        if weight < 0:
            raise ValueError("El peso no puede ser negativo.")
        if price < 0:
            raise ValueError("El precio no puede ser negativo.")
        self._weight = weight
        self._price  = price

    def get_weight(self) -> float:
        return self._weight

    def get_price(self) -> float:
        return self._price

    def describe(self, indent: int = 0) -> str:
        prefix = ' ' * indent
        return f"{prefix}Package: {self._name} ({self._weight}kg, ${self._price})"


class Container(LogisticsComponent):

    def __init__(self, name: str):
        super().__init__(name)
        self._items: list[LogisticsComponent] = []

    def add_item(self, item: LogisticsComponent) -> None:
        self._items.append(item)

    def remove_item(self, item: LogisticsComponent) -> None:
        self._items.remove(item)

    def get_weight(self) -> float:

        return sum(item.get_weight() for item in self._items)

    def get_price(self) -> float:

        return sum(item.get_price() for item in self._items)

    def describe(self, indent: int = 0) -> str:

        prefix = ' ' * indent
        lines = [f"{prefix}Container: {self._name}"]
        for item in self._items:
            lines.append(item.describe(indent + 2))
        return '\n'.join(lines)

class ReportPrinter:

    @staticmethod
    def print_report(component: LogisticsComponent) -> None:
        print(component.describe())
        print(f"Peso total:  {component.get_weight():.2f} kg")
        print(f"Valor total: ${component.get_price():.2f}")

    @staticmethod
    def save_report(component: LogisticsComponent, filepath: str) -> None:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(component.describe())
            f.write(f"\nPeso total:  {component.get_weight():.2f} kg\n")
            f.write(f"Valor total: ${component.get_price():.2f}\n")


if __name__ == "__main__":
    p1 = Package('Laptop', 2.5, 1500)
    p2 = Package('Phone',  0.3,  800)
    p3 = Package('Book',   1.0,   30)

    c1 = Container('Box A')
    c1.add_item(p1)
    c1.add_item(p2)

    c2 = Container('Box B')
    c2.add_item(p3)
    c2.add_item(c1)   

    ReportPrinter.print_report(c2)


class TestPackage(unittest.TestCase):

    def setUp(self):
        self.p = Package('Laptop', 2.5, 1500)

    def test_get_weight(self):
        self.assertEqual(self.p.get_weight(), 2.5)

    def test_get_price(self):
        self.assertEqual(self.p.get_price(), 1500)

    def test_get_name(self):
        self.assertEqual(self.p.get_name(), 'Laptop')

    def test_describe_contains_name(self):
        result = self.p.describe()
        self.assertIn('Laptop', result)
        self.assertIn('2.5', result)
        self.assertIn('1500', result)

    def test_describe_indent(self):
        result = self.p.describe(indent=4)
        self.assertTrue(result.startswith('    '))

    def test_negative_weight_raises(self):
        with self.assertRaises(ValueError):
            Package('Bad', -1, 100)

    def test_negative_price_raises(self):
        with self.assertRaises(ValueError):
            Package('Bad', 1, -100)


class TestContainer(unittest.TestCase):

    def setUp(self):
        self.p1 = Package('Laptop', 2.5, 1500)
        self.p2 = Package('Phone',  0.3,  800)
        self.p3 = Package('Book',   1.0,   30)
        self.c1 = Container('Box A')
        self.c1.add_item(self.p1)
        self.c1.add_item(self.p2)
        self.c2 = Container('Box B')
        self.c2.add_item(self.p3)
        self.c2.add_item(self.c1)

    def test_weight_single_container(self):
  
        self.assertAlmostEqual(self.c1.get_weight(), 2.8)

    def test_weight_nested_container(self):
 
        self.assertAlmostEqual(self.c2.get_weight(), 3.8)

    def test_price_single_container(self):
  
        self.assertEqual(self.c1.get_price(), 2300)

    def test_price_nested_container(self):
       
        self.assertEqual(self.c2.get_price(), 2330)

    def test_describe_contains_all_names(self):
        report = self.c2.describe()
        self.assertIn('Box B', report)
        self.assertIn('Box A', report)
        self.assertIn('Laptop', report)
        self.assertIn('Phone', report)
        self.assertIn('Book', report)

    def test_describe_hierarchy_indentation(self):
        report = self.c2.describe()
        lines = report.split('\n')
      
        self.assertFalse(lines[0].startswith(' '))  
        self.assertTrue(any(l.startswith('  ') for l in lines))

    def test_empty_container_weight(self):
        empty = Container('Vacío')
        self.assertEqual(empty.get_weight(), 0)

    def test_empty_container_price(self):
        empty = Container('Vacío')
        self.assertEqual(empty.get_price(), 0)

    def test_remove_item(self):
        self.c1.remove_item(self.p2)
        self.assertAlmostEqual(self.c1.get_weight(), 2.5)
        self.assertEqual(self.c1.get_price(), 1500)

    def test_polymorphism_no_isinstance_needed(self):

        items: list[LogisticsComponent] = [self.p1, self.c1, self.p3]
        total_weight = sum(i.get_weight() for i in items)
      
        self.assertAlmostEqual(total_weight, 6.3)


class TestDescribeOutput(unittest.TestCase):

    def test_describe_is_string(self):
        p = Package('X', 1, 10)
        self.assertIsInstance(p.describe(), str)

    def test_container_describe_is_string(self):
        c = Container('Y')
        c.add_item(Package('Z', 1, 5))
        self.assertIsInstance(c.describe(), str)

    def test_describe_does_not_print(self):

        import io, sys
        p = Package('Silent', 1, 10)
        captured = io.StringIO()
        sys.stdout = captured
        _ = p.describe()
        sys.stdout = sys.__stdout__
        self.assertEqual(captured.getvalue(), '')