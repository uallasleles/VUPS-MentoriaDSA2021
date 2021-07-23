# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from lib import vups

# Styles
# ============================================================================
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# Objeto Dash
# ============================================================================
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Dados
df = vups.get_data(test=True)

# Figuras
# ============================================================================
fig1 = vups.plot_test(df)
fig1.update_layout(
    plot_bgcolor = colors['background'],
    paper_bgcolor = colors['background'],
    font_color = colors['text']
)

#fig2 = vups.plot_qtd_pessoas_x_sintomas(df)

# Layout
# ============================================================================
app.layout = html.Div(
    style = {'backgroundColor': colors['background']},
    children=[
        html.H1(
            children = 'Título Dashboard',
            style = {
                'textAlign': 'center',
                'color': colors['text']
            }
        ),
        html.Div(
            children='''Dash: Um framework de aplicação web para Python.''',
            style = {
                'textAlign': 'center',
                'color': colors['text']
            }
        ),

        dcc.Graph(
            id = 'Gráfico 1',
            figure = fig1
        )
    ]
)


# ============================================================================
if __name__ == '__main__':
    app.run_server(debug=True)