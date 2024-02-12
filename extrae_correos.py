import os
import re
import email
import pandas as pd
from email.utils import parseaddr
from email.policy import default
from openpyxl import load_workbook

# Función para extraer la dirección IP del encabezado 'Received'
def extract_ip_from_received_headers(received_headers):
    # Regex para encontrar direcciones IPv4 en el texto
    ip_regex = r'[0-9]+(?:\.[0-9]+){3}'
    
    # Buscar a través de todos los encabezados 'Received' en reversa
    for header in reversed(received_headers):
        ips = re.findall(ip_regex, header)
        if ips:
            return ips[-1]
    return None

# Función para parsear el archivo y extraer la información requerida
def parse_eml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            msg = email.message_from_file(file, policy=default)
        except Exception as e:
            print(f"No se pudo procesar el archivo {file_path}: {e}")
            return None
    
    remitente_nombre, remitente_email = parseaddr(msg.get('From'))
    destinatario = msg.get('To')
    otros_destinatarios = msg.get_all('Cc')
    fecha = msg.get('Date')
    asunto = msg.get('Subject')
    received_headers = msg.get_all('Received')
    ip = extract_ip_from_received_headers(received_headers) if received_headers else None
    
    return {
        'nombre_remitente': remitente_nombre,
        'remitente': remitente_email,
        'destinatario': destinatario,
        'otros_destinatarios': otros_destinatarios,
        'fecha': fecha,
        'asunto': asunto,
        'ip': ip
    }

# Función para procesar todos los archivos en un directorio
def process_eml_files(directory):
    data = []
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        parsed_email = parse_eml(file_path)
        if parsed_email:  # Solo añadir si el parsing fue exitoso
            data.append(parsed_email)
    return data

# Definir el directorio donde se encuentran los archivos
eml_directory = 'mails'  # Actualiza con la ruta adecuada

# Procesar los archivos
eml_data = process_eml_files(eml_directory)

# Cargar el archivo Excel existente o crear uno nuevo si no existe
excel_path = 'bd_correos.xlsx'  # Actualiza con la ruta adecuada
if os.path.exists(excel_path):
    workbook = load_workbook(filename=excel_path)
    sheet = workbook.active
else:
    df_new = pd.DataFrame(columns=["id", "nombre_remitente", "remitente", "destinatario", "otros_destinatarios", "fecha", "asunto", "ip"])
    df_new.to_excel(excel_path, index=False)
    workbook = load_workbook(filename=excel_path)
    sheet = workbook.active

last_id = sheet.cell(row=sheet.max_row, column=1).value if sheet.max_row > 1 else 0


# Asegúrese de que last_id sea un entero antes de continuar
last_id = int(last_id) if last_id is not None else 0

# Añadir los datos de los emails al archivo Excel
for email_data in eml_data:
    # Solo proceder si email_data no es None
    if email_data:
        last_id += 1  # Incrementar el ID para cada entrada
        sheet.append([
            last_id,
            email_data.get('nombre_remitente'),
            email_data.get('remitente'),
            email_data.get('destinatario'),
            ", ".join(email_data['otros_destinatarios']) if email_data.get('otros_destinatarios') else None,
            email_data.get('fecha'),
            email_data.get('asunto'),
            email_data.get('ip')
        ])

# Guardar el archivo Excel con los nuevos datos
workbook.save(filename=excel_path)

# Imprimir la ruta al archivo Excel actualizado
print(f"Archivo Excel actualizado: {excel_path}")
