import os
import pandas as pd
import plotly.express as px
import sys
from matplotlib import pyplot as plt
from . import const
import json
import requests
import folium
import branca

# Path: onde estão armazenadas as classes e funções que serão utilizadas neste módulo:
#LIB_PATH = os.path.join('')
#sys.path.append(LIB_PATH)

def get_data(warn_bad_lines=True):
    PATH = os.path.join(const.DATADIR + const.DATAFILE)
    return pd.read_csv( PATH, 
                        sep=const.SEP, 
                        error_bad_lines=False, 
                        encoding='latin1',
                        warn_bad_lines=warn_bad_lines)

def plot_qtd_pessoas_x_sintomas(df):
    # Tratamento de dados
    from itertools import compress
    import matplotlib.pyplot as plt
    plt.style.use('seaborn-talk')
    
    df3 = df[['Classificacao', 'Febre', 'DificuldadeRespiratoria', 'Tosse', 'Coriza', 'DorGarganta', 'Diarreia', 'Cefaleia',
        'ComorbidadePulmao', 'ComorbidadeCardio', 'ComorbidadeRenal', 'ComorbidadeDiabetes', 'ComorbidadeTabagismo',
        'ComorbidadeObesidade', 'DataObito']].dropna()

    df3['Sintomas'] = df3[['Febre', 'DificuldadeRespiratoria', 'Tosse', 'Coriza', 'DorGarganta', 'Diarreia', 'Cefaleia',
        'ComorbidadePulmao', 'ComorbidadeCardio', 'ComorbidadeRenal', 'ComorbidadeDiabetes', 'ComorbidadeTabagismo',
        'ComorbidadeObesidade']].values.tolist()

    sintomas = ['Febre', 'DificuldadeRespiratoria', 'Tosse', 'Coriza', 'DorGarganta', 'Diarreia', 'Cefaleia',
        'ComorbidadePulmao', 'ComorbidadeCardio', 'ComorbidadeRenal', 'ComorbidadeDiabetes', 'ComorbidadeTabagismo',
        'ComorbidadeObesidade']

    df3['Sintomas'] = df3['Sintomas'].apply(lambda x: [True if item=='Sim' else False for item in x])

    df3['Sintomas'] = df3['Sintomas'].apply(lambda x: list(compress(sintomas, x)))

    df3['Qntd_sintomas'] = df3['Sintomas'].apply(lambda x: len(x))

    df3['Classificacao'].value_counts()

    # df2.iloc[df3[df3['Qntd_sintomas']==0].index].head()
    confirmados = df3[df3['Classificacao']=='Confirmados']
    descartados = df3[df3['Classificacao']=='Descartados']
    suspeitos = df3[df3['Classificacao']=='Suspeitos']
    #confirmados['DataObito'] = pd.to_datetime(confirmados['DataObito'])
    #descartados['DataObito'] = pd.to_datetime(descartados['DataObito'])
    #suspeitos['DataObito'] = pd.to_datetime(suspeitos['DataObito'])

    confirmados['Assintomatico'] = confirmados['Sintomas'].apply(lambda x:  'sim' if x==[] else 'nao')

    dic = {}
    
    for i in confirmados['Sintomas'].apply(lambda x: x):
        for j in i:
            dic[j] = dic.get(j, 0) + 1
    
    sintomas = pd.Series(dic)
    sintomas_prop = round(sintomas / sintomas.sum() * 100, ndigits=2)
    sintomas_prop.sort_values()
    
    pd.DataFrame({'Qntd': sintomas}).sort_values('Qntd').plot.barh(legend=False, figsize=(12,10))
    plt.xlabel('# de pessoas com o sintoma', fontsize=12)
    return 

def plot_bar(df):
    df = ''
    return

def plot_bar(df):
    return px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

def generate_table(df, max_rows=10):
    import dash_html_components as html

    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in df.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns
            ]) for i in range(min(len(df), max_rows))
        ])
    ]
)

def plot_sexo_idade(df):
    return px.bar(df, x='Sexo', y='IdadeNaDataNotificacao')

def plot_sexo_idade2(df):
    return plt.bar(df['Sexo'], df['IdadeNaDataNotificacao'])


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

    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                    size="pop", color="continent", hover_name="country",
                    log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig


def plot_map_folium():
    url = (
        "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data"
    )
    county_data = f"{url}/us_county_data.csv"
    county_geo = f"{url}/us_counties_20m_topo.json"


    df = pd.read_csv(county_data, na_values=[" "])

    colorscale = branca.colormap.linear.YlOrRd_09.scale(0, 50e3)
    employed_series = df.set_index("FIPS_Code")["Employed_2011"]


    def style_function(feature):
        employed = employed_series.get(int(feature["id"][-5:]), None)
        return {
            "fillOpacity": 0.5,
            "weight": 0,
            "fillColor": "#black" if employed is None else colorscale(employed),
        }


    m = folium.Map(location=[48, -102], tiles="cartodbpositron", zoom_start=3)

    folium.TopoJson(
        json.loads(requests.get(county_geo).text),
        "objects.us_counties_20m",
        style_function=style_function,
    ).add_to(m)
    
    return m