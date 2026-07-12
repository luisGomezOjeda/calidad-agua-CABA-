import streamlit as st
import pandas as pd
from pathlib import Path

# PROHIBIDO definir el diccionario acá afuera

@st.cache_data
def load_data():
    # 1. El diccionario NACE acá adentro
    datos_cargados = {}
    
    # 2. Ruta a prueba de fallos: busca 'dataSets' justo al lado de donde esté este script
    ruta_script = Path(__file__).resolve()
    current_folder = ruta_script.parent / 'dataSets'
    
    # Verificación de seguridad
    if not current_folder.exists():
        print(f"Error crítico: La carpeta no existe en {current_folder}")
        return datos_cargados
        
    for file in current_folder.glob('*.csv'):
        # 3. Tu genialidad del .strip() la mantenemos
        print(file.stem.strip())
        datos_cargados[file.stem.strip()] = pd.read_csv(file)
        
    # 4. Retornamos la variable local
    return datos_cargados

# 5. Ejecutamos y CAPTURAMOS el resultado en el flujo principal
datasets = load_data()