import pandas as pd

# Cargar el archivo CSV
datos = pd.read_csv('revanchita_18032024.csv')

# Concatenar las columnas de resultados
resultados = pd.concat([datos['F1'], datos['F2'], datos['F3'], datos['F4'], datos['F5'], datos['F6']])

# Contar la frecuencia de cada número
frecuencias = resultados.value_counts()

# Ordenar los números por su frecuencia, de mayor a menor
frecuencias_ordenadas = frecuencias.sort_values(ascending=False)

# Convertir la Series en un DataFrame para tener dos columnas: número y frecuencia
frecuencias_df = frecuencias_ordenadas.reset_index()
frecuencias_df.columns = ['Número', 'Frecuencia']

# Guardar el resultado en un archivo CSV
frecuencias_df.to_csv('frecuencias_numeros.csv', index=False)

print("Los resultados han sido guardados en 'frecuencias_numeros.csv'")
