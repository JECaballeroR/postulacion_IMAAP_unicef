import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
import base64
from pathlib import Path

st.header(
    "Prueba Técnica iMMAP-Datos-UNICEF Emergencias - JORGE ESTEBAN CABALLERO RODRIGUEZ"
)

st.write("## [Repositorio de Github](https://github.com/JECaballeroR/postulacion_IMAAP_unicef)")

st.markdown("""Como consideraciones generales:
- El pre-procesado y unificación de los datos se realizó en Python, en un [Jupyter Notebook](https://github.com/JECaballeroR/postulacion_IMAAP_unicef/blob/master/Postular%20IMMAP.ipynb)"
- Esto se hizo pues era más práctico para realizar ciertos procesos de la postulación.
- El archivo consolidado solicitado se encuentra en el repositorio [(aquí)](https://github.com/JECaballeroR/postulacion_IMAAP_unicef/blob/master/ExcelConsolidado.xlsx) y en el correo.
- El Dashboard se realizó en streamlit, principalmente por ser un framework de desarrollo rápido.
- El tiempo de trabajo en la prueba se limitó a las "4 o 6 horas" sugeridas en la llamada de notificación de la misma el día 15/09/2022
    - Por lo anterior, se limitó la limpieza de los datos y el tiempo al diseño de la solución a al mínimo viable
- Se asumen ciertos elementos

""")

st.write("A continuación se deja una versión del informe enviado en Word incrustado en el dashboard")

def load_bootstrap():
    return st.markdown(
        '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">',
        unsafe_allow_html=True,
    )


load_bootstrap()


def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded


def img_to_html(img_path):
    img_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(
        img_to_bytes(img_path)
    )
    return img_html


st.markdown(
    f"""# Informe General Trimestre:

## Mapa de vacantes por Departamento (Archivo – Demanda Laboral)
{img_to_html("images/Untitled.png")}

El departamento con mayor demanda de vacantes es Cundinamarca, con 208559 vacantes disponibles en el trimestre. Le sigue Antioquia, con 77586

Esto es coherente con el hecho de que Bogotá y Medellín son dos de las más grandes ciudades del país y por tanto, tengan una mayor concentración de talento.

Filtrando los datos solo por Bogotá y Medellín se tienen 238423 vacantes, que son más del 50% de las vacantes totales (453524)


{img_to_html("images/Untitled 1.png")}


## Top de actividades por mayor demanda (2 dígitos)

{img_to_html("images/Untitled 2.png")}

Las 3 actividades de más demanda fueron el código 52 (Almacenamiento y actividades complementarias al transporte), el código 42 (Obras de Ingeniería Civil) y el código 74 (otras actividades profesionales, científicas y técnicas).

Esto es coherente con la realidad colombiana, siendo un país en desarrollo se espera que principalmente construya nueva infraestructura para sustentar su progreso, y cómo consecuencia, almacene y transporte insumos. Así, es lógico que estos sectores presenten alta competencia.

### Top de actividades por mayor demanda (3 dígitos)

{img_to_html("images/Untitled 3.png")}

 Entrando a más especificidad, las dos actividades más representativas tienen el código 522 (Actividades de las estaciones, vías y servicios complementarios para el transporte), y 422 (Construcción de proyectos de servicio público).

Estas actividades son coherentes con lo esperado: Un país en desarrollo construye y transporta para sustentar dicho desarrollo.

## Demanda laboral por tipo.

{img_to_html("images/Untitled 4.png")}
{img_to_html("images/Untitled 5.png")}
{img_to_html("images/Untitled 6.png")}



Se ve que la mayor demanda está asociada a los trabajos de alta rotación (coherente con el tipo de trabajo).  De hecho, en general, se tienen la mayoría de las vacantes en Alta Rotación y en Alta Rotación y difícil consecución. Esto muestra un panorama donde constantemente habrá trabajos disponibles, pero es posible que por la alta rotación no sean atractivos para los posibles trabajadores. Hay pocas vacantes de largo plazo, pero de poca oferta (vacantes tipo DCS).

Siguiendo con el énfasis en los grupos de actividades de interés, se observa que para el código 52, la gran mayoría de vacantes son de alta rotación (hay 30096 en este nivel, y solo 142 en otros tipos) para el código 42 la mayoría son de alta rotación y difícil consecución (hay 16139 en este tipo, 5423 en ARS y no hay vacantes de otros tipos para este grupo de actividad).   Dada la naturaleza de estos trabajos, esto se encuentra dentro de esperado (construir requiere personal más capacitado, por ejemplo).

## Vacantes por sector

{img_to_html("images/Untitled 7.png")}

Dada la nota dada, se ignoran las actividades de empleo en el análisis (dado que debería redistribuirse).

Se observa un sector no esperado de acuerdo con el análisis anterior como el más activo: Servicios financieros, empresariales y otros (se esperaría el Comercio al por mayor y por menor…. Que esté de primero). A nivel general, hay coherencia con las proporciones de los sectores, y más aún las Actividades de Empleo teniendo tal volumen (existe un gran número de temporales en Colombia).

En general, obviando las actividades asociadas a Temporales, los sectores tienden a ser relativamente de tamaños similares (entre 5 y 20 mil vacantes). Aquellos sectores con mayor tamaño son sectores necesarios para un país en crecimiento (p.e., salud, manufactura, construcción, tecnología, comercio). Estos sectores son coherentes con las actividades que se ven de mayor volumen.

## Mapas de Oferta registrada (Izquierda) y Oferta Colocada (Derecha)

{img_to_html("images/Untitled 8.png")}

{img_to_html("images/Untitled 9.png")}

Aunque hay demanda en todo el país, la oferta se centra en los departamentos de mayor desarrollo metropolitano, dejando de lado departamentos cómo el Amazonas. Es posible que hayan ofertas laborales asociadas a estos departamentos pero con otra ubicación (ejemplo, trabajos que hagan trabajo de campo en estas zonas).

En la oferta, se observa también una concentración similar a la demanda en cuanto a la mayor concentración en Cundinamarca y Antioquia.

Además, la Oferta registrada es cerca de 8-10 veces más la oferta colocada,  y es cerca de 100 veces menos la demanda, lo cuál puede estar sugiriendo una problemática de desempleo: se solicita más trabajos de los que hay personal apto para realizarse. No obstante, es importante aclarar que la oferta se limita a lo registrado en el SISE y por tanto, no se incluye toda la red de prestadores: la comparación entre Oferta si puede aproximar la realidad, pero seguramente la razón entre oferta y demanda sería mejor al poder captar toda la información de los trabajadores.

### En resumen:

- La principal concentración de oferta y demanda está en Cundinamarca y Antioquia, principalmente en Bogotá y Medellín.
- Las principales actividades son 52 (Almacenamiento y actividades complementarias al transporte), el código 42 (Obras de Ingeniería Civil) y el código 74 (otras actividades profesionales, científicas y técnicas).
- Existe una menor colocación de la oferta que la oferta dada. La demanda parece ser mayor que la oferta, lo que sugiere una situación de desempleo alto.""",
    unsafe_allow_html=True,
)
