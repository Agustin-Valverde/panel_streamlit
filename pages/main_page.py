import streamlit as st 
import polars as pl
import altair as alt
import requests
from functions.rod_writer import *
from functions.charts import *

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
left_containers = []
left_col, right_col = st.columns([0.8, 0.2])


## LEFT COL
with left_col:
    st.subheader(f'Shippter Forwarding {date.today()}')
    cont = st.container(border=True, height=650, )


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

    with st.container(border=True, height=205) as item_1:
        st.empty()


    with st.container(border=True, height=205) as item_2:
        st.empty()


    with st.container(border=True, height=205) as item_3:
        st.empty()

