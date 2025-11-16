import streamlit as st
import sys
import os

# Configurar Python path para Docker
sys.path.append('/app')

# Importar componentes
from frontend.components.sidebar import render_sidebar
from frontend.components.data_display import display_data_preview, display_welcome_message

# Importar backend
from backend.file_handler import FileHandler

def main():
    """Aplicación principal de Streamlit - CON RECARGA AUTOMÁTICA"""
    
    # Configuración de la página
    st.set_page_config(
        page_title="Predictor de Demanda - IA",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS
    st.markdown("""
        <style>
        .main .block-container {
            padding-top: 2rem;
        }
        .stButton button {
            width: 100%;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Inicializar session_state para artículos
    if 'unique_articles' not in st.session_state:
        st.session_state.unique_articles = ["Todos", "Producto A", "Producto B", "Producto C"]
    if 'file_loaded' not in st.session_state:
        st.session_state.file_loaded = False
    
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
            
            # ACTUALIZAR LOS ARTÍCULOS EN SESSION_STATE
            nuevos_articulos = file_info['unique_articles']
            if (st.session_state.unique_articles != nuevos_articulos or 
                not st.session_state.file_loaded):
                
                st.session_state.unique_articles = nuevos_articulos
                st.session_state.file_loaded = True
                
                # FORZAR RECARGA para actualizar el dropdown
                st.rerun()
            
            display_data_preview(df, file_info)
    else:
        # Resetear cuando no hay archivo
        if st.session_state.file_loaded:
            st.session_state.unique_articles = ["Todos", "Producto A", "Producto B", "Producto C"]
            st.session_state.file_loaded = False
            st.rerun()
        
        display_welcome_message()

if __name__ == "__main__":
    main()