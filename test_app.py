import json
import pytest
from app import fetch_dollar_data, save_to_s3

def test_fetch_dollar_data(monkeypatch):
    """Prueba que fetch_dollar_data retorna un diccionario con la respuesta mockeada"""
    # Creamos un mock de la respuesta de requests.get
    class MockResponse:
        def raise_for_status(self): pass
        def json(self): return {"test": "ok"}

    # Reemplazamos requests.get por la clase mock
    monkeypatch.setattr("requests.get", lambda *args, **kwargs: MockResponse())

    # Ejecutamos la función
    data = fetch_dollar_data()
    assert isinstance(data, dict)
    assert data["test"] == "ok"

def test_save_to_s3(monkeypatch):
    """Prueba que save_to_s3 sube un archivo JSON a S3 usando un mock"""
    calls = {}

    # Mock de s3.put_object para capturar la llamada
    def mock_put_object(Bucket, Key, Body, ContentType):
        calls["Bucket"] = Bucket
        calls["Key"] = Key
        calls["Body"] = Body

    # Reemplazamos el cliente de S3 real por el mock
    monkeypatch.setattr("app.s3.put_object", mock_put_object)

    # Ejecutamos la función
    filename = save_to_s3({"mock": "data"})
    assert filename.startswith("dolar-")  # El archivo debe iniciar con dolar-
    assert calls["Bucket"].startswith("dolar-raw")  # El bucket debe ser el correcto