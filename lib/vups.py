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

from dask.distributed import Client, progress
client = Client(n_workers=2, threads_per_worker=2, memory_limit='1GB')
import dask
import dask.dataframe as dd

# Path: onde estão armazenadas as classes e funções que serão utilizadas neste módulo:
#LIB_PATH = os.path.join('')
#sys.path.append(LIB_PATH)

def get_data(warn_bad_lines=True, nrows=None):
    PATH = os.path.join(const.DATADIR + const.DATAFILE['FILENAME'])
    # pd.read_csv('data/dataframe_saved_v2.csv', parse_dates = ['Data'], usecols = list(range(0,6)))
    # ANALISAR A IMPLEMENTAÇÃO DO PARSE DATE
    dataset = dd.read_csv( PATH, 
                        sep=const.DATAFILE['SEP'], 
                        error_bad_lines=False, 
                        encoding=const.DATAFILE['ENCODING'],
                        nrows=nrows,
                        warn_bad_lines=warn_bad_lines)
    dataset = dtype_transform(dataset)
    return dataset

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
    map = folium.Map(location=[-16.3722412, -39.5757040], zoom_start=10)
    map.save('map.html')

def fn_date_cols(df):
    import re
    date_patern1 = re.compile(r'(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])')
    date_patern2 = re.compile(r'(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d')
    
    lst_cols = []

    for n in list(df.columns):
        i = df.columns.get_loc(n) # ÍNDICE DA COLUNA
        v = df.iloc[0, i]         # VALOR NA LINHA ZERO
        try:
            if (re.search(date_patern1, v) is not None) or (re.search(date_patern2, v) is not None):
                lst_cols.append(n)
        except:
            pass
            
    return lst_cols

def fn_number_cols(df):
    lst_cols = []
    
    for n in list(df.columns):
        i = df.columns.get_loc(n)   # ÍNDICE DA COLUNA
        v = df.iloc[1, i]           # VALOR NA LINHA ZERO
        try:
            if float(n):            # SE PASSAR, É UM NÚMERO (Tenta converter para float)
                lst_cols.append(n)
        except:
            pass
            
    return lst_cols

def dtype_transform(df):

    date_cols = fn_date_cols(df)
    for c in date_cols:
        try:
            df[c] = df[c].astype('datetime64[ns]')
        except:
            pass

    cat_cols = list(df.select_dtypes(include='object').columns)
    for c in cat_cols:
        try:
            df[c] = df[c].astype('category')
        except:
            pass

    numeric_cols = fn_number_cols(df)
    for c in numeric_cols:
        i = df.columns.get_loc(c) # ÍNDICE DA COLUNA
        v = df.iloc[0, i]         # VALOR NA LINHA ZERO
        try:
            if float(v) and not v.isdecimal():
                try:
                    df[c] = df[c].astype('float')
                except:
                    pass
            else: # isdecimal() - SE NÃO PASSAR, É UM NÚMERO INTEIRO (Verifica se todos os caracteres no Unicode são decimais)
                try: 
                    df[c] = df[c].astype('int64')
                except:
                    pass
        except:
            pass

    return df