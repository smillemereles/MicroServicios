from pymongo import MongoClient
from datetime import datetime
from config import MONGODB_URI, MONGODB_DB

def seed_database():
    client = MongoClient(MONGODB_URI)
    db = client[MONGODB_DB]
    
    # Limpiar colecciones existentes
    db.productos.delete_many({})
    db.inventario.delete_many({})
    
    # Insertar productos de prueba
    productos = [
        {
            "nombre": "Laptop Pro",
            "precio": 1299,
            "descripcion": "Laptop de alta gama para profesionales",
            "fecha_creacion": datetime.utcnow()
        },
        {
            "nombre": "Monitor 4K",
            "precio": 499,
            "descripcion": "Monitor 4K de 27 pulgadas",
            "fecha_creacion": datetime.utcnow()
        },
        {
            "nombre": "Teclado Mecánico",
            "precio": 129,
            "descripcion": "Teclado mecánico RGB",
            "fecha_creacion": datetime.utcnow()
        }
    ]
    
    # Insertar productos y sus inventarios
    for producto in productos:
        resultado = db.productos.insert_one(producto)
        
        # Crear inventario para cada producto
        db.inventario.insert_one({
            "producto_id": resultado.inserted_id,
            "cantidad": 100,
            "ultima_actualizacion": datetime.utcnow()
        })
    
    print("✅ Base de datos poblada con datos de prueba")
    print(f"📦 Productos insertados: {len(productos)}")

if __name__ == "__main__":
    seed_database()