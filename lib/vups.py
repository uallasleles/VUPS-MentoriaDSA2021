import os
import pandas as pd
from pandas.io.formats.format import CategoricalFormatter
import plotly.express as px
import sys
from matplotlib import pyplot as plt
from . import const
import json
import requests
import folium
import branca
import datetime

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

tax_cat_col = {
    # 'ano_arrecadacao': 'category', 
    # 'mes_arrecadacao': 'category', 
    # 'co_tipo_arrecadacao': 'category'
}

class datasets:
    def microdados(nrows=None, dtype=None):
        return get_data(file='MICRODADOS.csv', nrows=nrows, sep=';', encoding='latin1', dtype=dtype)
    
    def microdados_bairros(nrows=None, dtype=None):
        return get_data(file='MICRODADOS_BAIRROS.csv', nrows=nrows, sep=',', encoding='latin1', dtype=dtype)

    def arrecadacao_1998_a_2001(nrows=None, dtype=None):
        return get_data(file='Arrecadacao_01-01-1998_a_31-12-2001.csv', nrows=nrows, sep=',', encoding='utf-8', dtype=tax_cat_col)
    
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

# Função para agrupamento
def group_by(df, col):

    # Agregação
    grouped = df.groupby(by = col, as_index = False).agg({'va_arrecadacao': 'sum'})

    # Calculando a margem de lucro
    #grouped['Margem_Lucro'] = np.multiply(np.divide(grouped['Lucro'], grouped['Venda']), 100).round(2)
    
    return grouped


def plot_year_taxs(UF='ES', df=datasets.arrecadacao_1998_a_2001()):
    
    # INNER JOIN COM OS TIPOS DE ARRECADAÇÃO
    df = pd.merge(df, datasets.tipo_arrecadacao(), 
                  how='left', 
                  left_on='co_tipo_arrecadacao', 
                  right_on='CD_TIP_ARRECAD')

    # AGRUPANDO POR: UF, ANO, TRIBUTO
    df = group_by(df, ['sg_uf', 
                       'ano_arrecadacao', 
                       'NM_TIP_ARRECAD']).sort_values(["ano_arrecadacao", "va_arrecadacao"], ascending=False)

    # FILTRANDO O ESTADO
    df = df[df['sg_uf'] == UF]

    # CRIA O GRÁFICO
    fig = px.bar(df, 
                 x='ano_arrecadacao', 
                 y='va_arrecadacao',
                 hover_data=['NM_TIP_ARRECAD'], 
                 color='NM_TIP_ARRECAD',
                 labels={'pop':'population of Canada'}, 
                 height=600)

    return fig


def plot_tributos_ipca(cidade='AFONSO CLAUDIO'):

    # Obtendo os dados
    # ==========================================
    # fonte: https://dados.es.gov.br/dataset/portal-da-transparencia-transferencias-para-municipios
    transf_2018 = pd.read_csv('data/transfestadomunicipios-2018.csv', sep=';')
    transf_2019 = pd.read_csv('data/transfestadomunicipios-2019.csv', sep=';')
    transf_2020 = pd.read_csv('data/transfestadomunicipios-2020.csv', sep=';')
    transf_2021 = pd.read_csv('data/transfestadomunicipios-2021.csv', sep=';')

    # juntando informacoes em 1 dataset
    # ==========================================
    transferencias = pd.concat([transf_2018, transf_2019, transf_2020, transf_2021], ignore_index=True)

    # Mudando os codigos municipais errados das tres cidades com homonimos
    # ====================================================================
    # * Boa Esperança (MG - 3107109) -> (ES - 3201001)
    # * Presidente Keneddy (TO - 1718402) -> (ES - 3204302)
    # * Viana (MA - 2112803) -> (ES - 3205101)

    for i in range(len(transferencias)):
        #Boa Esperança
        if transferencias.loc[i, 'CodMunicipio'] == 3107109:
            transferencias.loc[i, 'CodMunicipio'] = 3201001
        elif transferencias.loc[i, 'CodMunicipio'] == 1718402:
            transferencias.loc[i, 'CodMunicipio'] = 3204302
        elif transferencias.loc[i, 'CodMunicipio'] == 2112803:
            transferencias.loc[i, 'CodMunicipio'] = 3205101

    # Transformando colunas pertinentes em numbers
    # ====================================================================
    calumns_to_num = ['IcmsTotal', 'Ipi', 'Ipva', 'FundoReducaoDesigualdades']
    for x in calumns_to_num:
        transferencias[x] = [round(float(transferencias[x].iloc[i].replace(',', '.')), 2) for i in range(len(transferencias))]

    # Criando coluna de totais
    # ====================================================================
    transferencias['TotalRepassado'] = transferencias[calumns_to_num[0]] + transferencias[calumns_to_num[1]] + transferencias[calumns_to_num[2]] + transferencias[calumns_to_num[3]]
    
    # Criando coluna com datatype
    # ====================================================================
    transferencias['Data'] = [datetime.datetime(transferencias['Ano'].iloc[i], transferencias['Mes'].iloc[i], 28) for i in range(len(transferencias))]

    # Criando filtros
    # ====================================================================
    df = transferencias[transferencias['NomeMunicipio']==cidade][['TotalRepassado', 'Data']]

    # Refazer de forma mais automatica -> aqui foi so para teste
    # ====================================================================
    list_date = list(df['Data'])
    ipca = [0.29, 0.32, 0.09, 0.22, 0.4, 1.26, 0.33, -0.09, 0.48, 0.45, -0.21, 0.15, 0.32, 0.43, 0.75, 0.57, 0.13, 0.01, 0.19, 0.11, -0.04, 0.1, 0.51, 1.15, 0.21, 0.25, 0.07, -0.31, -0.38, 0.26, 0.36, 0.24, 0.64, 0.86, 0.89, 1.35, 0.25, 0.86, 0.93, 0.31]
    dict_ipca={}
    for idx, i in enumerate(list_date):
        dict_ipca[i]=ipca[idx]

    df['IPCA'] = ipca
    
    # Valores de comparacao - ipca
    # ====================================================================
    list_valor_comparacao = []
    for i in range(len(df)):
        if i == 0:
            list_valor_comparacao.append(df['TotalRepassado'].iloc[i])
        else:
            list_valor_comparacao.append(round(list_valor_comparacao[i-1]*(1+df['IPCA'].iloc[i-1]/100), 2))
            
    df['ValorComparacao'] = list_valor_comparacao
    
    # Plot
    # ====================================================================
    import plotly.graph_objects as go
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=df['TotalRepassado'], x=df['Data'],
                        mode='lines',
                        name='Repasse Estadual'))
    fig.add_trace(go.Scatter(y=df['ValorComparacao'], x=df['Data'],
                       mode='lines',
                       name='Valor Ajustado por IPCA'))


    return fig

def plot_comp_tributos_cidades(list_cidades = ['ARACRUZ', 'ANCHIETA', 'CARIACICA', 'GUARAPARI', 'LINHARES', 'PIUMA']):
    #import pandas as pd
    #import datetime

    # Obtendo os dados
    # ==========================================
    # fonte: https://dados.es.gov.br/dataset/portal-da-transparencia-transferencias-para-municipios
    transf_2018 = pd.read_csv('data/transfestadomunicipios-2018.csv', sep=';')
    transf_2019 = pd.read_csv('data/transfestadomunicipios-2019.csv', sep=';')
    transf_2020 = pd.read_csv('data/transfestadomunicipios-2020.csv', sep=';')
    transf_2021 = pd.read_csv('data/transfestadomunicipios-2021.csv', sep=';')

    # juntando informacoes em 1 dataset
    # ==========================================
    transferencias = pd.concat([transf_2018, transf_2019, transf_2020, transf_2021], ignore_index=True)

    # Mudando os codigos municipais errados das tres cidades com homonimos
    # ====================================================================
    # * Boa Esperança (MG - 3107109) -> (ES - 3201001)
    # * Presidente Keneddy (TO - 1718402) -> (ES - 3204302)
    # * Viana (MA - 2112803) -> (ES - 3205101)

    for i in range(len(transferencias)):
        #Boa Esperança
        if transferencias.loc[i, 'CodMunicipio'] == 3107109:
            transferencias.loc[i, 'CodMunicipio'] = 3201001
        elif transferencias.loc[i, 'CodMunicipio'] == 1718402:
            transferencias.loc[i, 'CodMunicipio'] = 3204302
        elif transferencias.loc[i, 'CodMunicipio'] == 2112803:
            transferencias.loc[i, 'CodMunicipio'] = 3205101

    # Transformando colunas pertinentes em numbers
    # ====================================================================
    calumns_to_num = ['IcmsTotal', 'Ipi', 'Ipva', 'FundoReducaoDesigualdades']
    for x in calumns_to_num:
        transferencias[x] = [round(float(transferencias[x].iloc[i].replace(',', '.')), 2) for i in range(len(transferencias))]

    # Criando coluna de totais
    # ====================================================================
    transferencias['TotalRepassado'] = transferencias[calumns_to_num[0]] + transferencias[calumns_to_num[1]] + transferencias[calumns_to_num[2]] + transferencias[calumns_to_num[3]]
    
    # Criando coluna com datatype
    # ====================================================================
    transferencias['Data'] = [datetime.datetime(transferencias['Ano'].iloc[i], transferencias['Mes'].iloc[i], 28) for i in range(len(transferencias))]

    # ##############################################################################################################################################################################

    populacao_2018 = pd.read_csv('data/populacao_2018.csv')[['UF', 'COD. UF', 'COD. MUNIC', 'NOME DO MUNICÍPIO', 'POPULAÇÃO ESTIMADA']]
    populacao_2019 = pd.read_csv('data/populacao_2019.csv')[['UF', 'COD. UF', 'COD. MUNIC', 'NOME DO MUNICÍPIO', 'POPULAÇÃO ESTIMADA']]
    populacao_2020 = pd.read_csv('data/populacao_2020.csv')[['UF', 'COD. UF', 'COD. MUNIC', 'NOME DO MUNICÍPIO', 'POPULAÇÃO ESTIMADA']]
    populacao_2021 = pd.read_csv('data/populacao_2021.csv')[['UF', 'COD. UF', 'COD. MUNIC', 'NOME DO MUNICÍPIO', 'POPULAÇÃO ESTIMADA']]

    populacao_es_2018 = populacao_2018[populacao_2018['UF']=='ES']
    populacao_es_2019 = populacao_2019[populacao_2019['UF']=='ES']
    populacao_es_2020 = populacao_2020[populacao_2020['UF']=='ES']
    populacao_es_2021 = populacao_2021[populacao_2021['UF']=='ES']

    # ATENCAO ARRUMAR CODIGO PARA AS 3 CIDADES CITADAS
    # Criando coluna código
    ano = 2018
    for x in [populacao_es_2018, populacao_es_2019, populacao_es_2020, populacao_es_2021]:
        x['COD.GERAL'] = [int(str(int(x['COD. UF'].iloc[i])) + '00' +
                                    str(int(x['COD. MUNIC'].iloc[i])))
                                    if len(str(int(x['COD. MUNIC'].iloc[i]))) < 4
                                    else int(str(int(x['COD. UF'].iloc[i])) + '0' +
                                    str(int(x['COD. MUNIC'].iloc[i]))) for i in range(len(x))]
        x['ANO'] = ano
        ano += 1
    
    populacao_es = pd.concat([populacao_es_2018, populacao_es_2019, populacao_es_2020, populacao_es_2021], ignore_index=True)
    populacao_es['POPULAÇÃO ESTIMADA'] = [int(i.replace(',', '')) for i in populacao_es['POPULAÇÃO ESTIMADA']]

    boolean_series = transferencias['NomeMunicipio'].isin(list_cidades)
    df_repasse = transferencias[boolean_series][['NomeMunicipio', 'CodMunicipio', 'TotalRepassado', 'Data', 'Ano']]
    
    codigos = []
    for i in list_cidades:
        cod = transferencias[transferencias['NomeMunicipio'] == i]['CodMunicipio'].iloc[0]
        codigos.append(cod)
    
    boolean_series = populacao_es['COD.GERAL'].isin(codigos)
    df_pop = populacao_es[boolean_series][['COD.GERAL', 'POPULAÇÃO ESTIMADA', 'ANO']]
    
    #merge
    df = df_repasse.merge(df_pop, how= 'inner', left_on=['CodMunicipio', 'Ano'], right_on=['COD.GERAL', 'ANO'])
    df = df.drop(columns=['COD.GERAL'])
    
    #column arrec_percapita
    df['RepassPercapita'] = [round(df['TotalRepassado'].iloc[i]/df['POPULAÇÃO ESTIMADA'].iloc[0], 2) for i in range(len(df))]
    
    #plot percapita
    import plotly.graph_objects as go
    
    fig = go.Figure()
    for i in range(len(list_cidades)):
        fig.add_trace(go.Scatter(y=df[df['NomeMunicipio']==list_cidades[i]]['RepassPercapita'], 
                                 x=df[df['NomeMunicipio']==list_cidades[i]]['Data'],
                                 mode='lines',
                                 name=list_cidades[i]))
    return fig


def plot_comp_tributos_cidades_norm(list_cidades = ['ARACRUZ', 'ANCHIETA', 'CARIACICA', 'GUARAPARI', 'LINHARES', 'PIUMA']):
    #import pandas as pd
    #import datetime

    # Obtendo os dados
    # ==========================================
    # fonte: https://dados.es.gov.br/dataset/portal-da-transparencia-transferencias-para-municipios
    transf_2018 = pd.read_csv('data/transfestadomunicipios-2018.csv', sep=';')
    transf_2019 = pd.read_csv('data/transfestadomunicipios-2019.csv', sep=';')
    transf_2020 = pd.read_csv('data/transfestadomunicipios-2020.csv', sep=';')
    transf_2021 = pd.read_csv('data/transfestadomunicipios-2021.csv', sep=';')

    # juntando informacoes em 1 dataset
    # ==========================================
    transferencias = pd.concat([transf_2018, transf_2019, transf_2020, transf_2021], ignore_index=True)

    # Mudando os codigos municipais errados das tres cidades com homonimos
    # ====================================================================
    # * Boa Esperança (MG - 3107109) -> (ES - 3201001)
    # * Presidente Keneddy (TO - 1718402) -> (ES - 3204302)
    # * Viana (MA - 2112803) -> (ES - 3205101)

    for i in range(len(transferencias)):
        #Boa Esperança
        if transferencias.loc[i, 'CodMunicipio'] == 3107109:
            transferencias.loc[i, 'CodMunicipio'] = 3201001
        elif transferencias.loc[i, 'CodMunicipio'] == 1718402:
            transferencias.loc[i, 'CodMunicipio'] = 3204302
        elif transferencias.loc[i, 'CodMunicipio'] == 2112803:
            transferencias.loc[i, 'CodMunicipio'] = 3205101

    # Transformando colunas pertinentes em numbers
    # ====================================================================
    calumns_to_num = ['IcmsTotal', 'Ipi', 'Ipva', 'FundoReducaoDesigualdades']
    for x in calumns_to_num:
        transferencias[x] = [round(float(transferencias[x].iloc[i].replace(',', '.')), 2) for i in range(len(transferencias))]

    # Criando coluna de totais
    # ====================================================================
    transferencias['TotalRepassado'] = transferencias[calumns_to_num[0]] + transferencias[calumns_to_num[1]] + transferencias[calumns_to_num[2]] + transferencias[calumns_to_num[3]]
    
    # Criando coluna com datatype
    # ====================================================================
    transferencias['Data'] = [datetime.datetime(transferencias['Ano'].iloc[i], transferencias['Mes'].iloc[i], 28) for i in range(len(transferencias))]

    # ##############################################################################################################################################################################

    populacao_2018 = pd.read_csv('data/populacao_2018.csv')[['UF', 'COD. UF', 'COD. MUNIC', 'NOME DO MUNICÍPIO', 'POPULAÇÃO ESTIMADA']]
    populacao_2019 = pd.read_csv('data/populacao_2019.csv')[['UF', 'COD. UF', 'COD. MUNIC', 'NOME DO MUNICÍPIO', 'POPULAÇÃO ESTIMADA']]
    populacao_2020 = pd.read_csv('data/populacao_2020.csv')[['UF', 'COD. UF', 'COD. MUNIC', 'NOME DO MUNICÍPIO', 'POPULAÇÃO ESTIMADA']]
    populacao_2021 = pd.read_csv('data/populacao_2021.csv')[['UF', 'COD. UF', 'COD. MUNIC', 'NOME DO MUNICÍPIO', 'POPULAÇÃO ESTIMADA']]

    populacao_es_2018 = populacao_2018[populacao_2018['UF']=='ES']
    populacao_es_2019 = populacao_2019[populacao_2019['UF']=='ES']
    populacao_es_2020 = populacao_2020[populacao_2020['UF']=='ES']
    populacao_es_2021 = populacao_2021[populacao_2021['UF']=='ES']

    # ATENCAO ARRUMAR CODIGO PARA AS 3 CIDADES CITADAS
    # Criando coluna código
    ano = 2018
    for x in [populacao_es_2018, populacao_es_2019, populacao_es_2020, populacao_es_2021]:
        x['COD.GERAL'] = [int(str(int(x['COD. UF'].iloc[i])) + '00' +
                                    str(int(x['COD. MUNIC'].iloc[i])))
                                    if len(str(int(x['COD. MUNIC'].iloc[i]))) < 4
                                    else int(str(int(x['COD. UF'].iloc[i])) + '0' +
                                    str(int(x['COD. MUNIC'].iloc[i]))) for i in range(len(x))]
        x['ANO'] = ano
        ano += 1
    
    populacao_es = pd.concat([populacao_es_2018, populacao_es_2019, populacao_es_2020, populacao_es_2021], ignore_index=True)
    populacao_es['POPULAÇÃO ESTIMADA'] = [int(i.replace(',', '')) for i in populacao_es['POPULAÇÃO ESTIMADA']]

    boolean_series = transferencias['NomeMunicipio'].isin(list_cidades)
    df_repasse = transferencias[boolean_series][['NomeMunicipio', 'CodMunicipio', 'TotalRepassado', 'Data', 'Ano']]
    
    codigos = []
    for i in list_cidades:
        cod = transferencias[transferencias['NomeMunicipio'] == i]['CodMunicipio'].iloc[0]
        codigos.append(cod)
    
    boolean_series = populacao_es['COD.GERAL'].isin(codigos)
    df_pop = populacao_es[boolean_series][['COD.GERAL', 'POPULAÇÃO ESTIMADA', 'ANO']]
    
    #merge
    df = df_repasse.merge(df_pop, how= 'inner', left_on=['CodMunicipio', 'Ano'], right_on=['COD.GERAL', 'ANO'])
    df = df.drop(columns=['COD.GERAL'])
    
    #column arrec_percapita
    df['RepassPercapita'] = [round(df['TotalRepassado'].iloc[i]/df['POPULAÇÃO ESTIMADA'].iloc[i], 2) for i in range(len(df))]
    
    #plot percapita normalizado
    import plotly.graph_objects as go
    
    fig = go.Figure()
    for i in range(len(list_cidades)):
        fig.add_trace(go.Scatter(y=df[df['NomeMunicipio']==list_cidades[i]]['RepassPercapita']/df[df['NomeMunicipio']==list_cidades[i]]['RepassPercapita'].iloc[0]*100, 
                                 x=df[df['NomeMunicipio']==list_cidades[i]]['Data'],
                                 mode='lines',
                                 name=list_cidades[i]))
        
    return fig