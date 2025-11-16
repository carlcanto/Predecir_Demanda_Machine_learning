import streamlit as st
import pandas as pd

def display_data_preview(df: pd.DataFrame, file_info: dict):
    """Muestra vista previa de los datos cargados - VERSIÓN SIMPLE"""
    
    st.subheader("📊 Vista Previa de los Datos")
    
    # Métricas rápidas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Registros", f"{file_info['rows']:,}")
    
    with col2:
        st.metric("Total de Variables", file_info['columns'])
    
    with col3:
        st.metric("Variables Numéricas", len(file_info['numeric_columns']))
    
    with col4:
        st.metric("Variables Categóricas", len(file_info['categorical_columns']))
    
    # Mostrar artículos detectados
    if len(file_info['unique_articles']) > 1:
        articles_text = ", ".join(file_info['unique_articles'][1:4])  # Primeros 3
        if len(file_info['unique_articles']) > 4:
            articles_text += f"... (+{len(file_info['unique_articles'])-4} más)"
        st.info(f"**Artículos detectados:** {articles_text}")
    
    # Dataframe con datos originales
    st.dataframe(
        df.head(50),
        use_container_width=True,
        height=400
    )
    
    # Información de columnas
    with st.expander("🔍 Información Detallada de Columnas"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Columnas Numéricas:**")
            for col in file_info['numeric_columns']:
                st.write(f"• {col}")
        
        with col2:
            st.write("**Columnas Categóricas:**")
            for col in file_info['categorical_columns']:
                st.write(f"• {col}")

def display_welcome_message():
    """Muestra mensaje de bienvenida cuando no hay datos cargados"""
    
    st.markdown("""
    # 🤖 Sistema de Predicción de Demanda Optimizado por IA
    
    ## ¡Bienvenido!
    
    ### 🚀 Para comenzar:
    
    1. **Carga tus datos** en la barra lateral izquierda (formato Excel o CSV)
    2. **La aplicación mostrará** tus datos originales sin modificaciones
    3. **Verifica** que los datos se vean correctamente
    4. **Continúa** con las siguientes fases de desarrollo
    
    ### 📊 Estructura de datos esperada:
    
    Tu archivo debería contener columnas como:
    - **fecha**: Fechas de los registros
    - **articulo**: Nombre del producto  
    - **demanda**: Cantidad demandada
    - **precio**: Precio del producto
    - **promocion**: Si había promoción (0/1)
    
    ### 🎯 Próximos pasos:
    Una vez verificado que los datos se cargan correctamente, implementaremos:
    - Procesamiento automático de datos
    - Feature engineering
    - Modelos de machine learning
    """)