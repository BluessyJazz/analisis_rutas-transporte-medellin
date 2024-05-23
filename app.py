import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# Título de la aplicación
st.title('Visualización de Rutas de Transporte Público en Medellín')

# Carga de datos GeoJSON
geojson_file = 'rutas_de_transporte_publi.geojson'
gdf = gpd.read_file(geojson_file)

# Mostrar la tabla de datos
st.subheader('Tabla de Datos Geoespaciales')
st.write(gdf)

# Creación del mapa con Folium
st.subheader('Mapa de Rutas de Transporte Público')
m = folium.Map(location=[6.2442, -75.5812], zoom_start=12)

# Agregar rutas al mapa
for _, row in gdf.iterrows():
    folium.GeoJson(row['geometry']).add_to(m)

# Mostrar el mapa en la aplicación
st_folium(m, width=700, height=500)

m
