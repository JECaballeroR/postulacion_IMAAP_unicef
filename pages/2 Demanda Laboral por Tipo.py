import streamlit as st
import pandas as pd
import json
from urllib.request import urlopen
#import numpy as np
import plotly.graph_objs as go
import plotly.express as px
st.set_page_config(layout="wide")
st.sidebar.markdown("### Filtros")

st.markdown("### Página de Demanda por Tipo Laboral")

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
def plot_heatmap(df: pd.DataFrame, x: str, y: str, val:str):
    data_heatmap = (
        df.reset_index()[[x, y, val, "index"]]
            .groupby([x, y])
            .sum()
            .reset_index()
            .pivot(x, y, val)
            .fillna(0)
    )
    fig = px.imshow(
        data_heatmap,
        color_continuous_scale=px.colors.sequential.Blues,
        aspect="auto",
        title=f"Heatmap {x} vs {y}",
    )
    fig.update_traces(
        hovertemplate="<b><i>"
                      + x
                      + "</i></b>: %{y} <br><b><i>"
                      + y
                      + "</i></b>: %{x} <br><b><i>Vacantes</i></b>: %{z}<extra></extra>"
    )
    return fig








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

meses=st.sidebar.multiselect('Mes', options=dem_vacante['Mes'].unique(), default=dem_vacante['Mes'].unique(), )
@st.cache
def filtar_mes(df, meses=meses):
    return df[df['Mes'].apply(lambda x: x in meses)].copy()

@st.cache
def filtar_df(df, filtro, string):
    return df[df[string].apply(lambda x: x in filtro)].copy()

df_meses = filtar_df(dem_vacante, meses, "Mes")

sector=st.sidebar.multiselect('Sector', options=dem_vacante['nombre_sector'].unique(), default=dem_vacante['nombre_sector'].unique(), )

df_sector= filtar_df(df_meses, sector, 'nombre_sector')




df_sector = df_sector.melt(id_vars=["nombre_sector",
"ciuo 4d",
"Año",
"Mes",
"ciiu2dig",
"ciuo_3d"], value_vars=['ARS','NS',	'ARDC'	,'DCS'	,'DCN'], var_name='Tipo Vacante', value_name='Vacantes')
if sector:
    tipo=st.sidebar.multiselect('Tipo Vacante', options=df_sector['Tipo Vacante'].unique(), default=df_sector['Tipo Vacante'].unique(), )

    df_tipo= filtar_df(df_sector, tipo, 'Tipo Vacante')
    df_mostrar = df_tipo.groupby('Tipo Vacante').sum().reset_index()[['Tipo Vacante','Vacantes']]

    heatmap_df = df_tipo[['ciiu2dig', 'Tipo Vacante', 'Vacantes']].copy()

    heatmap_df = heatmap_df.rename(columns={'ciiu2dig': 'Actividad (2 digitos)'})

    col1, col2 = st.columns([2, 4])

    col1.markdown("""Los tipos de vacantes son:


    - ARS (Alta rotación solamente), 
    - NS (Neutral solamente), 
    - ARDC (Alta rotación y dificil consecución), 
    - DCS (Dificil consecución solamente) y 
    - DCN (Dificil consecución y neutrales)
    """)

    data_table = pd.DataFrame(df_mostrar[df_mostrar['Tipo Vacante'].apply(lambda x: x in ['ARS', 'ARDC', 'DCS'])])
    col1.dataframe(data_table)

    col2.plotly_chart(plot_heatmap(heatmap_df, x='Tipo Vacante', y='Actividad (2 digitos)', val='Vacantes'),
                      use_container_width=True)
    df_bar = df_tipo.groupby("nombre_sector").sum().reset_index()[['nombre_sector', 'Vacantes']].sort_values(
        by='Vacantes', ascending=False)
    col2.markdown("""### Vacantes por Sector""")

    col2.plotly_chart(px.bar(df_bar, x='nombre_sector', y='Vacantes'), use_container_width=True)
    col1.plotly_chart(px.bar(data_table.sort_values(by='Vacantes'), x='Tipo Vacante', y='Vacantes'), use_container_width=True)
else:
    st.warning("Elige al menos un sector para mostrar los resultados")

