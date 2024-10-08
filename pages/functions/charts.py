import streamlit as st
import altair as alt
import polars as pl


# Este archivo es para las funciones de todos los graficos para facilitar su orden
# Para esta iteración el rod no está filtrado de ninguna forma y ya esta .collect()
# Posiblemente habrá que agregar cache en algunas transformaciones si se vuelve muy lento

colors = ["#27b9a9", "#c1bbb4", "#2d6e68" , "#0a0a0a", "#394949"]

def all_services_bar_graph(rod, height):

    df_all_sevices = (
        rod.group_by(pl.col("all_services"))
        .agg(pl.len().alias("total"))
        .with_columns(
            pl.when(pl.col("all_services") == True).then(pl.lit("TLS")).otherwise(pl.lit("Sin TLS")).alias("all_services")
            )
    )


    bar_all_services = (
        alt.Chart(df_all_sevices).mark_bar(stroke="white").encode(
            alt.X('total:Q', stack="zero", title=None, axis = alt.Axis(ticks=False, labels=False)),
            alt.Color('all_services:N',
                      legend = None),
        )
    )

    legend_only = (
        alt.Chart(df_all_sevices).mark_rect(opacity=0).encode(
            alt.Color('all_services:N', scale=alt.Scale(range=colors),
                    legend = alt.Legend(
                          orient='left',
                          title="Servicios",
                          labelFontSize=20,
                          titleFontSize=25,
                          labelOffset = 10,
                          titlePadding = 15,
                          padding=28,
                          strokeColor="white",                          
                      ))
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

    graph_all_services = ((legend_only + bar_all_services + stack_labels)
                          .configure_axis(grid=False, domain=False)
                          .properties(height = height)
                          .resolve_legend(color='independent')
                          )

    return graph_all_services


def ratio_graph(rod: pl.DataFrame, height):

    df_ratio = (
        rod.group_by(pl.col("ratio"))
        .agg(pl.len().alias("total"))
    ).sort("ratio")

    print(df_ratio)

    ratios_bar = (
        alt.Chart(df_ratio).mark_bar(stroke="white").encode(
            alt.X('total:Q', stack="zero", title=None, axis = alt.Axis(ticks=False, labels=False)),
            alt.Color('ratio:N',
                      legend = None)
        )
    )

    legend_only = (
        alt.Chart(df_ratio).mark_rect(opacity=0).encode(
            alt.Color('ratio:N', scale=alt.Scale(range = colors),
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
            order = alt.Order("ratio:N")
        )
    )


    total_text = (
        alt.Chart(df_ratio).mark_text(
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

    graph_all_ratios = ((legend_only + ratios_bar + stack_labels)
                        .properties(height = height)
                        .configure_axis(grid=False, domain=False)
                        .resolve_legend(color='independent'))

    return(graph_all_ratios)


def type_graph(rod: pl.DataFrame, height):

    df_type = (
        rod.group_by(pl.col("type"))
        .agg(pl.len().alias("total"))
    ).sort("type", descending=True)

    print(df_type)

    type_bar = (
        alt.Chart(df_type).mark_bar(stroke= "white").encode(
            alt.X('total:Q', stack="zero", title=None, axis = alt.Axis(ticks=False, labels=False)),
            alt.Color('type:N',
                      legend = None)
        )
    )

    legend_only = (
        alt.Chart(df_type).mark_rect(opacity=0).encode(
            alt.Color('type:N', scale=alt.Scale(range = colors),
                    legend=alt.Legend(
                        orient='left',
                        title="Tipo",
                        labelFontSize=15,
                        titleFontSize=30,
                        labelOffset=5,
                        titlePadding=13,
                        padding=30,
                        columns=2,
                        strokeColor="white",
                    ))
        )
    )


    stack_labels = (
        alt.Chart(df_type).mark_text(
            align="center",
            baseline="middle",
            color="white",
            fontSize=30,
            dx = -30,
            dy=20
        ).encode(
            alt.X("total:Q", stack="zero"),
            text = alt.Text("total:Q"),
            order = alt.Order("type:N")
        )
    )

    total_text = (
        alt.Chart(df_type).mark_text(
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

    graph_all_type = ((legend_only + type_bar + stack_labels)
                      .properties(height = height)
                      .configure_axis(grid=False, domain=False)
                      .resolve_legend(color='independent') 
                      )

    return(graph_all_type)