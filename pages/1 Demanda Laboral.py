import streamlit as st
import pandas as pd
import json
from urllib.request import urlopen
#import numpy as np
import plotly.graph_objs as go
import plotly.express as px
st.set_page_config(layout="wide")

import plotly.offline as pyo # para exportar en html

st.header('### Página de Demanda Laboral')
st.markdown("### Enunciado: ")
st.markdown("""Con la información anterior realizar un Dashboard (obviando las vacantes sin
registro, que no contengan información municipal y departamental) donde se
muestre en una página el total de vacantes y filtros que permitan ver la información
por mes, departamento, municipio y ocupación. Hacer un mapa de vacantes
totales por departamento, una gráfica tipo Top de actividades con el mayor numero
de vacantes demandadas por dos y tres dígitos y un listado que muestre el
municipio, ocupación y vacantes.""")
@st.cache(allow_output_mutation=True)
def cargar_datos():
    data = pd.read_excel('ExcelConsolidado.xlsx', sheet_name='Demanda Laboral')
    dem_vacante= pd.read_excel('ExcelConsolidado.xlsx', sheet_name='Dem. Laboral por tipo vacante')

    data['Depto'] =  data['Depto'].apply(lambda x: x.replace("BOGOTA, D. C.", "CUNDINAMARCA"))
    data=data[[x for x in data.columns if "Unnamed" not in x]]
    with urlopen(
            'https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json') as response:
        departamentos_json = json.load(response)
    return data,  departamentos_json, dem_vacante


data,  departamentos_json, dem_vacante= cargar_datos()

st.sidebar.header('Filtros')


meses=st.sidebar.multiselect('Mes', options=data['Mes'].unique(), default=data['Mes'].unique(), )

@st.cache
def filtar_mes(df, meses=meses):
    return df[df['Mes'].apply(lambda x: x in meses)].copy()
df_meses = filtar_mes(data, meses=meses)

dpto= st.sidebar.multiselect('Departamento', options=df_meses['Depto'].unique(), default=df_meses['Depto'].unique())

@st.cache
def filtar_departamento(df, dpto=dpto):
    return df[df['Depto'].apply(lambda x: x in dpto)].copy()
@st.cache
def filtar_municipio(df, mpio):
        return df[df['Mpio'].apply(lambda x: x in mpio)]

df_dpto = filtar_departamento(df_meses, dpto=dpto)

@st.cache
def plot_map(df_mpio):
    df2 = df_mpio.groupby(['Depto']).sum().reset_index()
    locs = df2['Depto']

    for loc in departamentos_json['features']:
        loc['id'] = loc['properties']['NOMBRE_DPT']
    fig = go.Figure(go.Choroplethmapbox(
        geojson=departamentos_json,
        locations=locs,
        z=df2['Vacantes'],
        colorscale='Blues',
        colorbar_title="Vacantes"))
    fig.update_layout(mapbox_style="carto-positron",
                      mapbox_zoom=3.4,
                      mapbox_center={"lat": 4.570868, "lon": -74.2973328})
    return fig

@st.cache
def plot_ciiu2dig(df):
    data_vacantes=df.copy()
    data_vacantes=data_vacantes.groupby('ciiu2dig').sum().reset_index().sort_values(by="Vacantes", ascending=False).head(10)
    data_vacantes['ciiu2dig']=data_vacantes['ciiu2dig'].astype(str)
    return px.bar(data_vacantes, x='ciiu2dig', y='Vacantes')

@st.cache
def plot_ciiu3dig(df):
    data_vacantes=df.copy()
    data_vacantes=data_vacantes.groupby('ciuo_3d').sum().reset_index().sort_values(by="Vacantes", ascending=False).head(10)
    data_vacantes['ciuo_3d']=data_vacantes['ciuo_3d'].astype(int).astype(str)
    return px.bar(data_vacantes, x='ciuo_3d', y='Vacantes')


if dpto:
    mpio=st.sidebar.multiselect('Municipio',options=df_dpto['Mpio'].unique(), default=df_dpto['Mpio'].unique())

    df_mpio = filtar_municipio(df_dpto, mpio=mpio)

    st.markdown(f'# TOTAL DE VACANTES DE LA SELECCIÓN: <span style="color:#4BAAFF"> {df_mpio["Vacantes"].sum()} </span>', unsafe_allow_html=True)

    fig = plot_map(df_mpio=df_mpio)
    col1,col2=st.columns([2,3])
    col1.markdown("## Listado con municipio, código de actividad, vacantes")

    col1.dataframe((df_mpio[['Mpio','ciiu2dig', 'ciuo_3d', 'Vacantes' ]]
    .groupby(['Mpio','ciiu2dig', 'ciuo_3d']).sum().reset_index()
                   .sort_values(by='Vacantes', ascending=False)))
    col2.markdown("## Mapa de vacantes totales por departamento")

    col2.plotly_chart(fig, use_container_width=True)

    col1,col2=st.columns(2)
    col1.markdown("## Top actividades con mayor demanda de vacantes por 2 dígitos")
    col1.plotly_chart(plot_ciiu2dig(df_mpio), use_container_width=True)
    col2.markdown("## Top actividades con mayor demanda de vacantes por 3 dígitos")

    col2.plotly_chart(plot_ciiu3dig(df_mpio), use_container_width=True)

else:
    st.warning("Elija al menos un departamento para visualizar los datos")