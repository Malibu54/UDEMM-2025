# Análisis del código proporcionado
El código presenta una clase Subscription con un método calculate_price() que tiene varios problemas de diseño que generan bad smells

## Bad smells identificados

1. Long Method / Código de tipo Switch (condicionales encadenados)
El método calculate_price() hace varias cosas al mismo tiempo: calcula el descuento y calcula la comisión y devuelve el precio final. 
2. Magic Numbers
Los valores 0.95, 0.90, 0.85, 0.02, 0.01, 0.03 están hardcodeados sin ningún nombre que explique su significado. Si cambia una comisión, hay que buscar el número en el código.
3. Ausencia del patrón Strategy
La lógica de descuento y comisión está embebida con if/elif/else. Esto viola el Principio Abierto/Cerrado (OCP): para agregar un nuevo tipo de cliente o método de pago, hay que modificar el método existente.
4. Datos como strings literales
Los tipos de cliente y métodos de pago son strings crudos ('empresa', 'paypal'), lo que hace que un typo sea un error silencioso en tiempo de ejecución. Deberían ser Enums.
5. Falta de separación de responsabilidades
La clase mezcla la configuración del cliente (datos) con la lógica de cálculo de precios (comportamiento).