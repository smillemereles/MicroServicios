# rabbitmq_client.py
import pika
import json
from config import RABBITMQ_HOST, RABBITMQ_QUEUE

class RabbitMQClient:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.queue = RABBITMQ_QUEUE

    def conectar(self):
        if not self.connection or self.connection.is_closed:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=RABBITMQ_HOST)
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue, durable=True)

    def enviar_mensaje(self, mensaje):
        try:
            self.conectar()
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue,
                body=json.dumps(mensaje),
                properties=pika.BasicProperties(
                    delivery_mode=2  # mensaje persistente
                )
            )
        except Exception as e:
            print(f"Error al enviar mensaje a RabbitMQ: {e}")
            raise
        finally:
            if self.connection and not self.connection.is_closed:
                self.connection.close()