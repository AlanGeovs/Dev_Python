import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Cargar los datos
datos = pd.read_csv('frecuencias_sum_numeros.csv')

# Crear una lista que repita cada suma de valores la cantidad de veces indicada por su frecuencia
valores = []
for _, fila in datos.iterrows():
    valores.extend([fila['Número']] * fila['Frecuencia'])

# Crear la gráfica de distribución
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.histplot(valores, kde=True)

# Etiquetas y título
plt.title('Distribución Gaussiana de la Suma de Valores')
plt.xlabel('Suma de Valores')
plt.ylabel('Frecuencia')

# Mostrar la gráfica
plt.show()
