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

# from dask.distributed import Client, progress
# client = Client(n_workers=2, threads_per_worker=2, memory_limit='1GB')
# import dask
# import dask.dataframe as dd

# CONFIG #####################################################################
pd.options.display.float_format = '{:.2f}'.format


def get_data(
    warn_bad_lines=True, 
    nrows=None, 
    file=const.DATAFILE['FILENAME'], 
    sep=const.DATAFILE['SEP'],
    encoding=const.DATAFILE['ENCODING'],
    dtype=None):

    PATH = os.path.join(const.DATADIR + file)
    # pd.read_csv('data/dataframe_saved_v2.csv', parse_dates = ['Data'], usecols = list(range(0,6)))
    #TODO ANALISAR A IMPLEMENTAÇÃO DO PARSE DATE
    dataset = pd.read_csv(  PATH, 
                            sep=sep, 
                            error_bad_lines=False, 
                            encoding=encoding,
                            nrows=nrows,
                            warn_bad_lines=warn_bad_lines,
                            dtype=dtype)
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

    return plt.xlabel('# de pessoas com o sintoma', fontsize=12) 

def plot_bar():
    df = pd.DataFrame(
        {
            "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
            "Amount": [4, 1, 2, 2, 4, 5],
            "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
        }
    )
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
    fig = px.bar(df, x='Sexo', y='IdadeNaDataNotificacao')
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
                    df[c] = df[c].astype('float64')
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


class datasets:
    def microdados(nrows=None, dtype=None):
        return get_data(file='MICRODADOS.csv', nrows=nrows, sep=';', encoding='latin1', dtype=dtype)
    
    def microdados_bairros(nrows=None, dtype=None):
        return get_data(file='MICRODADOS_BAIRROS.csv', nrows=nrows, sep=',', encoding='latin1', dtype=dtype)

    def arrecadacao_1998_a_2001(nrows=None, dtype=None):
        return get_data(file='Arrecadacao_01-01-1998_a_31-12-2001.csv', nrows=nrows, sep=',', encoding='utf-8', dtype=dtype)
    
    def arrecadacao_2002_a_2005(nrows=None, dtype=None):
        return get_data(file='Arrecadacao_01-01-2002_a_31-12-2005.csv', nrows=nrows, sep=',', encoding='utf-8', dtype=dtype)
    
    def arrecadacao_2006_a_2009(nrows=None, dtype=None):
        return get_data(file='Arrecadacao_01-01-2006_a_31-12-2009.csv', nrows=nrows, sep=',', encoding='utf-8', dtype=dtype)
    
    def arrecadacao_2010_a_2013(nrows=None, dtype=None):
        return get_data(file='Arrecadacao_01-01-2010_a_31-12-2013.csv', nrows=nrows, sep=',', encoding='utf-8', dtype=dtype)
    
    def arrecadacao_2014_a_2017(nrows=None, dtype=None):
        return get_data(file='Arrecadacao_01-01-2014_a_31-12-2017.csv', nrows=nrows, sep=',', encoding='utf-8', dtype=dtype)
    
    def arrecadacao_2018_a_2020(nrows=None, dtype=None):
        return get_data(file='Arrecadacao_01-01-2018_a_09-12-2020.csv', nrows=nrows, sep=',', encoding='utf-8', dtype=dtype)
         
    def tipo_arrecadacao(nrows=None, dtype=None):
        return get_data(file='TipoArrecadacao.csv', nrows=nrows, sep=',', encoding='utf-8', dtype=dtype)