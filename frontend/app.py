import pandas as pd
import streamlit as st
import sys
import os

# === ESTE DEBE SER EL PRIMER COMANDO DE STREAMLIT ===
st.set_page_config(
    page_title="Predictor de Demanda - IA",
    page_icon="📈", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# === VERIFICACIÓN CRÍTICA ===
st.error("🚨 VERIFICANDO VERSIÓN DE FILE_HANDLER - " + str(__import__('datetime').datetime.now()))

# Configurar Python path para Docker
sys.path.append('/app')

# DEBUG DE IMPORTACIÓN - DESPUÉS de set_page_config
st.info("🔄 Iniciando aplicación...")

# Importar componentes
try:
    from frontend.components.sidebar import render_sidebar
    from frontend.components.data_display import display_data_preview, display_welcome_message
    st.success("✅ Componentes frontend importados")
except ImportError as e:
    st.error(f"❌ Error importando componentes: {e}")

# DEBUG: Antes de importar FileHandler
st.info("🔍 Intentando importar FileHandler...")

# Importar backend CON DEBUG
try:
    from backend.file_handler import FileHandler
    st.success("✅ FileHandler importado exitosamente")
    
    # DEBUG: Verificar si es la versión correcta
    if hasattr(FileHandler, 'load_file'):
        st.success("✅ FileHandler tiene método load_file")
    else:
        st.error("❌ FileHandler NO tiene método load_file")
        
except ImportError as e:
    st.error(f"❌ Error importando FileHandler: {e}")
    st.stop()

st.info("🔍 Intentando importar MLPredictor...")
try:
    from backend.ml_predictor import MLPredictor
    st.success("✅ MLPredictor importado exitosamente - " + pd.Timestamp.now().strftime("%H:%M:%S"))
except ImportError as e:
    st.error(f"❌ Error importando MLPredictor: {e}")
    # No paramos la app, solo mostramos error

def main():
    """Aplicación principal de Streamlit"""
    
    # Inicializar session_state para artículos
    if 'unique_articles' not in st.session_state:
        st.session_state.unique_articles = ["Todos", "Producto A", "Producto B", "Producto C"]
    
    # Renderizar sidebar y obtener configuraciones
    sidebar_config = render_sidebar()
    
    # Área principal de contenido
    if sidebar_config['uploaded_file'] is not None:
        st.info("🔄 Procesando archivo...")
        
        # Cargar y procesar archivo
        df, error = FileHandler.load_file(sidebar_config['uploaded_file'])
        
        if error:
            st.error(f"❌ Error al cargar archivo: {error}")
            display_welcome_message()
        else:
            st.success("✅ Archivo cargado exitosamente")
            file_info = FileHandler.get_file_info(df)
            
            # Actualizar artículos
            st.session_state.unique_articles = file_info['unique_articles']
            
            display_data_preview(df, file_info)
    else:
        display_welcome_message()

if __name__ == "__main__":
    main()