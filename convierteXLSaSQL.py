import pandas as pd

# Leer el archivo Excel
excel_file = 'inventario.xlsx'  # Nombre del archivo actualizado
df = pd.read_excel(excel_file)

# Abrir un archivo para escribir las sentencias SQL
with open('products.sql', 'w') as sql_file:
    # Escribir la sentencia para crear la tabla (opcional)
    sql_file.write("""
DROP TABLE IF EXISTS products;
CREATE TABLE products (
    SKU VARCHAR(50),
    ISBN VARCHAR(50),
    description TEXT,
    author VARCHAR(100),
    category VARCHAR(50),
    price_public FLOAT,
    stock INT
);
""")
    # Para cada fila en el DataFrame, escribir una sentencia INSERT INTO
    for index, row in df.iterrows():
        sql_file.write(f"INSERT INTO products (SKU, ISBN, description, author, category, price_public, stock) VALUES ('{row['SKU']}', '{row['ISBN']}', '{row['description'].replace("'", "''")}', '{row['author']}', '{row['category']}', {row['price_public']}, {row['stock']});\n")

print("Archivo SQL generado con éxito.")
