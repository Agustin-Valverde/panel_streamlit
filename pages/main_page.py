import streamlit as st 
import polars as pl
import altair as alt
import requests
from functions.rod_writer import *
from functions.charts import *
from streamlit_extras.stylable_container import stylable_container


# Archivo main, tiene mas sentido que desde aca solo controlar principalmente como se leen los datos
# y la estructura de la pagina


# DATA & Markdown
st.set_page_config(layout="wide")
st.markdown(
    """
<style>
button[title="View fullscreen"] {
    display: none;
}
</style>
""",
    unsafe_allow_html=True,
)

@st.cache_data
def cache_read_rod():
    df = read_rod_csv()
    return df

rod = cache_read_rod()


# MAIN PANEL
st.title(f'Shippter Forwarding {date.today()}')

left_containers = []
left_col, right_col = st.columns([0.8, 0.2], gap="medium")
subcol_1, subcol_2, subcol_3 = left_col.columns([0.33, 0.33, 0.33])



## LEFT COL
with left_col:
    with subcol_1:
        with st.container(border=True, height=185):
            st.write("OPS TOTALES")

    with subcol_2:
        with st.container(border=True, height=185):
            st.write("OPS SEMANALES")

    with subcol_3:
        with st.container(border=True, height=185):
            st.write("ULTIMAS OPS")

    with stylable_container(
        key="main_container",
        css_styles="""
        {
            border: 1px solid white;
            border-radius: 0.5rem;
            padding: calc(1em - 1px);
            box-shadow: 4px 4px 10px rgba(255, 255, 255, 0.25);
            }
        """
    ):
        cont = st.container(border=False, height=510)


with cont:
    #Todos los servicios

    graph_all_services = all_services_bar_graph(rod, 150)
    st.altair_chart(graph_all_services, use_container_width=True)


    graph_all_ratio = ratio_graph(rod, 150)
    st.altair_chart(graph_all_ratio, use_container_width=True)

    graph_all_type = type_graph(rod, 150)
    st.altair_chart(graph_all_type, use_container_width=True,)



# RIGHT COL

with right_col:
    st.subheader("Col_Der MISCELANEOS", divider='gray')

    # Definir el estilo CSS
    css_styles_cont = """
    {
        border: 1px solid white;
        border-radius: 0.5rem;
        padding: calc(1em - 1px);
        box-shadow: 4px 4px 10px rgba(255, 255, 255, 0.2);
        background-color: rgba(34,33,39,255)
    }
    """

    # Crear contenedores con un bucle
    right_containers = []
    for i in range(1, 4):  # Desde 1 hasta 3
        with stylable_container(key=f"right_{i}", css_styles=css_styles_cont):
            container = st.container(border=False, height=183)
            right_containers.append(container)

with right_containers[0]:
    st.write("SAAS")

with right_containers[1]:
    st.write("MAPA?")

with right_containers[2]:
    st.write("VENDEDOR TOP?")