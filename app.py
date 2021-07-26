# -*- coding: utf-8 -*-

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
import dash_core_components as dcc
from dash_core_components.Dropdown import Dropdown
from dash_core_components.Input import Input
import dash_html_components as html
from dash_html_components.Label import Label
import pandas as pd
from lib import vups
from dash.dependencies import Input, Output


# Styles
# ============================================================================
# Folha de Estilo CSS externa personalizada
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# Valores para customização inline dos componentes através da propriedade Style={}
colors = {
    'background': '#dbf6ff',
    'text': '#7FDBFF'
}

# Objeto Dash
# ============================================================================
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Dados
df = vups.get_data(test=True)
df1 = vups.get_data()

# Figuras
# ============================================================================
# fig1 = vups.plot_test(df)
# fig1.update_layout(
#    plot_bgcolor = colors['background'],
#    paper_bgcolor = colors['background'],
#    font_color = colors['text']
# )

#fig2 = vups.plot_qtd_pessoas_x_sintomas(df)

# Markdown
# ============================================================================
markdown_text = '''Embora o Dash exponha HTML por meio da biblioteca dash_html_components, pode ser entediante escrever sua cópia em HTML.   
Para escrever blocos de texto, você pode usar o componente Markdown na biblioteca dash_core_components.  
Aplicativos Dash podem ser escritos em Markdown. Dash usa a especificação CommonMark de Markdown.
'''

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
        html.Div(
            style={'columnCount': 2},
            children=[
                html.Label('Dropdown'),
                dcc.Dropdown(
                    options=[
                        {'label': u'Eunápolis', 'value': 'EU'},
                        {'label': 'Itabela', 'value': 'GT'},
                        {'label': 'Guaratinga', 'value': 'IB'},
                    ],
                    value='EU'
                ),

                html.Label('Multi-Select Dropdown'),
                dcc.Dropdown(
                    options=[
                        {'label': u'Eunápolis', 'value': 'EU'},
                        {'label': 'Itabela', 'value': 'GT'},
                        {'label': 'Guaratinga', 'value': 'IB'},
                    ],
                    value=['EU', 'GT'],
                    multi=True
                ),

                html.Label('Radio Items'),
                dcc.RadioItems(
                    options=[
                        {'label': u'Eunápolis', 'value': 'EU'},
                        {'label': 'Itabela', 'value': 'GT'},
                        {'label': 'Guaratinga', 'value': 'IB'},
                    ],
                    value='EU'
                ),

                html.Label('Checkboxes'),
                dcc.Checklist(
                    options=[
                        {'label': u'Eunápolis', 'value': 'EU'},
                        {'label': 'Itabela', 'value': 'GT'},
                        {'label': 'Guaratinga', 'value': 'IB'},
                    ],
                    value=['EU', 'GT'],
                ),

                html.Label('Text Input'),
                dcc.Input(value='Uallas Leles', type='text'),

                vups.generate_table(df),

                dcc.Markdown(children=markdown_text),

                dcc.Graph(
                    id = 'graph_1'
                ),
                
                html.Label('Ano'),
                dcc.Slider(
                    id='year-slider',
                    min=df['year'].min(),
                    max=df['year'].max(),
                    value=df['year'].min(),
                    marks={str(year): str(year) for year in df['year'].unique()},
                    step=None
                ),
            ]
        ),

        html.H6("Change the value in the text box to see callbacks in action!"),
        html.Div(["Input: ",
                dcc.Input(id='my-input', value='initial value', type='text')]),
        html.Br(),
        html.Div(id='my-output'),
    ]
)


@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value'))
def update_output_div(input_value):
    return 'Output: {}'.format(input_value)

@app.callback(
    Output(component_id='graph_1', component_property='figure'),
    Input(component_id='year-slider', component_property='value'))
def update_figure(selected_year):
    return vups.plot_scatter(df, selected_year)


# ============================================================================
if __name__ == '__main__':
    app.run_server(debug=True)