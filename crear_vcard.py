# Instalar panda https://blog.hubspot.es/website/que-es-pandas-python 
#Install
# pip install pandas
# pip install pandas xlrd openpyxl
# pip install openpyxl

import pandas as pd
import zipfile
import os

# Carga el archivo Excel en un DataFrame de pandas
#ruta_excel = '/listado-colegiados.xlsx'  # Cambia esto a la ruta de tu archivo Excel local
ruta_excel = 'E:/Documentos/NetBeansProjects/Dev_Python/listado-colegiados.xlsx'

df = pd.read_excel(ruta_excel)

# Función para crear los datos de vCard a partir de una fila del DataFrame
def crear_vcard(fila):
    plantilla_vcard = f"""
BEGIN:VCARD
VERSION:3.0
N:{fila['ASOCIADO']};;
FN:{fila['ASOCIADO']}
EMAIL:{fila['E-MAIL']}
TEL;TYPE=CELL:{fila['TELÉFONO']}
X-SOCIO-DESDE:{fila['SOCIO DESDE']}
X-PDU:{fila['PDU']}
X-CED-PROF:{fila['CED.PROF']}
X-SKU:{fila['SKU']}
END:VCARD
    """
    return plantilla_vcard.strip()

# Crea un vCard para cada fila del DataFrame y guarda en archivos individuales
archivos_vcard = []
for indice, fila in df.iterrows():
    vcard = crear_vcard(fila)
    sku = fila['SKU']
    nombre_archivo_vcard = f'E:/Documentos/NetBeansProjects/Dev_Python/descargas_vcard/{sku}.vcf'  # Cambia 'tu_directorio_de_salida' a la ruta de salida deseada
    with open(nombre_archivo_vcard, 'w') as archivo:
        archivo.write(vcard)
    archivos_vcard.append(nombre_archivo_vcard)

# Crea un archivo zip para almacenar todos los vCards
nombre_archivo_zip = 'E:/Documentos/NetBeansProjects/Dev_Python/descargas_vcard/vcards.zip'  # Cambia 'tu_directorio_de_salida' a la ruta de salida deseada
with zipfile.ZipFile(nombre_archivo_zip, 'w') as zipf:
    for archivo in archivos_vcard:
        zipf.write(archivo, arcname=os.path.basename(archivo))

