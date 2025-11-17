import streamlit as st
import pandas as pd

def display_data_preview(df: pd.DataFrame, file_info: dict):

    """Muestra vista previa de los datos cargados - CON VERIFICACIÓN MANUAL"""
    
    st.subheader("📊 Vista Previa de los Datos")
    
    # VERIFICACIÓN MANUAL: ¿Se crearon las features?
    features_esperadas = ['año', 'mes', 'dia', 'semana_año', 'dia_semana', 'nombre_dia', 'es_fin_semana']
    features_encontradas = [col for col in features_esperadas if col in df.columns]
    
    if features_encontradas:
        st.success(f"✅ VERIFICACIÓN: Se crearon {len(features_encontradas)} features temporales")
        st.info(f"📋 Features encontradas: {', '.join(features_encontradas)}")
    else:
        st.warning("⚠️ VERIFICACIÓN: No se encontraron features temporales creadas")
    
    # Resto del código igual...
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total de Registros", f"{file_info.get('rows', 0):,}")

    """Muestra vista previa de los datos cargados - CON MANEJO SEGURO"""
    
    st.subheader("📊 Vista Previa de los Datos")
    
    # Métricas rápidas - CON MANEJO SEGURO
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total de Registros", f"{file_info.get('rows', 0):,}")
    
    with col2:
        original_cols = file_info.get('original_columns', file_info.get('columns', 0))
        st.metric("Variables Originales", original_cols)
    
    with col3:
        st.metric("Variables del Sistema", file_info.get('system_columns', 0))
    
    with col4:
        st.metric("Variables Numéricas", len(file_info.get('numeric_columns', [])))
    
    with col5:
        date_cols = len(file_info.get('date_columns', []))
        st.metric("Columnas de Fecha", date_cols)
    
    # Mostrar artículos detectados
    if len(file_info.get('unique_articles', [])) > 1:
        articles_text = ", ".join(file_info['unique_articles'][1:4])
        if len(file_info['unique_articles']) > 4:
            articles_text += f"... (+{len(file_info['unique_articles'])-4} más)"
        st.info(f"**Artículos detectados:** {articles_text}")
    
    # Mostrar features creadas por el sistema
    if 'system_features' in file_info and file_info['system_features']:
        st.success(f"**🎯 Features temporales creadas:** {', '.join(file_info['system_features'])}")
    
    # Separar columnas originales y del sistema para mejor visualización
    system_features = file_info.get('system_features', [])
    columnas_originales = [col for col in df.columns if col not in system_features]
    columnas_sistema = system_features
    
    # Dataframe con datos ORIGINALES (sin features del sistema)
    st.write("**📋 Datos Originales:**")
    st.dataframe(
        df[columnas_originales].head(30),
        use_container_width=True,
        height=300
    )
    
    # Dataframe con FEATURES CREADAS por el sistema
    if columnas_sistema:
        st.write("**⚙️ Features Creadas por el Sistema:**")
        st.dataframe(
            df[columnas_sistema].head(10),
            use_container_width=True,
            height=250
        )
    
    # Información de columnas - CON MANEJO SEGURO
    with st.expander("🔍 Información Detallada de Columnas"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Columnas Originales:**")
            for col in columnas_originales:
                # Manejo seguro de data_types
                data_types = file_info.get('data_types', {})
                dtype = data_types.get(col, 'desconocido')
                st.write(f"• {col} ({dtype})")
        
        with col2:
            if columnas_sistema:
                st.write("**Features del Sistema:**")
                for col in columnas_sistema:
                    st.write(f"• {col} (feature temporal)")
    display_exploratory_analysis(df, file_info)

def display_welcome_message():
    """Muestra mensaje de bienvenida"""
    
    st.markdown("""
    # 🤖 Sistema de Predicción de Demanda - IA
    
    ## ¡Fase 2 - Iteración 2: Feature Engineering!
    
    **Nuevas funcionalidades implementadas:**
    - ✅ **Feature engineering temporal** (año, mes, día, semana)
    - ✅ **Separación clara** entre datos originales y features creadas
    - ✅ **Métricas mejoradas** para tracking de features
    
    ### 🚀 Para probar:
    
    1. **Carga tu archivo Excel** con columna 'fecha'
    2. **Verifica** que se crean las features temporales
    3. **Observa** la separación entre datos originales y features del sistema
    
    ### 🎯 Features creadas automáticamente:
    - **año, mes, dia**: Componentes básicos de fecha
    - **semana_año**: Número de semana (1-52)
    - **dia_semana**: Día de la semana (0=Lunes, 6=Domingo)
    - **nombre_dia**: Nombre del día en español
    - **es_fin_semana**: True/False para fines de semana
    """)

def display_exploratory_analysis(df: pd.DataFrame, file_info: dict):
    """Análisis exploratorio básico"""
    
    with st.expander("📈 Análisis Exploratorio", expanded=True):
        
        # 1. Estadísticas básicas de demanda
        if 'demanda' in df.columns:
            st.write("**📊 Estadísticas de Demanda:**")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Promedio", f"{df['demanda'].mean():.0f}")
            with col2:
                st.metric("Mediana", f"{df['demanda'].median():.0f}")
            with col3:
                st.metric("Máximo", f"{df['demanda'].max():.0f}")
            with col4:
                st.metric("Mínimo", f"{df['demanda'].min():.0f}")
        
        # 2. Distribución por artículo
        if 'articulo' in df.columns and 'demanda' in df.columns:
            st.write("**📦 Demanda por Artículo:**")
            demanda_por_articulo = df.groupby('articulo')['demanda'].agg(['sum', 'mean', 'count']).round(0)
            st.dataframe(demanda_por_articulo, use_container_width=True)
        
        # 3. Tendencia temporal si hay fecha
        date_cols = file_info.get('date_columns', [])
        if date_cols and 'demanda' in df.columns:
            fecha_col = date_cols[0]
            st.write("**📅 Tendencia Temporal:**")
            
            # Agrupar por mes para ver tendencia
            try:
                df_temp = df.copy()
                df_temp['año_mes'] = df_temp[fecha_col].dt.to_period('M')
                tendencia_mensual = df_temp.groupby('año_mes')['demanda'].sum().reset_index()
                tendencia_mensual['año_mes'] = tendencia_mensual['año_mes'].astype(str)
                
                st.line_chart(tendencia_mensual.set_index('año_mes')['demanda'])
            except:
                st.info("ℹ️ No se pudo generar gráfico de tendencia")