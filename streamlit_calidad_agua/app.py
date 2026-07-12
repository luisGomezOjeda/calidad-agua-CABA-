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
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio 
from plotly.subplots import make_subplots
import streamlit as st
from cache_data import load_data
from pathlib import Path

# --- LA PRIMERA INSTRUCCIÓN DE STREAMLIT ---
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

# Subplots a 2x3 para los Boxplots
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
    autosize=True,
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
    # Título Principal centrado
    st.markdown("<h1 style='text-align: center;'>Calidad del Agua (CABA)</h1>", unsafe_allow_html=True)
    
    st.link_button('calidad-agua', 'https://data.buenosaires.gob.ar/dataset/calidad-agua', icon_position='left', use_container_width=True)
    st.write("calidad-agua son distintos conjuntos de datos brindados por La Agencia de Protección Ambiental de la Ciudad de Buenos Aires, en el que se realizaron distintas mediciones ambientales y contaminantes en las principales masas de agua de la ciudad:")
    
    st.caption('- Rio Matanza Riachuelo')
    st.caption('- Desembocadura del Rio De La Plata')
    st.caption('- Arroyos de la ciudad: Maldonado, Vega, Medrano, Cildáñez, Ugarteche')
    st.caption('- Lagunas de la Reserva: de los Coipos, de los Patos, de las Gaviotas')
    
    st.write("#### Vista previa de los datos originales:")
    tab2024, tab2025, tab2026 = st.tabs(["Año 2024", "Año 2025", "Año 2026"])
    with tab2024:
        st.dataframe(calidad_del_agua_2024_head, use_container_width=True)
    with tab2025:
        st.dataframe(calidad_del_agua_2025_head, use_container_width=True)
    with tab2026:
        st.dataframe(calidad_del_agua_2026_head, use_container_width=True)
    
    # Definición de Variables
    st.markdown("<h3 style='text-align: center;'>Definición de Variables</h3>", unsafe_allow_html=True)
    st.markdown("""
    * **Oxígeno:** Mide la cantidad de oxígeno gaseoso disuelto en el agua. Es el indicador más crítico para la vida acuática. Un valor por debajo de 2-3 mg/L significa que los peces se asfixian. Equipo de medición: Sonda multiparamétrica (ej. YSI, Horiba) con sensor óptico o galvánico de oxígeno. Límite de Cuantificación: < 50 mg/L.
    * **Sólidos Disueltos Totales:** La suma de todas las sustancias inorgánicas y orgánicas contenidas en un líquido en forma molecular, ionizada o de suspensión micro granular. Básicamente, qué tan "salada" o cargada de minerales está el agua. Equipo de medición: Sonda multiparamétrica (mide conductividad eléctrica y la convierte a SDT) o conductímetro de campo.
    * **Demanda Química de Oxígeno (DQO):** Mide la cantidad de oxígeno necesario para oxidar toda la materia (orgánica e inorgánica) del agua usando reactivos químicos agresivos a alta temperatura. Es un indicador rápido de contaminación total. Equipo de medición: Espectrofotómetro (colorimetría) o titulación volumétrica tras digestión en un bloque calefactor.
    * **Demanda Biológica de Oxígeno (DBO5):** Mide la cantidad de oxígeno consumido por bacterias y microorganismos para degradar la materia orgánica biodegradable en un periodo de 5 days a 20°C. Equipo de medición: Respirometría (botellas ámbar con sensores de presión) o medición de oxígeno disuelto inicial vs. final (método Winkler). Límite de cuantificación: < 5 mg/L.
    * **Arsénico Total:** Mide la concentración total de este metaloide tóxico en el agua. En Argentina, gran parte del arsénico proviene de fuentes geológicas naturales, aunque también puede ser industrial. Equipo de medición: Espectrometría de Absorción Atómica (AAS) con horno de grafito, o ICP-MS (Espectrometría de Masas con Plasma Acoplado Inductivamente). Límite de cuantificación: < 4 µg/L.
    * **Coliformes Fecales:** Mide la concentración de un grupo específico de bacterias intestinales (como la E. coli) provenientes de las heces de humanos y animales de sangre caliente. No actúan como un contaminante químico, sino como el indicador biológico universal de contaminación cloacal cruda y riesgo de patógenos letales en el agua. Equipo de medición: Incubadora de laboratorio y contador de colonias (método de filtración por membrana en placas de Petri para obtener UFC) o bandejas de sellado térmico (método Colilert para obtener NMP). Límite de Cuantificación: < 1 UFC/100 mL, pudiendo registrar valores en los millones en aguas receptoras de efluentes sin tratamiento.
    """)
    
    # Transformación de datos
    st.markdown("<h3 style='text-align: center;'>Transformación De Los Datos</h3>", unsafe_allow_html=True)
    st.markdown("""
    Se puede observar cómo estos conjuntos de datos tienen un formato ancho en el que cada registro representa la medición histórica de todo un año de una determinación en un lugar en concreto. Para poder analizar estos datos se tiene que transformar los conjuntos de tal forma que cada registro represente las distintas mediciones de un día en un lugar en específico. Para lograr lo anterior se tiene que tener en cuenta el contexto de cada medición, lugar donde se realizó, tipo de masa y límite de cuantificación, para esto se siguieron los siguientes pasos:

    Convertir los conjuntos de datos a un formato largo, de tal forma que cada registro represente una medición de una determinación, en un lugar en específico en una fecha en concreto.
    1. Juntar todos los conjuntos de datos en uno solo.
    2. Tratar mediciones mal imputadas.
    3. Tratar las mediciones que están por debajo del límite de cuantificación mediante la regla de la EPA.
    4. Transformar los conjuntos de datos en un formato en el que cada registro representen las mediciones de las diferentes determinaciones que se hicieron en un día en un lugar en particular.
    5. Eliminar los registros de los días en el que no se realizó ningún tipo de muestreo.
    6. Utilizar la herramienta de KNNimputer de sklearn para imputar y completar los valores nulos en los registros faltantes.
    """)
    
    # Herramientas utilizadas
    st.markdown("<h3 style='text-align: center;'>Herramientas utilizadas</h3>", unsafe_allow_html=True)
    st.link_button('Google Colab Notebook', 'https://colab.research.google.com/drive/1l9pRzfESzWKU9MgF4pPo9TD3Fr-VSrUZ?usp=sharing', use_container_width=True)
    
    st.markdown('''
    <p>Desplegado bajo Python 3.12.13 utilizando las siguientes librerías core:</p>
    <ul>
      <li><strong><a href="https://matplotlib.org/" target="_blank">matplotlib</a>, <a href="https://seaborn.pydata.org/" target="_blank">seaborn</a></strong>: librerías que utilicé para desplegar los gráficos estáticos.</li>
      <li><strong><a href="https://plotly.com/python/" target="_blank">plotly</a></strong>: librería que mediante su módulo <em>express</em> desplegué los diferentes gráficos y mapas dinámicos.</li>
      <li><strong><a href="https://pandas.pydata.org/" target="_blank">pandas</a></strong>: librería que utilicé para visualizar la información en un formato tabular y realizar las diferentes transformaciones.</li>
      <li><strong><a href="https://scikit-learn.org/" target="_blank">sklearn</a></strong>: librería que utilicé para escalar los datos, rellenar los nulos con KNN y aplicar un algoritmo de PCA (análisis de componentes principales).</li>
    </ul>''', unsafe_allow_html=True)
    
    st.markdown("""
    <h4 style='text-align: center;'>El Límite De Cuantificación</h4>
    <p>
    Variable que define el umbral de exactitud o incertidumbre de la medición. Cada determinación tiene un umbral inferior de confianza donde si el valor de la medición está por debajo de este umbral, dicha medición tomará un porcentaje alto de incertidumbre, por encima de este umbral se define como zona de confianza. Para Tratar con las mediciones que caen por debajo de este umbral de confianza decidí utilizar La regla de la EPA, recomendado por La Agencia de Protección Ambiental de los Estados Unidos (EPA), en el que se divide el valor de la muestra por la raíz cuadrada de 2, asumiendo de esta manera a diferencia de la Sustitución por la Mitad que asume una distribución lineal por debajo del umbral, La regla de la EPA asume una distribución logarítmica.
    </p>""", unsafe_allow_html=True) 
    
    st.markdown("""
    <h4 style='text-align: center;'>KNN imputer</h4>
    <p>
    KNNimputer es un algoritmo de aprendizaje automático que utiliza la métrica de la distancia euclidiana para imputar los valores faltantes del promedio de los k vecinos mas cercanos.
    </p>""", unsafe_allow_html=True)
    
    st.markdown('''
    $$d(P,Q) = \sqrt{\sum_{i=1}^{n}(p_i - q_i)^2}$$

    $$d(P,Q) = \sqrt{(p_1 - q_1)^2 + (p_2 - q_2)^2 + \cdots + (p_n - q_n)^2}$$
    ''')  
    
    # Formato largo
    st.markdown("<h3 style='text-align: center;'>1. Convertir Los Conjuntos De Datos A Un Formato Largo</h3>", unsafe_allow_html=True)
    st.write("(un registro representa una medición, de una determinación, en un lugar en concreto)")
    st.write("Lo convierto en un formato largo para separar cada tipo de determinación y poder tratar los datos mal imputados y fuera de los límites de cuantificación de cada determinación.")
    
    st.dataframe(head_calidad_del_agua_pivot_processed, use_container_width=True)
    
    st.subheader('Límite de Cuantificación de las Determinaciones')
    st.caption('- **OXÍGENO:** <0.05mg/l y <0.1mg/l')
    st.caption('- **DQO:** <50')
    st.caption('- **DBO5 :** <5 mg O2/l')   
    st.caption('- **ARSÉNICO TOTAL:** <4 µg/l')   
    
    st.dataframe(frecuencia_determinacion, use_container_width=True)
    
    # Análisis de Variables
    st.markdown("<h3 style='text-align: center;'>Análisis de variables</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig_det, use_container_width=True)
    
    st.markdown('''
    <ul>
      <li>En promedio, el <strong>84%</strong> de los valores de las mediciones son nulas, por lo que existe un excedente de calendario.</li>
      <li>Únicamente las variables de <strong>coliformes fecales</strong> y <strong>oxígeno</strong> tienen errores de imputación.</li>
      <li>Las variables <strong>dqo</strong>, <strong>dbo5</strong> y <strong>arsénico total</strong> tienen en promedio un 3% de registros que están por debajo del límite de cuantificación.</li>
    </ul>''', unsafe_allow_html=True)
    
    # Frecuencia de muestreos
    st.markdown("<h3 style='text-align: center;'>Análisis De Frecuencias De Muestreos</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig_true, use_container_width=True)
    st.write("Este conjunto de datos tiene mayor proporción o mayor frecuencia de muestra de oxígeno y arsénico que el resto de mediciones, quizás se deba a que para el oxígeno utilizaron medidores de campos móviles más fáciles y agiles de medir que el resto de mediciones, que se realizaron mediante laboratorio. En cuanto a la frecuencia de medición del arsénico se deba a que se destinó mayor presupuesto e importancia a medir este contaminante, que históricamente es un contaminante relevante en la zona pampeana y el norte del país.")
    
    # Boxplots
    st.markdown("<h3 style='text-align: center;'>Análisis de Distribución De Mediciones</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('''
    <ul>
      <li><strong>Oxígeno:</strong> El 75% de las mediciones comprendidas desde el año 2024 a 2026 se midieron en un rango entre menos de 0.05 a 7.5.</li>
      <li><strong>Arsénico Total:</strong> Esta es la medición que más se asemeja a una distribución normal, ligeramente concentrada hacia la derecha en el que no se presentan valores atípicos.</li>
      <li><strong>Coliformes fecales:</strong> Presenta una distribución que tiende siempre a los valores inferiores, con 4 mediciones atípicamente altas que varían entre 0.25UFC/100 mL y 1.75UFC/100 mL.</li>
      <li><strong>Demanda Biológica de oxígeno (dbo5):</strong> la distribución de la demanda biológica de oxígeno tiene también una distribución con muy poca variación tendiendo a los valores bajos en el que el 50% de los valores centrales varía entre 10mg/L y 20mg/L.</li>
      <li><strong>DQO (demanda química de oxígeno):</strong> distribución que en el que el 75% de los registros varía entre valores cercanos a 0 y 70mg/L.</li>
      <li><strong>Sólidos disueltos totales:</strong> esta variable presenta una distribución bastante variada en el que el 50% de los valores centrales varía entre 300mg/L y 800mg/L.</li>
    </ul>''', unsafe_allow_html=True)

    # Formato Diario
    st.markdown("<h3 style='text-align: center;'>5. Transformación de los conjuntos de datos en un formato diario de mediciones</h3>", unsafe_allow_html=True)
    st.write("Transformé el significado de cada registro de tal forma que el tipo de masa, lugar, coordenadas y fecha son identificadores únicos de cada registro en donde contiene las mediciones de las determinaciones de un día determinado.")
    st.image(ruta_imagen, use_container_width=True)
    
    # Correlación Cruzada
    st.markdown("<h3 style='text-align: center;'>Análisis de Correlación Cruzada Entre Mediciones</h3>", unsafe_allow_html=True)
    st.dataframe(df_corr, use_container_width=True)
    st.plotly_chart(fig_corr, use_container_width=True)
    st.write("microorganismos, mientras que los coliformes fecales son un recuento biológico directo que indica cuánta materia fecal viva y peligrosa ingresó al agua a través de efluentes cloacales. Ambas variables presentan una correlación monotónica del 70%. Por ende, al fusionar matemáticamente la causa (la carga bacteriana) y el efecto (el consumo drástico de oxígeno), se obtiene un indicador consolidado y preciso para medir la contaminación biológica real de las distintas masas de agua.")
    st.write("También detecte una correlación entre arsénico total y sólidos disueltos totales. Por un lado, los sólidos disueltos totales miden la concentración de minerales en el agua y o por el otro lado el arsénico total mide la concentración de un mineral en específico. Juntar estas variables permite visualizar como es la tendencia entre el arsénico y los demás minerales.")
    
    # KNN Imputer
    st.markdown("<h3 style='text-align: center;'>6 y 7. Aplicación de KNNimputer:</h3>", unsafe_allow_html=True)
    st.markdown('''
    <p>Luego de transformar y unificar el conjunto de datos en un formato diario de muestreo, se eliminaron los días en los que no se realizaron determinaciones. Posteriormente, todas las variables fueron escaladas mediante <code>StandardScaler</code>, con el objetivo de llevarlas a una misma escala y evitar que las variables con valores numéricos más altos influyeran en mayor medida durante la imputación.</p>
    <p>A continuación, se aplicó el algoritmo <code>KNNImputer</code> con el hiperparámetro <code>n_neighbors = 2</code>. Este método estima los valores faltantes utilizando el promedio de los dos registros más similares o cercanos.</p>
    <p>Se almacenó una copia del conjunto de datos escalado para aplicar posteriormente el Análisis de Componentes Principales (<code>PCA</code>). Finalmente, una vez realizada la imputación, los datos fueron transformados nuevamente a su escala original para facilitar su interpretación y permitir futuros análisis.</p>
    ''', unsafe_allow_html=True)
    
    # PCA
    st.markdown("<h3 style='text-align: center;'>8. Análisis de Componentes Principales (PCA)</h3>", unsafe_allow_html=True)
    st.markdown('''
    <p>El Análisis de Componentes Principales (<code>PCA</code>) es un algoritmo de aprendizaje no supervisado utilizado para reducir la dimensionalidad de un conjunto de datos, especialmente cuando existen variables altamente correlacionadas entre sí.</p>
    <p>Matemáticamente, utiliza la matriz de covarianza, los autovectores y los autovalores. Estos últimos permiten identificar qué nuevos vectores capturan la mayor proporción de la varianza presente en los datos. El objetivo del algoritmo es proyectar la información original sobre nuevos ejes ortogonales denominados componentes principales.</p>
    <p>La cantidad de componentes principales retenidos se define mediante hiperparámetros y busca conservar la mayor cantidad posible de información proveniente de las variables originales.</p>
    <ul>
      <li>Se aplicó PCA sobre las variables <strong>arsénico total</strong> y <strong>sólidos disueltos totales</strong>, generando el <strong>Índice Inorgánico</strong>.</li>
      <li>Se aplicó PCA sobre las variables <strong>DBO5</strong> y <strong>coliformes fecales</strong>, generando el <strong>Índice de Contaminación Biológica</strong>.</li>
    </ul>
    
    <h3>Índice Inorgánico</h3>
    <ul>
      <li><strong>Valor alto o positivo:</strong> puede indicar una menor cantidad de agua disponible en el río o lago. En este escenario, los sólidos disueltos y el arsénico tienden a concentrarse, aumentando la carga mineral presente en el agua.</li>
      <li><strong>Valor bajo o negativo:</strong> puede representar una situación de dilución o crecida. Las lluvias o el deshielo incrementan el volumen de agua dulce, reduciendo la concentración de minerales y arsénico en el sistema.</li>
      <li><strong>Valor cercano a cero:</strong> puede representar una anomalía o un desacople entre las variables. Esto indica que el arsénico total y los sólidos disueltos dejaron de variar conjuntamente. Podría deberse a factores externos, como contaminación agrícola o urbana, o a procesos químicos que precipiten el arsénico hacia el fondo.</li>
    </ul>
    
    <h3>Índice de Contaminación Biológica</h3>
    <ul>
      <li><strong>Valor alto o positivo:</strong> puede indicar un aumento simultáneo de coliformes fecales y DBO5. Esta situación es compatible con una elevada carga de contaminación orgánica y fecal, que incrementa la actividad bacteriana y la demanda de oxígeno del agua.</li>
      <li><strong>Valor bajo o negativo:</strong> puede representar agua con baja carga de contaminación orgánica y fecal. En este caso, la demanda biológica de oxígeno es reducida y el sistema presenta condiciones biológicas más favorables.</li>
      <li><strong>Valor cercano a cero:</strong> puede indicar una anomalía industrial o un desacople orgánico. Esto ocurre cuando la DBO5 aumenta, pero los coliformes fecales permanecen bajos. Una explicación posible es el ingreso de materia orgánica procedente de actividades industriales, como plantas procesadoras de alimentos, jugueras o papeleras.</li>
    </ul>
    ''', unsafe_allow_html=True)
    
    # Mostrar el Preview de Datos de PCA de forma liviana (primeras 10 filas redondeadas)
    columnas_vista = ['FECHA', 'LUGAR', 'TIPO_DE_MASA', 'INDICE_INORGANICO', 'INDICE_CONTAMINACIÓN_BIOLOGICA']
    df_preview = df_PCA[columnas_vista].head(10).copy().round(2)
    df_preview['FECHA'] = df_preview['FECHA'].astype(str)
    st.dataframe(df_preview, use_container_width=True)
    
    # Gráficos de tendencias de índices
    st.plotly_chart(fig_trend_INDICE_INORGANICO, use_container_width=True)
    st.plotly_chart(fig_trend_INDICE_CONTAMINACION_ORGANICA, use_container_width=True)
    st.plotly_chart(fig_trend_OXIGENO, use_container_width=True)
    
    # Secciones regionales de análisis
    st.markdown('''
    <section>
      <h4 style="text-align: center;">Riachuelo</h4>
      <p>El Riachuelo es una masa de agua expuesta a múltiples fuentes de contaminación concentrada. Sin embargo, posee una dinámica hidrológica activa impulsada por su corriente constante y el régimen de lluvias.</p>
      <p>Esta tensión entre vertidos y dilución provoca la alta varianza estadística observada en las mediciones, haciendo que los niveles de demanda de oxígeno y los índices de contaminación biológica e inorgánica presenten fluctuaciones extremas.</p>
    </section>
    <section>
      <h4 style="text-align: center;">Arroyos</h4>
      <p>Los arroyos presentan un índice inorgánico marcadamente bajo, lo que refleja un efecto constante de dilución, típico de sistemas de desagüe pluvial en entornos urbanos.</p>
      <p>Respecto al Índice de Contaminación Biológica, la tendencia general se mantiene en valores negativos (ausencia de crisis biológica aguda), con la clara excepción de la desembocadura del Arroyo Medrano, que presenta una anomalía en su carga.</p>
      <p>En cuanto a la demanda de oxígeno, se detecta una clara tendencia de disminución (pérdida de oxígeno disuelto) concentrada en los meses de octubre de 2024 y abril de 2025.</p>
    </section>
    <section>
      <h4 style="text-align: center;">Lagos (Soldati y Lugano)</h4>
      <p>En cuanto al Índice Inorgánico, los lagos presentan ciclos de variación opuestos a los ecosistemas fluviales. Entre junio y septiembre de 2025, la tendencia natural se rompió (el índice tendió a 0). Es altamente probable que durante este trimestre un vertido o factor químico externo haya alterado la distribución natural entre el arsénico y el resto de los sólidos disueltos.</p>
      <p>Tanto el Lago Soldati como el Lago Lugano no parecen sufrir niveles crónicos de contaminación biológica cloacal. Sin embargo, durante el trimestre de junio a agosto de 2025 en el Lago Soldati, el índice biológico se anuló (tendió a 0). Este comportamiento anómalo señala el ingreso de un contaminante no biológico (industrial o químico) que disparó bruscamente la demanda de oxígeno sin aportar coliformes fecales.</p>
    </section>
    <section>
      <h4 style="text-align: center;">Río de la Plata</h4>
      <p>Dada su magnitud y el inmenso volumen de dilución que maneja esta masa de agua, el Índice Inorgánico presenta sustainedly valores negativos.</p>
      <p>Se diagnostican niveles bajos de contaminación biológica, manteniendo una concentración de oxígeno disuelto estable y saludable que varía en un rango de 3 mg/L a 9 mg/L.</p>
    </section>
    ''', unsafe_allow_html=True)
    
    # Mapas de Calor Integrados
    st.markdown("<h3 style='text-align: center;'>Visualización Espacio-Temporal: Mapas de Calor</h3>", unsafe_allow_html=True)
    st.write("Se realizaron tres mapas de color correspondientes a los años 2024, 2025 y 2026. Cada mapa utiliza los datos de la última muestra disponible de cada lugar para representar la distribución de los indicadores analizados: Índice Inorgánico, Índice de Contaminación Biológica y Oxígeno Disuelto.")
    
    st.markdown("<h4 style='text-align: center;'>Índice Inorgánico</h4>", unsafe_allow_html=True)
    st.plotly_chart(fig_integrada_INORGANICO, use_container_width=True)
    st.markdown('''
    <p>Se observa que, al comparar las últimas mediciones disponibles de cada año, el <strong>Índice Inorgánico</strong> presenta una tendencia general decreciente hacia las fechas más recientes. Con excepción del <strong>Lago Lugano</strong>, que registra un índice positivo, el resto de los cuerpos de agua presentan valores negativos, lo que indica una menor concentración relativa de compuestos inorgánicos disueltos en estos sitios.</p>''', unsafe_allow_html=True)
    
    st.markdown("<h4 style='text-align: center;'>Índice de Contaminación Biológica</h4>", unsafe_allow_html=True)
    st.plotly_chart(fig_integrada_CONTAMINACION_BIOLOGICA, use_container_width=True)
    st.markdown('''
    <p>El mapa biológico expone de forma contundente la crisis orgánica de la cuenca del <strong>Riachuelo</strong> y zonas puntuales del Arroyo Medrano, manteniendo focos calientes estables a lo largo del trienio estudiado.</p>''', unsafe_allow_html=True)
    
    st.markdown("<h4 style='text-align: center;'>Concentración de Oxígeno</h4>", unsafe_allow_html=True)
    st.plotly_chart(fig_integrada_OXIGENO, use_container_width=True)
    st.markdown('''
    <p>Se observa que, hacia finales de 2025, se registraron los niveles más altos de oxígeno disuelto de todo el período analizado.</p>''', unsafe_allow_html=True)
    
    # Conclusión General
    st.markdown("<h3 style='text-align: center;'>Conclusión General</h3>", unsafe_allow_html=True)
    st.markdown('''
    <p>A lo largo del presente informe técnico, la aplicación de modelos de reducción de dimensionalidad permitió aislar la dinámica hidrológica base de los distintos ecosistemas y detectar desviaciones críticas. Mediante el análisis de los componentes principales, se identificaron ubicaciones y períodos puntuales en los que los patrones naturales de correlación se rompieron por completo, evidenciando eventos de contaminación externa aguda.</p>
    <p>Como principales hallazgos, se destaca la detección de alteraciones químicas atípicas en los ecosistemas lacustres cerrados de la ciudad, así como la confirmación empírica de la elevada volatilidad de la cuenca del Riachuelo. En este último, la constante tensión entre los vertidos contaminantes y los fenómenos físicos de dilución genera una dinámica ambiental altamente inestable, la cual el modelo logró capturar y diferenciar de manera efectiva.</p>
    <p>Finalmente, uno de los aportes más importantes del trabajo radica en la etapa de preprocesamiento. La resolución de valores nulos mediante imputación espacial (<strong>KNNImputer</strong>) y la normalización de las variables mediante escalado estándar permitieron consolidar un conjunto de datos robusto, consistente y parametrizado. Esta base de datos limpia y estandarizada constituye un recurso de gran utilidad para facilitar futuros análisis estadísticos y el desarrollo de nuevos modelos de ciencia de datos.</p>
    ''', unsafe_allow_html=True)

if __name__ == "__main__":
    main()