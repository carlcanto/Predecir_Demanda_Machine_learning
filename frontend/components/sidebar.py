import streamlit as st

def render_sidebar():
    """Renderiza la barra lateral con filtros y controles"""
    
    with st.sidebar:
        st.markdown("""
            <style>
            .sidebar .sidebar-content {
                background-color: #f8f9fa;
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.title("⚙️ Configuración de Predicción")
        
        # Sección 1: Carga de Datos
        st.header("📁 Carga de Datos")
        uploaded_file = st.file_uploader(
            "Cargar Datos Históricos (CSV o Excel)",
            type=['csv', 'xlsx', 'xls'],
            help="Sube tu archivo con datos históricos de demanda"
        )
        
        # Botón para limpiar datos si hay archivo cargado
        if uploaded_file is not None:
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🗑️ Limpiar Datos", type="secondary", use_container_width=True):
                    st.rerun()
            with col2:
                st.info(f"📄 {uploaded_file.name}")
        
        # Sección 2: Selección de Artículos - VALORES DINÁMICOS
        st.header("📦 Selección de Artículos")
        
        # Usar session_state para pasar los artículos detectados
        if 'unique_articles' not in st.session_state:
            st.session_state.unique_articles = ["Todos", "Producto A", "Producto B", "Producto C"]
        
        articulo_seleccionado = st.selectbox(
            "Seleccionar Artículo:",
            options=st.session_state.unique_articles,
            help="Filtrar por artículo específico"
        )
        
        # Sección 3: Variables Adicionales
        st.header("📊 Variables Adicionales")
        incluir_promociones = st.checkbox("¿Incluir datos de Promociones?", value=True)
        incluir_precio = st.checkbox("¿Incluir datos de Precio?", value=True)
        
        # Sección 4: Horizonte de Predicción
        st.header("📅 Horizonte de Predicción")
        col1, col2 = st.columns(2)
        with col1:
            fecha_inicio = st.date_input("Predecir desde:")
        with col2:
            duracion = st.selectbox(
                "Por los próximos:",
                options=["7 días", "30 días", "90 días"]
            )
        
        # Botón Principal
        st.markdown("---")
        ejecutar_prediccion = st.button(
            "🎯 Ejecutar Predicción de Demanda",
            type="primary",
            use_container_width=True
        )
    
    return {
        'uploaded_file': uploaded_file,
        'articulo_seleccionado': articulo_seleccionado,
        'incluir_promociones': incluir_promociones,
        'incluir_precio': incluir_precio,
        'fecha_inicio': fecha_inicio,
        'duracion': duracion,
        'ejecutar_prediccion': ejecutar_prediccion
    }