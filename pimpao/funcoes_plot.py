def plot_calendar_heatmap_pkl(cidade='AFONSO CLAUDIO', tipo= 'NOVOS CASOS', mes_analise= 1, ano_analise= 2021):

    import pandas as pd
    import numpy as np

    df_calendar = pd.read_parquet('../../app/home/data/treated_data/MICRODADOS_tratado.parquet')
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

    # --------- NOVO PEDACO DE CODIGO PARA AJUSTAR PLOT ACUMULADA ---------
    if tipo == 'NOVOS CASOS':
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

    else:
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
                numero_casos = int(df_calendar_display.iloc[contador-1,-1])
                semana_do_ano = int(datetime(ano_analise, mes_analise, i).strftime('%W'))
                dia_da_semana = datetime(ano_analise, mes_analise, i).weekday()

            info_dia.append([dia, numero_casos, semana_do_ano, dia_da_semana])

    # --------- FIM NOVO CODIGO ---------

    #separando essa lista em outras 4
    dias, n_casos, semana, dia_semana = zip(*info_dia)

    #criando lista com o numero de casos de cada dia do mes e separado em lista por semana
    final_casos = []
    parcial_casos = []
    for i, week in enumerate(semana):
        if i == 0:
            parcial_casos.append(n_casos[i])
        elif i == n_dias - 1 and dia_semana[i]!=0:
            parcial_casos.append(n_casos[i])
            final_casos.append(parcial_casos)
        elif i == n_dias - 1 and dia_semana[i]==0:
            final_casos.append(parcial_casos)
            parcial_casos = []
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
        if i == len(dias) - 1 and dia_semana[i]!=0:
            parcial_dias.append(dia)
            final_dias.append(parcial_dias)
        elif i == len(dias) - 1 and dia_semana[i]==0:
            final_dias.append(parcial_dias)
            parcial_dias = []
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

    return fig1



def plot_tributos_ipca(cidade='AFONSO CLAUDIO'):
    import pandas as pd
    #datasets
    transferencias = pd.read_parquet('path/transf_estadual_tratado.parquet') #uallas ver path do arquivo

    df = transferencias[transferencias['NomeMunicipio']==cidade][['TotalRepassado', 'Data']]

    ipca = [0.29, 0.32, 0.09, 0.22, 0.4, 1.26, 0.33, -0.09, 0.48, 0.45, -0.21, 0.15, 0.32, 0.43, 0.75, 0.57, 0.13, 0.01, 0.19, 0.11, -0.04, 0.1, 0.51, 1.15, 0.21, 0.25, 0.07, -0.31, -0.38, 0.26, 0.36, 0.24, 0.64, 0.86, 0.89, 1.35, 0.25, 0.86, 0.93, 0.31]

    df['IPCA'] = ipca

    #valores de comparacao - ipca
    list_valor_comparacao = []
    for i in range(len(df)):
        if i == 0:
            list_valor_comparacao.append(df['TotalRepassado'].iloc[i])
        else:
            list_valor_comparacao.append(round(list_valor_comparacao[i-1]*(1+df['IPCA'].iloc[i-1]/100), 2))

    df['ValorComparacao'] = list_valor_comparacao

    #plot
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
    import pandas as pd
    import numpy as np
    import datetime

    transferencias = pd.read_parquet('path/transf_estadual_tratado.parquet') #uallas ver path do arquivo
    populacao_es = pd.read_parquet('path/populacao_es_tratado.parquet') #uallas ver path do arquivo

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
    import pandas as pd
    import numpy as np
    import datetime

    transferencias = pd.read_parquet('path/transf_estadual_tratado.parquet') #uallas ver path do arquivo
    populacao_es = pd.read_parquet('path/populacao_es_tratado.parquet') #uallas ver path do arquivo


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




def plot_mapa():
    import pandas as pd
    import plotly.express as px

    ranking_total = pd.read_parquet('path/ranking_total.parquet')
    geofile = pd.read_parquet('path/mapa.parquet')
    fig = px.choropleth_mapbox(ranking_total, geojson=geofile, color="Ranking",
                               locations="CodigoMunicipal", featureidkey="properties.cod_ibge",
                               center={"lat": -19.7, "lon": -40.5},
                               mapbox_style="carto-positron", zoom=6,
                               hover_name='Municipio',
                               color_continuous_scale='RdYlGn',
                               opacity=0.9,
                               animation_frame="Mes_desc")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_coloraxes(cauto=False, cmin = 78, cmax = 1)
    return fig
    #RdYlGn
    #blues_r


def plot_resumo(cidade='all'):
    import pandas as pd
    import plotly.express as px

    if cidades == 'all':
        df_casos = df_casos.groupby('date')[['acum', 'fatais', 'confirmados', 'recuperados']].sum()
        fig = px.line(df_casos[df_casos['date']<=datetime(2021, 7, 1)],
              x="date", y=["acum", 'fatais', 'confirmados', 'recuperados'],
              #color_discrete_sequence=['yellow', 'grey', 'red', 'green'],
              title='Dados Acumulativos')
    else:
        fig = px.line(df_casos[(df_casos['Municipio']==cidade) & (df_casos['date']<=datetime(2021, 7, 1))],
              x="date", y=["acum", 'fatais', 'confirmados', 'recuperados'],
              #color_discrete_sequence=['yellow', 'grey', 'red', 'green'],
              title='Dados Acumulativos')
    return fig
