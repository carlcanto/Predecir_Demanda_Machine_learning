import pandas as pd
import numpy as np
import os
from typing import Tuple, Optional, List, Dict
import streamlit as st

class FileHandler:
    """Manejador de archivos para carga de datos - SIN PROCESAMIENTO"""
    
    @staticmethod
    def load_file(uploaded_file) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
        """
        Carga archivo Excel o CSV - DATOS ORIGINALES
        """
        try:
            st.info(f"🔍 Cargando archivo: {uploaded_file.name}")
            
            if uploaded_file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(uploaded_file)
            elif uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                return None, "Formato de archivo no soportado"
            
            # DEBUG: Mostrar información del DataFrame cargado
            st.info(f"✅ Archivo cargado: {df.shape[0]} filas, {df.shape[1]} columnas")
            st.info(f"📋 Columnas: {list(df.columns)}")
            
            if 'articulo' in df.columns:
                st.info(f"🎯 Columna 'articulo' encontrada. Valores: {df['articulo'].head(3).tolist()}")
            else:
                st.warning("⚠️ Columna 'articulo' NO encontrada")
            
            # DEVOLVER DATOS ORIGINALES SIN MODIFICAR
            return df, None
            
        except Exception as e:
            return None, f"Error al cargar archivo: {str(e)}"
    
    @staticmethod
    def get_file_info(df: pd.DataFrame) -> dict:
        """Obtiene información básica del archivo cargado"""
        info = {
            'rows': df.shape[0],
            'columns': df.shape[1],
            'column_names': df.columns.tolist(),
            'numeric_columns': df.select_dtypes(include=['number']).columns.tolist(),
            'categorical_columns': df.select_dtypes(include=['object']).columns.tolist(),
            'date_columns': df.select_dtypes(include=['datetime64']).columns.tolist(),
            'unique_articles': FileHandler._detect_unique_articles_simple(df)
        }
        
        st.info(f"🎯 Artículos para dropdown: {info['unique_articles']}")
        return info
    
    @staticmethod
    def _detect_unique_articles_simple(df: pd.DataFrame) -> List[str]:
        """Detección simple de artículos"""
        # Buscar columna 'articulo' exacta
        if 'articulo' in df.columns:
            unique_vals = df['articulo'].dropna().unique()
            st.success(f"✅ Artículos detectados: {list(unique_vals)}")
            return ["Todos"] + [str(x) for x in unique_vals]
        
        st.warning("❌ Columna 'articulo' NO encontrada")
        return ["Todos"]