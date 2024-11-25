from flask import Flask, request, jsonify
from models import ProductoModel
from rabbitmq_client import RabbitMQClient
import json

app = Flask(__name__)
producto_model = ProductoModel()
rabbitmq_client = RabbitMQClient()

@app.route('/productos/<id>', methods=['PUT'])
def actualizar_producto(id):
    try:
        data = request.get_json()
        resultado = producto_model.actualizar_producto(id, data)
        
        if resultado.modified_count > 0:
            # Notificar al servicio de inventario
            mensaje = {
                'accion': 'producto_actualizado',
                'producto_id': id,
                'datos': data
            }
            rabbitmq_client.enviar_mensaje(mensaje)
            
            return jsonify({'mensaje': 'Producto actualizado exitosamente'}), 200
        else:
            return jsonify({'mensaje': 'Producto no encontrado'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/productos/<id>', methods=['DELETE'])
def eliminar_producto(id):
    try:
        resultado = producto_model.eliminar_producto(id)
        
        if resultado.deleted_count > 0:
            # Notificar al servicio de inventario
            mensaje = {
                'accion': 'producto_eliminado',
                'producto_id': id
            }
            rabbitmq_client.enviar_mensaje(mensaje)
            
            return jsonify({'mensaje': 'Producto eliminado exitosamente'}), 200
        else:
            return jsonify({'mensaje': 'Producto no encontrado'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500