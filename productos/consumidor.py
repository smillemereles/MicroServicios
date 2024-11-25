
import pika
import json
from pymongo import MongoClient
from datetime import datetime
from config import *

def get_mongodb_connection():
    client = MongoClient(MONGODB_URI)
    return client[MONGODB_DB]

def callback(ch, method, properties, body):
    try:
        mensaje = json.loads(body)
        print(f"Mensaje recibido: {mensaje}")
        
        # Registrar el evento en MongoDB
        db = get_mongodb_connection()
        db.eventos_productos.insert_one({
            'tipo': mensaje['accion'],
            'producto_id': mensaje.get('id'),
            'datos': mensaje,
            'timestamp': datetime.utcnow()
        })
        
    except Exception as e:
        print(f"Error procesando el mensaje: {e}")

def consume():
    credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
    parameters = pika.ConnectionParameters(
        host=RABBITMQ_HOST,
        port=RABBITMQ_PORT,
        credentials=credentials
    )
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare(queue=RABBITMQ_QUEUE, durable=True)
    channel.basic_consume(
        queue=RABBITMQ_QUEUE,
        on_message_callback=callback,
        auto_ack=True
    )
    print('Consumidor iniciado. Esperando mensajes...')
    channel.start_consuming()

if __name__ == '__main__':
    consume()