import requests
from bs4 import BeautifulSoup
import pandas as pd

# Deshabilita advertencias de SSL para simplificar el código
requests.packages.urllib3.disable_warnings()

def fetch_data(url):
    # Realizar la solicitud HTTP desactivando la verificación SSL
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Encontrar todas las filas de la tabla
    rows = soup.find_all('tr')
    data = []
    for row in rows:
        cols = row.find_all('td')
        if len(cols) > 5:  # Asegurarse de que la fila tenga el número esperado de columnas
            url = cols[0].find('p').text.strip() if cols[0].find('p') else 'No URL'
            name = cols[1].text.strip()
            political_actor = cols[2].text.strip()
            position = cols[3].text.strip()
            status = cols[4].text.strip()
            territory = cols[5].text.strip()

            data.append({
                'URL': url,
                'Nombre': name,
                'Actor Político': political_actor,
                'Cargo': position,
                'Calidad': status,
                'Ámbito Territorial': territory
            })

    return data

def save_to_excel(data, filename='datos_url_concejales.xlsx'):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False, engine='openpyxl')

# URL de la página a scrapear
url = 'http://sirec.iecm.mx/conoceles/resultados'

# Extraer datos
data = fetch_data(url)

# Guardar datos en Excel
save_to_excel(data)