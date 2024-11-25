from pymongo import MongoClient, ASCENDING
from datetime import datetime
from bson import ObjectId
from config import MONGODB_URI, MONGODB_DB

class ProductoModel:
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[MONGODB_DB]
        self.productos = self.db.productos
        self.setup_indexes()

    def setup_indexes(self):
        self.productos.create_index([("nombre", ASCENDING)])
        self.productos.create_index([("precio", ASCENDING)])

    def crear_producto(self, data):
        data['fecha_creacion'] = datetime.utcnow()
        return self.productos.insert_one(data)

    def obtener_productos(self):
        return list(self.productos.find())

    def obtener_producto(self, producto_id):
        return self.productos.find_one({'_id': ObjectId(producto_id)})

    def actualizar_producto(self, producto_id, data):
        data['fecha_actualizacion'] = datetime.utcnow()
        return self.productos.update_one(
            {'_id': ObjectId(producto_id)},
            {'$set': data}
        )

    def eliminar_producto(self, producto_id):
        return self.productos.delete_one({'_id': ObjectId(producto_id)})