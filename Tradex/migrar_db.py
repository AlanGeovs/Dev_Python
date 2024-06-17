import pandas as pd

# Load the Excel file
file_path = 'clients_tradex.xlsx'
clients_df = pd.read_excel(file_path)

# Clean column names
clients_df.columns = clients_df.columns.str.strip()

# Clean all fields of trailing and leading spaces
clients_df = clients_df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Check column names again
print(clients_df.columns)

# Generate SQL insert statements for all records in the DataFrame
insert_statements = []

for index, row in clients_df.iterrows():
    values = [
        row['id_user'], row['username'], row['cash_balance'], row['trade_balance'], 
        'NULL' if pd.isna(row['overdraft']) else row['overdraft'], 
        row['name'], row['last_name'], 
        'NULL' if pd.isna(row['last_name_second']) else row['last_name_second'], 
        row['trading_name'], row['legal_name'], 
        'NULL' if pd.isna(row['email']) else row['email'], 
        'NULL' if pd.isna(row['phone']) else row['phone'], 
        'NULL' if pd.isna(row['mobile']) else row['mobile'], 
        row['address'], 
        'NULL' if pd.isna(row['town']) else row['town'], 
        row['city'], row['cp'], 
        row['state'], row['country'], row['account_number'], 
        row['group'], row['status'], row['broker'], 
        'NULL' if pd.isna(row['commission_purchase']) else row['commission_purchase'], 
        'NULL' if pd.isna(row['commission_sale']) else row['commission_sale']
    ]
    values_str = ", ".join([f"'{str(v)}'" if isinstance(v, str) else str(v) for v in values])
    insert_statements.append(f"INSERT INTO clients VALUES ({values_str});")

# Save the insert statements to a text file
insert_file_path = 'insert_statements_clients.txt'
with open(insert_file_path, 'w') as file:
    file.write("\n".join(insert_statements))

print(f"INSERT statements have been saved to {insert_file_path}")
