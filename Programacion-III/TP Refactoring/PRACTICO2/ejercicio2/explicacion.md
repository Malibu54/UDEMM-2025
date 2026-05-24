# Análisis del código proporcionado
El patron identificado es Composite pero mal empleado generando bad smells

## Bad smells identificados

1. Violated Liskov Substitution Principle + isinstance chains
get_weight() y get_price() en Container hacen isinstance(i, Package) / isinstance(i, Container). Esto significa que el código necesita saber qué tipo concreto tiene cada elemento para procesarlo. Si se agrega un tercer tipo (ej. Pallet), hay que modificar ambos métodos en Container. Violación directa del OCP.
2. Duplicación de lógica (DRY)
Los métodos get_weight() y get_price() en Container son estructuralmente idénticos: mismo loop, mismo isinstance, mismo raise. La lógica se repite para cada propiedad que se quiera calcular.
3. Composite Pattern incompleto
El patrón Composite exige una interfaz común (Component) que tanto la hoja (Package) como el compuesto (Container) implementen. Sin esa abstracción, el cliente debe conocer los tipos concretos.
4. _name sin acceso uniforme
Package expone get_weight() y get_price() pero no tiene get_name(). El acceso a _name es directo en el f-string, rompiendo el encapsulamiento.
5. Método display() acoplado a print
display() imprime directamente, lo que lo hace inútil para generar reportes en string, escribir a archivo, etc. Violación del SRP.