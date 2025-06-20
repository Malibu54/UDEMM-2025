import csv
from collections import defaultdict

# Archivos de entrada subidos por el usuario
input_files = [
    '/UDEMM-2025/TP3/Ejercicio4/BANK_DATA1.csv',
    '/UDEMM-2025/TP3/Ejercicio4/BANK_DATA2.csv',
    'UDEMM-2025/TP3/Ejercicio4/BANK_DATA3.csv'
]

# Archivo de salida
output_file = '/UDEMM-2025/TP3/Ejercicio4/BANK_DATA_ORD.csv'

# Estructura para agrupar los datos por 'name'
data_summary = defaultdict(lambda: {'total_reserve': 0, 'total_cant': 0, 'code_country': ''})

# Leer y procesar todos los archivos
for file in input_files:
    with open(file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['name'].strip()
            reserve = float(row['reserve'])
            code_country = row['code_country'].strip()

            data_summary[name]['total_reserve'] += reserve
            data_summary[name]['total_cant'] += 1
            data_summary[name]['code_country'] = code_country

# Ordenar por nombre
sorted_data = sorted(data_summary.items(), key=lambda x: x[0])

# Escribir el archivo ordenado
with open(output_file, 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['name', 'total_reserve', 'total_cant', 'code_country']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for name, info in sorted_data:
        writer.writerow({
            'name': name,
            'total_reserve': info['total_reserve'],
            'total_cant': info['total_cant'],
            'code_country': info['code_country']
        })

output_file  # Devuelvo la ruta del archivo generado

