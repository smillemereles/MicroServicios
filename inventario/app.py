from flask import Flask, request, jsonify
from models import InventarioModel
from validaciones import validar_producto
from rabbitmq_client import RabbitMQClient
import json

app = Flask(__name__)
inventario_model = InventarioModel()
rabbitmq_client = RabbitMQClient()

@app.route('/inventario', methods=['POST'])
def agregar_inventario():
    try:
        data = request.get_json()
        producto_id = data.get('producto_id')
        cantidad = data.get('cantidad')

        # Validar que el producto existe
        if not validar_producto(producto_id):
            return jsonify({'mensaje': 'Producto no encontrado'}), 404

        resultado = inventario_model.agregar_inventario(producto_id, cantidad)
        
        # Notificar actualización
        mensaje = {
            'accion': 'inventario_actualizado',
            'producto_id': producto_id,
            'cantidad': cantidad
        }
        rabbitmq_client.enviar_mensaje(mensaje)
        
        return jsonify({
            'mensaje': 'Inventario actualizado',
            'id': str(resultado.upserted_id) if resultado.upserted_id else None
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Consumidor de eventos de productos
def procesar_evento_producto(ch, method, properties, body):
    try:
        mensaje = json.loads(body)
        accion = mensaje.get('accion')
        producto_id = mensaje.get('producto_id')

        if accion == 'producto_eliminado':
            # Eliminar inventario asociado
            inventario_model.eliminar_inventario(producto_id)
        elif accion == 'producto_actualizado':
            # Actualizar referencias si es necesario
            inventario_model.actualizar_referencias_producto(producto_id, mensaje.get('datos'))
            
    except Exception as e:
        print(f"Error procesando mensaje: {e}")

# Iniciar consumidor de eventos
def iniciar_consumidor():
    rabbitmq_client.consumir_mensajes(procesar_evento_producto, 'productos_queue')