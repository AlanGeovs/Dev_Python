import pandas as pd

# Leer el archivo CSV
df = pd.read_csv('revanchita_18032024.csv')

# Preparar las columnas para los rangos
df['F_1_9'] = 0
df['F_10_19'] = 0
df['F_20_29'] = 0
df['F_30_39'] = 0
df['F_40_49'] = 0
df['F_50_56'] = 0

# Función para contar los números en los rangos especificados
def contar_rangos(fila):
    for i in range(1, 7):  # F1 a F6
        numero = fila[f'F{i}']
        if 1 <= numero <= 9:
            fila['F_1_9'] += 1
        elif 10 <= numero <= 19:
            fila['F_10_19'] += 1
        elif 20 <= numero <= 29:
            fila['F_20_29'] += 1
        elif 30 <= numero <= 39:
            fila['F_30_39'] += 1
        elif 40 <= numero <= 49:
            fila['F_40_49'] += 1
        elif 50 <= numero <= 56:
            fila['F_50_56'] += 1
    return fila

# Aplicar la función a cada fila del DataFrame
df = df.apply(contar_rangos, axis=1)

# Seleccionar solo las columnas requeridas para el nuevo CSV
columnas_requeridas = ['CONCURSO', 'F_1_9', 'F_10_19', 'F_20_29', 'F_30_39', 'F_40_49', 'F_50_56']
df_resultado = df[columnas_requeridas]

# Guardar el resultado en un nuevo archivo CSV
df_resultado.to_csv('revanchita_rangos.csv', index=False)

print("Archivo 'revanchita_rangos.csv' generado exitosamente.")
