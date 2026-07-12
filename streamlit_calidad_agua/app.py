import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio 
from plotly.subplots import make_subplots
import streamlit as st
from cache_data import load_data
from pathlib import Path
pio.templates.default = 'plotly_dark'

datasets = load_data()

df_map_det = datasets['porcentaje_determinacion']
fig_det = px.bar(df_map_det,x='determinación',y=['errores de imputación','fuera de limite','nulos'],barmode='group',title='Porcentaje De Mediciones Nulas, Fuera De Limite y Errores De Imputación por Determinación')
fig_det.update_yaxes(title_text='Porcentaje')

calidad_del_agua_2024_head = datasets['calidad_del_agua_2024_head']
calidad_del_agua_2025_head = datasets['calidad_del_agua_2025_head']
calidad_del_agua_2026_head = datasets['calidad_del_agua_2026_head']
calidad_del_agua_melt = datasets['calidad_del_agua_melt']
head_calidad_del_agua_pivot_PCA = datasets['head_calidad_del_agua_pivot_PCA']

df_true_values = datasets['cantidad_mediciones_no_nulas']

frecuencia_determinacion = datasets['frecuencia_determinacion']

fig_true = px.bar(df_true_values,x='determinación',y='cantidad',color='determinación',title='Cantidad de mediciones no nulas por determinación')

df_pivot = datasets['calidad_del_agua_pivot_not_processed']

print(datasets.keys())

head_calidad_del_agua_pivot_processed = datasets['head_calidad_del_agua_pivot_processed']


texto_outliers = "<b>Lugar:</b> " + df_pivot['LUGAR'] + "<br><b>Fecha:</b> " + df_pivot['FECHA'].astype(str)

fig = make_subplots(
    rows=3, cols=3,
    subplot_titles=("Gráfico de Líneas", "Gráfico de Barras", "Dispersión", "Área")
)

fig.add_trace(
    go.Box(y=df_pivot['oxígeno'], name='Oxígeno',text=texto_outliers,boxpoints='outliers'),
    row=1, col=1
)

fig.add_trace(
    go.Box(y=df_pivot['arsénico total'], name='Arsénico Total',text=texto_outliers,boxpoints='outliers'),
    row=1, col=2
)

fig.add_trace(
    go.Box(y=df_pivot['coliformes fecales'], name='Coliformes Fecales',text=texto_outliers,boxpoints='outliers'),
    row=1, col=3
)

fig.add_trace(
    go.Box(y=df_pivot['dbo5'], name='dbo5',text=texto_outliers,boxpoints='outliers'),
    row=2, col=1
)

fig.add_trace(
    go.Box(y=df_pivot['dqo'], name='DQO',text=texto_outliers,boxpoints='outliers'),
    row=2, col=2
)

fig.add_trace(
    go.Box(y=df_pivot['sólidos disueltos totales'], name='Sólidos Disueltos Totales',text=texto_outliers,boxpoints='outliers'),
    row=2, col=3
)

fig.update_layout(
    title_text="Boxplots de Mediciones por Determinación",
    height=700,
    width=1000,
    autosize=False,
    margin=dict(l=0, r=0, t=250, b=0)
)

df_corr = datasets['correlacion_determinaciones']
df_corr.index = df_corr['Unnamed: 0']
df_corr = df_corr.drop(columns=['Unnamed: 0'])
df_corr.index.name= 'Determinación'
fig_corr = px.imshow(
    df_corr,
    text_auto=True,
    aspect="auto",
    title='Correlacion Cruzada De Spearman Entre Las Distintas Determinaciones'
)

df_PCA = datasets['completed_calidad_del_agua_pivot_PCA']

fig_trend_INDICE_INORGANICO = px.line(df_PCA,x='FECHA',y='INDICE_INORGANICO',color='TIPO_DE_MASA',line_group='LUGAR',title='INDICE INORGANICO')

fig_trend_INDICE_CONTAMINACION_ORGANICA = px.line(df_PCA,x='FECHA',y='INDICE_CONTAMINACIÓN_BIOLOGICA',color='TIPO_DE_MASA',line_group='LUGAR',title='INDICE_CONTAMINACIÓN_BIOLOGICA')

fig_trend_OXIGENO = px.line(df_PCA,x='FECHA',y='OXÍGENO',color='TIPO_DE_MASA',line_group='LUGAR',title='OXÍGENO')

print(datasets.keys())
df_PCA_2024 = datasets['completed_calidad_del_agua_pivot_PCA_2024']
df_PCA_2025 = datasets['completed_calidad_del_agua_pivot_PCA_2025']
df_PCA_2026 = datasets['completed_calidad_del_agua_pivot_PCA_2026']



fig_map_INORGANICO_2024 = px.density_mapbox(
    df_PCA_2024,
    lat='LAT',
    lon='LONG',
    z='INDICE_INORGANICO',
    radius=15,                            # Define el tamaño físico del punto de calor
    mapbox_style="open-street-map",       # Requerido: Carga el mapa base gratuito
    color_continuous_scale="Viridis",     # Escala de color visible y profesional
    opacity=0.6,                          # Permite ver las calles debajo del mapa de calor
    zoom=11.5,                              # Zoom inicial aproximado
    # --- CONFIGURACIÓN DEL HOVER (INFORMACIÓN FLOTANTE) ---
    #hover_name='NOMBRE_ESTACION',    # Columna que aparecerá arriba en NEGRITA (ej. Nombre de la estación, ID o Ciudad)
    hover_data={
        'LAT': True,                 # Muestra la Latitud
        'LONG': True,            
        'FECHA' : True,# Muestra la Longitud
        'INDICE_INORGANICO': ':.2f', # Muestra el índice formateado a 2 decimales
        'LUGAR': True,   # Puedes agregar cualquier otra columna de df_PCA aquí
        'TIPO_DE_MASA': True        # Puedes agregar cualquier otra columna de df_PCA aquí
    },
     height=900,
)

fig_map_INORGANICO_2024.update_layout(margin={"r":0,"t":40,"l":0,"b":0}) # Maximiza el espacio del mapa


fig_map_INORGANICO_2025 = px.density_mapbox(
    df_PCA_2025,
    lat='LAT',
    lon='LONG',
    z='INDICE_INORGANICO',
    radius=15,                            # Define el tamaño físico del punto de calor
    mapbox_style="open-street-map",       # Requerido: Carga el mapa base gratuito
    color_continuous_scale="Viridis",     # Escala de color visible y profesional
    opacity=0.6,                          # Permite ver las calles debajo del mapa de calor
    zoom=11.5,                              # Zoom inicial aproximado
    title="Indice INORGANICO en 2025",
    # --- CONFIGURACIÓN DEL HOVER (INFORMACIÓN FLOTANTE) ---
    #hover_name='NOMBRE_ESTACION',    # Columna que aparecerá arriba en NEGRITA (ej. Nombre de la estación, ID o Ciudad)
    hover_data={
        'LAT': True,                 # Muestra la Latitud
        'LONG': True,       
        'FECHA' : True,# Muestra la Longitud
        'INDICE_INORGANICO': ':.2f', # Muestra el índice formateado a 2 decimales
        'LUGAR': True,   # Puedes agregar cualquier otra columna de df_PCA aquí
        'TIPO_DE_MASA': True        # Puedes agregar cualquier otra columna de df_PCA aquí
    },
     height=900,
)

fig_map_INORGANICO_2025.update_layout(margin={"r":0,"t":40,"l":0,"b":0}) # Maximiza el espacio del mapa


fig_map_INORGANICO_2026 = px.density_mapbox(
    df_PCA_2026,
    lat='LAT',
    lon='LONG',
    z='INDICE_INORGANICO',
    radius=15,                            # Define el tamaño físico del punto de calor
    mapbox_style="open-street-map",       # Requerido: Carga el mapa base gratuito
    color_continuous_scale="Viridis",     # Escala de color visible y profesional
    opacity=0.6,                          # Permite ver las calles debajo del mapa de calor
    zoom=11.5,                              # Zoom inicial aproximado
    title="Indice INORGANICO en 2026",
    # --- CONFIGURACIÓN DEL HOVER (INFORMACIÓN FLOTANTE) ---
    #hover_name='NOMBRE_ESTACION',    # Columna que aparecerá arriba en NEGRITA (ej. Nombre de la estación, ID o Ciudad)
    hover_data={
        'LAT': True,                 # Muestra la Latitud
        'FECHA' : True,
        'LONG': True,                # Muestra la Longitud
        'INDICE_INORGANICO': ':.2f', # Muestra el índice formateado a 2 decimales
        'LUGAR': True,   # Puedes agregar cualquier otra columna de df_PCA aquí
        'TIPO_DE_MASA': True,        # Puedes agregar cualquier otra columna de df_PCA aquí
    },
     height=900,
)

fig_map_INORGANICO_2026.update_layout(margin={"r":0,"t":40,"l":0,"b":0}) # Maximiza el espacio del mapa

# 1. Creamos una figura vacía maestra
fig_integrada_INORGANICO = go.Figure()

# 2. Extraemos el 'trace' (los datos del mapa de calor) de las figuras que ya creaste con px
fig_integrada_INORGANICO.add_trace(fig_map_INORGANICO_2024.data[0])
fig_integrada_INORGANICO.add_trace(fig_map_INORGANICO_2025.data[0])
fig_integrada_INORGANICO.add_trace(fig_map_INORGANICO_2026.data[0])

# 3. Configuramos para que al inicio SOLO se vea el mapa 2024
fig_integrada_INORGANICO.data[0].visible = True
fig_integrada_INORGANICO.data[1].visible = False
fig_integrada_INORGANICO.data[2].visible = False

# 4. Heredamos la configuración del mapa base (zoom, estilo de calle) de la primera figura
fig_integrada_INORGANICO.update_layout(fig_map_INORGANICO_2024.layout)

# 5. Aplicamos tu diseño oscuro y los botones de Plotly
fig_integrada_INORGANICO.update_layout(
    paper_bgcolor='#121212', # Fondo oscuro global
    font=dict(color='#e0e0e0'), # Texto claro
    title=dict(text="Índice INORGANICO", y=1),
    margin=dict(r=0, t=0, l=0, b=0), # Dejamos espacio arriba para los botones
    
    # Creamos el menú de botones nativo
    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            x=0.1,
            y=1.08, # Posición justo encima del mapa
            pad={"r": 10, "t": 20, "l": 10, "b": 10},
            xanchor="center",
            yanchor="bottom",
            showactive=True,
            bgcolor="#2d2d2d",         # Fondo de botones inactivos
            bordercolor="#00adb5",
            font=dict(color="#808080"),
            buttons=list([
                dict(label="📊 Año 2024",
                     method="update",
                     # Al hacer clic, vuelve True el índice 0 y False los demás, y cambia el título
                     args=[{"visible": [True, False, False]},
                           {"title": "Índice INORGÁNICO en 2024"}]),
                
                dict(label="📊 Año 2025",
                     method="update",
                     args=[{"visible": [False, True, False]},
                           {"title": "Índice INORGÁNICO en 2025"}]),
                
                dict(label="📊 Año 2026",
                     method="update",
                     args=[{"visible": [False, False, True]},
                           {"title": "Índice INORGÁNICO en 2026"}]),
            ]),
        )
    ]
)

fig_map_CONTAMINACION_BIOLOGICA_2024 = px.density_mapbox(
    df_PCA_2024,
    lat='LAT',
    lon='LONG',
    z='INDICE_CONTAMINACIÓN_BIOLOGICA',
    radius=15,
    mapbox_style="open-street-map",
    color_continuous_scale="Viridis",
    opacity=0.6,
    zoom=11.5,
    # CORRECCIÓN AQUÍ: Renombras la columna que estás usando en Z
    labels={"INDICE_CONTAMINACIÓN_BIOLOGICA": "INDICE_CONTAMINACIÓN_BIOLOGICA"}, 
    hover_data={
        'LAT': True,
        'LONG': True,
        'FECHA' : True,
        'INDICE_CONTAMINACIÓN_BIOLOGICA': ':.2f',
        'LUGAR': True,
        'TIPO_DE_MASA': True
    },
    height=900,
)

fig_map_CONTAMINACION_BIOLOGICA_2024.update_layout(margin={"r":0,"t":40,"l":0,"b":0})


fig_map_CONTAMINACION_BIOLOGICA_2025 = px.density_mapbox(
    df_PCA_2025,
    lat='LAT',
    lon='LONG',
    labels={"INDICE_CONTAMINACIÓN_BIOLOGICA": "INDICE_CONTAMINACIÓN_BIOLOGICA"}, 
    z='INDICE_CONTAMINACIÓN_BIOLOGICA',
    radius=15,
    mapbox_style="open-street-map",
    color_continuous_scale="Viridis",
    opacity=0.6,
    zoom=11.5,
    hover_data={
        'LAT': True,
        'LONG': True,
        'FECHA' : True,
        'INDICE_CONTAMINACIÓN_BIOLOGICA': ':.2f',
        'LUGAR': True,
        'TIPO_DE_MASA': True
    },
    height=900,
)

fig_map_CONTAMINACION_BIOLOGICA_2025.update_layout(margin={"r":0,"t":40,"l":0,"b":0})


fig_map_CONTAMINACION_BIOLOGICA_2026 = px.density_mapbox(
    df_PCA_2026,
    lat='LAT',
    lon='LONG',
    z='INDICE_CONTAMINACIÓN_BIOLOGICA',
    labels={'INDICE_CONTAMINACIÓN_BIOLOGICA':'INDICE_CONTAMINACIÓN_BIOLOGICA'},
    radius=15,
    mapbox_style="open-street-map",
    color_continuous_scale="Viridis",
    opacity=0.6,
    zoom=11.5,
    hover_data={
        'LAT': True,
        'FECHA' : True,
        'LONG': True,
        'INDICE_CONTAMINACIÓN_BIOLOGICA': ':.2f',
        'LUGAR': True,
        'TIPO_DE_MASA': True,
    },
    height=900,
)

fig_map_CONTAMINACION_BIOLOGICA_2026.update_layout(margin={"r":0,"t":40,"l":0,"b":0})

# 1. Figura vacía
fig_integrada_CONTAMINACION_BIOLOGICA = go.Figure()

# 2. Agregamos trazas
fig_integrada_CONTAMINACION_BIOLOGICA.add_trace(fig_map_CONTAMINACION_BIOLOGICA_2024.data[0])
fig_integrada_CONTAMINACION_BIOLOGICA.add_trace(fig_map_CONTAMINACION_BIOLOGICA_2025.data[0])
fig_integrada_CONTAMINACION_BIOLOGICA.add_trace(fig_map_CONTAMINACION_BIOLOGICA_2026.data[0])

# 3. Visibilidad inicial
fig_integrada_CONTAMINACION_BIOLOGICA.data[0].visible = True
fig_integrada_CONTAMINACION_BIOLOGICA.data[1].visible = False
fig_integrada_CONTAMINACION_BIOLOGICA.data[2].visible = False

# 4. CORRECCIÓN AQUÍ: Heredas de CONTAMINACION_BIOLOGICA_2024, no de INORGANICO
fig_integrada_CONTAMINACION_BIOLOGICA.update_layout(fig_map_CONTAMINACION_BIOLOGICA_2024.layout)

# 5. Estilos generales y menú de botones
fig_integrada_CONTAMINACION_BIOLOGICA.update_layout(
    paper_bgcolor='#121212',
    font=dict(color='#e0e0e0'),
    margin=dict(r=0, t=0, l=0, b=0),
    
    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            x=0.1,
            y=1.08,
            pad={"r": 10, "t": 20, "l": 10, "b": 10},
            xanchor="center",
            yanchor="bottom",
            showactive=True,
            bgcolor="#2d2d2d",
            bordercolor="#00adb5",
            font=dict(color="#808080"),
            buttons=list([
                dict(label="📊 Año 2024",
                     method="update",
                     args=[{"visible": [True, False, False]},
                           {"title": "Índice de Contaminación Biológica en 2024"}]),
                
                dict(label="📊 Año 2025",
                     method="update",
                     args=[{"visible": [False, True, False]},
                           {"title": "Índice de Contaminación Biológica en 2025"}]),
                
                dict(label="📊 Año 2026",
                     method="update",
                     args=[{"visible": [False, False, True]},
                           {"title": "Índice de Contaminación Biológica en 2026"}]),
            ]),
        )
    ]
)

fig_map_OXIGENO_2024 = px.density_mapbox(
    df_PCA_2024,
    lat='LAT',
    lon='LONG',
    z='OXÍGENO',
    radius=15,                            # Define el tamaño físico del punto de calor
    mapbox_style="open-street-map",       # Requerido: Carga el mapa base gratuito
    color_continuous_scale="Viridis",     # Escala de color visible y profesional
    opacity=0.6,                          # Permite ver las calles debajo del mapa de calor
    zoom=11,                              # Zoom inicial aproximado
    # --- CONFIGURACIÓN DEL HOVER (INFORMACIÓN FLOTANTE) ---
    #hover_name='NOMBRE_ESTACION',    # Columna que aparecerá arriba en NEGRITA (ej. Nombre de la estación, ID o Ciudad)
    hover_data={
        'LAT': True,                 # Muestra la Latitud
        'LONG': True,            
        'FECHA' : True,# Muestra la Longitud
        'OXÍGENO': ':.2f', # Muestra el índice formateado a 2 decimales
        'LUGAR': True,   # Puedes agregar cualquier otra columna de df_PCA aquí
        'TIPO_DE_MASA': True        # Puedes agregar cualquier otra columna de df_PCA aquí
    },
     height=900,
)

fig_map_OXIGENO_2024.update_layout(margin={"r":0,"t":40,"l":0,"b":0}) # Maximiza el espacio del mapa


fig_map_OXIGENO_2025 = px.density_mapbox(
    df_PCA_2025,
    lat='LAT',
    lon='LONG',
    z='OXÍGENO',
    radius=15,                            # Define el tamaño físico del punto de calor
    mapbox_style="open-street-map",       # Requerido: Carga el mapa base gratuito
    color_continuous_scale="Viridis",     # Escala de color visible y profesional
    opacity=0.6,                          # Permite ver las calles debajo del mapa de calor
    zoom=11,                              # Zoom inicial aproximado
    # --- CONFIGURACIÓN DEL HOVER (INFORMACIÓN FLOTANTE) ---
    #hover_name='NOMBRE_ESTACION',    # Columna que aparecerá arriba en NEGRITA (ej. Nombre de la estación, ID o Ciudad)
    hover_data={
        'LAT': True,                 # Muestra la Latitud
        'LONG': True,       
        'FECHA' : True,# Muestra la Longitud
        'OXÍGENO': ':.2f', # Muestra el índice formateado a 2 decimales
        'LUGAR': True,   # Puedes agregar cualquier otra columna de df_PCA aquí
        'TIPO_DE_MASA': True        # Puedes agregar cualquier otra columna de df_PCA aquí
    },
     height=900,
)

fig_map_OXIGENO_2025.update_layout(margin={"r":0,"t":40,"l":0,"b":0}) # Maximiza el espacio del mapa


fig_map_OXIGENO_2026 = px.density_mapbox(
    df_PCA_2026,
    lat='LAT',
    lon='LONG',
    z='OXÍGENO',
    radius=15,                            # Define el tamaño físico del punto de calor
    mapbox_style="open-street-map",       # Requerido: Carga el mapa base gratuito
    color_continuous_scale="Viridis",     # Escala de color visible y profesional
    opacity=0.6,                          # Permite ver las calles debajo del mapa de calor
    zoom=11,                              # Zoom inicial aproximado
    # --- CONFIGURACIÓN DEL HOVER (INFORMACIÓN FLOTANTE) ---
    #hover_name='NOMBRE_ESTACION',    # Columna que aparecerá arriba en NEGRITA (ej. Nombre de la estación, ID o Ciudad)
    hover_data={
        'LAT': True,                 # Muestra la Latitud
        'FECHA' : True,
        'LONG': True,                # Muestra la Longitud
        'OXÍGENO': ':.2f', # Muestra el índice formateado a 2 decimales
        'LUGAR': True,   # Puedes agregar cualquier otra columna de df_PCA aquí
        'TIPO_DE_MASA': True,        # Puedes agregar cualquier otra columna de df_PCA aquí
    },
     height=900,
)

fig_map_OXIGENO_2026.update_layout(margin={"r":0,"t":40,"l":0,"b":0}) # Maximiza el espacio del mapa

# 1. Creamos una figura vacía maestra
fig_integrada_OXIGENO = go.Figure()

# 2. Extraemos el 'trace' (los datos del mapa de calor) de las figuras que ya creaste con px
fig_integrada_OXIGENO.add_trace(fig_map_OXIGENO_2024.data[0])
fig_integrada_OXIGENO.add_trace(fig_map_OXIGENO_2025.data[0])
fig_integrada_OXIGENO.add_trace(fig_map_OXIGENO_2026.data[0])

# 3. Configuramos para que al inicio SOLO se vea el mapa 2024
fig_integrada_OXIGENO.data[0].visible = True
fig_integrada_OXIGENO.data[1].visible = False
fig_integrada_OXIGENO.data[2].visible = False

# 4. Heredamos la configuración del mapa base (zoom, estilo de calle) de la primera figura
fig_integrada_OXIGENO.update_layout(fig_map_OXIGENO_2024.layout)



# 5. Aplicamos tu diseño oscuro y los botones de Plotly
fig_integrada_OXIGENO.update_layout(
    paper_bgcolor='#121212', # Fondo oscuro global
    font=dict(color='#e0e0e0'), # Texto claro
    margin=dict(r=0, t=0, l=0, b=0), # Dejamos espacio arriba para los botones
    
    # Creamos el menú de botones nativo
    updatemenus=[
        dict(
            type="buttons",
            direction="right",
            x=0.1,
            y=1.08, # Posición justo encima del mapa
            pad={"r": 10, "t": 20, "l": 10, "b": 10},
            xanchor="center",
            yanchor="bottom",
            showactive=True,
            bgcolor="#2d2d2d",         # Fondo de botones inactivos
            bordercolor="#00adb5",
            font=dict(color="#808080"),
            buttons=list([
                dict(label="📊 Año 2024",
                     method="update",
                     # Al hacer clic, vuelve True el índice 0 y False los demás, y cambia el título
                     args=[{"visible": [True, False, False]},
                           {"title": "Índice OXÍGENO en 2024"}]),
                
                dict(label="📊 Año 2025",
                     method="update",
                     args=[{"visible": [False, True, False]},
                           {"title": "Índice OXÍGENO en 2025"}]),
                
                dict(label="📊 Año 2026",
                     method="update",
                     args=[{"visible": [False, False, True]},
                           {"title": "Índice OXÍGENO en 2026"}]),
            ]),
        )
    ]
)

ruta_script = Path(__file__).resolve()

# 2. Armamos la ruta blindada hacia la imagen
ruta_imagen = ruta_script.parent / 'dataSets' / 'carbon.png'


def main():
    st.title("**Calidad del Agua (CABA)**",text_alignment='center')
    st.link_button('calidad-agua', 'https://data.buenosaires.gob.ar/dataset/calidad-agua',icon_position='left',use_container_width=True)
    st.write("calidad-agua son distintos conjuntos de datos brindado por La Agencia de Protección Ambiental de la Ciudad de Buenos Aires, en el que se realizaron distintas mediciones ambientales y contaminantes en las principales masas de agua de la ciudad:")
    st.caption('- Rio Matanza Riachuelo',width='stretch')
    st.caption('- Desembocadura del Rio De La Plata',width='stretch')
    st.caption('- Arroyos de la ciudad:',width='stretch')   
    st.caption('- - Arroyo Maldonado, Arroyo Vega, Arroyo Medrano, Arroyo Cildáñez, Arroyo Ugarteche',width='stretch')
    st.caption('- Lagunas de la Reserva:',width='stretch')
    st.caption('- - Laguna de los Coipos, Laguna de los Patos, Laguna de las Gaviotas',width='stretch')
    st.dataframe(calidad_del_agua_2024_head,width='stretch')
    st.dataframe(calidad_del_agua_2025_head,width='stretch')
    st.dataframe(calidad_del_agua_2026_head,width='stretch')
    
    st.subheader('**Definición de Variables**',text_alignment='center')
    st.subheader('''
Oxígeno: 
Mide la cantidad de oxígeno gaseoso disuelto en el agua. Es el indicador más crítico para la vida acuática. Un valor por debajo de 2-3 mg/L significa que los peces se asfixian.
Equipo de medición: Sonda multiparamétrica (ej. YSI, Horiba) con sensor óptico o galvánico de oxígeno
Límite de Cuantificación: < 50 mg/L.''')
    
    
    st.subheader('''
Sólidos Disueltos Totales:
La suma de todas las sustancias inorgánicas y orgánicas contenidas en un líquido en forma molecular, ionizada o de suspensión micro granular. Básicamente, qué tan "salada" o cargada de minerales está el agua.
Equipo de medición: Sonda multiparamétrica (mide conductividad eléctrica y la convierte a SDT) o conductímetro de campo.
                 ''')
    st.subheader('''
Demanda Química de Oxígeno (DQO):
Mide la cantidad de oxígeno necesario para oxidar toda la materia (orgánica e inorgánica) del agua usando reactivos químicos agresivos a alta temperatura. Es un indicador rápido de contaminación total.
Equipo de medición: Espectrofotómetro (colorimetría) o titulación volumétrica tras digestión en un bloque calefactor.
                 ''')
    st.subheader('''
Demanda Biológica de Oxígeno (DBO5):
Mide la cantidad de oxígeno consumido por bacterias y microorganismos para degradar la materia orgánica biodegradable en un periodo de 5 días a 20°C.
Equipo de medición: Respirometría (botellas ámbar con sensores de presión) o medición de oxígeno disuelto inicial vs. final (método Winkler).
Límite de cuantificación: < 5 mg/L
                 ''')
    st.subheader('''
Arsénico Total:
Mide la concentración total de este metaloide tóxico en el agua. En Argentina, gran parte del arsénico proviene de fuentes geológicas naturales, aunque también puede ser industrial.
Equipo de medición: Espectrometría de Absorción Atómica (AAS) con horno de grafito, o ICP-MS (Espectrometría de Masas con Plasma Acoplado Inductivamente).
Límite de cuantificación: < 4 µg/L.
                 ''')
    st.subheader('''
Coliformes Fecales:
Mide la concentración de un grupo específico de bacterias intestinales (como la E. coli) provenientes de las heces de humanos y animales de sangre caliente. No actúan como un contaminante químico, sino como el indicador biológico universal de contaminación cloacal cruda y riesgo de patógenos letales en el agua.
Equipo de medición: Incubadora de laboratorio y contador de colonias (método de filtración por membrana en placas de Petri para obtener UFC) o bandejas de sellado térmico (método Colilert para obtener NMP).
-Límite de Cuantificación: < 1 UFC/100 mL (o < 1 NMP/100 mL), pudiendo registrar valores en los millones en aguas receptoras de efluentes sin tratamiento.
                 ''')
    
    st.subheader('''
                 
                 
                 
                 ''')
    st.subheader('**Transformación De Los Datos**',text_alignment='center')

    st.text('''
Se puede observar cómo estos conjuntos de datos tienen un formato ancho en el que cada registro representa la medición histórica de todo un año de una determinación en un lugar en concreto. Para poder analizar estos datos se tiene que transformar los conjuntos de tal forma que cada registro represente las distintas mediciones de un día en un lugar en específico. Para lograr lo anterior se tiene que tener en cuenta el contexto de cada medición, lugar donde se realizó, tipo de masa y límite de cuantificación, para esto se siguieron los siguientes pasos:

convertir los conjuntos de datos a un formato largo, de tal forma que cada registro represente una medición de una determinación, en un lugar en específico en una fecha en concreto.

 - 1. Juntar todos los conjuntos de datos en uno solo.
 
 - 2.Tratar mediciones mal imputadas.
 
 - 3. Tratar las mediciones que están por debajo del límite de cuantificación mediante la regla de la EPA.
 
 - 4. transformar los conjuntos de datos en un formato en el que cada registro representen las mediciones de las diferentes determinaciones que se hicieron en un día en un lugar en particular.
 
 - 5. Eliminar los registros de los días en el que no se realizó ningún tipo de muestreo.
 
 - 6. Utilizar la herramienta de KNNimputer de sklearn para imputar y completar los valores nulos en los registros faltantes.
                 ''')
    st.subheader('''
                 
                 
                 
                 ''')
    st.subheader('**Herramientas que utilice**',text_alignment='center')
    st.markdown("<p style='text-align: center;'>Este informe fue desarrollado en un entorno de Google Colab:</p>", unsafe_allow_html=True)
    st.link_button('Google Colab', 'https://colab.research.google.com/drive/1l9pRzfESzWKU9MgF4pPo9TD3Fr-VSrUZ?usp=sharing',icon_position='left',use_container_width=True)
    
    st.markdown('''
<p>
  En el que desplegué Python 3.12.13 y utilicé bibliotecas integradas y dedicadas a este lenguaje de programación:
</p>
<ul>
  <li><strong><a href="https://matplotlib.org/" target="_blank">matplotlib</a>, <a href="https://seaborn.pydata.org/" target="_blank">seaborn</a></strong>: librerías que utilicé para desplegar los gráficos estáticos.</li>
  <li><strong><a href="https://plotly.com/python/" target="_blank">plotly</a></strong>: librería que mediante su módulo <em>express</em> desplegué los diferentes gráficos y mapas dinámicos.</li>
  <li><strong><a href="https://pandas.pydata.org/" target="_blank">pandas</a></strong>: librería que utilicé para visualizar la información en un formato tabular y realizar las diferentes transformaciones.</li>
  <li><strong><a href="https://scikit-learn.org/" target="_blank">sklearn</a></strong>: librería que utilicé para escalar los datos, rellenar los nulos con KNN y aplicar un algoritmo de PCA (análisis de componentes principales).</li>
</ul>
                ''',unsafe_allow_html=True)
    st.markdown("""
<h4 style='text-align: left;'>El Límite De Cuantificación</h4>
<p>
Variable que define el umbral de exactitud o incertidumbre de la medición. Cada determinación tiene un umbral inferior de confianza donde si el valor de la medición está por debajo de este umbral, dicha medición tomará un porcentaje alto de incertidumbre, por encima de este umbral se define como zona de confianza. Para Tratar con las mediciones que caen por debajo de este umbral de confianza decidí utilizar La regla de la EPA, recomendado por La Agencia de Protección Ambiental de los Estados Unidos (EPA), en el que se divide el valor de la muestra por la raíz cuadrada de 2, asumiendo de esta manera a diferencia de la Sustitución por la Mitad que asume una distribución lineal por debajo del umbral, La regla de la EPA asume una distribución logarítmica.
</p>""", unsafe_allow_html=True) 
    st.markdown("""
<h4 style='text-align: left;'>KNN imputer</h4>
<p>
KNNimputer es un algoritmo de aprendizaje automático que utiliza la métrica de la distancia euclidiana para imputar los valores faltantes del promedio de los k vecinos mas cercanos.
</p>""", unsafe_allow_html=True)
    st.markdown('''
                $$d(P,Q) = \sqrt{\sum_{i=1}^{n}(p_i - q_i)^2}$$

                $$d(P,Q) = \sqrt{(p_1 - q_1)^2 + (p_2 - q_2)^2 + \cdots + (p_n - q_n)^2}$$
                ''')  
    st.subheader('''
                 
                 
                 
                 ''')
    st.subheader('**1.Convertir Los Conjuntos De Datos A Un Formato Largo**',text_alignment='center')
    st.text('''
(un registro representa una medición, de una determinación, en un lugar en concreto)
Lo convierto en un formato largo para separar cada tipo de determinación y poder tratar los datos mal imputados y fuera de los límites de cuantificación de cada determinación.
            ''')
    st.dataframe(head_calidad_del_agua_pivot_processed,width='stretch')
    st.subheader('Límite de Cuantificación de las Determinaciones')
    st.caption('- **OXÍGENO:** <0.05mg/l y <0.1mg/l',width='stretch')
    st.caption('- **DQO:** <50',width='stretch')
    st.caption('- **DBO5 :** <5 mg O2/l',width='stretch')   
    st.caption('- **ARSÉNICO TOTAL:**<4 µg/l',width='stretch')   
    st.dataframe(frecuencia_determinacion,width='stretch')
    st.subheader('**Análisis de variables**',text_alignment='center')
    st.plotly_chart(fig_det)
    st.markdown('''
<ul>
  <li>En promedio, el <strong>84%</strong> de los valores de las mediciones son nulas, por lo que existe un excedente de calendario.</li>
  <li>Únicamente las variables de <strong>coliformes fecales</strong> y <strong>oxígeno</strong> tienen errores de imputación.</li>
  <li>Las variables <strong>dqo</strong>, <strong>dbo5</strong> y <strong>arsénico total</strong> tienen en promedio un 3% de registros que están por debajo del límite de cuantificación.</li>
</ul>
                ''',unsafe_allow_html=True)
    st.subheader('**Análisis De Frecuencias De Muestreos**',text_alignment='center')
    st.plotly_chart(fig_true)
    st.markdown('''
Este conjunto de datos tiene mayor proporción o mayor frecuencia de muestra de oxígeno y arsénico que el resto de mediciones, quizás se deba a que para el oxígeno utilizaron medidores de campos móviles más fáciles y agiles de medir que el resto de mediciones, que se realizaron mediante laboratorio. En cuanto a la frecuencia de medición del arsénico se deba a que se destinó mayor presupuesto e importancia a medir este contaminante, que históricamente es un contaminante relevante en la zona pampeana y el norte del país.
                ''')
    
    st.subheader('**Análisis de Distribución De Mediciones**',text_alignment='center')
    st.plotly_chart(fig)
    st.markdown('''
<ul>
  <li>
    <strong>Oxígeno:</strong> El 75% de las mediciones registradas entre los años
    2024 y 2026 se encuentra en un rango inferior a 0,05 y hasta 7,5.
  </li>

  <li>
    <strong>Arsénico total:</strong> Esta es la variable que más se asemeja a una
    distribución normal. Presenta una ligera concentración hacia la derecha y no
    se observan valores atípicos.
  </li>

  <li>
    <strong>Coliformes fecales:</strong> Presenta una distribución concentrada
    principalmente en los valores inferiores. Sin embargo, se identifican cuatro
    mediciones atípicamente altas, con valores que varían entre 0,25 UFC/100 mL y
    1,75 UFC/100 mL.
  </li>

  <li>
    <strong>Demanda biológica de oxígeno (DBO5):</strong> La distribución presenta
    poca variación y tiende hacia valores bajos. El 50% central de las mediciones
    varía entre 10 mg/L y 20 mg/L.
  </li>

  <li>
    <strong>Demanda química de oxígeno (DQO):</strong> El 75% de los registros
    varía entre valores cercanos a 0 mg/L y 70 mg/L.
  </li>

  <li>
    <strong>Sólidos disueltos totales:</strong> Presenta una distribución bastante
    variada. El 50% central de los valores se encuentra entre 300 mg/L y 800 mg/L.
  </li>
</ul>
                ''',unsafe_allow_html=True)

    st.markdown('''




    ''')
    st.subheader('**5. Transformación de los conjuntos de datos en un formato diario de mediciones**',text_alignment='center')
    st.text('''
    Transforme el significado de cada registro de tal forma que el tipo de masa, lugar, coordenadas y fecha son identificadores únicos de cada registro en donde contiene las mediciones de las determinaciones de un día determinado.
        ''')
    st.image(ruta_imagen,use_container_width=True)
    st.markdown('''
                
                
                
                
                ''')
    st.subheader('**Análisis de Correlación Cruzada Entre Mediciones**',text_alignment='center')
    st.dataframe(df_corr)
    st.plotly_chart(fig_corr,use_container_width=True)
    st.markdown('''
microorganismos, mientras que los coliformes fecales son un recuento biológico directo que indica cuánta materia fecal viva y peligrosa ingresó al agua a través de efluentes cloacales. Ambas variables presentan una correlación monotónica del 70%. Por ende, al fusionar matemáticamente la causa (la carga bacteriana) y el efecto (el consumo drástico de oxígeno), se obtiene un indicador consolidado y preciso para medir la contaminación biológica real de las distintas masas de agua.                
                ''')
    st.markdown('''
También detecte una correlación entre arsénico total y sólidos disueltos totales. Por un lado, los sólidos disueltos totales miden la concentración de minerales en el agua y o por el otro lado el arsénico total mide la concentración de un mineral en específico. Juntar estas variables permite visualizar como es la tendencia entre el arsénico y los demás minerales.
                ''')
    st.markdown('''
                
                
                
                
                ''')
    
    st.subheader('**6 y 7. Aplicación de KNNimputer:**',text_alignment='center')
    st.markdown('''
<p>
  Luego de transformar y unificar el conjunto de datos en un formato diario de
  muestreo, se eliminaron los días en los que no se realizaron determinaciones.
  Posteriormente, todas las variables fueron escaladas mediante
  <code>StandardScaler</code>, con el objetivo de llevarlas a una misma escala y
  evitar que las variables con valores numéricos más altos influyeran en mayor
  medida durante la imputación.
</p>

<p>
  A continuación, se aplicó el algoritmo <code>KNNImputer</code> con el
  hiperparámetro <code>n_neighbors = 2</code>. Este método estima los valores
  faltantes utilizando el promedio de los dos registros más similares o cercanos.
</p>

<p>
  Se almacenó una copia del conjunto de datos escalado para aplicar posteriormente
  el Análisis de Componentes Principales (<code>PCA</code>). Finalmente, una vez
  realizada la imputación, los datos fueron transformados nuevamente a su escala
  original para facilitar su interpretación y permitir futuros análisis.
</p>''',unsafe_allow_html=True)
    st.subheader('''
                 
                 
                 
                 
                 
                 ''')
    st.subheader('**8. Análisis de Componentes Principales (PCA)**',text_alignment='center')
    st.markdown('''
  <p>
    El Análisis de Componentes Principales (<code>PCA</code>) es un algoritmo de
    aprendizaje no supervisado utilizado para reducir la dimensionalidad de un
    conjunto de datos, especialmente cuando existen variables altamente
    correlacionadas entre sí.
  </p>

  <p>
    Matemáticamente, utiliza la matriz de covarianza, los autovectores y los
    autovalores. Estos últimos permiten identificar qué nuevos vectores capturan
    la mayor proporción de la varianza presente en los datos. El objetivo del
    algoritmo es proyectar la información original sobre nuevos ejes ortogonales
    denominados componentes principales.
  </p>

  <p>
    La cantidad de componentes principales retenidos se define mediante
    hiperparámetros y busca conservar la mayor cantidad posible de información
    proveniente de las variables originales.
  </p>

  <ul>
    <li>
      Se aplicó PCA sobre las variables <strong>arsénico total</strong> y
      <strong>sólidos disueltos totales</strong>, generando el
      <strong>Índice Inorgánico</strong>.
    </li>

    <li>
      Se aplicó PCA sobre las variables <strong>DBO5</strong> y
      <strong>coliformes fecales</strong>, generando el
      <strong>Índice de Contaminación Biológica</strong>.
    </li>
  </ul>

  <h3>Índice Inorgánico</h3>

  <ul>
    <li>
      <strong>Valor alto o positivo:</strong> puede indicar una menor cantidad de
      agua disponible en el río o lago. En este escenario, los sólidos disueltos
      y el arsénico tienden a concentrarse, aumentando la carga mineral presente
      en el agua.
    </li>

    <li>
      <strong>Valor bajo o negativo:</strong> puede representar una situación de
      dilución o crecida. Las lluvias o el deshielo incrementan el volumen de agua
      dulce, reduciendo la concentración de minerales y arsénico en el sistema.
    </li>

    <li>
      <strong>Valor cercano a cero:</strong> puede representar una anomalía o un
      desacople entre las variables. Esto indica que el arsénico total y los
      sólidos disueltos dejaron de variar conjuntamente. Podría deberse a factores
      externos, como contaminación agrícola o urbana, o a procesos químicos que
      precipiten el arsénico hacia el fondo.
    </li>
  </ul>

  <h3>Índice de Contaminación Biológica</h3>

  <ul>
    <li>
      <strong>Valor alto o positivo:</strong> puede indicar un aumento simultáneo
      de coliformes fecales y DBO5. Esta situación es compatible con una elevada
      carga de contaminación orgánica y fecal, que incrementa la actividad
      bacteriana y la demanda de oxígeno del agua.
    </li>

    <li>
      <strong>Valor bajo o negativo:</strong> puede representar agua con baja
      carga de contaminación orgánica y fecal. En este caso, la demanda biológica
      de oxígeno es reducida y el sistema presenta condiciones biológicas más
      favorables.
    </li>

    <li>
      <strong>Valor cercano a cero:</strong> puede indicar una anomalía industrial
      o un desacople orgánico. Esto ocurre cuando la DBO5 aumenta, pero los
      coliformes fecales permanecen bajos. Una posible explicación es el ingreso
      de materia orgánica procedente de actividades industriales, como plantas
      procesadoras de alimentos, jugueras o papeleras.
    </li>
  </ul>''',unsafe_allow_html=True)
    
    st.dataframe(head_calidad_del_agua_pivot_PCA,width='stretch')
    
    
    st.plotly_chart(fig_trend_INDICE_INORGANICO,use_container_width=True)
    st.plotly_chart(fig_trend_INDICE_CONTAMINACION_ORGANICA,use_container_width=True)
    st.plotly_chart(fig_trend_OXIGENO,use_container_width=True)
    
    st.markdown('''
<section>
  <h7>Riachuelo</h7>
  <p>
    El Riachuelo es una masa de agua expuesta a múltiples fuentes de contaminación
    concentrada. Sin embargo, posee una dinámica hidrológica activa impulsada por
    su corriente constante y el régimen de lluvias.
  </p>
  <p>
    Esta tensión entre vertidos y dilución provoca la alta varianza estadística
    observada en las mediciones, haciendo que los niveles de demanda de oxígeno y
    los índices de contaminación biológica e inorgánica presenten fluctuaciones
    extremas.
  </p>
</section>

<section>
  <h7>Arroyos</h7>
  <p>
    Los arroyos presentan un índice inorgánico marcadamente bajo, lo que refleja
    un efecto constante de dilución, típico de sistemas de desagüe pluvial en
    entornos urbanos.
  </p>
  <p>
    Respecto al Índice de Contaminación Biológica, la tendencia general se mantiene
    en valores negativos (ausencia de crisis biológica aguda), con la clara
    excepción de la desembocadura del Arroyo Medrano, que presenta una anomalía en
    su carga.
  </p>
  <p>
    En cuanto a la demanda de oxígeno, se detecta una clara tendencia de disminución
    (pérdida de oxígeno disuelto) concentrada en los meses de octubre de 2024 y abril
    de 2025.
  </p>
</section>

<section>
  <h7>Lagos (Soldati y Lugano)</h7>
  <p>
    En cuanto al Índice Inorgánico, los lagos presentan ciclos de variación opuestos
    a los ecosistemas fluviales. Entre junio y septiembre de 2025, la tendencia
    natural se rompió (el índice tendió a 0). Es altamente probable que durante este
    trimestre un vertido o factor químico externo haya alterado la distribución
    natural entre el arsénico y el resto de los sólidos disueltos.
  </p>
  <p>
    Tanto el Lago Soldati como el Lago Lugano no parecen sufrir niveles crónicos de
    contaminación biológica cloacal. Sin embargo, durante el trimestre de junio a
    agosto de 2025 en el Lago Soldati, el índice biológico se anuló (tendió a 0).
    Este comportamiento anómalo señala el ingreso de un contaminante no biológico
    (industrial o químico) que disparó bruscamente la demanda de oxígeno sin aportar
    coliformes fecales.
  </p>
</section>

<section>
  <h7>Río de la Plata</h7>
  <p>
    Dada su magnitud y el inmenso volumen de dilución que maneja esta masa de agua,
    el Índice Inorgánico presenta sostenidamente valores negativos.
  </p>
  <p>
    Se diagnostican niveles bajos de contaminación biológica, manteniendo una
    concentración de oxígeno disuelto estable y saludable que varía en un rango de
    3 mg/L a 9 mg/L.
  </p>
</section>''',unsafe_allow_html=True)
    st.subheader('''
                 
                 
                 
                 
                 
               ''')
    st.subheader('Mapas de calor',text_alignment='center')
    st.text('''Se realizaron tres mapas de color correspondientes a los años 2024, 2025 y 2026. Cada mapa utiliza los datos de la última muestra disponible de cada lugar para representar la distribución de los indicadores analizados: Índice Inorgánico, Índice de Contaminación Biológica y Oxígeno Disuelto.''')
    st.plotly_chart(fig_integrada_INORGANICO)
    st.markdown('''
<p>
  Se observa que, al comparar las últimas mediciones disponibles de cada año,
  el <strong>Índice Inorgánico</strong> presenta una tendencia general decreciente
  hacia las fechas más recientes.
</p>

<p>
  Con excepción del <strong>Lago Lugano</strong>, que registra un índice positivo,
  el resto de los cuerpos de agua presentan valores negativos, lo que indica una
  menor concentración relativa de compuestos inorgánicos disueltos en estos sitios.
</p>
                ''',unsafe_allow_html=True)
    st.plotly_chart(fig_integrada_CONTAMINACION_BIOLOGICA)
    st.markdown('''
<p>
  Se observa que, al comparar las últimas mediciones disponibles de cada año,
  el <strong>Índice Inorgánico</strong> presenta una tendencia general decreciente
  hacia las fechas más recientes.
</p>

<p>
  Con excepción del <strong>Lago Lugano</strong>, que registra un índice positivo,
  el resto de los cuerpos de agua presentan valores negativos, lo que indica una
  menor concentración relativa de compuestos inorgánicos disueltos en estos sitios.
</p>
                ''',unsafe_allow_html=True)
    st.plotly_chart(fig_integrada_OXIGENO)
    st.markdown('''
<p>
  Se observa que, hacia finales de 2025, se registraron los niveles más altos de
  oxígeno disuelto de todo el período analizado.
</p>
''',unsafe_allow_html=True)
    st.subheader('''
                 
                 
                 
                 
                 
               ''')
    st.subheader('Conclusión General',text_alignment='center')
    st.markdown('''
  <p>
    A lo largo del presente informe técnico, la aplicación de modelos de reducción
    de dimensionalidad permitió aislar la dinámica hidrológica base de los distintos
    ecosistemas y detectar desviaciones críticas. Mediante el análisis de los
    componentes principales, se identificaron ubicaciones y períodos puntuales en
    los que los patrones naturales de correlación se rompieron por completo,
    evidenciando eventos de contaminación externa aguda.
  </p>

  <p>
    Como principales hallazgos, se destaca la detección de alteraciones químicas
    atípicas en los ecosistemas lacustres cerrados de la ciudad, así como la
    confirmación empírica de la elevada volatilidad de la cuenca del Riachuelo. En
    este último, la constante tensión entre los vertidos contaminantes y los
    fenómenos físicos de dilución genera una dinámica ambiental altamente inestable,
    la cual el modelo logró capturar y diferenciar de manera efectiva.
  </p>

  <p>
    Finalmente, uno de los aportes más importantes del trabajo radica en la etapa de
    preprocesamiento. La resolución de valores nulos mediante imputación espacial
    (<strong>KNNImputer</strong>) y la normalización de las variables mediante
    escalado estándar permitieron consolidar un conjunto de datos robusto,
    consistente y parametrizado. Esta base de datos limpia y estandarizada constituye
    un recurso de gran utilidad para facilitar futuros análisis estadísticos y el
    desarrollo de nuevos modelos de ciencia de datos.
  </p>
''',unsafe_allow_html=True)
    
    st.set_page_config(layout="wide")
if __name__ == "__main__":
    main()
    
