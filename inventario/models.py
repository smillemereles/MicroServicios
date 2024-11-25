# models.py
from pymongo import MongoClient, ASCENDING, DESCENDING
from bson import ObjectId
from datetime import datetime
from config import MONGODB_URI, MONGODB_DB

class InventarioModel:
    def __init__(self):
        self.client = MongoClient(MONGODB_URI)
        self.db = self.client[MONGODB_DB]
        self.inventario = self.db.inventario
        self.movimientos = self.db.movimientos
        self.setup_indexes()

    def setup_indexes(self):
        """Configurar índices necesarios"""
        # Índice para producto_id
        self.inventario.create_index([("producto_id", ASCENDING)])
        # Índice para fecha en movimientos
        self.movimientos.create_index([("fecha", DESCENDING)])

    def agregar_inventario(self, producto_id, cantidad):
        """Agregar o actualizar inventario"""
        resultado = self.inventario.update_one(
            {"producto_id": producto_id},
            {
                "$inc": {"cantidad": cantidad},
                "$setOnInsert": {"fecha_creacion": datetime.utcnow()},
                "$set": {"ultima_actualizacion": datetime.utcnow()}
            },
            upsert=True
        )
        
        # Registrar movimiento
        self.registrar_movimiento(producto_id, "entrada", cantidad)
        
        return resultado

    def obtener_inventario(self, producto_id=None):
        """Obtener inventario de un producto o todos"""
        if producto_id:
            return self.inventario.find_one({"producto_id": producto_id})
        return list(self.inventario.find())

    def actualizar_inventario(self, producto_id, cantidad):
        """Actualizar cantidad de inventario"""
        resultado = self.inventario.update_one(
            {"producto_id": producto_id},
            {
                "$set": {
                    "cantidad": cantidad,
                    "ultima_actualizacion": datetime.utcnow()
                }
            }
        )
        
        self.registrar_movimiento(producto_id, "actualizacion", cantidad)
        return resultado

    def registrar_movimiento(self, producto_id, tipo, cantidad):
        """Registrar movimiento de inventario"""
        return self.movimientos.insert_one({
            "producto_id": producto_id,
            "tipo": tipo,
            "cantidad": cantidad,
            "fecha": datetime.utcnow()
        })

    def obtener_movimientos(self, producto_id=None, limite=100):
        """Obtener historial de movimientos"""
        filtro = {"producto_id": producto_id} if producto_id else {}
        return list(self.movimientos.find(filtro).sort("fecha", DESCENDING).limit(limite))

    def obtener_estadisticas(self, producto_id=None):
        """Obtener estadísticas de inventario"""
        match = {"producto_id": producto_id} if producto_id else {}
        pipeline = [
            {"$match": match},
            {
                "$group": {
                    "_id": "$producto_id",
                    "total_movimientos": {"$sum": 1},
                    "cantidad_actual": {"$first": "$cantidad"},
                    "ultima_actualizacion": {"$max": "$ultima_actualizacion"}
                }
            }
        ]
        return list(self.inventario.aggregate(pipeline))