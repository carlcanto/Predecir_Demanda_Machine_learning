import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import streamlit as st
from typing import Dict, Optional, Any

# === DEBUG: VERIFICAR QUE EL ARCHIVO SE CARGA ===
st.success("🔥 ml_predictor.py CARGADO - " + pd.Timestamp.now().strftime("%H:%M:%S"))

class MLPredictor:
    """Predictor de Machine Learning para demostración en conferencia"""
    
    @staticmethod
    def predict_demand(df: pd.DataFrame, articulo: str = "Todos", dias_futuro: int = 30) -> Optional[Dict[str, Any]]:
        """
        Predice demanda futura usando Random Forest
        
        Args:
            df: DataFrame con datos históricos
            articulo: Artículo específico o "Todos"
            dias_futuro: Número de días a predecir (7-365)
            
        Returns:
            Dict con datos históricos y predicciones
        """
        
        st.info(f"🤖 INICIANDO PREDICCIÓN ML - Artículo: {articulo}, Días: {dias_futuro}")
        
        try:
            # VERIFICAR DATOS DE ENTRADA
            st.info("🔍 Verificando datos de entrada...")
            if df.empty:
                st.error("❌ DataFrame vacío")
                return None
                
            if 'demanda' not in df.columns:
                st.error("❌ Columna 'demanda' no encontrada")
                return None
                
            if 'fecha' not in df.columns:
                st.error("❌ Columna 'fecha' no encontrada")
                return None
            
            # FILTRAR POR ARTÍCULO SI NO ES "TODOS"
            df_ml = df.copy()
            if articulo != "Todos":
                if 'articulo' not in df_ml.columns:
                    st.error("❌ Columna 'articulo' no encontrada para filtrar")
                    return None
                    
                df_ml = df_ml[df_ml['articulo'] == articulo]
                st.info(f"✅ Filtrando por artículo: {articulo} - {len(df_ml)} registros")
            
            # VERIFICAR QUE HAY SUFICIENTES DATOS
            if len(df_ml) < 10:
                st.warning(f"⚠️ Pocos datos para entrenar ({len(df_ml)} registros)")
                return None
            
            # PREPARAR FEATURES PARA ML
            st.info("🔄 Preparando features para ML...")
            
            # Asegurar que la fecha esté en datetime
            df_ml['fecha'] = pd.to_datetime(df_ml['fecha'])
            df_ml = df_ml.sort_values('fecha').reset_index(drop=True)
            
            # Crear features temporales
            df_ml['dias_desde_inicio'] = (df_ml['fecha'] - df_ml['fecha'].min()).dt.days
            
            # Usar features existentes o crear básicas
            feature_columns = []
            if all(col in df_ml.columns for col in ['año', 'mes', 'dia', 'dia_semana']):
                feature_columns = ['año', 'mes', 'dia', 'dia_semana']
                st.info("✅ Usando features temporales existentes")
            else:
                # Crear features básicas desde la fecha
                df_ml['año'] = df_ml['fecha'].dt.year
                df_ml['mes'] = df_ml['fecha'].dt.month
                df_ml['dia'] = df_ml['fecha'].dt.day
                df_ml['dia_semana'] = df_ml['fecha'].dt.dayofweek
                feature_columns = ['año', 'mes', 'dia', 'dia_semana']
                st.info("✅ Creando features temporales básicas")
            
            # PREPARAR DATOS PARA ENTRENAMIENTO
            X = df_ml[feature_columns]
            y = df_ml['demanda']
            
            st.info(f"📊 Datos para entrenamiento: {X.shape[0]} muestras, {X.shape[1]} features")
            
            # ENTRENAR MODELO
            st.info("🏋️ Entrenando modelo Random Forest...")
            model = RandomForestRegressor(
                n_estimators=100,
                random_state=42,
                max_depth=10
            )
            
            model.fit(X, y)
            st.success("✅ Modelo entrenado exitosamente")
            
            # GENERAR PREDICCIONES FUTURAS
            st.info("🔮 Generando predicciones futuras...")
            
            ultima_fecha = df_ml['fecha'].max()
            st.info(f"📅 Última fecha histórica: {ultima_fecha.strftime('%Y-%m-%d')}")
            
            # Crear fechas futuras
            fechas_futuras = pd.date_range(
                start=ultima_fecha + pd.Timedelta(days=1),
                periods=dias_futuro,
                freq='D'
            )
            
            # Preparar features para fechas futuras
            X_future = pd.DataFrame({
                'año': fechas_futuras.year,
                'mes': fechas_futuras.month,
                'dia': fechas_futuras.day,
                'dia_semana': fechas_futuras.dayofweek
            })
            
            # Hacer predicciones
            predicciones = model.predict(X_future)
            
            st.success(f"🎯 Predicción completada - {len(predicciones)} días futuros")
            
            # PREPARAR RESULTADOS
            resultado = {
                'fechas_historicas': df_ml['fecha'].values,
                'demanda_historica': df_ml['demanda'].values,
                'fechas_futuras': fechas_futuras,
                'predicciones': predicciones,
                'articulo': articulo,
                'dias_prediccion': dias_futuro,
                'modelo_info': f"RandomForest (n_estimators=100)"
            }
            
            return resultado
            
        except Exception as e:
            st.error(f"❌ ERROR en predict_demand: {str(e)}")
            import traceback
            st.error(f"📋 Traceback: {traceback.format_exc()}")
            return None
    
    @staticmethod
    def export_to_excel(prediction_data: Dict[str, Any]) -> bytes:
        """Exporta datos históricos y predicciones a Excel"""
        
        try:
            st.info("💾 Preparando archivo Excel para descarga...")
            
            # Crear DataFrame combinado
            datos_historicos = pd.DataFrame({
                'Fecha': prediction_data['fechas_historicas'],
                'Demanda': prediction_data['demanda_historica'],
                'Tipo': 'Histórico'
            })
            
            datos_prediccion = pd.DataFrame({
                'Fecha': prediction_data['fechas_futuras'],
                'Demanda': prediction_data['predicciones'],
                'Tipo': 'Predicción'
            })
            
            # Combinar datos
            df_completo = pd.concat([datos_historicos, datos_prediccion], ignore_index=True)
            df_completo = df_completo.sort_values('Fecha')
            
            # Crear archivo Excel en memoria
            output = pd.ExcelWriter('prediccion_demanda.xlsx', engine='openpyxl')
            df_completo.to_excel(output, sheet_name='Predicción Completa', index=False)
            
            # Agregar hoja de resumen
            resumen = pd.DataFrame({
                'Métrica': ['Artículo', 'Días Predicción', 'Modelo', 'Total Registros'],
                'Valor': [
                    prediction_data['articulo'],
                    prediction_data['dias_prediccion'],
                    prediction_data['modelo_info'],
                    len(df_completo)
                ]
            })
            resumen.to_excel(output, sheet_name='Resumen', index=False)
            
            output.close()
            
            # Leer archivo como bytes para descarga
            with open('prediccion_demanda.xlsx', 'rb') as f:
                excel_bytes = f.read()
            
            st.success("✅ Archivo Excel preparado exitosamente")
            return excel_bytes
            
        except Exception as e:
            st.error(f"❌ Error exportando a Excel: {e}")
            return None

# === VERIFICACIÓN DE IMPORTS ===
st.success("✅ MLPredictor importado correctamente")