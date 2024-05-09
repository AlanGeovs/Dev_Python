import pandas as pd
from collections import Counter

# Paso 1: Leer el archivo CSV
df = pd.read_csv('revanchita_18032024.csv')

# Paso 2: Crear una representación de cada conjunto de 6 números
# Ordenamos los números para evitar diferencias por orden y los convertimos a tuplas (que son hashables)
df['conjunto_numeros'] = df.apply(lambda row: tuple(sorted([row[f'F{i}'] for i in range(1, 7)])), axis=1)

# Paso 3: Contar la frecuencia de cada conjunto único de números
conteo_conjuntos = Counter(df['conjunto_numeros'])

# Paso 4: Identificar la frecuencia más alta
_, frecuencia_max = conteo_conjuntos.most_common(1)[0]

# Paso 5: Filtrar todos los conjuntos de números que tienen la frecuencia máxima
conjuntos_mas_frecuentes = [conjunto for conjunto, frecuencia in conteo_conjuntos.items() if frecuencia == frecuencia_max]

print(f'Conjuntos de números que se repiten {frecuencia_max} veces:')
for conjunto in conjuntos_mas_frecuentes:
    print(conjunto)
