import streamlit as st
import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium

# Configurar la página
st.set_page_config(page_title='Rutas de Transporte Público Colectivo en Medellín',
                   page_icon='🚌',
                   layout='wide',
                   initial_sidebar_state='expanded')

# Función para cargar datos geográficos
@st.cache_data
def load_geo_data(filepath):
    data = gpd.read_file(filepath)
    return data

# Función para mostrar el mapa
def show_map(gdf, filter_column=None, filter_value=None):
    # Filtrar los datos si se proporciona un filtro
    if filter_column and filter_value:
        gdf = gdf[gdf[filter_column] == filter_value]

    # Crear un mapa centrado en Medellín
    m = folium.Map(location=[6.2442, -75.5812], zoom_start=12)

    # Agregar las rutas al mapa
    for _, row in gdf.iterrows():
        if row.geometry.geom_type == 'LineString':
            folium.PolyLine(
                locations=[(lat, lon) for lon, lat in row.geometry.coords],
                color="blue",
                weight=2.5,
                opacity=1
            ).add_to(m)
        elif row.geometry.geom_type == 'MultiLineString':
            for linestring in row.geometry.geoms:
                folium.PolyLine(
                    locations=[(lat, lon) for lon, lat in linestring.coords],
                    color="blue",
                    weight=2.5,
                    opacity=1
                ).add_to(m)
    
    st_folium(m, width=700, height=500)

# Función para mostrar información detallada
def show_route_info(gdf, route_name):
    route = gdf[gdf['nombre'] == route_name].iloc[0]
    st.write(f"### Información de la Ruta: {route_name}")
    st.write(f"**Empresa:** {route['empresa']}")
    st.write(f"**Número de paradas:** {len(route.geometry.coords)}")
    st.write(f"**Longitud total:** {route.geometry.length:.2f} km")

# Función principal
def main():
    st.title("Rutas de Transporte Público Colectivo en Medellín")
    st.write("Explora y analiza las rutas de transporte público colectivo en Medellín.")

    # Ruta al archivo GeoJSON
    geojson_file = "rutas_de_transporte_publi.geojson"

    # Cargar datos geográficos
    data_load_state = st.text('Cargando datos...')
    gdf = load_geo_data(geojson_file)
    data_load_state.text('Datos cargados con éxito!')

    # Verificar si las columnas 'empresa' y 'nombre' existen en el DataFrame
    if 'empresa' not in gdf.columns or 'nombre' not in gdf.columns:
        st.error("Las columnas necesarias ('empresa' y 'nombre') no se encuentran en el dataset.")
        st.write("Columnas disponibles en el dataset:", list(gdf.columns))
        return

    # Mostrar el mapa inicial
    show_map(gdf.copy())

    # Filtrar rutas por empresa
    empresas = gdf['empresa'].unique()
    empresa_seleccionada = st.selectbox("Selecciona una empresa", empresas)

    # Mostrar el mapa filtrado por empresa
    show_map(gdf.copy(), filter_column='empresa', filter_value=empresa_seleccionada)

    # Seleccionar una ruta para mostrar información detallada
    rutas = gdf[gdf['empresa'] == empresa_seleccionada]['nombre'].unique()
    ruta_seleccionada = st.selectbox("Selecciona una ruta", rutas)

    # Mostrar información detallada de la ruta seleccionada
    show_route_info(gdf.copy(), ruta_seleccionada)

if __name__ == "__main__":
    main()
