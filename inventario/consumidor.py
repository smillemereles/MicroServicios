import pika
import json
from pymongo import MongoClient
import os

def get_mongodb_connection():
    client = MongoClient(os.getenv('MONGODB_URI', 'mongodb://localhost:27017/'))
    return client['inventario_db']

def callback(ch, method, properties, body):
    try:
        mensaje = json.loads(body)
        print(f"Mensaje recibido: {mensaje}")
        

        db = get_mongodb_connection()
        db.eventos_inventario.insert_one({
            'tipo': mensaje['accion'],
            'producto_id': mensaje['producto_id'],
            'cantidad': mensaje['cantidad'],
            'timestamp': datetime.utcnow()
        })
        
    except Exception as e:
        print(f"Error procesando mensaje: {e}")

def iniciar_consumidor():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='inventario_queue', durable=True)
    channel.basic_consume(
        queue='inventario_queue',
        on_message_callback=callback,
        auto_ack=True
    )
    print('Consumidor iniciado. Esperando mensajes...')
    channel.start_consuming()

if __name__ == '__main__':
    iniciar_consumidor()
