import pandas as pd
import requests

# Función para verificar el estado de un sitio web
def verificar_sitio(url):
    # Asegurarse de que la URL comience con http:// o https://
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url  # O considera 'https://' si esperas que el sitio soporte SSL
    
    try:
        respuesta = requests.get(url, timeout=20)  # Aumenta el timeout si es necesario
        if respuesta.status_code == 200:
            return 'Activo'
        else:
            return 'Inactivo'
    except requests.RequestException as e:
        print(f"Error al acceder a {url}: {e}")
        return 'Inactivo'

# Leer el archivo Excel
df = pd.read_excel('paginas.xlsx')

# Suponiendo que la columna con las URLs se llama 'Sitio Web'
df['Estado'] = df['Sitio Web'].apply(verificar_sitio)

# Imprimir los resultados
print(df)

# Guardar el DataFrame modificado de nuevo en un archivo Excel
# Puedes especificar el nombre del archivo de salida como prefieras
df.to_excel('paginas_con_estado.xlsx', index=False)
