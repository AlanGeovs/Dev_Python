import pandas as pd
from bs4 import BeautifulSoup

# Lista de archivos HTML
html_files = ['1449.html', '1457.html', '1462.html', '1466.html', '1473.html', '1476.html', '1480.html', '1531.html', '1540.html', '1541.html', 
              '1542.html', '1543.html', '1544.html', '1545.html', '1546.html', '1547.html'
              ]

# Lista para almacenar los detalles de los coches
car_details_list = []

for html_file in html_files:
    # Leer el archivo HTML
    with open(html_file, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parsear el HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extraer los datos requeridos
    car_details = {}

    # ID, Title, Year, Marca, Version, Modelo, Condición
    header_div = soup.find('div', class_='carHeader_title_container__RX+pz')
    if header_div:
        header = header_div.find('h2').text
        condition = header.split()[0]  # USED o NEW
        car_details['Condición'] = 'Usado' if condition == 'USED' else 'Nuevo'
        car_details['Year'] = header.split()[1]  # Año

        title_parts = header.split(' ')
        marca_modelo = title_parts[2]  # Ejemplo: Nissan-
        marca_modelo_parts = marca_modelo.split('-')
        car_details['Marca'] = marca_modelo_parts[0]  # Marca
        car_details['version'] = header.split('-')[-1].strip()  # Versión
        car_details['Title'] = " ".join(header.split()[2:5])  # Título sin "USED" y el año
        
        # Extraer el Modelo del Title
        title_parts = car_details['Title'].split('-')
        if len(title_parts) > 1:
            car_details['Modelo'] = title_parts[1].strip()

    vin_stock_div = soup.find('div', class_='carHeader_vin_stock__sAgTs')
    if vin_stock_div:
        car_details['id'] = vin_stock_div.find_all('p')[0].text.split(': ')[1]

    # Precio
    price_div = soup.find('div', class_='carDetailsPricing_perico__QUUrz')
    if price_div:
        price = price_div.find('div', class_='carDetailsPricing_col_1__5ukV9').find_all('p')[1].text.strip()
        car_details['precio'] = price.replace('$', '').strip()

    # Imágenes
    image_container = soup.find('div', class_='carImage_image_container__T8VGl')
    if image_container:
        image_tags = image_container.find_all('img')
        car_details['Image_URL'] = ','.join(['https://desantorsa-carmax-resized.s3.us-west-1.amazonaws.com/test/Image/Car/' + img['src'].split('/')[-1] for img in image_tags])

    # Colores
    info_container = soup.find('div', class_='carInformation_information_container__0ECe+')
    if info_container:
        color_elements = info_container.find_all('p', class_='carInformation_info_value__iT9SB')
        if len(color_elements) >= 2:
            car_details['Color'] = color_elements[0].text.strip()
            car_details['Color_int'] = color_elements[1].text.strip()

        # Kilometraje, Motor, Transmisión, Combustible, Cilindros
        details_elements = info_container.find_all('div', class_='carInformation_single_info__mfLjA')
        for element in details_elements:
            label = element.find('p').text.strip().strip(':').lower()
            value = element.find('p', class_='carInformation_info_value__iT9SB').text.strip()
            if 'mileage' in label:
                car_details['km'] = value
            elif 'motor' in label:
                car_details['Cilindros'] = value
            elif 'transmisión' in label:
                car_details['Transmisión'] = value
            elif 'combustible' in label:
                car_details['Combustible'] = 'Gasolina' if value == '4' else value

    # Características y Seguridad
    characteristics_tags = soup.find('div', class_='carInformation_characteristic_content__7XQ2d')
    if characteristics_tags:
        characteristics = [tag.text for tag in characteristics_tags.find_all('p')]
        characteristics_text = '|'.join([char for char in characteristics])
        characteristics_text = characteristics_text.split('|After submitting your information')[0]  # Eliminar desde el texto especificado
        car_details['Características'] = characteristics_text
        car_details['Seguridad'] = '|'.join([char for char in characteristics if 'ABS' in char or 'Bolsas de Aire' in char])

    # Asignar valores vacíos para los campos no encontrados en el ejemplo
    fields = ['id', 'Title', 'Content', 'precio', 'km', 'version', 'Image_URL', 'Condición', 'Tipo', 'Marca', 'Modelo', 'year', 'Tipo_unidad', 'Transmisión', 'Combustible', 'Cilindros', 'Color', 'Color_int', 'Puertas', 'Características', 'Seguridad']
    for field in fields:
        if field not in car_details:
            car_details[field] = ''

    # Agregar los detalles del coche a la lista
    car_details_list.append(car_details)

# Crear un DataFrame y guardar en Excel
df = pd.DataFrame(car_details_list)
df.to_excel('car_details.xlsx', index=False)

print("Datos extraídos y guardados en car_details.xlsx")
