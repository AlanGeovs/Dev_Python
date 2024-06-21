import pandas as pd
from bs4 import BeautifulSoup

# Lista de archivos HTML
html_files = [
    '1433.html','1434.html','1435.html', '1436.html', '1437.html', '1438.html', '1439.html', '1440.html', '1441.html', '1442.html', '1443.html', '1444.html', '1445.html', '1446.html', '1447.html', '1448.html', '1449.html', '1450.html', 
    '1451.html', '1452.html', '1453.html', '1454.html', '1455.html', '1456.html', '1457.html', '1458.html', '1459.html', '1460.html', 
    '1461.html', '1462.html', '1463.html', '1464.html', '1465.html', '1466.html', '1467.html', '1468.html', '1469.html', '1470.html', 
    '1471.html', '1472.html', '1473.html', '1474.html', '1475.html', '1476.html', '1477.html', '1478.html', '1479.html', '1480.html',
    '1481.html', '1482.html', '1483.html', '1484.html', '1485.html', '1486.html', '1487.html', '1488.html', '1489.html', '1490.html',
    '1491.html', '1492.html', '1493.html', '1494.html', '1495.html', '1496.html', '1497.html', '1498.html', '1499.html', '1500.html',
    '1501.html', '1502.html', '1503.html', '1504.html', '1505.html', '1506.html', '1507.html', '1508.html', '1509.html', '1510.html',
    '1511.html', '1512.html', '1513.html', '1514.html', '1515.html', '1516.html', '1517.html', '1518.html', '1519.html', '1520.html',
    '1521.html', '1522.html', '1523.html', '1524.html', '1525.html', '1527.html', '1528.html', '1529.html', '1530.html',
    '1531.html', '1532.html', '1533.html', '1534.html', '1535.html', '1536.html', '1537.html', '1538.html', '1539.html', '1540.html', 
    '1541.html', '1542.html', '1543.html', '1544.html','1545.html', '1546.html', '1547.html'
]

# Mapeo de modelos a tipos
model_to_type = {
    'Versa': 'Sedan',
    'Sentra': 'Sedan',
    'Altima': 'Sedan',
    'Maxima': 'Sedan',
    'March': 'Hatchback',
    'V-Drive': 'Sedan',
    'Kicks': 'Crossover',
    'Kicks e': 'Crossover',
    'X-Trail': 'SUV',
    'Qashqai': 'SUV',
    'Murano': 'SUV', 
    'Pathfinder': 'SUV',
    'Armada': 'SUV',
    'Frontier': 'Pick-up',
    'NP 300': 'Pick-up',
    'NP300': 'Pick-up',
    'Np 300': 'Pick-up',
    'Np300': 'Pick-up',
    'Titan': 'Pick-up',
    'Leaf': 'Hatchback',
    '370Z': 'Coupe',
    'GT-R': 'Deportivo',
    'Urvan': 'Van (Furgoneta)'
}

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
            model = title_parts[1].strip()
            car_details['Modelo'] = model
            # Ajuste para manejar correctamente los modelos V-Drive y X-Trail
            if 'V-Drive' in car_details['Title']:
                car_details['Modelo'] = 'V-Drive'
            elif 'X-Trail' in car_details['Title']:
                car_details['Modelo'] = 'X-Trail'

            # Asignar el tipo basado en el modelo
            car_details['Tipo'] = model_to_type.get(car_details['Modelo'], '')

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
        car_details['Image_URL'] = ', '.join(['https://desantorsa-carmax-resized.s3.us-west-1.amazonaws.com/test/Image/Car/' + img['src'].split('/')[-1] for img in image_tags])

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
        characteristics_text = '; '.join([char for char in characteristics])
        characteristics_text = characteristics_text.split('; After submitting your information')[0]  # Eliminar desde el texto especificado
        car_details['Características'] = characteristics_text
        car_details['Seguridad'] = '; '.join([char for char in characteristics if 'ABS' in char or 'Bolsas de Aire' in char])

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