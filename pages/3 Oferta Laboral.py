import streamlit as st
import pandas as pd
import json
from urllib.request import urlopen
#import numpy as np
import plotly.graph_objs as go
import plotly.express as px
st.set_page_config(layout="wide")
@st.cache
def plot_map(df, col_departamento, col_data):
    df2 = df.groupby([col_departamento]).sum().reset_index()
    locs = df2[col_departamento]

    for loc in departamentos_json['features']:
        loc['id'] = loc['properties']['NOMBRE_DPT']
    fig = go.Figure(go.Choroplethmapbox(
        geojson=departamentos_json,
        locations=locs,
        z=df2[col_data],
        colorscale='Blues',
        colorbar_title=col_data))
    fig.update_layout(mapbox_style="carto-positron",
                      mapbox_zoom=3.4,
                      mapbox_center={"lat": 4.570868, "lon": -74.2973328})
    return fig
@st.cache
def show_table(data):
    df=data.copy()
    df=df.dropna()

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    fill_color='#262730',
                    align='center'),
        cells=dict(values=[df[x] for x in df.columns],
                   fill_color='#373737',
                   align='center'))
    ])

    return fig

@st.cache(allow_output_mutation=True)
def cargar_datos():
    registrados= pd.read_excel('ExcelConsolidado.xlsx', sheet_name='Oferta Laboral - Registrados').dropna()
    colocados= pd.read_excel('ExcelConsolidado.xlsx', sheet_name='Oferta Laboral - Colocados')

    colocados['Departamento Residencia '] =   colocados['Departamento Residencia '].apply(lambda x: x.replace("BOGOTÁ, D.C.", "CUNDINAMARCA"))
    registrados['Departamento_Residencia '] =  registrados['Departamento_Residencia '].apply(lambda x: str(x).replace("BOGOTÁ, D.C.", "CUNDINAMARCA") if isinstance(x,str) else x)
    colocados=colocados[colocados['ciiu2dig'].apply(lambda x: x not in ['NA', 'nan', 'na'])]
    with urlopen(

            'https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json') as response:
        departamentos_json = json.load(response)
    return registrados, colocados,  departamentos_json
registrados, colocados,  departamentos_json = cargar_datos()
@st.cache
def filtrar_df(df, filtro, string):
    return df[df[string].apply(lambda x: x in filtro)].copy()
mes = st.sidebar.multiselect("Meses", options=registrados['Mes'].unique(), default=registrados['Mes'].unique())


registrados=filtrar_df(registrados, mes, 'Mes')
colocados=filtrar_df( colocados, mes, 'Mes')



col1, col2=st.columns(2)

registrados_agrupado=registrados.groupby(['Año','Mes', 'País', 'Departamento_Residencia ']).sum().reset_index()
fig =show_table(registrados_agrupado)

col1.markdown("### Oferta Registrada")
col1.plotly_chart(fig,use_container_width=True)



col1.markdown("### Mapa Oferta Registrada")
col1.plotly_chart( plot_map(registrados_agrupado, col_departamento='Departamento_Residencia ', col_data='Registrados'))

colocados_agrupado=colocados.groupby(['Año','Mes', 'País', 'Departamento Residencia '])['Colocados'].sum().reset_index()
fig2 = show_table(colocados_agrupado)
col2.markdown("### Oferta Colocada")
col2.plotly_chart(fig2, use_container_width=True)
col2.markdown("### Mapa Oferta Colocada")
col2.plotly_chart( plot_map(colocados_agrupado, col_departamento='Departamento Residencia ', col_data='Colocados'))


