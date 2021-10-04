# -*- encoding: utf-8 -*-
"""
Programa de Mentoria DSA 2021
"""

import pandas as pd
import string
import unicodedata
from datetime import datetime
import math


def minMax(x):
    return pd.Series(
        index=['min', 'max'],
        data=[
            x.min(skipna=True, numeric_only=True),
            x.max(skipna=True, numeric_only=True)])


def remove_espaco(df, lst_cols=[]):
    espaco = " "
    for c in lst_cols:
        df[c] = df[c].str.replace(espaco, "")
    return(df)


def remove_pontuacao(df, lst_cols=[]):
    pontuacao = string.punctuation
    for c in lst_cols:
        for p in pontuacao:
            df[c] = df[c].str.replace(p, "")
    return(df)


def remove_acento(s):
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


def group_by(df, col):
    """
    Função para agrupamento
    """
    # Agregação
    grouped = df.groupby(by=col, as_index=False).agg({"va_arrecadacao": "sum"})

    return(grouped)


def tratando_microdados(df):

    # --------- FILTROS ---------
    COLUMNS = ['DataCadastro', 'DataDiagnostico', 'DataEncerramento', 'Classificacao', 'Evolucao', 'Municipio']

    # Municipios do ES
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

    # uallas >>>>>>>>>>> COLOCAR AQUI IMPORTACAO DO DATAFRAME POR FUNCAO <<<<<<<<<<<<<<

    # --------- CRIANDO DF_CALENDAR_NEW(CASOS NOVOS) ---------
    df_calendar_new = df[df['Classificacao']=='Confirmados'].groupby(['Municipio','DataDiagnostico'])['DataCadastro'].size().reset_index(name='count_new')

    # Renomeando coluna DataDiagnostico
    df_calendar_new.rename(columns={'DataDiagnostico': 'date'}, inplace=True)

    # transformando o dtype na coluna 'date' para datetime
    df_calendar_new['date'] = df_calendar_new['date'].astype('datetime64[ns]')

    # --------- CRIANDO DF_CALENDAR_CLOSED(CASOS FECHADOS) ---------
    # df_calendar_closed -> filtrar pacientes com covid confirmados; groupby(Municipio, DataEncerramento); contar ocorrencias
    df_calendar_closed = df[df['Classificacao']=='Confirmados'].groupby(['Municipio','DataEncerramento'])['DataCadastro'].size().reset_index(name='count_closed')

    # renomendo coluna DataEncerramento
    df_calendar_closed.rename(columns={'DataEncerramento': 'date'}, inplace=True)

    # transformando o dtype na coluna 'date' para datetime
    df_calendar_closed['date'] = df_calendar_closed['date'].astype('datetime64[ns]')

    # --------- CRIANDO DF_CALENDAR_OBITOS ---------
    df_calendar_obitos = df[(df['Classificacao']=='Confirmados') & (df['Evolucao'] == 'Óbito pelo COVID-19')].groupby(['Municipio','DataEncerramento'])['DataCadastro'].size().reset_index(name='count_obito')

    # renomendo coluna DataEncerramento
    df_calendar_obitos.rename(columns={'DataEncerramento': 'date'}, inplace=True)

    # transformando o dtype na coluna 'date' para datetime
    df_calendar_obitos['date'] = df_calendar_obitos['date'].astype('datetime64[ns]')

    # --------- MERGE ENTRE OS DFs CRIADOS ---------
    df_calendar_temp = pd.merge(df_calendar_new, df_calendar_closed, how='outer', left_on=['Municipio', 'date'], right_on=['Municipio', 'date'])
    df_calendar = pd.merge(df_calendar_temp, df_calendar_obitos, how='outer', left_on=['Municipio', 'date'], right_on=['Municipio', 'date'])

    # --------- FILTRO DE DATAS ---------
    # filtrando por período entre 2020 e 2021 (extrair dados com datas erradas)
    df_calendar = df_calendar[(df_calendar['date'].dt.year>=2020) & (df_calendar['date'].dt.year<2022)]

    # --------- DF DE DATAS AUXILIAR ---------
    # criando df_date_aux para preencher o df_calendar com todas as datas do períodom, e fazendo o merge com o df_calendar por cidade
    municipios = df_calendar['Municipio'].unique()

    for i in municipios:
        delta = df_calendar[df_calendar['Municipio']==i]['date'].max() - df_calendar[df_calendar['Municipio']==i]['date'].min()
        df_date_aux = pd.DataFrame({'Municipio':i, 'date': pd.date_range(df_calendar[df_calendar['Municipio']==i]['date'].min(), periods=delta.days).tolist()})
        df_calendar = pd.merge(df_calendar, df_date_aux, how='outer', left_on=['Municipio', 'date'], right_on=['Municipio', 'date'])

    # --------- AJUSTANDO DF_CALENDAR ---------
    # organizando por cidade/data
    df_calendar = df_calendar.sort_values(["Municipio", "date"]).reset_index()
    df_calendar = df_calendar.drop('index', axis=1)

    # --------- DEALING WITH NAN ---------
    # preenchendo Nan com zero(0)
    for i in ['count_new', 'count_closed', 'count_obito']:
        df_calendar[i] = df_calendar[i].fillna(0)

    # --------- FEATURE ENGINEERING ---------
    # criando coluna acumulado por cidade
    municipios = df_calendar['Municipio'].unique()
    acum = []
    for idx, i in enumerate(df_calendar['date']):
        if df_calendar['Municipio'].iloc[idx] == df_calendar['Municipio'].iloc[idx-1]:
            try:
                acum.append(acum[idx-1] + df_calendar['count_new'].iloc[idx] - df_calendar['count_closed'].iloc[idx])
            except:
                acum.append(df_calendar['count_new'].iloc[idx] - df_calendar['count_closed'].iloc[idx])
        else:
            acum.append(0 + df_calendar['count_new'].iloc[idx] - df_calendar['count_closed'].iloc[idx])

    df_calendar['acum'] = acum

    # criando coluna casos recuperados por cidade
    df_calendar['recup'] = df_calendar['count_closed'] - df_calendar['count_obito']


    # criando colunas de dia/semana/dia_da_semana/mes/ano
    df_calendar['day'] = [i.day for i in df_calendar['date']]
    df_calendar['week'] = [i.week for i in df_calendar['date']]
    df_calendar['weekday'] = [i.weekday() for i in df_calendar['date']]
    df_calendar['month'] = [i.month for i in df_calendar['date']]
    df_calendar['year'] = [i.year for i in df_calendar['date']]


    # ---------- CRIANDO COLUNAS PARA SEREM UTILIZADAS NO PLOT DE RESUMO ----------
    cidades = df_calendar['Municipio'].unique()

    # --- TOTAL CASOS FATAIS ACUMULADOS POR DIA POR CIDADE ---
    fatais = []
    for i in cidades:
        for j in range(len(df_calendar[df_calendar['Municipio']==i])):
            if j == 0:
                total = df_calendar[df_calendar['Municipio']==i]['count_obito'].iloc[j]
                fatais.append(total)
            else:
                total = total+df_calendar[df_calendar['Municipio']==i]['count_obito'].iloc[j]
                fatais.append(total)

    df_calendar['fatais'] = fatais


    # --- TOTAL CASOS CONFIRMADOS ACUMULADOS POR DIA POR CIDADE ---
    confirmados = []
    for i in cidades:
        for j in range(len(df_calendar[df_calendar['Municipio']==i])):
            if j == 0:
                total = df_calendar[df_calendar['Municipio']==i]['count_new'].iloc[j]
                confirmados.append(total)
            else:
                total = total+df_calendar[df_calendar['Municipio']==i]['count_new'].iloc[j]
                confirmados.append(total)

    df_calendar['confirmados'] = confirmados

    # --- TOTAL CASOS RECUPERADOS ACUMULADOS POR DIA POR CIDADE ---
    recuperados = []
    for i in cidades:
        for j in range(len(df_calendar[df_calendar['Municipio']==i])):
            if j == 0:
                total = df_calendar[df_calendar['Municipio']==i]['recup'].iloc[j]
                recuperados.append(total)
            else:
                total = total+df_calendar[df_calendar['Municipio']==i]['recup'].iloc[j]
                recuperados.append(total)

    df_calendar['recuperados'] = recuperados


    # --------- SALVANDO DADOS TRATADOS EM .PARQUET ---------
    df_calendar.to_parquet('../../app/home/data/treated_data/MICRODADOS_tratado.parquet')


# funcao para mudar sistema de coordenadas do arquivo GOEjason.
def utmToLatLng(zone, easting, northing, northernHemisphere=False):
   if not northernHemisphere:
     northing = 10000000 - northing

   a = 6378137
   e = 0.081819191
   e1sq = 0.006739497
   k0 = 0.9996

   arc = northing / k0
   mu = arc / (a * (1 - math.pow(e, 2) / 4.0 - 3 * math.pow(e, 4) / 64.0 - 5 * math.pow(e, 6) / 256.0))

   ei = (1 - math.pow((1 - e * e), (1 / 2.0))) / (1 + math.pow((1 - e * e), (1 / 2.0)))

   ca = 3 * ei / 2 - 27 * math.pow(ei, 3) / 32.0

   cb = 21 * math.pow(ei, 2) / 16 - 55 * math.pow(ei, 4) / 32
   cc = 151 * math.pow(ei, 3) / 96
   cd = 1097 * math.pow(ei, 4) / 512
   phi1 = mu + ca * math.sin(2 * mu) + cb * math.sin(4 * mu) + cc * math.sin(6 * mu) + cd * math.sin(8 * mu)

   n0 = a / math.pow((1 - math.pow((e * math.sin(phi1)), 2)), (1 / 2.0))

   r0 = a * (1 - e * e) / math.pow((1 - math.pow((e * math.sin(phi1)), 2)), (3 / 2.0))
   fact1 = n0 * math.tan(phi1) / r0

   _a1 = 500000 - easting
   dd0 = _a1 / (n0 * k0)
   fact2 = dd0 * dd0 / 2

   t0 = math.pow(math.tan(phi1), 2)
   Q0 = e1sq * math.pow(math.cos(phi1), 2)
   fact3 = (5 + 3 * t0 + 10 * Q0 - 4 * Q0 * Q0 - 9 * e1sq) * math.pow(dd0, 4) / 24

   fact4 = (61 + 90 * t0 + 298 * Q0 + 45 * t0 * t0 - 252 * e1sq - 3 * Q0 * Q0) * math.pow(dd0, 6) / 720

   lof1 = _a1 / (n0 * k0)
   lof2 = (1 + 2 * t0 + Q0) * math.pow(dd0, 3) / 6.0
   lof3 = (5 - 2 * Q0 + 28 * t0 - 3 * math.pow(Q0, 2) + 8 * e1sq + 24 * math.pow(t0, 2)) * math.pow(dd0, 5) / 120
   _a2 = (lof1 - lof2 + lof3) / math.cos(phi1)
   _a3 = _a2 * 180 / math.pi

   latitude = 180 * (phi1 - fact1 * (fact2 + fact3 + fact4)) / math.pi

   if not northernHemisphere:
     latitude = -latitude

   longitude = ((zone > 0) and (6 * zone - 183.0) or 3.0) - _a3

   return [longitude, latitude]


def tratando_transferencias_estaduais(transferencias):
   import pandas as pd

   # >>>>>>>>>>>>>>IMPORTAR AQUI DF POR FUNCAO<<<<<<<<<<<<<<<<<<

   # transferencias = uallas -> ver se algum tratamento que esta sendo feito aqui, ja esta sendo feito pela sua funcao

   #############################################################


   # mudando os codigos municipais errados das tres cidades com homonimos
   # * Boa Esperança (MG - 3107109) -> (ES - 3201001)
   # * Presidente Kenedy (TO - 1718402) -> (ES - 3204302)
   # * Viana (MA - 2112803) -> (ES - 3205101)
   for i in range(len(transferencias)):
       # Boa Esperança
       if transferencias.loc[i, 'CodMunicipio'] == 3107109:
           transferencias.loc[i, 'CodMunicipio'] = 3201001
       # Presidente Kenedy
       elif transferencias.loc[i, 'CodMunicipio'] == 1718402:
           transferencias.loc[i, 'CodMunicipio'] = 3204302
       # Viana
       elif transferencias.loc[i, 'CodMunicipio'] == 2112803:
           transferencias.loc[i, 'CodMunicipio'] = 3205101


   # transformando colunas pertinentes em numbers
   calumns_to_num = ['IcmsTotal', 'Ipi', 'Ipva', 'FundoReducaoDesigualdades']
   for x in calumns_to_num:
       transferencias[x] = [round(float(transferencias[x].iloc[i].replace(',', '.')), 2) for i in range(len(transferencias))]

   # criando coluna de totais
   transferencias['TotalRepassado'] = transferencias[calumns_to_num[0]] + transferencias[calumns_to_num[1]] + transferencias[calumns_to_num[2]] + transferencias[calumns_to_num[3]]

   # criando coluna com datatype
   transferencias['Data'] = [datetime.datetime(transferencias['Ano'].iloc[i], transferencias['Mes'].iloc[i], 28) for i in range(len(transferencias))]

   transferencias.to_parquet('path/transf_estadual_tratado.parquet') # uallas -> ver path


def tratando_dados_populacao():
   import pandas as pd

   # populacao_2018 = pd.read_csv('../dados/originais/populacao_2018.csv')[['UF', 'COD. UF', 'COD. MUNIC', 'NOME DO MUNICÍPIO', 'POPULAÇÃO ESTIMADA']]
   # populacao_2019 = pd.read_csv('../dados/originais/populacao_2019.csv')[['UF', 'COD. UF', 'COD. MUNIC', 'NOME DO MUNICÍPIO', 'POPULAÇÃO ESTIMADA']]
   # populacao_2020 = pd.read_csv('../dados/originais/populacao_2020.csv')[['UF', 'COD. UF', 'COD. MUNIC', 'NOME DO MUNICÍPIO', 'POPULAÇÃO ESTIMADA']]
   # populacao_2021 = pd.read_csv('../dados/originais/populacao_2021.csv')[['UF', 'COD. UF', 'COD. MUNIC', 'NOME DO MUNICÍPIO', 'POPULAÇÃO ESTIMADA']]

   # filtro
   # populacao_es_2018 = populacao_2018[populacao_2018['UF']=='ES']
   # populacao_es_2019 = populacao_2019[populacao_2019['UF']=='ES']
   # populacao_es_2020 = populacao_2020[populacao_2020['UF']=='ES']
   # populacao_es_2021 = populacao_2021[populacao_2021['UF']=='ES']


   # >>>>>>>>>>>>>>>>>>>>> ADICIONAR DF VIA FUNCAO AQUI <<<<<<<<<<<<<<<<<<<

   # populacao =
   ########################################################################

   # ----------------- CODIGO ADICIONAL NO TRATAMENTO PRÉ CONCATENACAO --------------- uallas -> acho que vamos ter que adionar esse pedaço na tua funcao de tratamento pois precisa ser antes do concat
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

   # -----------------------------------------------------------------------------------
   # merge
   # populacao_es = pd.concat([populacao_es_2018, populacao_es_2019, populacao_es_2020, populacao_es_2021], ignore_index=True)

   # transformando populacao estimanda em int
   populacao_es['POPULAÇÃO ESTIMADA'] = [int(i.replace(',', '')) for i in populacao_es['POPULAÇÃO ESTIMADA']]

   populacao_es.to_parquet('path/populacao_es_tratado.parquet')
