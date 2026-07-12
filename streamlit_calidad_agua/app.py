import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio 
from plotly.subplots import make_subplots
import streamlit as st
from cache_data import load_data
from pathlib import Path

# --- ERROR 1 CORREGIDO: DEBE SER LA PRIMERA INSTRUCCIÓN DE STREAMLIT ---
st.set_page_config(layout="wide")

pio.templates.default = 'plotly_dark'

# --- CARGA DE DATASETS ---
datasets = load_data()

df_map_det = datasets['porcentaje_determinacion']
fig_det = px.bar(
    df_map_det,
    x='determinación',
    y=['errores de imputación', 'fuera de limite', 'nulos'],
    barmode='group',
    title='Porcentaje De Mediciones Nulas, Fuera De Limite y Errores De Imputación por Determinación'
)
fig_det.update_yaxes(title_text='Porcentaje')
fig_det.update_layout(autosize=True)

calidad_del_agua_2024_head = datasets['calidad_del_agua_2024_head']
calidad_del_agua_2025_head = datasets['calidad_del_agua_2025_head']
calidad_del_agua_2026_head = datasets['calidad_del_agua_2026_head']
calidad_del_agua_melt = datasets['calidad_del_agua_melt']
head_calidad_del_agua_pivot_PCA = datasets['head_calidad_del_agua_pivot_PCA']

df_true_values = datasets['cantidad_mediciones_no_nulas']
frecuencia_determinacion = datasets['frecuencia_determinacion']

fig_true = px.bar(df_true_values, x='determinación', y='cantidad', color='determinación', title='Cantidad de mediciones no nulas por determinación')
fig_true.update_layout(autosize=True)

df_pivot = datasets['calidad_del_agua_pivot_not_processed']
head_calidad_del_agua_pivot_processed = datasets['head_calidad_del_agua_pivot_processed']

texto_outliers = "<b>Lugar:</b> " + df_pivot['LUGAR'] + "<br><b>Fecha:</b> " + df_pivot['FECHA'].astype(str)

# --- ERROR 3 CORREGIDO: Rediseño de subplots a 2x3 para evitar espacios vacíos y habilitar el responsive ---
fig = make_subplots(
    rows=2, cols=3,
    subplot_titles=("Oxígeno", "Arsénico Total", "Coliformes Fecales", "DBO5", "DQO", "Sólidos Disueltos Totales")
)

fig.add_trace(go.Box(y=df_pivot['oxígeno'], name='Oxígeno', text=texto_outliers, boxpoints='outliers'), row=1, col=1)
fig.add_trace(go.Box(y=df_pivot['arsénico total'], name='Arsénico Total', text=texto_outliers, boxpoints='outliers'), row=1, col=2)
fig.add_trace(go.Box(y=df_pivot['coliformes fecales'], name='Coliformes Fecales', text=texto_outliers, boxpoints='outliers'), row=1, col=3)
fig.add_trace(go.Box(y=df_pivot['dbo5'], name='dbo5', text=texto_outliers, boxpoints='outliers'), row=2, col=1)
fig.add_trace(go.Box(y=df_pivot['dqo'], name='DQO', text=texto_outliers, boxpoints='outliers'), row=2, col=2)
fig.add_trace(go.Box(y=df_pivot['sólidos disueltos totales'], name='Sólidos Disueltos Totales', text=texto_outliers, boxpoints='outliers'), row=2, col=3)

fig.update_layout(
    title_text="Boxplots de Mediciones por Determinación",
    height=700,
    autosize=True,  # Se estira dinámicamente
    margin=dict(l=20, r=20, t=100, b=20)
)

# --- MATRIZ DE CORRELACIÓN ---
df_corr = datasets['correlacion_determinaciones']
if 'Unnamed: 0' in df_corr.columns:
    df_corr.index = df_corr['Unnamed: 0']
    df_corr = df_corr.drop(columns=['Unnamed: 0'])
df_corr.index.name = 'Determinación'

fig_corr = px.imshow(
    df_corr,
    text_auto=True,
    aspect="auto",
    title='Correlación Cruzada De Spearman Entre Las Distintas Determinaciones'
)
fig_corr.update_layout(autosize=True)

# --- MAPAS Y PCA DATA ---
df_PCA = datasets['completed_calidad_del_agua_pivot_PCA']

fig_trend_INDICE_INORGANICO = px.line(df_PCA, x='FECHA', y='INDICE_INORGANICO', color='TIPO_DE_MASA', line_group='LUGAR', title='INDICE INORGANICO')
fig_trend_INDICE_CONTAMINACION_ORGANICA = px.line(df_PCA, x='FECHA', y='INDICE_CONTAMINACIÓN_BIOLOGICA', color='TIPO_DE_MASA', line_group='LUGAR', title='INDICE_CONTAMINACIÓN_BIOLOGICA')
fig_trend_OXIGENO = px.line(df_PCA, x='FECHA', y='OXÍGENO', color='TIPO_DE_MASA', line_group='LUGAR', title='OXÍGENO')

df_PCA_2024 = datasets['completed_calidad_del_agua_pivot_PCA_2024']
df_PCA_2025 = datasets['completed_calidad_del_agua_pivot_PCA_2025']
df_PCA_2026 = datasets['completed_calidad_del_agua_pivot_PCA_2026']

# ==========================================
# MAPA INTEGRADO: ÍNDICE INORGÁNICO
# ==========================================
fig_map_INORGANICO_2024 = px.density_mapbox(df_PCA_2024, lat='LAT', lon='LONG', z='INDICE_INORGANICO', radius=15, mapbox_style="open-street-map", color_continuous_scale="Viridis", opacity=0.6, zoom=11.5, hover_data={'LAT': True, 'LONG': True, 'FECHA' : True, 'INDICE_INORGANICO': ':.2f', 'LUGAR': True, 'TIPO_DE_MASA': True}, height=900)
fig_map_INORGANICO_2025 = px.density_mapbox(df_PCA_2025, lat='LAT', lon='LONG', z='INDICE_INORGANICO', radius=15, mapbox_style="open-street-map", color_continuous_scale="Viridis", opacity=0.6, zoom=11.5, hover_data={'LAT': True, 'LONG': True, 'FECHA' : True, 'INDICE_INORGANICO': ':.2f', 'LUGAR': True, 'TIPO_DE_MASA': True}, height=900)
fig_map_INORGANICO_2026 = px.density_mapbox(df_PCA_2026, lat='LAT', lon='LONG', z='INDICE_INORGANICO', radius=15, mapbox_style="open-street-map", color_continuous_scale="Viridis", opacity=0.6, zoom=11.5, hover_data={'LAT': True, 'LONG': True, 'FECHA' : True, 'INDICE_INORGANICO': ':.2f', 'LUGAR': True, 'TIPO_DE_MASA': True}, height=900)

fig_integrada_INORGANICO = go.Figure()
fig_integrada_INORGANICO.add_trace(fig_map_INORGANICO_2024.data[0])
fig_integrada_INORGANICO.add_trace(fig_map_INORGANICO_2025.data[0])
fig_integrada_INORGANICO.add_trace(fig_map_INORGANICO_2026.data[0])
fig_integrada_INORGANICO.data[0].visible = True
fig_integrada_INORGANICO.data[1].visible = False
fig_integrada_INORGANICO.data[2].visible = False
fig_integrada_INORGANICO.update_layout(fig_map_INORGANICO_2024.layout)
fig_integrada_INORGANICO.update_layout(
    paper_bgcolor='#121212', font=dict(color='#e0e0e0'), title=dict(text="Índice INORGANICO", y=1), margin=dict(r=0, t=0, l=0, b=0),
    updatemenus=[dict(type="buttons", direction="right", x=0.1, y=1.08, pad={"r": 10, "t": 20, "l": 10, "b": 10}, xanchor="center", yanchor="bottom", showactive=True, bgcolor="#2d2d2d", bordercolor="#00adb5", font=dict(color="#808080"),
    buttons=list([
        dict(label="📊 Año 2024", method="update", args=[{"visible": [True, False, False]}, {"title": "Índice INORGÁNICO en 2024"}]),
        dict(label="📊 Año 2025", method="update", args=[{"visible": [False, True, False]}, {"title": "Índice INORGÁNICO en 2025"}]),
        dict(label="📊 Año 2026", method="update", args=[{"visible": [False, False, True]}, {"title": "Índice INORGÁNICO en 2026"}])
    ]))]
)

# ==========================================
# MAPA INTEGRADO: CONTAMINACIÓN BIOLÓGICA
# ==========================================
fig_map_CONTAMINACION_BIOLOGICA_2024 = px.density_mapbox(df_PCA_2024, lat='LAT', lon='LONG', z='INDICE_CONTAMINACIÓN_BIOLOGICA', radius=15, mapbox_style="open-street-map", color_continuous_scale="Viridis", opacity=0.6, zoom=11.5, labels={"INDICE_CONTAMINACIÓN_BIOLOGICA": "Contaminación Biológica"}, hover_data={'LAT': True, 'LONG': True, 'FECHA' : True, 'INDICE_CONTAMINACIÓN_BIOLOGICA': ':.2f', 'LUGAR': True, 'TIPO_DE_MASA': True}, height=900)
fig_map_CONTAMINACION_BIOLOGICA_2025 = px.density_mapbox(df_PCA_2025, lat='LAT', lon='LONG', z='INDICE_CONTAMINACIÓN_BIOLOGICA', radius=15, mapbox_style="open-street-map", color_continuous_scale="Viridis", opacity=0.6, zoom=11.5, labels={"INDICE_CONTAMINACIÓN_BIOLOGICA": "Contaminación Biológica"}, hover_data={'LAT': True, 'LONG': True, 'FECHA' : True, 'INDICE_CONTAMINACIÓN_BIOLOGICA': ':.2f', 'LUGAR': True, 'TIPO_DE_MASA': True}, height=900)
fig_map_CONTAMINACION_BIOLOGICA_2026 = px.density_mapbox(df_PCA_2026, lat='LAT', lon='LONG', z='INDICE_CONTAMINACIÓN_BIOLOGICA', radius=15, mapbox_style="open-street-map", color_continuous_scale="Viridis", opacity=0.6, zoom=11.5, labels={"INDICE_CONTAMINACIÓN_BIOLOGICA": "Contaminación Biológica"}, hover_data={'LAT': True, 'LONG': True, 'FECHA' : True, 'INDICE_CONTAMINACIÓN_BIOLOGICA': ':.2f', 'LUGAR': True, 'TIPO_DE_MASA': True}, height=900)

fig_integrada_CONTAMINACION_BIOLOGICA = go.Figure()
fig_integrada_CONTAMINACION_BIOLOGICA.add_trace(fig_map_CONTAMINACION_BIOLOGICA_2024.data[0])
fig_integrada_CONTAMINACION_BIOLOGICA.add_trace(fig_map_CONTAMINACION_BIOLOGICA_2025.data[0])
fig_integrada_CONTAMINACION_BIOLOGICA.add_trace(fig_map_CONTAMINACION_BIOLOGICA_2026.data[0])
fig_integrada_CONTAMINACION_BIOLOGICA.data[0].visible = True
fig_integrada_CONTAMINACION_BIOLOGICA.data[1].visible = False
fig_integrada_CONTAMINACION_BIOLOGICA.data[2].visible = False
fig_integrada_CONTAMINACION_BIOLOGICA.update_layout(fig_map_CONTAMINACION_BIOLOGICA_2024.layout)
fig_integrada_CONTAMINACION_BIOLOGICA.update_layout(
    paper_bgcolor='#121212', font=dict(color='#e0e0e0'), margin=dict(r=0, t=0, l=0, b=0),
    updatemenus=[dict(type="buttons", direction="right", x=0.1, y=1.08, pad={"r": 10, "t": 20, "l": 10, "b": 10}, xanchor="center", yanchor="bottom", showactive=True, bgcolor="#2d2d2d", bordercolor="#00adb5", font=dict(color="#808080"),
    buttons=list([
        dict(label="📊 Año 2024", method="update", args=[{"visible": [True, False, False]}, {"title": "Índice de Contaminación Biológica en 2024"}]),
        dict(label="📊 Año 2025", method="update", args=[{"visible": [False, True, False]}, {"title": "Índice de Contaminación Biológica en 2025"}]),
        dict(label="📊 Año 2026", method="update", args=[{"visible": [False, False, True]}, {"title": "Índice de Contaminación Biológica en 2026"}])
    ]))]
)

# ==========================================
# MAPA INTEGRADO: OXÍGENO DISUELTO
# ==========================================
fig_map_OXIGENO_2024 = px.density_mapbox(df_PCA_2024, lat='LAT', lon='LONG', z='OXÍGENO', radius=15, mapbox_style="open-street-map", color_continuous_scale="Viridis", opacity=0.6, zoom=11, hover_data={'LAT': True, 'LONG': True, 'FECHA' : True, 'OXÍGENO': ':.2f', 'LUGAR': True, 'TIPO_DE_MASA': True}, height=900)
fig_map_OXIGENO_2025 = px.density_mapbox(df_PCA_2025, lat='LAT', lon='LONG', z='OXÍGENO', radius=15, mapbox_style="open-street-map", color_continuous_scale="Viridis", opacity=0.6, zoom=11, hover_data={'LAT': True, 'LONG': True, 'FECHA' : True, 'OXÍGENO': ':.2f', 'LUGAR': True, 'TIPO_DE_MASA': True}, height=900)
fig_map_OXIGENO_2026 = px.density_mapbox(df_PCA_2026, lat='LAT', lon='LONG', z='OXÍGENO', radius=15, mapbox_style="open-street-map", color_continuous_scale="Viridis", opacity=0.6, zoom=11, hover_data={'LAT': True, 'LONG': True, 'FECHA' : True, 'OXÍGENO': ':.2f', 'LUGAR': True, 'TIPO_DE_MASA': True}, height=900)

fig_integrada_OXIGENO = go.Figure()
fig_integrada_OXIGENO.add_trace(fig_map_OXIGENO_2024.data[0])
fig_integrada_OXIGENO.add_trace(fig_map_OXIGENO_2025.data[0])
fig_integrada_OXIGENO.add_trace(fig_map_OXIGENO_2026.data[0])
fig_integrada_OXIGENO.data[0].visible = True
fig_integrada_OXIGENO.data[1].visible = False
fig_integrada_OXIGENO.data[2].visible = False
fig_integrada_OXIGENO.update_layout(fig_map_OXIGENO_2024.layout)
fig_integrada_OXIGENO.update_layout(
    paper_bgcolor='#121212', font=dict(color='#e0e0e0'), margin=dict(r=0, t=0, l=0, b=0),
    updatemenus=[dict(type="buttons", direction="right", x=0.1, y=1.08, pad={"r": 10, "t": 20, "l": 10, "b": 10}, xanchor="center", yanchor="bottom", showactive=True, bgcolor="#2d2d2d", bordercolor="#00adb5", font=dict(color="#808080"),
    buttons=list([
        dict(label="📊 Año 2024", method="update", args=[{"visible": [True, False, False]}, {"title": "Índice OXÍGENO en 2024"}]),
        dict(label="📊 Año 2025", method="update", args=[{"visible": [False, True, False]}, {"title": "Índice OXÍGENO en 2025"}]),
        dict(label="📊 Año 2026", method="update", args=[{"visible": [False, False, True]}, {"title": "Índice OXÍGENO en 2026"}])
    ]))]
)

# --- CONFIGURACIÓN DE RUTA DE IMAGEN ---
ruta_script = Path(__file__).resolve()
ruta_imagen = ruta_script.parent / 'dataSets' / 'carbon.png'

# ==========================================
# FUNCIÓN PRINCIPAL DE RENDERIZADO
# ==========================================
def main():
    # Usamos HTML <h1> centrado para el título principal
    st.markdown("<h1 style='text-align: center;'>Calidad del Agua (CABA)</h1>", unsafe_allow_html=True)
    
    st.link_button('calidad-agua', 'https://data.buenosaires.gob.ar/dataset/calidad-agua', icon_position='left', use_container_width=True)
    st.write("calidad-agua son distintos conjuntos de datos brindados por La Agencia de Protección Ambiental de la Ciudad de Buenos Aires, en el que se realizaron distintas mediciones ambientales y contaminantes en las principales masas de agua de la ciudad:")
    
    st.caption('- Rio Matanza Riachuelo')
    st.caption('- Desembocadura del Rio De La Plata')
    st.caption('- Arroyos de la ciudad: Maldonado, Vega, Medrano, Cildáñez, Ugarteche')
    st.caption('- Lagunas de la Reserva: de los Coipos, de los Patos, de las Gaviotas')
    
    st.dataframe(calidad_del_agua_2024_head, use_container_width=True)
    st.dataframe(calidad_del_agua_2025_head, use_container_width=True)
    st.dataframe(cal_agua_2026_head := calidad_del_agua_2026_head, use_container_width=True)
    
    # Usamos HTML <h3> centrado para los subheaders
    st.markdown("<h3 style='text-align: center;'>Definición de Variables</h3>", unsafe_allow_html=True)
    st.markdown("""
    * **Oxígeno:** Mide la cantidad de oxígeno gaseoso disuelto en el agua. Es el indicador más crítico para la vida acuática. Límite de Cuantificación: < 50 mg/L.
    * **Sólidos Disueltos Totales:** Suma de sustancias inorgánicas y orgánicas disueltas. Indica qué tan cargada de minerales está el agua.
    * **Demanda Química de Oxígeno (DQO):** Oxígeno necesario para oxidar toda la materia orgánica e inorgánica mediante reactivos químicos.
    * **Demanda Biológica de Oxígeno (DBO5):** Oxígeno consumido por microorganismos para degradar la materia orgánica en 5 días a 20°C.
    * **Arsénico Total:** Concentración del metaloide tóxico en el agua. Límite de cuantificación: < 4 µg/L.
    * **Coliformes Fecales:** Concentración de bacterias intestinales. Indicador universal de contaminación cloacal cruda. Límite: < 1 UFC/100 mL.
    """)
    
    st.markdown("<h3 style='text-align: center;'>Transformación De Los Datos</h3>", unsafe_allow_html=True)
    st.text('''
    Para poder analizar estos datos se transformaron los conjuntos de tal forma que cada registro represente las distintas mediciones de un día en un lugar en específico. Pasos realizados:
    1. Juntar todos los conjuntos de datos en uno solo.
    2. Tratar mediciones mal imputadas.
    3. Tratar sub-límites de cuantificación mediante la regla de la EPA.
    4. Pivotear datos a formato diario estructurado.
    5. Eliminar días sin muestreo efectivo.
    6. Utilizar KNNImputer para rellenar los valores nulos.
    ''')
    
    st.markdown("<h3 style='text-align: center;'>Herramientas utilizadas</h3>", unsafe_allow_html=True)
    st.link_button('Google Colab Notebook', 'https://colab.research.google.com/drive/1l9pRzfESzWKU9MgF4pPo9TD3Fr-VSrUZ?usp=sharing', use_container_width=True)
    
    st.markdown('''
    <p>Desplegado bajo Python 3.12.13 utilizando las siguientes librerías core:</p>
    <ul>
      <li><strong>matplotlib, seaborn</strong>: Gráficos estáticos de distribución.</li>
      <li><strong>plotly</strong>: Módulo Express y Graph Objects para gráficos y mapas dinámicos interactivos.</li>
      <li><strong>pandas</strong>: Manipulación tabular, agregaciones y estructuración de dataframes.</li>
      <li><strong>sklearn</strong>: Escalado estándar (StandardScaler), KNNImputer y Reducción de Dimensionalidad (PCA).</li>
    </ul>''', unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center;'>Análisis de variables</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig_det, use_container_width=True)
    
    st.markdown('''
    <ul>
      <li>En promedio, el <strong>84%</strong> de los valores de las mediciones son nulas, por lo que existe un excedente de calendario.</li>
      <li>Únicamente las variables de <strong>coliformes fecales</strong> y <strong>oxígeno</strong> tienen errores de imputación.</li>
      <li>Las variables <strong>dqo</strong>, <strong>dbo5</strong> y <strong>arsénico total</strong> tienen en promedio un 3% de registros por debajo del límite de cuantificación.</li>
    </ul>''', unsafe_allow_html=True)
    
    
    st.markdown("<h3 style='text-align: center;'>Análisis De Frecuencias De Muestreos</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig_true, use_container_width=True)
    
    st.markdown("<h3 style='text-align: center;'>Análisis de Distribución De Mediciones</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("<h3 style='text-align: center;'>Análisis de Correlación Cruzada Entre Mediciones</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig_corr, use_container_width=True)
    
    st.markdown("<h3 style='text-align: center;'>Análisis de Componentes Principales (PCA)</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig_trend_INDICE_INORGANICO, use_container_width=True)
    st.plotly_chart(fig_trend_INDICE_CONTAMINACION_ORGANICA, use_container_width=True)
    st.plotly_chart(fig_trend_OXIGENO, use_container_width=True)
    
    st.markdown("<h3 style='text-align: center;'>Visualización Espacio-Temporal: Mapas de Calor</h3>", unsafe_allow_html=True)
    
    # Usamos HTML <h4> centrado para los títulos menores que tenías con st.write
    st.markdown("<h4 style='text-align: center;'>Índice Inorgánico</h4>", unsafe_allow_html=True)
    st.plotly_chart(fig_integrada_INORGANICO, use_container_width=True)
    st.markdown('''
    <p>Se observa que el <strong>Índice Inorgánico</strong> presenta una tendencia general decreciente hacia las fechas más recientes, con excepción del Lago Lugano que sostiene anomalías minerales aisladas.</p>''', unsafe_allow_html=True)
    
    st.markdown("<h4 style='text-align: center;'>Índice de Contaminación Biológica</h4>", unsafe_allow_html=True)
    st.plotly_chart(fig_integrada_CONTAMINACION_BIOLOGICA, use_container_width=True)
    st.markdown('''
    <p>El mapa biológico expone de forma contundente la crisis orgánica de la cuenca del <strong>Riachuelo</strong> y zonas puntuales del Arroyo Medrano, manteniendo focos calientes estables a lo largo del trienio estudiado.</p>''', unsafe_allow_html=True)
    
    st.markdown("<h4 style='text-align: center;'>Concentración de Oxígeno</h4>", unsafe_allow_html=True)
    st.plotly_chart(fig_integrada_OXIGENO, use_container_width=True)

if __name__ == "__main__":
    main()