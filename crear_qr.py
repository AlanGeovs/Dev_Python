#importar pandas qr code 
# pip install pandas qrcode

import pandas as pd
import qrcode
import os
import zipfile

# Cargar el archivo Excel en un DataFrame de pandas
ruta_excel = 'E:/Documentos/NetBeansProjects/Dev_Python/listado-colegiados.xlsx'  # Cambia esto a la ruta de tu archivo Excel local
df = pd.read_excel(ruta_excel)

# Directorio para guardar imágenes QR
directorio_imagenes_qr = 'E:/Documentos/NetBeansProjects/Dev_Python/Código QR'  # Cambia esto a tu directorio deseado
os.makedirs(directorio_imagenes_qr, exist_ok=True)

# Función para crear código QR
def crear_codigo_qr(sku, url_base="https://www.ecum.mx/colegiados/"):
    #url = f"{url_base}{sku}.vcf"
    url = f"{url_base}{sku}.pdf"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    ruta_imagen = os.path.join(directorio_imagenes_qr, f"{sku}.png")
    img.save(ruta_imagen)
    return ruta_imagen

# Crear código QR para cada SKU en el DataFrame
archivos_imagenes_qr = []
for sku in df['SKU']:
    ruta_imagen_qr = crear_codigo_qr(sku)
    archivos_imagenes_qr.append(ruta_imagen_qr)

# Crear un archivo zip para almacenar todas las imágenes QR
nombre_archivo_zip = 'qr_codes.zip'  # Cambia esto a tu nombre de archivo zip deseado
with zipfile.ZipFile(nombre_archivo_zip, 'w') as zipf:
    for archivo in archivos_imagenes_qr:
        zipf.write(archivo, arcname=os.path.basename(archivo))
