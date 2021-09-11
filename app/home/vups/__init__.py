import os
from numpy import empty
from numpy.ma import isin
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
    on_bad_lines='warn',
    usecols=None,
    nrows=None,
    file=const.DATAFILE['FILENAME'],
    sep=const.DATAFILE['SEP'],
    encoding=const.DATAFILE['ENCODING'],
    dtype=None,
    FIELD = None,
    VALUE = None):

    PATH = os.path.join(const.DATADIR + file)

    dataset = pd.read_csv(  filepath_or_buffer  = PATH,
                            usecols             = usecols,
                            sep                 = sep,
                            nrows               = nrows,
                            encoding            = encoding,
                            on_bad_lines        = on_bad_lines,
                            dtype               = dtype
                            )
    dataset = dtype_transform(dataset)

    return dataset

# def plot_qtd_pessoas_x_sintomas(df):
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
    ])

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
        v = df.iloc[:, i]         # VALOR NA LINHA ZERO
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
        v = df.iloc[:, i]           # VALOR NA LINHA ZERO
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
        v = df.iloc[:0, i]         # VALOR NA LINHA ZERO
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
    def microdados(columns=None, nrows=None, dtype={'DataObito': 'object'}, field=None, value=None):
        return get_data(file='MICRODADOS.csv', usecols=columns, nrows=nrows, sep=';', encoding='latin1', dtype=dtype, FIELD=field, VALUE=value)

    def microdados_bairros(columns=None, nrows=None, dtype=None):
        return get_data(file='MICRODADOS_BAIRROS.csv', usecols=columns, nrows=nrows, sep=',', encoding='latin1', dtype=dtype)

    def arrecadacao_1998_a_2001(columns=None, nrows=None, dtype=None):
        return get_data(file='Arrecadacao_01-01-1998_a_31-12-2001.csv', usecols=columns, nrows=nrows, sep=',', encoding='utf-8', dtype=tax_cat_col)

    def arrecadacao_2002_a_2005(columns=None, nrows=None, dtype=None):
        return get_data(file='Arrecadacao_01-01-2002_a_31-12-2005.csv', usecols=columns, nrows=nrows, sep=',', encoding='utf-8', dtype=dtype)

    def arrecadacao_2006_a_2009(columns=None, nrows=None, dtype=None):
        return get_data(file='Arrecadacao_01-01-2006_a_31-12-2009.csv', usecols=columns, nrows=nrows, sep=',', encoding='utf-8', dtype=dtype)

    def arrecadacao_2010_a_2013(columns=None, nrows=None, dtype=None):
        return get_data(file='Arrecadacao_01-01-2010_a_31-12-2013.csv', usecols=columns, nrows=nrows, sep=',', encoding='utf-8', dtype=dtype)

    def arrecadacao_2014_a_2017(columns=None, nrows=None, dtype=None):
        return get_data(file='Arrecadacao_01-01-2014_a_31-12-2017.csv', usecols=columns, nrows=nrows, sep=',', encoding='utf-8', dtype=dtype)

    def arrecadacao_2018_a_2020(columns=None, nrows=None, dtype=None):
        return get_data(file='Arrecadacao_01-01-2018_a_09-12-2020.csv', usecols=columns, nrows=nrows, sep=',', encoding='utf-8', dtype=dtype)

    def tipo_arrecadacao(columns=None, nrows=None, dtype=None):
        return get_data(file='TipoArrecadacao.csv', usecols=columns, nrows=nrows, sep=',', encoding='utf-8', dtype=dtype)

    # Transferência Estado-Municipios
    def transfestadomunicipios_2018(columns=None, nrows=None, dtype=None):
        return get_data(file='transfestadomunicipios-2018.csv', usecols=columns, nrows=nrows, sep=';', encoding='utf-8', dtype=dtype)

    def transfestadomunicipios_2019(columns=None, nrows=None, dtype=None):
        return get_data(file='transfestadomunicipios-2019.csv', usecols=columns, nrows=nrows, sep=';', encoding='utf-8', dtype=dtype)

    def transfestadomunicipios_2020(columns=None, nrows=None, dtype=None):
        return get_data(file='transfestadomunicipios-2020.csv', usecols=columns, nrows=nrows, sep=';', encoding='utf-8', dtype=dtype)

    def transfestadomunicipios_2021(columns=None, nrows=None, dtype=None):
        return get_data(file='transfestadomunicipios-2021.csv', usecols=columns, nrows=nrows, sep=';', encoding='utf-8', dtype=dtype)     

    # POPULAÇÃO
    def populacao_2018(columns=None, nrows=None, dtype=None):
        return get_data(file='populacao_2018.csv', usecols=columns, nrows=nrows, sep=',', encoding='utf-8', dtype=dtype)

    def populacao_2019(columns=None, nrows=None, dtype=None):
        return get_data(file='populacao_2019.csv', usecols=columns, nrows=nrows, sep=',', encoding='utf-8', dtype=dtype)

    def populacao_2020(columns=None, nrows=None, dtype=None):
        return get_data(file='populacao_2020.csv', usecols=columns, nrows=nrows, sep=',', encoding='utf-8', dtype=dtype)

    def populacao_2021(columns=None, nrows=None, dtype=None):
        return get_data(file='populacao_2021.csv', usecols=columns, nrows=nrows, sep=',', encoding='utf-8', dtype=dtype)


def group_by(df, col):
    """
    Função para agrupamento
    """
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
    fig.update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)'
    })

    return fig

def plot_calendar_heatmap(cidade='AFONSO CLAUDIO', tipo= 'NOVOS CASOS', mes_analise= 1, ano_analise= 2021):
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

    COLUMNS = ['Municipio', 'Classificacao', 'DataDiagnostico', 'DataCadastro', 'DataEncerramento']
    
    # --------- FILTRANDO DF PARA CIDADES DO ES ---------
    filtro_es = ['AGUIA BRANCA', 'ALTO RIO NOVO', 'ARACRUZ', 'BAIXO GUANDU',
       'COLATINA', 'GOVERNADOR LINDENBERG', 'IBIRACU', 'JOAO NEIVA',
       'LINHARES', 'MANTENOPOLIS', 'MARILANDIA', 'PANCAS', 'RIO BANANAL',
       'SAO DOMINGOS DO NORTE', 'SAO GABRIEL DA PALHA',
       'SAO ROQUE DO CANAA', 'SOORETAMA', 'VILA VALERIO',
       'AFONSO CLAUDIO', 'BREJETUBA', 'CARIACICA', 'CONCEICAO DO CASTELO',
       'DOMINGOS MARTINS', 'FUNDAO', 'GUARAPARI', 'IBATIBA', 'ITAGUACU',
       'ITARANA', 'LARANJA DA TERRA', 'MARECHAL FLORIANO',
       'SANTA LEOPOLDINA', 'SANTA MARIA DE JETIBA', 'SANTA TERESA',
       'SERRA', 'VENDA NOVA DO IMIGRANTE', 'VIANA', 'VILA VELHA',
       'VITORIA', 'AGUA DOCE DO NORTE', 'BARRA DE SAO FRANCISCO',
       'BOA ESPERANCA', 'CONCEICAO DA BARRA', 'ECOPORANGA', 'JAGUARE',
       'MONTANHA', 'MUCURICI', 'NOVA VENECIA', 'PEDRO CANARIO',
       'PINHEIROS', 'PONTO BELO', 'SAO MATEUS', 'VILA PAVAO', 'ALEGRE',
       'ALFREDO CHAVES', 'ANCHIETA', 'APIACA', 'ATILIO VIVACQUA',
       'BOM JESUS DO NORTE', 'CACHOEIRO DE ITAPEMIRIM', 'CASTELO',
       'DIVINO DE SAO LOURENCO', 'DORES DO RIO PRETO', 'GUACUI',
       'IBITIRAMA', 'ICONHA', 'IRUPI', 'ITAPEMIRIM', 'IUNA',
       'JERONIMO MONTEIRO', 'MARATAIZES', 'MIMOSO DO SUL', 'MUNIZ FREIRE',
       'MUQUI', 'PIUMA', 'PRESIDENTE KENNEDY', 'RIO NOVO DO SUL',
       'SAO JOSE DO CALCADO', 'VARGEM ALTA']

    # --------- BUSCANDO DF ---------
    df = datasets.microdados(columns=COLUMNS, field='Municipio', value=filtro_es)

    # --------- CRIANDO DF_CALENDAR_NEW(CASOS NOVOS) E DF_CALENDAR_CLOSED(CASOS FECHADOS) ---------
    #df_calendar_new -> filtrar pacientes com covid confirmados; groupby(Municipio, DataDiagnostico); contar ocorrencias
    df_calendar_new = df[df['Classificacao']=='Confirmados'].groupby(['Municipio','DataDiagnostico'])['DataCadastro'].size().reset_index(name='count_new')

    #renomendo coluna DataDiagnostico
    df_calendar_new.rename(columns={'DataDiagnostico': 'date'}, inplace=True)

    #transformando o dtype na coluna 'date' para datetime
    df_calendar_new['date'] = df_calendar_new['date'].astype('datetime64[ns]')

    #df_calendar_closed -> filtrar pacientes com covid confirmados; groupby(Municipio, DataEncerramento); contar ocorrencias
    df_calendar_closed = df[df['Classificacao']=='Confirmados'].groupby(['Municipio','DataEncerramento'])['DataCadastro'].size().reset_index(name='count_closed')

    #--- ATENCAO!!! --- DataEncerramento NAO esta sendo transformada automaticamente, por isso vamos forçar essa transformação aqui
    #após corrigido, retirar esse pedaço de código
    #transformando DataEncerramento em datatype
    #df_calendar_closed['DataEncerramento'] = pd.to_datetime(df_calendar_closed['DataEncerramento'], format='%Y-%m-%d')

    #transformando valores de casos fechados em negativo
    df_calendar_closed['count_closed'] = df_calendar_closed['count_closed']*-1

    #renomendo coluna DataEncerramento
    df_calendar_closed.rename(columns={'DataEncerramento': 'date'}, inplace=True)

    #transformando o dtype na coluna 'date' para datetime
    df_calendar_closed['date'] = df_calendar_closed['date'].astype('datetime64[ns]')

    # --------- MERGE ENTRE OS DOIS DFs CRIADOS ---------
    df_calendar = pd.merge(df_calendar_new, df_calendar_closed, how='outer', left_on=['Municipio', 'date'], right_on=['Municipio', 'date'])

    # --------- TRABLHANDO O NOVO DF ---------
    #organizando por cidade/data
    df_calendar = df_calendar.sort_values(["Municipio", "date"]).reset_index()

    #preenchendo Nan com zero(0)
    for i in ['count_new', 'count_closed']:
        df_calendar[i] = df_calendar[i].fillna(0)

    #criando coluna acumulado por cidade
    municipios = df_calendar['Municipio'].unique()
    acum = []
    for idx, i in enumerate(df_calendar['date']):
        if df_calendar['Municipio'].iloc[idx] == df_calendar['Municipio'].iloc[idx-1]:
            try:
                acum.append(acum[idx-1] + df_calendar['count_new'].iloc[idx] + df_calendar['count_closed'].iloc[idx])
            except:
                acum.append(df_calendar['count_new'].iloc[idx] + df_calendar['count_closed'].iloc[idx])
        else:
            acum.append(0 + df_calendar['count_new'].iloc[idx] + df_calendar['count_closed'].iloc[idx])

    df_calendar['acum'] = acum

    #criando colunas de dia/semana/dia_da_semana/mes/ano
    df_calendar['day'] = [i.day for i in df_calendar['date']]
    df_calendar['week'] = [i.week for i in df_calendar['date']]
    df_calendar['weekday'] = [i.weekday() for i in df_calendar['date']]
    df_calendar['month'] = [i.month for i in df_calendar['date']]
    df_calendar['year'] = [i.year for i in df_calendar['date']]

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

    #aplicando filtros
    if tipo == 'NOVOS CASOS':
        df_calendar_display = df_calendar[(df_calendar['Municipio'] == cidade) &
                                               (df_calendar['month'] == mes_analise) &
                                               (df_calendar['year'] == ano_analise)][['Municipio', 'date', 'day', 'week', 'weekday', 'month', 'year', 'count_new']].sort_values(by=['day']).reset_index().drop(columns=['index'])
    else:
        df_calendar_display = df_calendar[(df_calendar['Municipio'] == cidade) &
                                               (df_calendar['month'] == mes_analise) &
                                               (df_calendar['year'] == ano_analise)][['Municipio', 'date', 'day', 'week', 'weekday', 'month', 'year', 'acum']].sort_values(by=['day']).reset_index().drop(columns=['index'])

    #criando listagem com a contagem de casos para cada dia do mes e as informações da semana do ano e dia da semana
    #preenchendo com zero os dias em que nao tiveram registros
    info_dia = []
    contador = 0
    for i in range(1, n_dias + 1):
        if i == df_calendar_display['day'].iloc[contador]:
            dia = i
            numero_casos = int(df_calendar_display.iloc[contador,-1])
            semana_do_ano = df_calendar_display['week'].iloc[contador]
            dia_da_semana = df_calendar_display['weekday'].iloc[contador]
            if contador < len(df_calendar_display)-1:
                contador = contador + 1
        else:
            dia = i
            numero_casos = 0
            semana_do_ano = int(datetime(ano_analise, mes_analise, i).strftime('%W'))
            dia_da_semana = datetime(ano_analise, mes_analise, i).weekday()

        info_dia.append([dia, numero_casos, semana_do_ano, dia_da_semana])

    #separando essa lista em outras 4
    dias, n_casos, semana, dia_semana = zip(*info_dia)

    #criando lista com o numero de casos de cada dia do mes e separado em lista por semana
    final_casos = []
    parcial_casos = []
    for i, week in enumerate(semana):
        if i == 0:
            parcial_casos.append(n_casos[i])
        elif i == n_dias - 1:
            parcial_casos.append(n_casos[i])
            final_casos.append(parcial_casos)
        else:
            if week == semana[i-1]:
                parcial_casos.append(n_casos[i])
            else:
                final_casos.append(parcial_casos)
                parcial_casos = []
                parcial_casos.append(n_casos[i])

    #calculando o valor maximo da quantidade de casos para servir como ponto maximo da escala de cores
    max_value = []
    for i in range(len(final_casos)):
        max_value.append(max(final_casos[i]))

    max_value = max(max_value)

    #preenchendo valores relativos aos dias que completam as semanas com menos de 7 dias (inicio/final)
    #o max_value serve para ajustar a cor (branco) que vai ser printado no heatmap para esses valores de preenchimento
    while len(final_casos[0]) < 7:
        final_casos[0].insert(0, 0.001*max_value)

    while len(final_casos[-1]) < 7:
        final_casos[-1].append(0.001*max_value)

    #transformando valores a serem pintados em cinza, em negativo
    for i in range(len(final_casos)):
        for j in range(len(final_casos[i])):
            if final_casos[i][j]>0 and final_casos[i][j]<1:
                final_casos[i][j] = final_casos[i][j]*-1

    #tranformando dias de int para str
    dias = list(map(str, dias))

    #preenchendo lista de acordo com o exigido para o plot (lista de listas para cada semana do mes)
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

    #preenchendo as semanas que ficaram com menos de 7 dias com os dias do mes anterior e subsequente
    if mes_analise in [1, 2, 4, 6, 8, 9, 11]:
        contador = 0
        while len(final_dias[0]) < 7:
            final_dias[0].insert(0, str(31-contador))
            contador += 1
        contador = 0
        while len(final_dias[-1]) < 7:
            final_dias[-1].append(str(contador+1))
            contador += 1
    elif mes_analise == 3 and ano_analise != 2020:
        contador = 0
        while len(final_dias[0]) < 7:
            final_dias[0].insert(0, str(28-contador))
            contador += 1
        contador = 0
        while len(final_dias[-1]) < 7:
            final_dias[-1].append(str(contador+1))
            contador += 1
    elif mes_analise == 3 and ano_analise == 2020:
        contador = 0
        while len(final_dias[0]) < 7:
            final_dias[0].insert(0, str(29-contador))
            contador += 1
        contador = 0
        while len(final_dias[-1]) < 7:
            final_dias[-1].append(str(contador+1))
            contador += 1
    elif mes_analise in [5, 7, 10, 12]:
        contador = 0
        while len(final_dias[0]) < 7:
            final_dias[0].insert(0, str(30-contador))
            contador += 1
        contador = 0
        while len(final_dias[-1]) < 7:
            final_dias[-1].append(str(contador+1))
            contador += 1

    #criando os labels das semanas
    y_label = []
    for i in range(len(final_dias)):
        y_label.append('Semana ' + str(i+1))

    # --------- CALENDAR HEATMAP PLOT ---------

    #plot do heatmap estilo calendario (com a quantida de casos por dia)

    import plotly.figure_factory as ff

    z = final_casos[::-1]

    x = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sabado', 'Domingo']
    y = y_label[::-1]

    z_text = final_dias[::-1]

    fig1 = ff.create_annotated_heatmap(z,
                                      x=x,
                                      y=y,
                                      annotation_text=z_text,
                                      colorscale=[[0.0, 'rgb(235, 236, 240)'], #valores negativos
                                                  [0.00001, 'rgb(255,255,255)'],
                                                  [0.1, 'rgb(255,245,240)'],
                                                  [0.2, 'rgb(252,201,180)'],
                                                  [0.4, 'rgb(251,136,104)'],
                                                  [0.6, 'rgb(242,67,49)'],
                                                  [0.8, 'rgb(187,19,25)'],
                                                  [1.0, 'rgb(115,2,23)']],
                                      showscale=True)

    #titulo plot
    meses = ['Janeiro', 'Feveireiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    mes_plot = meses[mes_analise - 1]
    if tipo == 'NOVOS CASOS':
        fig1.update_layout(title_text= 'Casos Novos por dia - ' +
                           cidade.title() + ' - ' +
                           mes_plot + ' ' +
                           str(ano_analise), title_x=0.5)
    else:
        fig1.update_layout(title_text= 'Casos Acumulados - ' +
                           cidade.title() + ' - ' +
                           mes_plot + ' ' +
                           str(ano_analise), title_x=0.5)

    # fig1.update_layout({
    # 'plot_bgcolor': 'rgba(0,0,0,0)',
    # 'paper_bgcolor': 'rgba(0,0,0,0)'})

    return fig1

def plot_tributos_ipca(cidade='AFONSO CLAUDIO'):

    # Obtendo os dados
    # ==========================================
    # fonte: https://dados.es.gov.br/dataset/portal-da-transparencia-transferencias-para-municipios
    transf_2018 = datasets.transfestadomunicipios_2018()
    transf_2019 = datasets.transfestadomunicipios_2019()
    transf_2020 = datasets.transfestadomunicipios_2020()
    transf_2021 = datasets.transfestadomunicipios_2021()

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
    transf_2018 = datasets.transfestadomunicipios_2018()
    transf_2019 = datasets.transfestadomunicipios_2019()
    transf_2020 = datasets.transfestadomunicipios_2020()
    transf_2021 = datasets.transfestadomunicipios_2021()

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
    COLUMNS=['UF', 'COD. UF', 'COD. MUNIC', 'NOME DO MUNICÍPIO', 'POPULAÇÃO ESTIMADA']
    populacao_2018 = datasets.populacao_2018(columns=COLUMNS)
    populacao_2019 = datasets.populacao_2019(columns=COLUMNS)
    populacao_2020 = datasets.populacao_2020(columns=COLUMNS)
    populacao_2021 = datasets.populacao_2021(columns=COLUMNS)

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
    transf_2018 = datasets.transfestadomunicipios_2018()
    transf_2019 = datasets.transfestadomunicipios_2019()
    transf_2020 = datasets.transfestadomunicipios_2020()
    transf_2021 = datasets.transfestadomunicipios_2021()

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
    COLUMNS=['UF', 'COD. UF', 'COD. MUNIC', 'NOME DO MUNICÍPIO', 'POPULAÇÃO ESTIMADA']
    populacao_2018 = datasets.populacao_2018(columns=COLUMNS)
    populacao_2019 = datasets.populacao_2019(columns=COLUMNS)
    populacao_2020 = datasets.populacao_2020(columns=COLUMNS)
    populacao_2021 = datasets.populacao_2021(columns=COLUMNS)

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

    # fig.update_layout({
    # 'plot_bgcolor': 'rgba(0,0,0,0)',
    # 'paper_bgcolor': 'rgba(0,0,0,0)'})

    return fig