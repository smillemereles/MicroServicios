from pymongo import MongoClient
from config import MONGODB_URI, MONGODB_DB

def test_connection():
    try:
        # Crear cliente de MongoDB
        client = MongoClient(MONGODB_URI)
        
        # Acceder a la base de datos
        db = client[MONGODB_DB]
        
        # Probar la conexión
        client.server_info()
        
        print("✅ Conexión exitosa a MongoDB")
        print(f"📁 Base de datos: {MONGODB_DB}")
        print("📊 Colecciones disponibles:")
        for collection in db.list_collection_names():
            print(f"  - {collection}")
            
        return True
        
    except Exception as e:
        print("❌ Error de conexión a MongoDB:")
        print(f"Error: {str(e)}")
        return False
    
if __name__ == "__main__":
    test_connection()