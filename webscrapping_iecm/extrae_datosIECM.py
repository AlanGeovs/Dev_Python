import requests
from bs4 import BeautifulSoup
import pandas as pd
import urllib3

# Suprimir advertencias de seguridad
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def extract_data(url):
    try:
        # Realizar la solicitud HTTP desactivando la verificación SSL
        response = requests.get(url, verify=False)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracción de datos básicos con comprobaciones para evitar errores
        data = {
            "Nombre": soup.find('p', class_='h5').get_text(strip=True) if soup.find('p', class_='h5') else 'No disponible',
            "Partido o coalición": soup.find_all('p', class_='h6')[0].get_text(strip=True) if soup.find_all('p', class_='h6') else 'No disponible',
            "Cargo": soup.find_all('p', class_='h6')[1].get_text(strip=True) if len(soup.find_all('p', class_='h6')) > 1 else 'No disponible',
            "Edad": soup.find_all('p', class_='h6')[2].get_text(strip=True) if len(soup.find_all('p', class_='h6')) > 2 else 'No disponible',
            "Ámbito territorial": soup.find_all('p', class_='h6')[3].get_text(strip=True) if len(soup.find_all('p', class_='h6')) > 3 else 'No disponible',
            "Sexo": soup.find_all('p', class_='h6')[4].get_text(strip=True) if len(soup.find_all('p', class_='h6')) > 4 else 'No disponible',
            "Teléfono": soup.find('div', class_='col-sm-12 col-md-6 col-lg-4').find('li').get_text(strip=True) if soup.find('div', class_='col-sm-12 col-md-6 col-lg-4') and soup.find('div', class_='col-sm-12 col-md-6 col-lg-4').find('li') else 'No disponible',
            "Correo electrónico": soup.find_all('div', class_='col-sm-12 col-md-6 col-lg-4')[1].find('li').get_text(strip=True) if len(soup.find_all('div', class_='col-sm-12 col-md-6 col-lg-4')) > 1 and soup.find_all('div', class_='col-sm-12 col-md-6 col-lg-4')[1].find('li') else 'No disponible',
            "Página web": soup.find('div', class_='col-sm-12 col-md-12 col-lg-4').find('span').get_text(strip=True) if soup.find('div', class_='col-sm-12 col-md-12 col-lg-4') and soup.find('div', class_='col-sm-12 col-md-12 col-lg-4').find('span') else 'No disponible'
        }

        # Extracción de datos de redes sociales
        social_media_icons = ['twitter', 'youtube', 'facebook', 'instagram', 'tiktok']
        for icon in social_media_icons:
            social_media = soup.find('h2', class_=f'bi bi-{icon}')
            if social_media and social_media.parent and 'href' in social_media.parent.attrs:
                data[f"{icon}_link"] = social_media.parent['href']
                data[f"{icon}_username"] = social_media.parent.find('small').get_text(strip=True) if social_media.parent.find('small') else 'No disponible'
            else:
                data[f"{icon}_link"] = 'No disponible'
                data[f"{icon}_username"] = 'No disponible'

    except Exception as e:
        print(f"Error processing {url}: {e}")
        return None

    return data

# Leer URLs del archivo de texto
with open('rutas_candidatos_iecm.txt', 'r') as file:
    urls = file.read().splitlines()

# Lista para almacenar todos los datos
all_data = []

# Procesar cada URL
for url in urls:
    candidate_data = extract_data(url)
    if candidate_data:
        all_data.append(candidate_data)

# Crear DataFrame de pandas con todos los datos
df = pd.DataFrame(all_data)

# Guardar en archivo Excel
df.to_excel('datos_candidatos_completos.xlsx', index=False)
