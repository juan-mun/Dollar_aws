import os
import json
import time
import requests
import boto3
from datetime import datetime

# Cliente de S3 de boto3
s3 = boto3.client("s3")

# Nombre del bucket definido como variable de entorno
BUCKET_NAME = os.getenv("BUCKET_NAME", "dolar-raw-cmjm")

# URL del servicio REST del Banco de la República
BANREP_URL = "https://totoro.banrep.gov.co/estadisticas-economicas/rest/consultaDatosService/consultaMercadoCambiario"

def fetch_dollar_data():
    """
    Consulta los datos del dólar desde la API del Banco de la República.

    Returns:
        dict: Respuesta JSON con los datos del mercado cambiario.
    """
    response = requests.get(BANREP_URL, timeout=10)
    response.raise_for_status()  # Lanza excepción si hubo error en la petición
    return response.json()

def save_to_s3(data: dict):
    """
    Guarda los datos en bruto en un bucket de S3 con el formato dolar-timestamp.json.

    Args:
        data (dict): Respuesta JSON que será guardada en S3.
    """
    timestamp = int(time.time())  # Usamos timestamp actual
    filename = f"dolar-{timestamp}.json"  # Nombre del archivo

    # Subida del archivo al bucket en formato JSON
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=filename,
        Body=json.dumps(data, ensure_ascii=False),
        ContentType="application/json"
    )

    return filename

def lambda_handler(event=None, context=None):
    try:
        data = fetch_dollar_data()
        filename = save_to_s3(data)
        print(f"Datos guardados en s3://{BUCKET_NAME}/{filename}")
        return {"status": "ok", "file": filename}
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"status": "error", "message": str(e)}

