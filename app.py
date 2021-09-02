# -*- coding: utf-8 -*-
"""
Run this app with `python app.py` and
visit http://127.0.0.1:8050/ in your web browser.
"""

# Imports
# ============================================================================
import locale
import time
from typing import Container
from branca.element import IFrame

import dash
from dash_bootstrap_components._components import CardHeader
import dash_core_components as dcc
from dash_core_components.Dropdown import Dropdown
from dash_core_components.Graph import Graph
from dash_core_components.Input import Input
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash_html_components.Br import Br
from dash_html_components.Label import Label
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import dash_table as dt
import plotly.express as px

import pandas as pd
import numpy as np
from lib import vups

from sklearn import datasets
from sklearn.cluster import KMeans

import warnings
warnings.filterwarnings("ignore")


# ============================================================================
# Endereço HOSTNAME (IP local)
# ============================================================================
import socket
HOST = socket.gethostbyname(socket.gethostname())


# ============================================================================
# Dados
# ============================================================================
df = vups.get_data(nrows=1000)

# ============================================================================
# Styles
# ============================================================================
# Folha de Estilo CSS externa personalizada
FA = "https://use.fontawesome.com/releases/v5.15.1/css/all.css"
PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

CSS = [dbc.themes.YETI, FA]
#CSS = [dbc.themes.SANDSTONE, FA]

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
#    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
#    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# Tabs Style
tab_style = {'border': '1px solid black', 'padding': '6px', 'fontWeight': 'bold', 'margin':'0.5rem',}
tab_selected_style = {'border': '1px solid white', 'background-color': '#3298CC', 'padding': '6px', 'margin':'0.5rem'}

# Formatar os números decimais
locale.setlocale(locale.LC_ALL, '')

# ============================================================================
# Objeto Dash
# ============================================================================
app = dash.Dash(
    __name__,
    external_stylesheets = CSS,
    suppress_callback_exceptions = True,
    meta_tags = [{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])

server = app.server


# ============================================================================
# Figuras
# ============================================================================
fig1 = vups.plot_year_taxs()
fig2 = vups.plot_tributos_ipca()
fig3 = vups.plot_comp_tributos_cidades()
fig4 = vups.plot_comp_tributos_cidades_norm()
#fig2 = vups.plot_sexo_idade(df)
#fig3 = vups.plot_qtd_pessoas_x_sintomas(df)


# ============================================================================
# Mapas
# ============================================================================ 
# vups.plot_map_folium(),

# ============================================================================
# Home Page
# ============================================================================

##### Título #####
header = dbc.Row(html.H1('Boletim de Arrecadação dos Tributos Estaduais'))

##### Barra Lateral #####
sidebar = html.Div(
    [
        html.Div( # LOGO -----------------------------------------------------
            [
                html.Img(src=PLOTLY_LOGO, style={"width": "3rem"}),
                html.H2("VUPS"),
            ],
            className="sidebar-header",
        ),

        html.Hr(),
        
        dbc.Nav( # MENUS -----------------------------------------------------
            [
                dbc.NavLink( # HOME ------------------------------------------
                    [
                        html.I(className="fas fa-home mr-2"), 
                        html.Span("Home")
                    ], 
                    href="/", 
                    active="exact",
                ),

                dbc.NavLink( # ANÁLISES --------------------------------------
                    [
                        html.I(className="fas fa-chart-area mr-2"),
                        html.Span("Análises"),
                    ],
                    href="/page-1", 
                    active="exact",
                ),

                dbc.NavLink( # ANÁLISES --------------------------------------
                    [
                        html.I(className="fas fa-hand-holding-usd mr-2"),
                        html.Span("Informações"),
                    ],
                    href="/page-2",
                    active="exact",
                ),

                dbc.NavLink( # ANÁLISES --------------------------------------
                    [
                        html.I(className="fas fa-toolbox mr-2"),
                        html.Span("Utils"),
                    ],
                    href="/page-3",
                    active="exact",
                ),

                dbc.NavLink( # ANÁLISES --------------------------------------
                    [
                        html.I(className="fas fa-cog mr-2"),
                        html.Span("Setup"),
                    ],
                    href="/page-4",
                    active="exact",
                ),                

            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar",
    style=SIDEBAR_STYLE,
)


content = html.Div(
    id="page-content", 
    className="content")

tab_control = dbc.Container(
    [
        dcc.Store(id="store"),
        html.H1("Dynamically rendered tab content"),
        
        html.Hr(),

        dbc.Button(
            "Regenerate graphs",
            color="primary",
            block=True,
            id="button",
            className="mb-3",
        ),

        dbc.Tabs(
            [
                dbc.Tab(label="COVID", tab_id="scatter"),
                dbc.Tab(label="TRIBUTOS", tab_id="histogram"),
            ],
            id="tabs",
            active_tab="scatter",
        ),
        html.Div(id="tab-content", className="p-4"),
    ]
)

controls = dbc.Card(
    [
        dbc.FormGroup(
            [
                dbc.Label("X variable"),
                dcc.Dropdown(
                    id="x-variable",
                    options=[
                        {"label": col, "value": col} for col in df.columns
                    ],
                    value="",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Y variable"),
                dcc.Dropdown(
                    id="y-variable",
                    options=[
                        {"label": col, "value": col} for col in df.columns
                    ],
                    value="",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Cluster count"),
                dbc.Input(id="cluster-count", type="number", value=3),
            ]
        ),
    ],
    body=True,
)

container1 = dbc.Container(
    [
        html.H1("Tributos"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=4),
                dbc.Col(dcc.Graph(id="cluster-graph"), md=8),
            ],
            align="center",
        ),
    ],
    fluid=True,
)

card_content = [
    dbc.CardHeader("Card header"),
    dbc.CardBody(
        [
            html.H5("Card title", className="card-title"),
            html.P(
                "Aqui pode ficar um KPI.",
                className="card-text",
            ),
        ]
    ),
]

# KPIs
kpis_widget = html.Div([
        dbc.Row(
            [
                dbc.Col(dbc.Card(card_content, color="light"), width=6, lg=3),
                dbc.Col(dbc.Card(card_content, color="dark", inverse=True), width=6, lg=3),
                dbc.Col(dbc.Card(card_content, color="info", inverse=True), width=6, lg=3),
                dbc.Col(dbc.Card(card_content, color="success", inverse=True), width=6, lg=3),
            ]
        )
])

summary = dbc.Container(
    [
        header,
        html.Hr(),
        kpis_widget,
        html.Br(),
        dbc.Row([
            dbc.Col(dcc.Graph(id='fig1', figure=fig1)),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='fig2', figure=fig2)),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='fig3', figure=fig3)),
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='fig4', figure=fig4)),
        ]),
        dbc.Row([
            dbc.Col(dcc.Markdown('''
            ### INSIGHTS
            Em Janeiro de 2020, Piuma entra no Fundo de Redução de Desigualdades, o que deveria fazer com que seus recursos aumentassem, entretanto, o repasse do ICMS cai mais da metade, fazendo com que seus recursos diminuam consideravelmente.
            
            Também em Janeiro de 2020, Itapemirim passa a receber recursos do Fundo de Redução de Desigualdades, entretanto, deferentemente de Piuma, o valor de repasse de ICMS aumenta em 40% na mesma data, fazendo com que um salto em seus recursos aconteçam a partir de 2020.
            ''')),
        ]),
    ]
)

container_template = dbc.Container([
    dbc.Card([
        dbc.CardHeader(''),
        dbc.CardBody(''),
    ])
])


# selfservice_components = dbc.Container(
#     [
#         html.H2('Self-service para componentes bootstrap.'),

#         # KPIs
#         html.Div([
#                 dbc.Row(
#                     [
#                         dbc.Col(dbc.Card(card_content, color="light"), width=6, lg=3),
#                         dbc.Col(dbc.Card(card_content, color="dark", inverse=True), width=6, lg=3),
#                         dbc.Col(dbc.Card(card_content, color="info", inverse=True), width=6, lg=3),
#                         dbc.Col(dbc.Card(card_content, color="success", inverse=True), width=6, lg=3),
#                     ]
#                 )
#         ]),

#         # Alerts
#         dbc.Card([
#             dbc.CardBody([
#                 html.H1('Alert'),
#                 html.Div(
#                     [
#                         dbc.Alert("This is a primary alert", color="primary"),
#                         dbc.Alert("This is a secondary alert", color="secondary"),
#                         dbc.Alert("This is a success alert! Well done!", color="success"),
#                         dbc.Alert("This is a warning alert... be careful...", color="warning"),
#                         dbc.Alert("This is a danger alert. Scary!", color="danger"),
#                         dbc.Alert("This is an info alert. Good to know!", color="info"),
#                         dbc.Alert("This is a light alert", color="light"),
#                         dbc.Alert("This is a dark alert", color="dark"),
#                     ]
#                 )
#             ])
#         ]),

#         html.Br(),

#         # Alert Link
#         dbc.Card([
#             dbc.CardBody([
#                 html.H1('Alert Link'),
#                 html.Div(
#                     [
#                         dbc.Alert(
#                             [
#                                 "This is a primary alert with an ",
#                                 html.A("example link", href="#", className="alert-link"),
#                             ],
#                             color="primary",
#                         ),
#                         dbc.Alert(
#                             [
#                                 "This is a danger alert with an ",
#                                 html.A("example link", href="#", className="alert-link"),
#                             ],
#                             color="danger",
#                         )
#                     ]
#                 )
#             ])
#         ]),

#         html.Hr(),
#         html.Iframe(id="Mapa", srcDoc=open('map.html', 'r').read(), width='100%', height='600')
#     ]
# )

setup_page = dbc.Container([
    dbc.Card(
        dbc.CardFooter(
            html.Div(
                [
                    dcc.Interval(id="progress-interval", n_intervals=0, interval=500),
                    dbc.Progress(id="progress"),
                ]
            )
        )
    ),
])


##### Layout Geral #####
# ============================================================================
app.layout = html.Div(
    [
        dcc.Location(id="url"), 
        sidebar,
        content,
    ]
)


# Funções
# ============================================================================

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return summary
    elif pathname == "/page-1":
        return tab_control
    elif pathname == "/page-2":
        return container1
    elif pathname == "/page-4":
        return setup_page
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


# ============================================================================
if __name__ == '__main__':
    # ## Acesso em local network
    # app.run_server(debug=False, port=8080, host="0.0.0.0")

    # ## AWS
    app.run_server(debug=True, host=HOST)

    # ## Debug
    # app.run_server(debug=True, port=8080, host=HOST)

    # ## Para não fazer o refresh automático, use:
    # app.run_server(dev_tools_hot_reload=False)