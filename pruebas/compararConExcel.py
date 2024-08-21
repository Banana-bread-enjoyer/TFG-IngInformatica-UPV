import json
import os
import pandas as pd
import pyodbc
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from unidecode import unidecode

# Define the connection string
connection_string = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=ASUSMARTA\TFG;"
    r"DATABASE=TFG;"
    r"Trusted_Connection=yes;"
)

conn = pyodbc.connect(connection_string)
cursor = conn.cursor()

# Query to retrieve expediente numbers from the database
query = "SELECT num_expediente FROM Licitaciones"
cursor.execute(query)

# Fetch all expediente numbers and store them in a list
expedientes_db = [row[0] for row in cursor.fetchall()]

# Close the cursor and the connection
cursor.close()
conn.close()

# Read the Excel file (make sure to update the path to your actual file)
excel_path = 'C:/Users/Marta/Documents/UPV-Ing. Inf/TFG/Expedientes.xlsx'
df_excel = pd.read_excel(excel_path, engine='openpyxl')

# Clean and normalize the num_expediente in the Excel file and the database for better matching
df_excel['EXPEDIENTE'] = df_excel['EXPEDIENTE'].apply(lambda x: unidecode(str(x)).strip().lower())
expedientes_db = [unidecode(str(exp)).strip().lower() for exp in expedientes_db]

# Filter rows in the Excel where the num_expediente is present in the database list
df_filtered = df_excel[df_excel['EXPEDIENTE'].isin(expedientes_db)]

# Save the filtered rows to a new Excel file
df_filtered.to_excel('filtrado_expedientes.xlsx', index=False)

# Or simply display the filtered DataFrame
print(df_filtered)
