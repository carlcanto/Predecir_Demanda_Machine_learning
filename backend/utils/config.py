import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    """Configuración de la aplicación"""
    # Configuración de Streamlit
    STREAMLIT_PORT = int(os.getenv('STREAMLIT_SERVER_PORT', 8501))
    STREAMLIT_HOST = os.getenv('STREAMLIT_SERVER_ADDRESS', '0.0.0.0')
    
    # Configuración de datos
    ALLOWED_EXTENSIONS = {'.xlsx', '.xls', '.csv'}
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB