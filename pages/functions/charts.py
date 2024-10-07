import streamlit as st
import altair as alt
import polars as pl


# Este archivo es para las funciones de todos los graficos para facilitar su orden
# Para esta iteración el rod no está filtrado de ninguna forma y ya esta .collect()
# Posiblemente habrá que agregar cache en algunas transformaciones si se vuelve muy lento

def all_services_bar_graph(rod, height):

    df_all_sevices = (
        rod.group_by(pl.col("all_services"))
        .agg(pl.len().alias("total"))
        .with_columns(
            pl.when(pl.col("all_services") == True).then(pl.lit("TLS")).otherwise(pl.lit("Sin TLS")).alias("all_services")
            )
    )


    bar_all_services = (
        alt.Chart(df_all_sevices).mark_bar().encode(
            alt.X('total:Q', stack="zero", title=None, axis = alt.Axis(ticks=False, labels=False)),
            alt.Color('all_services:N', scale=alt.Scale(scheme='category20'),
                      legend = alt.Legend(
                          orient='left',
                          title="Servicios",
                          labelFontSize=20,
                          titleFontSize=25,
                          labelOffset = 10,
                          titlePadding = 15,
                          padding=28,
                          strokeColor="white",                          
                      )),
        )
    )

    stack_labels = (
        alt.Chart(df_all_sevices).mark_text(
            align="center",
            baseline="middle",
            color="white",
            fontSize=30,
            dx = -30,
            dy=20
        ).encode(
            alt.X("total:Q", stack="zero"),
            text = alt.Text("total:Q"),
        )
    )

    total_text = (
        alt.Chart(df_all_sevices).mark_text(
            align="left",
            baseline="middle",
            dx = 10,
            fontSize=30
            )
    ).encode(
        alt.X('sum(total):Q', stack=True, title=None),
        alt.Text('sum(total):Q'),
        color=alt.value('white')
    )

    graph_all_services = ((bar_all_services + total_text + stack_labels)
                          .configure_axis(grid=False, domain=False)
                          .properties(
                              height = height,
                              #title = alt.TitleParams(text = 'Servicios', align='center', fontSize=20)
                              )
                          )

    return graph_all_services


def ratio_graph(rod, height):

    df_ratio = (
        rod.group_by(pl.col("ratio"))
        .agg(pl.len().alias("total"))
    ).sort("ratio", )

    print(df_ratio)

    ratios_bar = (
        alt.Chart(df_ratio).mark_bar().encode(
            alt.X('total:Q', stack="zero", title=None, axis = alt.Axis(ticks=False, labels=False)),
            alt.Color('ratio:N', scale=alt.Scale(scheme='category20'),
                      legend = alt.Legend(
                          orient='left',
                          title="Ratio",
                          labelFontSize=15,
                          titleFontSize=30,
                          labelOffset = 5,
                          titlePadding = 18,
                          padding=25,
                          strokeColor="white",
                          columns = 3                        
                      ))
        )
    )

    stack_labels = (
        alt.Chart(df_ratio).mark_text(
            align="center",
            baseline="middle",
            color="white",
            fontSize=30,
            dx = -30,
            dy=20
        ).encode(
            alt.X("total:Q", stack="zero"),
            text = alt.Text("total:Q"),
        )
    )


    graph_all_ratios = (ratios_bar + stack_labels).properties(height = height).configure_axis(grid=False, domain=False)

    return(graph_all_ratios)