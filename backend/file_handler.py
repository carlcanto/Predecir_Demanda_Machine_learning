import pandas as pd
import numpy as np
import os
from typing import Tuple, Optional, List, Dict, Any
import streamlit as st

# === VERSIÓN NUEVA - DATAPROCESSOR INTEGRADO ===
st.error("🔥 FILE_HANDLER NUEVO - DATAPROCESSOR INTEGRADO - " + pd.Timestamp.now().strftime("%H:%M:%S"))

class DataProcessor:
    """DataProcessor integrado - VERSIÓN NUEVA"""
    
    @staticmethod
    def _handle_missing_values(df: pd.DataFrame, show_messages: bool = True) -> pd.DataFrame:
        """Manejo INTELIGENTE de valores faltantes"""
        df_processed = df.copy()
        
        if show_messages:
            st.info("🔍 Analizando valores faltantes...")
        
        for col in df_processed.columns:
            missing_count = df_processed[col].isna().sum()
            
            if missing_count > 0:
                missing_pct = (missing_count / len(df_processed)) * 100
                
                # Estrategias según tipo de columna
                if df_processed[col].dtype in ['float64', 'int64']:
                    # Numéricas: usar mediana (menos sensible a outliers)
                    if missing_pct < 10:  # Solo si menos del 10% faltante
                        fill_value = df_processed[col].median()
                        df_processed[col].fillna(fill_value, inplace=True)
                        if show_messages:
                            st.info(f"🔧 {missing_count} valores numéricos faltantes en '{col}' llenados con {fill_value:.2f}")
                    elif show_messages:
                        st.warning(f"⚠️ Columna '{col}' tiene {missing_pct:.1f}% valores faltantes")
                
                elif df_processed[col].dtype == 'object':
                    # Categóricas: usar moda solo si pocos faltantes
                    if missing_pct < 5:
                        if not df_processed[col].mode().empty:
                            fill_value = df_processed[col].mode()[0]
                            df_processed[col].fillna(fill_value, inplace=True)
                            if show_messages:
                                st.info(f"🔧 {missing_count} valores categóricos faltantes en '{col}' llenados con '{fill_value}'")
        
        return df_processed

    @staticmethod
    def _convert_only_fecha_column(df: pd.DataFrame, show_messages: bool = True) -> pd.DataFrame:
        """Convierte SOLO la columna 'fecha'"""
        df_processed = df.copy()
        
        if 'fecha' in df_processed.columns:
            if not pd.api.types.is_datetime64_any_dtype(df_processed['fecha']):
                df_processed['fecha'] = pd.to_datetime(df_processed['fecha'], errors='coerce')
                if show_messages:
                    st.success("✅ 'fecha' convertida a datetime")
        return df_processed

    @staticmethod
    def _basic_feature_engineering(df: pd.DataFrame, show_messages: bool = True) -> pd.DataFrame:
        """Feature engineering básico"""
        df_processed = df.copy()
        
        if 'fecha' in df_processed.columns and pd.api.types.is_datetime64_any_dtype(df_processed['fecha']):
            if df_processed['fecha'].notna().sum() > 0:
                if show_messages:
                    st.info("🔄 Creando features temporales...")
                
                df_processed['año'] = df_processed['fecha'].dt.year
                df_processed['mes'] = df_processed['fecha'].dt.month
                df_processed['dia'] = df_processed['fecha'].dt.day
                df_processed['semana_año'] = df_processed['fecha'].dt.isocalendar().week
                df_processed['dia_semana'] = df_processed['fecha'].dt.dayofweek
                df_processed['nombre_dia'] = df_processed['fecha'].dt.day_name()
                df_processed['es_fin_semana'] = df_processed['fecha'].dt.dayofweek >= 5
                
                if show_messages:
                    st.success("🎉 FEATURES CREADAS: año, mes, dia, semana_año, dia_semana, nombre_dia, es_fin_semana")
        
        return df_processed

    @staticmethod
    def auto_process_data(df: pd.DataFrame, show_messages: bool = True) -> pd.DataFrame:
        st.info("🎯 DATA PROCESSOR - INICIANDO...")
        
        df_processed = df.copy()
        
        # 1. PRIMERO: Manejar valores faltantes
        df_processed = DataProcessor._handle_missing_values(df_processed, show_messages)
        
        # 2. LUEGO: Convertir fechas
        if show_messages:
            st.info("🔍 Verificando columna 'fecha'...")
        
        if 'fecha' in df_processed.columns:
            if show_messages:
                st.success("✅ Columna 'fecha' encontrada")
            
            df_processed = DataProcessor._convert_only_fecha_column(df_processed, show_messages)
            
            # 3. FINALMENTE: Feature engineering
            df_processed = DataProcessor._basic_feature_engineering(df_processed, show_messages)
        else:
            if show_messages:
                st.error("❌ Columna 'fecha' NO encontrada")
        
        return df_processed
    
    @staticmethod
    def detect_unique_articles(df: pd.DataFrame) -> List[str]:
        """Detección INTELIGENTE de columna de artículos"""
        
        # Múltiples nombres posibles para artículos
        articulo_names = ['articulo', 'producto', 'product', 'item', 'sku', 'descripcion', 'nombre']
        
        # Buscar por nombres exactos primero
        for col in df.columns:
            if col.lower() in articulo_names:
                unique_vals = df[col].dropna().unique()
                if len(unique_vals) > 0:
                    st.success(f"✅ Columna de artículos detectada: '{col}'")
                    return ["Todos"] + [str(x) for x in unique_vals]
        
        # Buscar por patrón en el nombre
        for col in df.columns:
            col_lower = col.lower()
            if any(name in col_lower for name in articulo_names):
                unique_vals = df[col].dropna().unique()
                if len(unique_vals) > 0 and len(unique_vals) < len(df) * 0.5:
                    st.success(f"✅ Columna de artículos detectada: '{col}'")
                    return ["Todos"] + [str(x) for x in unique_vals]
        
        # Buscar primera columna categórica con valores repetidos
        for col in df.select_dtypes(include=['object']).columns:
            unique_vals = df[col].dropna().unique()
            if 1 < len(unique_vals) < len(df) * 0.3:  # No único, no todos distintos
                st.info(f"ℹ️ Columna candidata para artículos: '{col}'")
                return ["Todos"] + [str(x) for x in unique_vals]
        
        st.warning("⚠️ No se pudo detectar automáticamente la columna de artículos")
        return ["Todos"]
    
    @staticmethod
    def get_data_quality_report(df: pd.DataFrame) -> Dict[str, Any]:
        features_sistema = ['año', 'mes', 'dia', 'semana_año', 'dia_semana', 'nombre_dia', 'es_fin_semana']
        columnas_sistema = [col for col in df.columns if col in features_sistema]
        
        data_types = {}
        for col in df.columns:
            data_types[col] = str(df[col].dtype)
        
        return {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'original_columns': len(df.columns) - len(columnas_sistema),
            'system_columns': len(columnas_sistema),
            'missing_values': {col: {'count': df[col].isna().sum(), 'percentage': (df[col].isna().sum() / len(df)) * 100} for col in df.columns},
            'data_types': data_types,
            'system_features': columnas_sistema
        }
    
    @staticmethod
    def suggest_target_column(df: pd.DataFrame) -> Optional[str]:
        return 'demanda' if 'demanda' in df.columns else None

class FileHandler:
    """FileHandler NUEVO con DataProcessor"""
    
    @staticmethod
    def load_file(uploaded_file) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        st.error("🔥 FILE_HANDLER.load_file() EJECUTADO - VERSIÓN NUEVA")
        
        try:
            st.info(f"🔍 Cargando archivo: {uploaded_file.name}")
            
            if uploaded_file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(uploaded_file)
            elif uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                return None, "Formato no soportado"
            
            st.info(f"✅ Archivo cargado: {df.shape[0]} filas, {df.shape[1]} columnas")
            
            # LLAMAR AL DATA PROCESSOR
            st.info("🔄 INICIANDO DATA PROCESSOR...")
            df_processed = DataProcessor.auto_process_data(df)
            st.info("✅ DATA PROCESSOR COMPLETADO")
            
            # Verificar cambios
            nuevas_columnas = set(df_processed.columns) - set(df.columns)
            if nuevas_columnas:
                st.success(f"🎉 NUEVAS COLUMNAS: {list(nuevas_columnas)}")
            else:
                st.error("❌ NO SE CREARON NUEVAS COLUMNAS")
            
            return df_processed, None
            
        except Exception as e:
            return None, f"Error: {str(e)}"
    
    @staticmethod
    def get_file_info(df: pd.DataFrame) -> dict:
        info = DataProcessor.get_data_quality_report(df)
        
        info.update({
            'column_names': df.columns.tolist(),
            'numeric_columns': df.select_dtypes(include=['number']).columns.tolist(),
            'categorical_columns': df.select_dtypes(include=['object']).columns.tolist(),
            'date_columns': df.select_dtypes(include=['datetime64']).columns.tolist(),
            'unique_articles': DataProcessor.detect_unique_articles(df),
            'suggested_target': DataProcessor.suggest_target_column(df)
        })
        
        return info