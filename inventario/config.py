

import os
from dotenv import load_dotenv

load_dotenv()

# URLs de servicios
PRODUCTOS_SERVICE_URL = os.getenv('PRODUCTOS_SERVICE_URL', 'http://localhost:5000')
