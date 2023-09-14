import logging
import pyodbc
import azure.functions as func
import pandas as pd
import io
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

def main(mytimer: func.TimerRequest) -> None:
    logging.info('Python timer trigger function started.')

    server = '**********'
    database = '******'
    username = '*******'
    password = '*********'
    driver = '{ODBC Driver 17 for SQL Server}'

    conn_string = f'Driver={driver};Server={server};Database={database};UID={username};PWD={password};'
    conn = pyodbc.connect(conn_string)
    
    cursor = conn.cursor()
    
    logging.info('Connected to SQL Server.')

    cursor.execute("SELECT * FROM Employees")
    rows = cursor.fetchall()
    
    logging.info('Data fetched from SQL database.')
    
    df = pd.DataFrame.from_records(rows, columns=[desc[0] for desc in cursor.description])

    logging.info('DataFrame created.')
    
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
    
    output.seek(0)
    
    logging.info('Excel file created in memory.')
    
    blob_service_client = BlobServiceClient.from_connection_string("DefaultEndpointsProtocol=https;AccountName=*******;AccountKey=********")
    blob_client = blob_service_client.get_blob_client(container="containercsvfiles", blob="blob_name.xlsx")
    blob_client.upload_blob(output.read(), overwrite=True)
    
    logging.info('Excel file saved to Blob Storage.')
    logging.info('Python timer trigger function completed.')


