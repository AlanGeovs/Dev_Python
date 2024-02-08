import pandas as pd

# Leer el archivo Excel
excel_file = 'inventario.xlsx'
df = pd.read_excel(excel_file)

# Función para validar y formatear los valores
def validate_and_format(value, data_type):
    if pd.isnull(value):
        if data_type in ['varchar', 'text']:
            return ''
        elif data_type in ['float', 'int']:
            return 0
    else:
        if data_type in ['varchar', 'text']:
            return str(value).replace("'", "''")  # Manejo de comillas simples para SQL
        else:
            return value

# Abrir un archivo para escribir las sentencias SQL
with open('products.sql', 'w') as sql_file:
    # Escribir la sentencia para crear la tabla (opcional)
    sql_file.write("""
DROP TABLE IF EXISTS products;
CREATE TABLE products (
  id_product int(11) NOT NULL,
  type_product int(1) DEFAULT NULL,
  SKU varchar(50) DEFAULT NULL,
  ISBN varchar(50) DEFAULT NULL,
  price_public float DEFAULT NULL,
  price_supplier float DEFAULT NULL,
  discount_supplier int(2) DEFAULT NULL,
  stock int(50) DEFAULT NULL,
  description text,
  publisher varchar(100) DEFAULT NULL,
  author varchar(100) DEFAULT NULL,
  category varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
ALTER TABLE `products`
  ADD PRIMARY KEY (`id_product`);
ALTER TABLE `products`
  MODIFY `id_product` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;
""")

    # Para cada fila en el DataFrame, escribir una sentencia INSERT INTO
    for index, row in df.iterrows():
        sku = validate_and_format(row['SKU'], 'varchar')
        isbn = validate_and_format(row['ISBN'], 'varchar')
        description = validate_and_format(row['description'], 'text')
        author = validate_and_format(row['author'], 'varchar')
        category = validate_and_format(row['category'], 'varchar')
        price_public = validate_and_format(row['price_public'], 'float')
        stock = validate_and_format(row['stock'], 'int')

        sql_file.write(f"INSERT INTO products (SKU, ISBN, description, author, category, price_public, stock) VALUES ('{sku}', '{isbn}', '{description}', '{author}', '{category}', {price_public}, {stock});\n")

print("Archivo SQL generado y validado con éxito.")
