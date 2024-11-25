import requests
from config import PRODUCTOS_SERVICE_URL

def validar_producto(producto_id):
    """Validación del producto en el servicio de productos"""
    try:
        response = requests.get(f'{PRODUCTOS_SERVICE_URL}/productos/{producto_id}')
        if response.status_code == 200:
            return True
        return False
    except requests.RequestException as e:
        print(f"Error al validar producto: {e}")
        return False