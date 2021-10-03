# -*- encoding: utf-8 -*-
"""
Programa de Mentoria DSA 2021
"""

from app.home import vups
from app.home.vups import utils as vups_utils
from plotly.data import gapminder
import plotly.express as px
from . import const
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import pandas as pd
import os
import datetime
import itertools
import numpy as np
import folium

def plot_kpi_percentage_progress():
    """
    Global Actual Progress
    Baseline 46%
    """
    resumo = fn_resumo_microdados()
    fig_c1 = go.Figure(
        go.Indicator(
            mode="number+delta",
            value=resumo.get("n_confirmados"),
            number={
                # "suffix": "%",
                "font": {"size": 36, "color": "#008080", "family": "Arial"},
            },
            delta={"position": "bottom", "reference": 46, "relative": True},
            domain={"x": [0, 1], "y": [0, 1]},
        )
    )
    fig_c1.update_layout(
        autosize=False,
        width=200,
        height=72,
        margin=dict(l=20, r=20, b=20, t=30),
        paper_bgcolor="#fbfff0",
        font={"size": 36},
    )
    return fig_c1

def plot_kpi_spend_hours():
    """
    Global Spend Hours
    Baseline 92.700
    """
    resumo = fn_resumo_microdados()
    fig_c2 = go.Figure(
        go.Indicator(
            mode="number+delta",
            value=resumo.get('n_descartados'),
            number={
                # "suffix": " HH",
                "font": {"size": 36, "color": "#008080", "family": "Arial"},
                "valueformat": ",f",
            },
            delta={"position": "bottom", "reference": 92700},
            domain={"x": [0, 1], "y": [0, 1]},
        )
    )
    fig_c2.update_layout(
        autosize=False,
        width=200,
        height=72,
        margin=dict(l=20, r=20, b=20, t=30),
        paper_bgcolor="#fbfff0",
        font={"size": 36},
    )
    fig_c2.update_traces(
        delta_decreasing_color="#3D9970",
        delta_increasing_color="#FF4136",
        delta_valueformat="f",
        selector=dict(type="indicator"),
    )
    return fig_c2

def plot_kpi_tcpi():
    """
    TPCI - To Complete Performance Index ≤ 1.00
    """
    resumo = fn_resumo_microdados()
    fig_c3 = go.Figure(
        go.Indicator(
            mode="number+delta",
            value=resumo.get('n_supeitos'),
            number={"font": {"size": 36, "color": "#008080", "family": "Arial"}},
            delta={"position": "bottom", "reference": 1, "relative": False},
            domain={"x": [0, 1], "y": [0, 1]},
        )
    )
    fig_c3.update_layout(
        autosize=False,
        width=200,
        height=72,
        margin=dict(l=20, r=20, b=20, t=30),
        paper_bgcolor="#fbfff0",
        font={"size": 36},
    )
    fig_c3.update_traces(
        delta_decreasing_color="#3D9970",
        delta_increasing_color="#FF4136",
        delta_valueformat=".3f",
        selector=dict(type="indicator"),
    )
    return fig_c3

def plot_kpi_obitos():
    """
    TPCI - To Complete Performance Index ≤ 1.00
    """
    resumo = fn_resumo_microdados()
    fig_c3 = go.Figure(
        go.Indicator(
            mode="number+delta",
            value=resumo.get('n_obitos'),
            number={"font": {"size": 36, "color": "#008080", "family": "Arial"}},
            delta={"position": "bottom", "reference": 1, "relative": False},
            domain={"x": [0, 1], "y": [0, 1]},
        )
    )
    fig_c3.update_layout(
        autosize=False,
        width=200,
        height=72,
        margin=dict(l=20, r=20, b=20, t=30),
        paper_bgcolor="#fbfff0",
        font={"size": 36},
    )
    fig_c3.update_traces(
        delta_decreasing_color="#3D9970",
        delta_increasing_color="#FF4136",
        delta_valueformat=".3f",
        selector=dict(type="indicator"),
    )
    return fig_c3

def plot_small_bar_percentage_progress():
    x = ["Actual", "Previous", "Average", "Planned"]
    y = [5.5, 4.2, 6.3, 8.5]
    fig_m_prog = go.Figure([go.Bar(x=x, y=y, text=y, textposition="auto")])
    fig_m_prog.update_layout(
        paper_bgcolor="#fbfff0",
        plot_bgcolor="#fbfff0",
        font={"color": "#008080", "family": "Arial"},
        height=100,
        width=250,
        margin=dict(l=15, r=1, b=4, t=4),
    )
    fig_m_prog.update_yaxes(title="y", visible=False, showticklabels=False)
    fig_m_prog.update_traces(marker_color="#17A2B8", selector=dict(type="bar"))
    return fig_m_prog

def plot_small_bar_spend_hours():
    x = ["Δ vs Prev", "Δ vs Aver", "Δ vs Plan"]
    y = [10, 12, 8]
    fig_m_hh = go.Figure([go.Bar(x=x, y=y, text=y, textposition="auto")])
    fig_m_hh.update_layout(
        paper_bgcolor="#fbfff0",
        plot_bgcolor="#fbfff0",
        font={"color": "#008080", "family": "Arial"},
        height=100,
        width=250,
        margin=dict(l=15, r=1, b=1, t=1),
    )
    fig_m_hh.update_yaxes(title="y", visible=False, showticklabels=False)
    fig_m_hh.update_traces(marker_color="#17A2B8", selector=dict(type="bar"))
    return fig_m_hh

def plot_line_progress_actual_planned():
    data = pd.read_excel(os.path.join(const.DATADIR, "curva.xlsx"))
    y = data.loc[data.Activity_name == "Total"]
    # Create traces
    fig3 = go.Figure()
    fig3.add_trace(
        go.Scatter(
            x=y["Date"],
            y=y["Progress"],
            mode="lines",
            name="Progress",
            marker_color="#FF4136",
        )
    )
    fig3.add_trace(
        go.Scatter(
            x=y["Date"],
            y=y["Baseline"],
            mode="lines",
            name="Baseline",
            marker_color="#17A2B8",
        )
    )
    fig3.update_layout(
        title={"text": "Actual Progress vs Planned", "x": 0.5},
        paper_bgcolor="#fbfff0",
        plot_bgcolor="#fbfff0",
        font={"color": "#008080", "size": 12, "family": "Georgia"},
        height=220,
        width=540,
        legend=dict(orientation="h", yanchor="top", y=0.99, xanchor="left", x=0.01),
        margin=dict(l=1, r=1, b=1, t=30),
    )
    fig3.update_xaxes(
        showline=True,
        linewidth=1,
        linecolor="#F7F7F7",
        mirror=True,
        nticks=6,
        rangemode="tozero",
        showgrid=False,
        gridwidth=0.5,
        gridcolor="#F7F7F7",
    )
    fig3.update_yaxes(
        showline=True,
        linewidth=1,
        linecolor="#F7F7F7",
        mirror=True,
        nticks=10,
        rangemode="tozero",
        showgrid=True,
        gridwidth=0.5,
        gridcolor="#F7F7F7",
    )
    fig3.layout.yaxis.tickformat = ",.0%"
    return fig3

def plot_widget_cost_variance():
    fig_cv = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=1.05,
            number={
                "font": {"size": 22, "color": "#008080", "family": "Arial"},
                "valueformat": "#,##0",
            },
            domain={"x": [0, 1], "y": [0, 1]},
            gauge={
                "axis": {"range": [None, 1.5], "tickwidth": 1, "tickcolor": "black"},
                "bar": {"color": "#06282d"},
                "bgcolor": "white",
                "steps": [
                    {"range": [0, 1], "color": "#FF4136"},
                    {"range": [1, 1.5], "color": "#3D9970"},
                ],
            },
        )
    )

    fig_cv.update_layout(
        paper_bgcolor="#fbfff0",
        font={"color": "#008080", "family": "Arial"},
        height=135,
        width=250,
        margin=dict(l=10, r=10, b=15, t=20),
    )
    return fig_cv

def plot_widget_schedule_variance():
    fig_sv = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=0.95,
            number={
                "font": {"size": 22, "color": "#008080", "family": "Arial"},
                "valueformat": "#,##0",
            },
            domain={"x": [0, 1], "y": [0, 1]},
            gauge={
                "axis": {"range": [None, 1.5], "tickwidth": 1, "tickcolor": "black"},
                "bar": {"color": "#06282d"},
                "bgcolor": "white",
                "steps": [
                    {"range": [0, 1], "color": "#FF4136"},
                    {"range": [1, 1.5], "color": "#3D9970"},
                ],
            },
        )
    )
    fig_sv.update_layout(
        paper_bgcolor="#fbfff0",
        font={"color": "#008080", "family": "Arial"},
        height=135,
        width=250,
        margin=dict(l=10, r=10, b=15, t=20),
    )
    return fig_sv

def plot_bar_hours_spend_planned():
    y = data.loc[data.Activity_name == "Total"]
    y = data.loc[data.Activity_name == "Total"]
    fig_hh = go.Figure()
    fig_hh.add_trace(
        go.Bar(
            x=y["Date"], y=y["Spend_Hours"], name="Spend Hours", marker_color="#FF4136"
        )
    )
    fig_hh.add_trace(
        go.Bar(
            x=y["Date"],
            y=y["Planned_Hours"],
            name="Planned Hours",
            marker_color="#17A2B8",
        )
    )
    fig_hh.update_layout(
        barmode="group",
        title={"text": "Spend Hours vs Planned", "x": 0.5},
        paper_bgcolor="#fbfff0",
        plot_bgcolor="#fbfff0",
        font={"color": "#008080", "family": "Georgia"},
        height=250,
        width=540,
        legend=dict(orientation="h", yanchor="top", y=0.99, xanchor="left", x=0.01),
        margin=dict(l=5, r=1, b=1, t=25),
    )
    fig_hh.update_xaxes(
        showline=True,
        linewidth=1,
        linecolor="#F7F7F7",
        mirror=True,
        nticks=6,
        rangemode="tozero",
        showgrid=False,
        gridwidth=0.5,
        gridcolor="#F7F7F7",
    )
    fig_hh.update_yaxes(
        showline=True,
        linewidth=1,
        linecolor="#F7F7F7",
        mirror=True,
        nticks=10,
        rangemode="tozero",
        showgrid=False,
        gridwidth=0.5,
        gridcolor="#F7F7F7",
    )
    return fig_hh

def plot_gantt():
    # *******Gantt Chart
    df = pd.DataFrame(
        [
            dict(Disc="Civ", Start="2021-01-04", Finish="2021-08-10"),
            dict(Disc="Mec", Start="2021-03-05", Finish="2021-09-15"),
            dict(Disc="Pip", Start="2021-04-20", Finish="2021-11-30"),
            dict(Disc="Ele", Start="2021-05-20", Finish="2021-12-05"),
            dict(Disc="Ins", Start="2021-06-20", Finish="2021-12-20"),
            dict(Disc="Com", Start="2021-07-20", Finish="2021-12-30"),
        ]
    )
    fig2 = px.timeline(df, x_start="Start", x_end="Finish", y="Disc")
    fig2.update_yaxes(autorange="reversed")
    fig2.update_layout(
        title={"text": "Main dates", "x": 0.5},
        plot_bgcolor="#eef9ea",
        paper_bgcolor="#eef9ea",
        font={"color": "#008080", "family": "Georgia"},
        height=340,
        width=550,
        margin=dict(l=51, r=5, b=10, t=50),
    )
    fig2.update_traces(marker_color="#17A2B8", selector=dict(type="bar"))
    return fig2

gapminder = px.data.gapminder()

def plot_slider_bubbles(df=gapminder):
    fig = px.scatter(
        df,
        x="gdpPercap",
        y="lifeExp",
        animation_frame="year",
        animation_group="country",
        size="pop",
        color="continent",
        hover_name="country",
        log_x=True,
        size_max=55,
        range_x=[100, 100000],
        range_y=[25, 90],
    )

    fig["layout"].pop("updatemenus")

    return fig

def plot_bar_with_line():
    y_saving = [1.3586, 2.2623000000000002, 4.9821999999999997, 6.5096999999999996,
                7.4812000000000003, 7.5133000000000001, 15.2148, 17.520499999999998
                ]
    y_net_worth = [93453.919999999998, 81666.570000000007, 69889.619999999995,
                78381.529999999999, 141395.29999999999, 92969.020000000004,
                66090.179999999993, 122379.3]
    x = ['Japan', 'United Kingdom', 'Canada', 'Netherlands',
        'United States', 'Belgium', 'Sweden', 'Switzerland']


    # Creating two subplots
    fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=True,
                        shared_yaxes=False, vertical_spacing=0.001)

    fig.append_trace(go.Bar(
        x=y_saving,
        y=x,
        marker=dict(
            color='rgba(50, 171, 96, 0.6)',
            line=dict(
                color='rgba(50, 171, 96, 1.0)',
                width=1),
        ),
        name='Household savings, percentage of household disposable income',
        orientation='h',
    ), 1, 1)

    fig.append_trace(go.Scatter(
        x=y_net_worth, y=x,
        mode='lines+markers',
        line_color='rgb(128, 0, 128)',
        name='Household net worth, Million USD/capita',
    ), 1, 2)

    fig.update_layout(
        title='Household savings & net worth for eight OECD countries',
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=True,
            domain=[0, 0.85],
        ),
        yaxis2=dict(
            showgrid=False,
            showline=True,
            showticklabels=False,
            linecolor='rgba(102, 102, 102, 0.8)',
            linewidth=2,
            domain=[0, 0.85],
        ),
        xaxis=dict(
            zeroline=False,
            showline=False,
            showticklabels=True,
            showgrid=True,
            domain=[0, 0.42],
        ),
        xaxis2=dict(
            zeroline=False,
            showline=False,
            showticklabels=True,
            showgrid=True,
            domain=[0.47, 1],
            side='top',
            dtick=25000,
        ),
        legend=dict(x=0.029, y=1.038, font_size=10),
        margin=dict(l=100, r=20, t=70, b=70),
        paper_bgcolor='rgb(248, 248, 255)',
        plot_bgcolor='rgb(248, 248, 255)',
    )

    annotations = []

    y_s = np.round(y_saving, decimals=2)
    y_nw = np.rint(y_net_worth)

    # Adding labels
    for ydn, yd, xd in zip(y_nw, y_s, x):
        # labeling the scatter savings
        annotations.append(dict(xref='x2', yref='y2',
                                y=xd, x=ydn - 20000,
                                text='{:,}'.format(ydn) + 'M',
                                font=dict(family='Arial', size=12,
                                        color='rgb(128, 0, 128)'),
                                showarrow=False))
        # labeling the bar net worth
        annotations.append(dict(xref='x1', yref='y1',
                                y=xd, x=yd + 3,
                                text=str(yd) + '%',
                                font=dict(family='Arial', size=12,
                                        color='rgb(50, 171, 96)'),
                                showarrow=False))
    # Source
    annotations.append(dict(xref='paper', yref='paper',
                            x=-0.2, y=-0.109,
                            text='OECD "' +
                                '(2015), Household savings (indicator), ' +
                                'Household net worth (indicator). doi: ' +
                                '10.1787/cfc6f499-en (Accessed on 05 June 2015)',
                            font=dict(family='Arial', size=10, color='rgb(150,150,150)'),
                            showarrow=False))

    fig.update_layout(annotations=annotations)

    return fig

def plot_bar_color_palette():
    top_labels = ['Strongly<br>agree', 'Agree', 'Neutral', 'Disagree',
                'Strongly<br>disagree']

    colors = ['rgba(38, 24, 74, 0.8)', 'rgba(71, 58, 131, 0.8)',
            'rgba(122, 120, 168, 0.8)', 'rgba(164, 163, 204, 0.85)',
            'rgba(190, 192, 213, 1)']

    x_data = [[21, 30, 21, 16, 12],
            [24, 31, 19, 15, 11],
            [27, 26, 23, 11, 13],
            [29, 24, 15, 18, 14]]

    y_data = ['The course was effectively<br>organized',
            'The course developed my<br>abilities and skills ' +
            'for<br>the subject', 'The course developed ' +
            'my<br>ability to think critically about<br>the subject',
            'I would recommend this<br>course to a friend']

    fig = go.Figure()

    for i in range(0, len(x_data[0])):
        for xd, yd in zip(x_data, y_data):
            fig.add_trace(go.Bar(
                x=[xd[i]], y=[yd],
                orientation='h',
                marker=dict(
                    color=colors[i],
                    line=dict(color='rgb(248, 248, 249)', width=1)
                )
            ))

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            domain=[0.15, 1]
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        barmode='stack',
        paper_bgcolor='rgb(248, 248, 255)',
        plot_bgcolor='rgb(248, 248, 255)',
        margin=dict(l=120, r=10, t=140, b=80),
        showlegend=False,
    )

    annotations = []

    for yd, xd in zip(y_data, x_data):
        # labeling the y-axis
        annotations.append(dict(xref='paper', yref='y',
                                x=0.14, y=yd,
                                xanchor='right',
                                text=str(yd),
                                font=dict(family='Arial', size=14,
                                        color='rgb(67, 67, 67)'),
                                showarrow=False, align='right'))
        # labeling the first percentage of each bar (x_axis)
        annotations.append(dict(xref='x', yref='y',
                                x=xd[0] / 2, y=yd,
                                text=str(xd[0]) + '%',
                                font=dict(family='Arial', size=14,
                                        color='rgb(248, 248, 255)'),
                                showarrow=False))
        # labeling the first Likert scale (on the top)
        if yd == y_data[-1]:
            annotations.append(dict(xref='x', yref='paper',
                                    x=xd[0] / 2, y=1.1,
                                    text=top_labels[0],
                                    font=dict(family='Arial', size=14,
                                            color='rgb(67, 67, 67)'),
                                    showarrow=False))
        space = xd[0]
        for i in range(1, len(xd)):
                # labeling the rest of percentages for each bar (x_axis)
                annotations.append(dict(xref='x', yref='y',
                                        x=space + (xd[i]/2), y=yd,
                                        text=str(xd[i]) + '%',
                                        font=dict(family='Arial', size=14,
                                                color='rgb(248, 248, 255)'),
                                        showarrow=False))
                # labeling the Likert scale
                if yd == y_data[-1]:
                    annotations.append(dict(xref='x', yref='paper',
                                            x=space + (xd[i]/2), y=1.1,
                                            text=top_labels[i],
                                            font=dict(family='Arial', size=14,
                                                    color='rgb(67, 67, 67)'),
                                            showarrow=False))
                space += xd[i]

    fig.update_layout(annotations=annotations)

    return fig

def plot_bar():
    df = pd.DataFrame(
        {
            "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
            "Amount": [4, 1, 2, 2, 4, 5],
            "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
        }
    )
    return px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

def generate_table(df, max_rows=10):
    import dash_html_components as html

    return html.Table(
        [
            html.Thead(html.Tr([html.Th(col) for col in df.columns])),
            html.Tbody(
                [
                    html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
                    for i in range(min(len(df), max_rows))
                ]
            ),
        ]
    )

def plot_sexo_idade(df):
    fig = px.bar(df, x="Sexo", y="IdadeNaDataNotificacao")
    return fig

def plot_scatter(df, selected_year):
    """
    ===============================
    plot_scatter
    ===============================

    Plot the classification probability for different classifiers. We use a 3 class
    dataset, and we classify it with a Support Vector classifier, L1 and L2
    penalized logistic regression with either a One-Vs-Rest or multinomial setting,
    and Gaussian process classification.
    """
    print(__doc__)

    # Author: Uallas Leles <uallasleles@hotmail.com>
    # License: BSD 3 clause

    filtered_df = df[df.year == selected_year]

    fig = px.scatter(
        filtered_df,
        x="gdpPercap",
        y="lifeExp",
        size="pop",
        color="continent",
        hover_name="country",
        log_x=True,
        size_max=55,
    )

    fig.update_layout(transition_duration=500)

    return fig

def plot_map_folium():
    map = folium.Map(location=[-16.3722412, -39.5757040], zoom_start=10)
    map.save("map.html")

##############################################################################
# OFICIAIS
##############################################################################

def plot_year_taxs(UF="ES"):
    
    # INNER JOIN COM OS TIPOS DE ARRECADAÇÃO
    df = pd.merge(
        vups.datasets.arrecadacao(),
        vups.datasets.tipo_arrecadacao(),
        how="left",
        left_on="co_tipo_arrecadacao",
        right_on="CD_TIP_ARRECAD",
    )

    # AGRUPANDO POR: UF, ANO, TRIBUTO
    df = vups.group_by(df, ["sg_uf", "ano_arrecadacao", "NM_TIP_ARRECAD"]).sort_values(
        ["ano_arrecadacao", "va_arrecadacao"], ascending=False
    )

    # FILTRANDO O ESTADO
    df = df[df["sg_uf"] == UF]

    # CRIA O GRÁFICO
    fig = px.bar(
        df,
        x="ano_arrecadacao",
        y="va_arrecadacao",
        hover_data=["NM_TIP_ARRECAD"],
        color="NM_TIP_ARRECAD",
        labels={"pop": "population of Canada"},
        height=600,
    )
    fig.update_layout(
        {"plot_bgcolor": "rgba(0,0,0,0)", "paper_bgcolor": "rgba(0,0,0,0)"}
    )

    return fig

def plot_calendar_heatmap(cidade="AFONSO CLAUDIO", tipo="NOVOS CASOS", mes_analise=1, ano_analise=2021):
    """
    OBJETIVO:
    plt_calendar_heatmap plota um heatmap em forma de calendário, filtrado por cidade, mes, ano,
    e tipo de informação

    PARÂMETROS:
    cidade: filtra o df baseado na cidade fornecida como parametro de entrada
    tipo: o plot retorna dois tipos de informação -> novos casos de covid por dia e casos acumulado de covid. dessa
    meneira, pode assumir dois valores ('NOVOS CASOS', 'ACUMULADO')
    mes_analise: filtra o df baseado no mês fornecido como parametro de entrada
    ano_analise: filtra o df baseado no ano fornecido como parametro de entrada

    DIFICULDADES:
    por fazer uso da base de dados MICRODADOS, que tem aproximadamente 500mb, a função tem demorado
    por volta de 1min:30s para ser executada (no meu computador).

    PONTOS DE ATENÇÃO:
    (linha 8): tive que comentar #import folium #import branca para conseguir rodar o script

    (linha 356): por algum motivo, a coluna 'DataEncerramento' não está sendo tratada (str -> datatype)
    automaticamente pela função criada pelo Uallas. Fiz um tratamento forçado para que conseguisse rodar
    a função

    AUTOR:
    Guilherme
    """

    COLUMNS = [
        "Municipio",
        "Classificacao",
        "DataDiagnostico",
        "DataCadastro",
        "DataEncerramento",
    ]

    # --------- FILTRANDO DF PARA CIDADES DO ES ---------
    filtro_es = [
        "AGUIA BRANCA",
        "ALTO RIO NOVO",
        "ARACRUZ",
        "BAIXO GUANDU",
        "COLATINA",
        "GOVERNADOR LINDENBERG",
        "IBIRACU",
        "JOAO NEIVA",
        "LINHARES",
        "MANTENOPOLIS",
        "MARILANDIA",
        "PANCAS",
        "RIO BANANAL",
        "SAO DOMINGOS DO NORTE",
        "SAO GABRIEL DA PALHA",
        "SAO ROQUE DO CANAA",
        "SOORETAMA",
        "VILA VALERIO",
        "AFONSO CLAUDIO",
        "BREJETUBA",
        "CARIACICA",
        "CONCEICAO DO CASTELO",
        "DOMINGOS MARTINS",
        "FUNDAO",
        "GUARAPARI",
        "IBATIBA",
        "ITAGUACU",
        "ITARANA",
        "LARANJA DA TERRA",
        "MARECHAL FLORIANO",
        "SANTA LEOPOLDINA",
        "SANTA MARIA DE JETIBA",
        "SANTA TERESA",
        "SERRA",
        "VENDA NOVA DO IMIGRANTE",
        "VIANA",
        "VILA VELHA",
        "VITORIA",
        "AGUA DOCE DO NORTE",
        "BARRA DE SAO FRANCISCO",
        "BOA ESPERANCA",
        "CONCEICAO DA BARRA",
        "ECOPORANGA",
        "JAGUARE",
        "MONTANHA",
        "MUCURICI",
        "NOVA VENECIA",
        "PEDRO CANARIO",
        "PINHEIROS",
        "PONTO BELO",
        "SAO MATEUS",
        "VILA PAVAO",
        "ALEGRE",
        "ALFREDO CHAVES",
        "ANCHIETA",
        "APIACA",
        "ATILIO VIVACQUA",
        "BOM JESUS DO NORTE",
        "CACHOEIRO DE ITAPEMIRIM",
        "CASTELO",
        "DIVINO DE SAO LOURENCO",
        "DORES DO RIO PRETO",
        "GUACUI",
        "IBITIRAMA",
        "ICONHA",
        "IRUPI",
        "ITAPEMIRIM",
        "IUNA",
        "JERONIMO MONTEIRO",
        "MARATAIZES",
        "MIMOSO DO SUL",
        "MUNIZ FREIRE",
        "MUQUI",
        "PIUMA",
        "PRESIDENTE KENNEDY",
        "RIO NOVO DO SUL",
        "SAO JOSE DO CALCADO",
        "VARGEM ALTA",
    ]

    # --------- BUSCANDO DF ---------
    df = vups.datasets.microdados(columns=COLUMNS)

    df["DataEncerramento"] = df["DataEncerramento"].astype("datetime64[ns]")

    # --------- CRIANDO DF_CALENDAR_NEW(CASOS NOVOS) E DF_CALENDAR_CLOSED(CASOS FECHADOS) ---------
    # df_calendar_new -> filtrar pacientes com covid confirmados; groupby(Municipio, DataDiagnostico); contar ocorrencias
    df_calendar_new = (
        df[df["Classificacao"] == "Confirmados"]
        .groupby(["Municipio", "DataDiagnostico"])["DataCadastro"]
        .size()
        .reset_index(name="count_new")
    )

    # renomendo coluna DataDiagnostico
    df_calendar_new.rename(columns={"DataDiagnostico": "date"}, inplace=True)

    # df_calendar_closed -> filtrar pacientes com covid confirmados; groupby(Municipio, DataEncerramento); contar ocorrencias
    df_calendar_closed = (
        df[df["Classificacao"] == "Confirmados"]
        .groupby(["Municipio", "DataEncerramento"])["DataCadastro"]
        .size()
        .reset_index(name="count_closed")
    )

    # transformando valores de casos fechados em negativo
    df_calendar_closed["count_closed"] = df_calendar_closed["count_closed"] * -1

    # renomendo coluna DataEncerramento
    df_calendar_closed.rename(columns={"DataEncerramento": "date"}, inplace=True)

    # --------- MERGE ENTRE OS DOIS DFs CRIADOS ---------
    df_calendar = pd.merge(
        df_calendar_new,
        df_calendar_closed,
        how="outer",
        left_on=["Municipio", "date"],
        right_on=["Municipio", "date"],
    )

    # --------- TRABLHANDO O NOVO DF ---------
    # organizando por cidade/data
    df_calendar = df_calendar.sort_values(["Municipio", "date"]).reset_index()

    # preenchendo Nan com zero(0)
    for i in ["count_new", "count_closed"]:
        df_calendar[i] = df_calendar[i].fillna(0)

    # criando coluna acumulado por cidade
    municipios = df_calendar["Municipio"].unique()
    acum = []
    for idx, i in enumerate(df_calendar["date"]):
        if df_calendar["Municipio"].iloc[idx] == df_calendar["Municipio"].iloc[idx - 1]:
            try:
                acum.append(
                    acum[idx - 1]
                    + df_calendar["count_new"].iloc[idx]
                    + df_calendar["count_closed"].iloc[idx]
                )
            except:
                acum.append(
                    df_calendar["count_new"].iloc[idx]
                    + df_calendar["count_closed"].iloc[idx]
                )
        else:
            acum.append(
                0
                + df_calendar["count_new"].iloc[idx]
                + df_calendar["count_closed"].iloc[idx]
            )

    df_calendar["acum"] = acum

    # criando colunas de dia/semana/dia_da_semana/mes/ano
    df_calendar["day"] = [i.day for i in df_calendar["date"]]
    df_calendar["week"] = [i.week for i in df_calendar["date"]]
    df_calendar["weekday"] = [i.weekday() for i in df_calendar["date"]]
    df_calendar["month"] = [i.month for i in df_calendar["date"]]
    df_calendar["year"] = [i.year for i in df_calendar["date"]]

    # --------- CIANDO LISTAS PARA PLOTAGEM DO CALENDÁRIO ---------
    # variaveis para ajudar na manipulacao dso dados
    # quantidade de dias no mes de análise
    dias_28 = [2]
    dias_31 = [1, 3, 5, 7, 8, 10, 12]
    dias_30 = [4, 6, 9, 11]

    if mes_analise in dias_28 and ano_analise != 2020:
        n_dias = 28
    elif mes_analise in dias_30:
        n_dias = 30
    elif mes_analise in dias_31:
        n_dias = 31
    else:
        n_dias = 29

    # aplicando filtros
    if tipo == "NOVOS CASOS":
        df_calendar_display = (
            df_calendar[
                (df_calendar["Municipio"] == cidade)
                & (df_calendar["month"] == mes_analise)
                & (df_calendar["year"] == ano_analise)
            ][
                [
                    "Municipio",
                    "date",
                    "day",
                    "week",
                    "weekday",
                    "month",
                    "year",
                    "count_new",
                ]
            ]
            .sort_values(by=["day"])
            .reset_index()
            .drop(columns=["index"])
        )
    else:
        df_calendar_display = (
            df_calendar[
                (df_calendar["Municipio"] == cidade)
                & (df_calendar["month"] == mes_analise)
                & (df_calendar["year"] == ano_analise)
            ][["Municipio", "date", "day", "week", "weekday", "month", "year", "acum"]]
            .sort_values(by=["day"])
            .reset_index()
            .drop(columns=["index"])
        )

    # criando listagem com a contagem de casos para cada dia do mes e as informações da semana do ano e dia da semana
    # preenchendo com zero os dias em que nao tiveram registros
    info_dia = []
    contador = 0
    for i in range(1, n_dias + 1):
        if i == df_calendar_display["day"].iloc[contador]:
            dia = i
            numero_casos = int(df_calendar_display.iloc[contador, -1])
            semana_do_ano = df_calendar_display["week"].iloc[contador]
            dia_da_semana = df_calendar_display["weekday"].iloc[contador]
            if contador < len(df_calendar_display) - 1:
                contador = contador + 1
        else:
            dia = i
            numero_casos = 0
            semana_do_ano = int(datetime(ano_analise, mes_analise, i).strftime("%W"))
            dia_da_semana = datetime(ano_analise, mes_analise, i).weekday()

        info_dia.append([dia, numero_casos, semana_do_ano, dia_da_semana])

    # separando essa lista em outras 4
    dias, n_casos, semana, dia_semana = zip(*info_dia)

    # criando lista com o numero de casos de cada dia do mes e separado em lista por semana
    final_casos = []
    parcial_casos = []
    for i, week in enumerate(semana):
        if i == 0:
            parcial_casos.append(n_casos[i])
        elif i == n_dias - 1:
            parcial_casos.append(n_casos[i])
            final_casos.append(parcial_casos)
        else:
            if week == semana[i - 1]:
                parcial_casos.append(n_casos[i])
            else:
                final_casos.append(parcial_casos)
                parcial_casos = []
                parcial_casos.append(n_casos[i])

    # calculando o valor maximo da quantidade de casos para servir como ponto maximo da escala de cores
    max_value = []
    for i in range(len(final_casos)):
        max_value.append(max(final_casos[i]))

    max_value = max(max_value)

    # preenchendo valores relativos aos dias que completam as semanas com menos de 7 dias (inicio/final)
    # o max_value serve para ajustar a cor (branco) que vai ser printado no heatmap para esses valores de preenchimento
    while len(final_casos[0]) < 7:
        final_casos[0].insert(0, 0.001 * max_value)

    while len(final_casos[-1]) < 7:
        final_casos[-1].append(0.001 * max_value)

    # transformando valores a serem pintados em cinza, em negativo
    for i in range(len(final_casos)):
        for j in range(len(final_casos[i])):
            if final_casos[i][j] > 0 and final_casos[i][j] < 1:
                final_casos[i][j] = final_casos[i][j] * -1

    # tranformando dias de int para str
    dias = list(map(str, dias))

    # preenchendo lista de acordo com o exigido para o plot (lista de listas para cada semana do mes)
    final_dias = []
    parcial_dias = []
    contador = dia_semana[0] + 1

    for i, dia in enumerate(dias):
        if i == len(dias) - 1:
            parcial_dias.append(dia)
            final_dias.append(parcial_dias)
        elif contador < 8:
            parcial_dias.append(dia)
            contador += 1
        else:
            final_dias.append(parcial_dias)
            parcial_dias = []
            parcial_dias.append(dia)
            contador = 2

    # preenchendo as semanas que ficaram com menos de 7 dias com os dias do mes anterior e subsequente
    if mes_analise in [1, 2, 4, 6, 8, 9, 11]:
        contador = 0
        while len(final_dias[0]) < 7:
            final_dias[0].insert(0, str(31 - contador))
            contador += 1
        contador = 0
        while len(final_dias[-1]) < 7:
            final_dias[-1].append(str(contador + 1))
            contador += 1
    elif mes_analise == 3 and ano_analise != 2020:
        contador = 0
        while len(final_dias[0]) < 7:
            final_dias[0].insert(0, str(28 - contador))
            contador += 1
        contador = 0
        while len(final_dias[-1]) < 7:
            final_dias[-1].append(str(contador + 1))
            contador += 1
    elif mes_analise == 3 and ano_analise == 2020:
        contador = 0
        while len(final_dias[0]) < 7:
            final_dias[0].insert(0, str(29 - contador))
            contador += 1
        contador = 0
        while len(final_dias[-1]) < 7:
            final_dias[-1].append(str(contador + 1))
            contador += 1
    elif mes_analise in [5, 7, 10, 12]:
        contador = 0
        while len(final_dias[0]) < 7:
            final_dias[0].insert(0, str(30 - contador))
            contador += 1
        contador = 0
        while len(final_dias[-1]) < 7:
            final_dias[-1].append(str(contador + 1))
            contador += 1

    # criando os labels das semanas
    y_label = []
    for i in range(len(final_dias)):
        y_label.append("Semana " + str(i + 1))

    # --------- CALENDAR HEATMAP PLOT ---------

    # plot do heatmap estilo calendario (com a quantidade de casos por dia)

    z = final_casos[::-1]

    x = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sabado", "Domingo"]
    y = y_label[::-1]

    z_text = final_dias[::-1]

    fig1 = ff.create_annotated_heatmap(
        z,
        x=x,
        y=y,
        annotation_text=z_text,
        colorscale=[
            [0.0, "rgb(235, 236, 240)"],  # valores negativos
            [0.00001, "rgb(255,255,255)"],
            [0.1, "rgb(255,245,240)"],
            [0.2, "rgb(252,201,180)"],
            [0.4, "rgb(251,136,104)"],
            [0.6, "rgb(242,67,49)"],
            [0.8, "rgb(187,19,25)"],
            [1.0, "rgb(115,2,23)"],
        ],
        showscale=True,
    )

    # titulo plot
    meses = [
        "Janeiro",
        "Feveireiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    ]
    mes_plot = meses[mes_analise - 1]
    if tipo == "NOVOS CASOS":
        fig1.update_layout(
            title_text="Casos Novos por dia - "
            + cidade.title()
            + " - "
            + mes_plot
            + " "
            + str(ano_analise),
            title_x=0.5,
        )
    else:
        fig1.update_layout(
            title_text="Casos Acumulados - "
            + cidade.title()
            + " - "
            + mes_plot
            + " "
            + str(ano_analise),
            title_x=0.5,
        )

    # fig1.update_layout({
    # 'plot_bgcolor': 'rgba(0,0,0,0)',
    # 'paper_bgcolor': 'rgba(0,0,0,0)'})

    return fig1

def plot_tributos_ipca(cidade="AFONSO CLAUDIO"):

    # Obtendo os dados
    # ==========================================
    # fonte: https://dados.es.gov.br/dataset/portal-da-transparencia-transferencias-para-municipios

    # juntando informacoes em 1 dataset
    # ==========================================
    transferencias = vups.datasets.transferencias()

    # Mudando os codigos municipais errados das tres cidades com homonimos
    # ====================================================================
    # * Boa Esperança (MG - 3107109) -> (ES - 3201001)
    # * Presidente Keneddy (TO - 1718402) -> (ES - 3204302)
    # * Viana (MA - 2112803) -> (ES - 3205101)

    for i in range(len(transferencias)):
        # Boa Esperança
        if transferencias.loc[i, "CodMunicipio"] == 3107109:
            transferencias.loc[i, "CodMunicipio"] = 3201001
        elif transferencias.loc[i, "CodMunicipio"] == 1718402:
            transferencias.loc[i, "CodMunicipio"] = 3204302
        elif transferencias.loc[i, "CodMunicipio"] == 2112803:
            transferencias.loc[i, "CodMunicipio"] = 3205101

    # Transformando colunas pertinentes em numbers
    # ====================================================================
    calumns_to_num = ["IcmsTotal", "Ipi", "Ipva", "FundoReducaoDesigualdades"]
    for x in calumns_to_num:
        transferencias[x] = [
            round(float(transferencias[x].iloc[i].replace(",", ".")), 2)
            for i in range(len(transferencias))
        ]

    # Criando coluna de totais
    # ====================================================================
    transferencias["TotalRepassado"] = (
        transferencias[calumns_to_num[0]]
        + transferencias[calumns_to_num[1]]
        + transferencias[calumns_to_num[2]]
        + transferencias[calumns_to_num[3]]
    )

    # Criando coluna com datatype
    # ====================================================================
    transferencias["Data"] = [
        datetime.datetime(
            transferencias["Ano"].iloc[i], transferencias["Mes"].iloc[i], 28
        )
        for i in range(len(transferencias))
    ]

    # Criando filtros
    # ====================================================================
    df = transferencias[transferencias["NomeMunicipio"] == cidade][
        ["TotalRepassado", "Data"]
    ]

    # Refazer de forma mais automatica -> aqui foi so para teste
    # ====================================================================
    list_date = list(df["Data"])
    ipca = [
        0.29,
        0.32,
        0.09,
        0.22,
        0.4,
        1.26,
        0.33,
        -0.09,
        0.48,
        0.45,
        -0.21,
        0.15,
        0.32,
        0.43,
        0.75,
        0.57,
        0.13,
        0.01,
        0.19,
        0.11,
        -0.04,
        0.1,
        0.51,
        1.15,
        0.21,
        0.25,
        0.07,
        -0.31,
        -0.38,
        0.26,
        0.36,
        0.24,
        0.64,
        0.86,
        0.89,
        1.35,
        0.25,
        0.86,
        0.93,
        0.31,
    ]
    dict_ipca = {}
    for idx, i in enumerate(list_date):
        dict_ipca[i] = ipca[idx]

    df["IPCA"] = ipca

    # Valores de comparacao - ipca
    # ====================================================================
    list_valor_comparacao = []
    for i in range(len(df)):
        if i == 0:
            list_valor_comparacao.append(df["TotalRepassado"].iloc[i])
        else:
            list_valor_comparacao.append(
                round(
                    list_valor_comparacao[i - 1] * (1 + df["IPCA"].iloc[i - 1] / 100), 2
                )
            )

    df["ValorComparacao"] = list_valor_comparacao

    # Plot
    # ====================================================================
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            y=df["TotalRepassado"], x=df["Data"], mode="lines", name="Repasse Estadual"
        )
    )
    fig.add_trace(
        go.Scatter(
            y=df["ValorComparacao"],
            x=df["Data"],
            mode="lines",
            name="Valor Ajustado por IPCA",
        )
    )

    return fig

def plot_comp_tributos_cidades(list_cidades=["ARACRUZ", "ANCHIETA", "CARIACICA", "GUARAPARI", "LINHARES", "PIUMA"]):
    # import pandas as pd
    # import datetime

    # Obtendo os dados
    # ==========================================
    # fonte: https://dados.es.gov.br/dataset/portal-da-transparencia-transferencias-para-municipios
    transferencias = vups.datasets.transferencias()

    # Mudando os codigos municipais errados das tres cidades com homonimos
    # ====================================================================
    # * Boa Esperança (MG - 3107109) -> (ES - 3201001)
    # * Presidente Keneddy (TO - 1718402) -> (ES - 3204302)
    # * Viana (MA - 2112803) -> (ES - 3205101)

    for i in range(len(transferencias)):
        # Boa Esperança
        if transferencias.loc[i, "CodMunicipio"] == 3107109:
            transferencias.loc[i, "CodMunicipio"] = 3201001
        elif transferencias.loc[i, "CodMunicipio"] == 1718402:
            transferencias.loc[i, "CodMunicipio"] = 3204302
        elif transferencias.loc[i, "CodMunicipio"] == 2112803:
            transferencias.loc[i, "CodMunicipio"] = 3205101

    # Transformando colunas pertinentes em numbers
    # ====================================================================
    calumns_to_num = ["IcmsTotal", "Ipi", "Ipva", "FundoReducaoDesigualdades"]
    for x in calumns_to_num:
        transferencias[x] = [
            round(float(transferencias[x].iloc[i].replace(",", ".")), 2)
            for i in range(len(transferencias))
        ]

    # Criando coluna de totais
    # ====================================================================
    transferencias["TotalRepassado"] = (
        transferencias[calumns_to_num[0]]
        + transferencias[calumns_to_num[1]]
        + transferencias[calumns_to_num[2]]
        + transferencias[calumns_to_num[3]]
    )

    # Criando coluna com datatype
    # ====================================================================
    transferencias["Data"] = [
        datetime.datetime(
            transferencias["Ano"].iloc[i], transferencias["Mes"].iloc[i], 28
        )
        for i in range(len(transferencias))
    ]

    # ##############################################################################################################################################################################
    COLUMNS = ["UF", "COD. UF", "COD. MUNIC", "NOME DO MUNICÍPIO", "POPULAÇÃO ESTIMADA"]
    
    populacao = vups.datasets.populacao(columns=COLUMNS)
    populacao_es = populacao[populacao["UF"] == "ES"]

    # ATENCAO ARRUMAR CODIGO PARA AS 3 CIDADES CITADAS
    # Criando coluna código
    ano = 2018
    for x in [populacao_es]:
        x["COD.GERAL"] = [
            int(str(int(x["COD. UF"].iloc[i]))
                + "00"
                + str(int(x["COD. MUNIC"].iloc[i]))
            )
            if len(str(int(x["COD. MUNIC"].iloc[i]))) < 4
            else int(
                str(int(x["COD. UF"].iloc[i])) + "0" + str(int(x["COD. MUNIC"].iloc[i]))
            )
            for i in range(len(x))
        ]
        x["ANO"] = ano
        ano += 1

    populacao_es["POPULAÇÃO ESTIMADA"] = [
        int(i.replace(",", "")) for i in populacao_es["POPULAÇÃO ESTIMADA"]
    ]

    boolean_series = transferencias["NomeMunicipio"].isin(list_cidades)
    df_repasse = transferencias[boolean_series][
        ["NomeMunicipio", "CodMunicipio", "TotalRepassado", "Data", "Ano"]
    ]

    codigos = []
    for i in list_cidades:
        cod = transferencias[transferencias["NomeMunicipio"] == i]["CodMunicipio"].iloc[
            0
        ]
        codigos.append(cod)

    boolean_series = populacao_es["COD.GERAL"].isin(codigos)
    df_pop = populacao_es[boolean_series][["COD.GERAL", "POPULAÇÃO ESTIMADA", "ANO"]]

    # merge
    df = df_repasse.merge(
        df_pop,
        how="inner",
        left_on=["CodMunicipio", "Ano"],
        right_on=["COD.GERAL", "ANO"],
    )
    df = df.drop(columns=["COD.GERAL"])

    # column arrec_percapita
    df["RepassPercapita"] = [
        round(df["TotalRepassado"].iloc[i] / df["POPULAÇÃO ESTIMADA"].iloc[0], 2)
        for i in range(len(df))
    ]

    # plot percapita
    fig = go.Figure()
    for i in range(len(list_cidades)):
        fig.add_trace(
            go.Scatter(
                y=df[df["NomeMunicipio"] == list_cidades[i]]["RepassPercapita"],
                x=df[df["NomeMunicipio"] == list_cidades[i]]["Data"],
                mode="lines",
                name=list_cidades[i],
            )
        )
    
    fig.update_layout({
        # 'plot_bgcolor': 'rgba(0,0,0,0)',
        # 'paper_bgcolor': 'rgba(0,0,0,0)'
        'plot_bgcolor': "#d8e3d3",
        'paper_bgcolor': 'rgba(0,0,0,0)',
    })

    return fig

def plot_comp_tributos_cidades_norm(list_cidades=["ARACRUZ", "ANCHIETA", "CARIACICA", "GUARAPARI", "LINHARES", "PIUMA"]):

    # Obtendo os dados
    # ==========================================
    # fonte: https://dados.es.gov.br/dataset/portal-da-transparencia-transferencias-para-municipios
    transferencias = vups.datasets.transferencias()

    # Mudando os codigos municipais errados das tres cidades com homonimos
    # ====================================================================
    # * Boa Esperança (MG - 3107109) -> (ES - 3201001)
    # * Presidente Keneddy (TO - 1718402) -> (ES - 3204302)
    # * Viana (MA - 2112803) -> (ES - 3205101)

    for i in range(len(transferencias)):
        # Boa Esperança
        if transferencias.loc[i, "CodMunicipio"] == 3107109:
            transferencias.loc[i, "CodMunicipio"] = 3201001
        elif transferencias.loc[i, "CodMunicipio"] == 1718402:
            transferencias.loc[i, "CodMunicipio"] = 3204302
        elif transferencias.loc[i, "CodMunicipio"] == 2112803:
            transferencias.loc[i, "CodMunicipio"] = 3205101

    # Transformando colunas pertinentes em numbers
    # ====================================================================
    calumns_to_num = ["IcmsTotal", "Ipi", "Ipva", "FundoReducaoDesigualdades"]
    for x in calumns_to_num:
        transferencias[x] = [
            round(float(transferencias[x].iloc[i].replace(",", ".")), 2)
            for i in range(len(transferencias))
        ]

    # Criando coluna de totais
    # ====================================================================
    transferencias["TotalRepassado"] = (
        transferencias[calumns_to_num[0]]
        + transferencias[calumns_to_num[1]]
        + transferencias[calumns_to_num[2]]
        + transferencias[calumns_to_num[3]]
    )

    # Criando coluna com datatype
    # ====================================================================
    transferencias["Data"] = [
        datetime.datetime(
            transferencias["Ano"].iloc[i], transferencias["Mes"].iloc[i], 28
        )
        for i in range(len(transferencias))
    ]

    # ##############################################################################################################################################################################
    COLUMNS = ["UF", "COD. UF", "COD. MUNIC", "NOME DO MUNICÍPIO", "POPULAÇÃO ESTIMADA"]
    populacao = vups.datasets.populacao(columns=COLUMNS)
    populacao_es = populacao[populacao["UF"] == "ES"]

    # ATENCAO ARRUMAR CODIGO PARA AS 3 CIDADES CITADAS
    # Criando coluna código
    ano = 2018
    for x in [populacao_es]:
        x["COD.GERAL"] = [
            int(
                str(int(x["COD. UF"].iloc[i]))
                + "00"
                + str(int(x["COD. MUNIC"].iloc[i]))
            )
            if len(str(int(x["COD. MUNIC"].iloc[i]))) < 4
            else int(
                str(int(x["COD. UF"].iloc[i])) + "0" + str(int(x["COD. MUNIC"].iloc[i]))
            )
            for i in range(len(x))
        ]
        x["ANO"] = ano
        ano += 1

    populacao_es["POPULAÇÃO ESTIMADA"] = [
        int(i.replace(",", "")) for i in populacao_es["POPULAÇÃO ESTIMADA"]
    ]

    boolean_series = transferencias["NomeMunicipio"].isin(list_cidades)
    df_repasse = transferencias[boolean_series][
        ["NomeMunicipio", "CodMunicipio", "TotalRepassado", "Data", "Ano"]
    ]

    codigos = []
    for i in list_cidades:
        cod = transferencias[transferencias["NomeMunicipio"] == i]["CodMunicipio"].iloc[
            0
        ]
        codigos.append(cod)

    boolean_series = populacao_es["COD.GERAL"].isin(codigos)
    df_pop = populacao_es[boolean_series][["COD.GERAL", "POPULAÇÃO ESTIMADA", "ANO"]]

    # merge
    df = df_repasse.merge(
        df_pop,
        how="inner",
        left_on=["CodMunicipio", "Ano"],
        right_on=["COD.GERAL", "ANO"],
    )
    df = df.drop(columns=["COD.GERAL"])

    # column arrec_percapita
    df["RepassPercapita"] = [
        round(df["TotalRepassado"].iloc[i] / df["POPULAÇÃO ESTIMADA"].iloc[i], 2)
        for i in range(len(df))
    ]

    # plot percapita normalizado
    fig = go.Figure()
    for i in range(len(list_cidades)):
        fig.add_trace(
            go.Scatter(
                y=df[df["NomeMunicipio"] == list_cidades[i]]["RepassPercapita"]
                / df[df["NomeMunicipio"] == list_cidades[i]]["RepassPercapita"].iloc[0]
                * 100,
                x=df[df["NomeMunicipio"] == list_cidades[i]]["Data"],
                mode="lines",
                name=list_cidades[i],
            )
        )

    fig.update_layout({
    # 'plot_bgcolor': 'rgba(0,0,0,0)',
    # 'paper_bgcolor': 'rgba(0,0,0,0)'
    'plot_bgcolor': "#d8e3d3",
    'paper_bgcolor': 'rgba(0,0,0,0)',
    })

    return fig

def plot_n_pessoas_por_sintomas():
    df = vups.datasets.microdados_bairros()
    df2 = vups.datasets.microdados()
    # 2
    df3 = df2[['Classificacao', 'Febre', 'DificuldadeRespiratoria', 'Tosse', 'Coriza', 'DorGarganta', 'Diarreia', 'Cefaleia',
        'ComorbidadePulmao', 'ComorbidadeCardio', 'ComorbidadeRenal', 'ComorbidadeDiabetes', 'ComorbidadeTabagismo',
        'ComorbidadeObesidade', 'DataObito']].dropna()
    # 3
    df3['Sintomas'] = df3[['Febre', 'DificuldadeRespiratoria', 'Tosse', 'Coriza', 'DorGarganta', 'Diarreia', 'Cefaleia',
        'ComorbidadePulmao', 'ComorbidadeCardio', 'ComorbidadeRenal', 'ComorbidadeDiabetes', 'ComorbidadeTabagismo',
        'ComorbidadeObesidade']].values.tolist()
    # 4
    sintomas = ['Febre', 'DificuldadeRespiratoria', 'Tosse', 'Coriza', 'DorGarganta', 'Diarreia', 'Cefaleia',
        'ComorbidadePulmao', 'ComorbidadeCardio', 'ComorbidadeRenal', 'ComorbidadeDiabetes', 'ComorbidadeTabagismo',
        'ComorbidadeObesidade']
    # 5
    df3['Sintomas'] = df3['Sintomas'].apply(lambda x: [True if item=='Sim' else False for item in x])
    #
    df3['Sintomas'] = df3['Sintomas'].apply(lambda x: list(itertools.compress(sintomas, x)))
    #
    df3['Qntd_sintomas'] = df3['Sintomas'].apply(lambda x: len(x))
    #
    confirmados = df3[df3['Classificacao']=='Confirmados']
    descartados = df3[df3['Classificacao']=='Descartados']
    suspeitos = df3[df3['Classificacao']=='Suspeitos']
    #
    confirmados['Assintomatico'] = confirmados.Sintomas.apply(lambda x:  'sim' if x==[] else 'nao')

    # 7
    dic = {}
    for i in confirmados['Sintomas'].apply(lambda x: x):
        for j in i:
            dic[j] = dic.get(j, 0) + 1

    # x = sintomas
    x = pd.Series(sorted(dic.values()))
    # y_saving = sintomas_prop
    y_saving = round(x / x.sum() * 100, ndigits=2)

    x = list(sorted(dic.keys()))

    fig = go.Figure()
    fig.add_trace(go.Bar(
            x=y_saving,
            y=x,
            marker=dict(
                color='rgba(50, 171, 96, 0.6)',
                line=dict(
                    color='rgba(50, 171, 96, 1.0)',
                    width=1),
            ),
            name='Sintomas mais frequentes',
            orientation='h',
        )
    )

    fig.update_layout(
        title={"text": "Sintomas mais frequentes", "x": 0.5},
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=True,
            domain=[0, 1],
        ),

        xaxis=dict(
            zeroline=False,
            showline=False,
            showticklabels=False,
            showgrid=True,
            domain=[0, 1],
        ),

        legend=dict(x=0.029, y=1.038, font_size=10),
        margin=dict(l=100, r=20, t=70, b=20),
        paper_bgcolor='rgb(248, 248, 255)',
        plot_bgcolor='rgb(248, 248, 255)',
    )

    annotations = []

    y_s = np.round(y_saving, decimals=2)

    # Adding labels
    for yd, xd in zip(y_s, x):

        # labeling the bar net worth
        annotations.append(dict(
            xref='x1', 
            yref='y1',
            y=xd, 
            x=yd + 3,
            text=str(yd) + '%',
            font=dict(
                family='Arial', 
                size=12, 
                color='rgb(50, 171, 96)'), 
            showarrow=False))

    fig.update_layout(annotations=annotations)

    return fig

def fn_resumo_microdados():
    md = vups.datasets.microdados()
    df_classificacao = pd.DataFrame(md.Classificacao.value_counts()).T
    df_periodo = pd.DataFrame(vups_utils.minMax(md['DataNotificacao'])).T
    
    resumo_microdados = {
        'n_obs': md.shape[0],
        'n_var': md.shape[1],
        'n_confirmados': df_classificacao.Confirmados[0],
        'n_descartados': df_classificacao.Descartados[0],
        'n_supeitos': df_classificacao.Suspeito[0],
        'n_obitos': md.DataObito.count(),
        'periodo_inicio': df_periodo['min'][0],
        'periodo_fim': df_periodo['max'][0]
    }

    return(resumo_microdados)

def fn_resumo():
    resumo = fn_resumo_microdados()
    texto1 = "Número de observações: {}".format(resumo.get('n_obs'))
    texto2 = "\nNúmero de variáveis: {}".format(resumo.get('n_var'))
    texto3 = "\nConfirmados: {}".format(resumo.get('n_confirmados'))
    texto4 = "\nDescartados: {}".format(resumo.get('n_descartados'))
    texto5 = "\nSuspeitos: {}".format(resumo.get('n_supeitos'))
    texto6 = "\nÓbitos: {}".format(resumo.get('n_obitos'))
    texto7 = "\nOs dados coletados compreendem um período de {:%d/%m/%Y} à {:%d/%m/%Y}.".format(resumo.get('periodo_inicio'), resumo.get('periodo_fim'))
    texto = texto1 + texto2 + texto3 + texto4 + texto5 + texto6 + texto7
    return(texto)