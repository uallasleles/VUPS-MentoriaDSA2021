# -*- coding: utf-8 -*-
"""
Run this app with `python app.py` and
visit http://127.0.0.1:8050/ in your web browser.
"""

# Imports
# ============================================================================
import locale
import time

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

import pandas as pd
import numpy as np
from lib import vups

from sklearn import datasets
from sklearn.cluster import KMeans

import warnings
warnings.filterwarnings("ignore")

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

# Objeto Dash
# ============================================================================
app = dash.Dash(
    __name__,
    external_stylesheets = CSS,
    suppress_callback_exceptions = True,
    meta_tags = [{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])

server = app.server

# Dados
# ============================================================================
df = vups.get_data()[:100]
iris_raw = datasets.load_iris()
iris = pd.DataFrame(iris_raw["data"], columns=iris_raw["feature_names"])

# Figuras
# ============================================================================
#fig1 = vups.Plots.plot_scatter(df)

# Mapas
# ============================================================================ 
mapa = vups.plot_map_folium(),


##### Home Page #####

# Conteúdo
# ============================================================================

##### Barra Lateral #####

header = dbc.Row(
    html.H1('Dashboard Esboço')
)

# Componente sidebar
sidebar1 = html.Div(
    [      
        html.H4("Dashboard Analítico", className = "text-white p-1", style = {'marginTop':'1rem'}),
        html.Hr(style = {"borderTop": "1px dotted white"}),
        dbc.Nav(
            [
                dbc.NavLink("Visão Geral", href="/", active="exact"),
                dbc.NavLink("Análise Financeira", href="/pagina-1", active="exact"),
                dbc.NavLink("Conclusão", href="/pagina-2", active="exact"),
            ],
            vertical = True,
            pills = True,
            style = {'fontSize':16}
        ),
        html.P(u"Versão 1.0", className = 'fixed-bottom text-white p-2'),

    ],
    className = 'bg-dark',

    style = {"position": "fixed",
             "top": 0,
             "left": 0,
             "bottom": 0,
             "width": "14rem",
             "padding": "1rem",},
)

sidebar2 = html.Div(
    [
        html.Div(
            [
                html.Img(src=PLOTLY_LOGO, style={"width": "3rem"}),
                html.H2("VUPS"),
            ],
            className="sidebar-header",
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.I(className="fas fa-home mr-2"), 
                        html.Span("Home")
                    ], 
                    href="/", 
                    active="exact"
                ),

                dbc.NavLink(
                    [
                        html.I(className="fas fa-chart-area mr-2"),
                        html.Span("Análises"),
                    ],
                    href="/page-1", 
                    active="exact",
                ),

                dbc.NavLink(
                    [
                        html.I(className="fas fa-hand-holding-usd mr-2"),
                        html.Span("Informações"),
                    ],
                    href="/page-2",
                    active="exact",
                ),

                dbc.NavLink(
                    [
                        html.I(className="fas fa-toolbox mr-2"),
                        html.Span("Utils"),
                    ],
                    href="/page-3",
                    active="exact",
                ),

                dbc.NavLink(
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
    className="content",
    )

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
                        {"label": col, "value": col} for col in iris.columns
                    ],
                    value="sepal length (cm)",
                ),
            ]
        ),
        dbc.FormGroup(
            [
                dbc.Label("Y variable"),
                dcc.Dropdown(
                    id="y-variable",
                    options=[
                        {"label": col, "value": col} for col in iris.columns
                    ],
                    value="sepal width (cm)",
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

iris_container = dbc.Container(
    [
        html.H1("Iris k-means clustering"),
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
kpis = html.Div([
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
        kpis,
        html.Br(),
        dt.DataTable(
            id='table',
            columns=[{'name': i, 'id': i} for i in df.columns],
            data= df.to_dict('records'),
            style_table={'overflowX': 'auto'},
            style_cell={
                'height': 'auto',
                'textOverflow': 'ellipsis',
                # all three widths are needed
                'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                'whiteSpace': 'normal'
            },
            fixed_rows={ 'headers': True, 'data': 0 },
            style_data_conditional=[
                {'if': {'column_id': 'index'},
                'width': '50px'},
                {'if': {'column_id': 'Year'},
                'width': '50px'},
                {'if': {'column_id': 'Country'},
                'width': '100px'},
                {'if': {'column_id': 'Continent'},
                'width': '70px'},
                {'if': {'column_id': 'Emission'},
                'width': '75px'},
            ],
            virtualization=True,
            page_action='none',
            # tooltip_data=[
            #     {
            #         column: {'value': str(value), 'type': 'markdown'}
            #         for column, value in row.items()
            #     } for row in df.to_dict('records')
            # ],
            # tooltip_duration=None,
        )
    ]
)

container_template = dbc.Container([
    dbc.Card([
        dbc.CardHeader(''),
        dbc.CardBody(''),
    ])
])

selfservice_components = dbc.Container(
    [
        html.H2('Self-service para componentes bootstrap.'),

        # KPIs
        html.Div([
                dbc.Row(
                    [
                        dbc.Col(dbc.Card(card_content, color="light"), width=6, lg=3),
                        dbc.Col(dbc.Card(card_content, color="dark", inverse=True), width=6, lg=3),
                        dbc.Col(dbc.Card(card_content, color="info", inverse=True), width=6, lg=3),
                        dbc.Col(dbc.Card(card_content, color="success", inverse=True), width=6, lg=3),
                    ]
                )
        ]),

        # Alerts
        dbc.Card([
            dbc.CardBody([
                html.H1('Alert'),
                html.Div(
                    [
                        dbc.Alert("This is a primary alert", color="primary"),
                        dbc.Alert("This is a secondary alert", color="secondary"),
                        dbc.Alert("This is a success alert! Well done!", color="success"),
                        dbc.Alert("This is a warning alert... be careful...", color="warning"),
                        dbc.Alert("This is a danger alert. Scary!", color="danger"),
                        dbc.Alert("This is an info alert. Good to know!", color="info"),
                        dbc.Alert("This is a light alert", color="light"),
                        dbc.Alert("This is a dark alert", color="dark"),
                    ]
                )
            ])
        ]),

        html.Br(),

        # Alert Link
        dbc.Card([
            dbc.CardBody([
                html.H1('Alert Link'),
                html.Div(
                    [
                        dbc.Alert(
                            [
                                "This is a primary alert with an ",
                                html.A("example link", href="#", className="alert-link"),
                            ],
                            color="primary",
                        ),
                        dbc.Alert(
                            [
                                "This is a danger alert with an ",
                                html.A("example link", href="#", className="alert-link"),
                            ],
                            color="danger",
                        )
                    ]
                )
            ])
        ]),

        html.Hr(),
        dcc.Graph(figure=mapa),        
    ]
)

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
app.layout = html.Div([
    dcc.Location(id="url"), 
    sidebar2, 
    content])

# Funções
# ============================================================================

# ----------------------------------------------------------------------------
@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return summary
    elif pathname == "/page-1":
        return tab_control
    elif pathname == "/page-2":
        return iris_container
    elif pathname == "/page-3":
        return selfservice_components
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

# ----------------------------------------------------------------------------
@app.callback(
    Output("cluster-graph", "figure"),
    [
        Input("x-variable", "value"),
        Input("y-variable", "value"),
        Input("cluster-count", "value"),
    ],
)
def make_graph(x, y, n_clusters):
    # minimal input validation, make sure there's at least one cluster
    km = KMeans(n_clusters=max(n_clusters, 1))
    df = iris.loc[:, [x, y]]
    km.fit(df.values)
    df["cluster"] = km.labels_

    centers = km.cluster_centers_

    data = [
        go.Scatter(
            x=df.loc[df.cluster == c, x],
            y=df.loc[df.cluster == c, y],
            mode="markers",
            marker={"size": 8},
            name="Cluster {}".format(c),
        )
        for c in range(n_clusters)
    ]

    data.append(
        go.Scatter(
            x=centers[:, 0],
            y=centers[:, 1],
            mode="markers",
            marker={"color": "#000", "size": 12, "symbol": "diamond"},
            name="Cluster centers",
        )
    )

    layout = {"xaxis": {"title": x}, "yaxis": {"title": y}}
    
    return go.Figure(data=data, layout=layout)

# ----------------------------------------------------------------------------
# make sure that x and y values can't be the same variable
def filter_options(v):
    """Disable option v"""
    return [
        {"label": col, "value": col, "disabled": col == v}
        for col in iris.columns
    ]

# functionality is the same for both dropdowns, so we reuse filter_options
app.callback(Output("x-variable", "options"), [Input("y-variable", "value")])(
    filter_options
)
app.callback(Output("y-variable", "options"), [Input("x-variable", "value")])(
    filter_options
)

# ----------------------------------------------------------------------------
@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"), Input("store", "data")],
)
def render_tab_content(active_tab, data):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab and data is not None:
        if active_tab == "scatter":
            return dcc.Graph(figure=data["scatter"])
        elif active_tab == "histogram":
            return dbc.Container([
                dbc.Row([
                    dbc.Col(
                        dbc.Card([
                            dbc.CardHeader('Histograma 1'),
                            dbc.CardBody([
                                dcc.Graph(figure=data["hist_1"]),
                            ]),
                        ]),
                        width=6
                    ),
                    dbc.Col(
                        dbc.Card([
                            dbc.CardHeader('Histograma 2'),
                            dbc.CardBody([
                                dcc.Graph(figure=data["hist_2"]),
                            ]),
                        ]),
                        width=6
                    ),
                ]),
            ])
    return "No tab selected"

# ----------------------------------------------------------------------------
@app.callback(Output("store", "data"), [Input("button", "n_clicks")])
def generate_graphs(n):
    """
    This callback generates three simple graphs from random data.
    """
    if not n:
        # generate empty graphs when app loads
        return {k: go.Figure(data=[]) for k in ["scatter", "hist_1", "hist_2"]}

    # simulate expensive graph generation process
    time.sleep(2)

    # generate 100 multivariate normal samples
    data = np.random.multivariate_normal([0, 0], [[1, 0.5], [0.5, 1]], 100)

    scatter = go.Figure(
        data=[go.Scatter(x=data[:, 0], y=data[:, 1], mode="markers")]
    )
    hist_1 = go.Figure(data=[go.Histogram(x=data[:, 0])])
    hist_2 = go.Figure(data=[go.Histogram(x=data[:, 1])])

    # save figures in a dictionary for sending to the dcc.Store
    return {"scatter": scatter, "hist_1": hist_1, "hist_2": hist_2}

# ----------------------------------------------------------------------------
@app.callback(
    [Output("progress", "value"), Output("progress", "children")],
    [Input("progress-interval", "n_intervals")],
)
def update_progress(n):
    # check progress of some background process, in this example we'll just
    # use n_intervals constrained to be in 0-100
    progress = min(n % 110, 100)
    # only add text after 5% progress to ensure text isn't squashed too much
    return progress, f"{progress} %" if progress >= 5 else ""


# ============================================================================
if __name__ == '__main__':
    # ## Acesso em local network
    # app.run_server(debug=False, port=8080, host="0.0.0.0")
    
    # ## Debug
    app.run_server(debug=True, port=8080, host="0.0.0.0")

    # ## Para não fazer o refresh automático, use:
    # app.run_server(dev_tools_hot_reload=False)