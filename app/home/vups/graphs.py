from plotly.data import gapminder
import plotly.express as px
from . import const
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pandas as pd
import os


def plot_kpi_percentage_progress():
    """
    Global Actual Progress
    Baseline 46%
    """
    fig_c1 = go.Figure(
        go.Indicator(
            mode="number+delta",
            value=35,
            number={
                "suffix": "%",
                "font": {"size": 36, "color": "#008080", "family": "Arial"},
            },
            delta={"position": "bottom", "reference": 46, "relative": False},
            domain={"x": [0, 1], "y": [0, 1]},
        )
    )
    fig_c1.update_layout(
        autosize=False,
        width=350,
        height=86,
        margin=dict(l=20, r=20, b=20, t=30),
        paper_bgcolor="#fbfff0",
        font={"size": 20},
    )
    return fig_c1


def plot_kpi_spend_hours():
    """
    Global Spend Hours
    Baseline 92.700
    """
    fig_c2 = go.Figure(
        go.Indicator(
            mode="number+delta",
            value=73500,
            number={
                "suffix": " HH",
                "font": {"size": 40, "color": "#008080", "family": "Arial"},
                "valueformat": ",f",
            },
            delta={"position": "bottom", "reference": 92700},
            domain={"x": [0, 1], "y": [0, 1]},
        )
    )
    fig_c2.update_layout(
        autosize=False,
        width=350,
        height=90,
        margin=dict(l=20, r=20, b=20, t=30),
        paper_bgcolor="#fbfff0",
        font={"size": 20},
    )
    fig_c2.update_traces(
        delta_decreasing_color="#3D9970",
        delta_increasing_color="#FF4136",
        delta_valueformat="f",
        selector=dict(type="indicator"),
    )
    return fig_c2


def plot_kpi_tcpi():
    """
    TPCI - To Complete Performance Index ≤ 1.00
    """
    fig_c3 = go.Figure(
        go.Indicator(
            mode="number+delta",
            value=1.085,
            number={"font": {"size": 40, "color": "#008080", "family": "Arial"}},
            delta={"position": "bottom", "reference": 1, "relative": False},
            domain={"x": [0, 1], "y": [0, 1]},
        )
    )
    fig_c3.update_layout(
        autosize=False,
        width=350,
        height=90,
        margin=dict(l=20, r=20, b=20, t=30),
        paper_bgcolor="#fbfff0",
        font={"size": 20},
    )
    fig_c3.update_traces(
        delta_decreasing_color="#3D9970",
        delta_increasing_color="#FF4136",
        delta_valueformat=".3f",
        selector=dict(type="indicator"),
    )
    return fig_c3


def plot_small_bar_percentage_progress():
    x = ["Actual", "Previous", "Average", "Planned"]
    y = [5.5, 4.2, 6.3, 8.5]
    fig_m_prog = go.Figure([go.Bar(x=x, y=y, text=y, textposition="auto")])
    fig_m_prog.update_layout(
        paper_bgcolor="#fbfff0",
        plot_bgcolor="#fbfff0",
        font={"color": "#008080", "family": "Arial"},
        height=100,
        width=250,
        margin=dict(l=15, r=1, b=4, t=4),
    )
    fig_m_prog.update_yaxes(title="y", visible=False, showticklabels=False)
    fig_m_prog.update_traces(marker_color="#17A2B8", selector=dict(type="bar"))
    return fig_m_prog


def plot_small_bar_spend_hours():
    x = ["Δ vs Prev", "Δ vs Aver", "Δ vs Plan"]
    y = [10, 12, 8]
    fig_m_hh = go.Figure([go.Bar(x=x, y=y, text=y, textposition="auto")])
    fig_m_hh.update_layout(
        paper_bgcolor="#fbfff0",
        plot_bgcolor="#fbfff0",
        font={"color": "#008080", "family": "Arial"},
        height=100,
        width=250,
        margin=dict(l=15, r=1, b=1, t=1),
    )
    fig_m_hh.update_yaxes(title="y", visible=False, showticklabels=False)
    fig_m_hh.update_traces(marker_color="#17A2B8", selector=dict(type="bar"))
    return fig_m_hh


data = pd.read_excel(os.path.join(const.DATADIR + "curva.xlsx"))


def plot_line_progress_actual_planned():
    y = data.loc[data.Activity_name == "Total"]
    # Create traces
    fig3 = go.Figure()
    fig3.add_trace(
        go.Scatter(
            x=y["Date"],
            y=y["Progress"],
            mode="lines",
            name="Progress",
            marker_color="#FF4136",
        )
    )
    fig3.add_trace(
        go.Scatter(
            x=y["Date"],
            y=y["Baseline"],
            mode="lines",
            name="Baseline",
            marker_color="#17A2B8",
        )
    )
    fig3.update_layout(
        title={"text": "Actual Progress vs Planned", "x": 0.5},
        paper_bgcolor="#fbfff0",
        plot_bgcolor="#fbfff0",
        font={"color": "#008080", "size": 12, "family": "Georgia"},
        height=220,
        width=540,
        legend=dict(orientation="h", yanchor="top", y=0.99, xanchor="left", x=0.01),
        margin=dict(l=1, r=1, b=1, t=30),
    )
    fig3.update_xaxes(
        showline=True,
        linewidth=1,
        linecolor="#F7F7F7",
        mirror=True,
        nticks=6,
        rangemode="tozero",
        showgrid=False,
        gridwidth=0.5,
        gridcolor="#F7F7F7",
    )
    fig3.update_yaxes(
        showline=True,
        linewidth=1,
        linecolor="#F7F7F7",
        mirror=True,
        nticks=10,
        rangemode="tozero",
        showgrid=True,
        gridwidth=0.5,
        gridcolor="#F7F7F7",
    )
    fig3.layout.yaxis.tickformat = ",.0%"
    return fig3


def plot_widget_cost_variance():
    fig_cv = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=1.05,
            number={
                "font": {"size": 22, "color": "#008080", "family": "Arial"},
                "valueformat": "#,##0",
            },
            domain={"x": [0, 1], "y": [0, 1]},
            gauge={
                "axis": {"range": [None, 1.5], "tickwidth": 1, "tickcolor": "black"},
                "bar": {"color": "#06282d"},
                "bgcolor": "white",
                "steps": [
                    {"range": [0, 1], "color": "#FF4136"},
                    {"range": [1, 1.5], "color": "#3D9970"},
                ],
            },
        )
    )

    fig_cv.update_layout(
        paper_bgcolor="#fbfff0",
        font={"color": "#008080", "family": "Arial"},
        height=135,
        width=250,
        margin=dict(l=10, r=10, b=15, t=20),
    )
    return fig_cv


def plot_widget_schedule_variance():
    fig_sv = go.Figure(
        go.Indicator(
            mode="gauge+number+delta",
            value=0.95,
            number={
                "font": {"size": 22, "color": "#008080", "family": "Arial"},
                "valueformat": "#,##0",
            },
            domain={"x": [0, 1], "y": [0, 1]},
            gauge={
                "axis": {"range": [None, 1.5], "tickwidth": 1, "tickcolor": "black"},
                "bar": {"color": "#06282d"},
                "bgcolor": "white",
                "steps": [
                    {"range": [0, 1], "color": "#FF4136"},
                    {"range": [1, 1.5], "color": "#3D9970"},
                ],
            },
        )
    )
    fig_sv.update_layout(
        paper_bgcolor="#fbfff0",
        font={"color": "#008080", "family": "Arial"},
        height=135,
        width=250,
        margin=dict(l=10, r=10, b=15, t=20),
    )
    return fig_sv


def plot_bar_hours_spend_planned():
    y = data.loc[data.Activity_name == "Total"]
    y = data.loc[data.Activity_name == "Total"]
    fig_hh = go.Figure()
    fig_hh.add_trace(
        go.Bar(
            x=y["Date"], y=y["Spend_Hours"], name="Spend Hours", marker_color="#FF4136"
        )
    )
    fig_hh.add_trace(
        go.Bar(
            x=y["Date"],
            y=y["Planned_Hours"],
            name="Planned Hours",
            marker_color="#17A2B8",
        )
    )
    fig_hh.update_layout(
        barmode="group",
        title={"text": "Spend Hours vs Planned", "x": 0.5},
        paper_bgcolor="#fbfff0",
        plot_bgcolor="#fbfff0",
        font={"color": "#008080", "family": "Georgia"},
        height=250,
        width=540,
        legend=dict(orientation="h", yanchor="top", y=0.99, xanchor="left", x=0.01),
        margin=dict(l=5, r=1, b=1, t=25),
    )
    fig_hh.update_xaxes(
        showline=True,
        linewidth=1,
        linecolor="#F7F7F7",
        mirror=True,
        nticks=6,
        rangemode="tozero",
        showgrid=False,
        gridwidth=0.5,
        gridcolor="#F7F7F7",
    )
    fig_hh.update_yaxes(
        showline=True,
        linewidth=1,
        linecolor="#F7F7F7",
        mirror=True,
        nticks=10,
        rangemode="tozero",
        showgrid=False,
        gridwidth=0.5,
        gridcolor="#F7F7F7",
    )
    return fig_hh


def plot_gantt():
    # *******Gantt Chart
    df = pd.DataFrame(
        [
            dict(Disc="Civ", Start="2021-01-04", Finish="2021-08-10"),
            dict(Disc="Mec", Start="2021-03-05", Finish="2021-09-15"),
            dict(Disc="Pip", Start="2021-04-20", Finish="2021-11-30"),
            dict(Disc="Ele", Start="2021-05-20", Finish="2021-12-05"),
            dict(Disc="Ins", Start="2021-06-20", Finish="2021-12-20"),
            dict(Disc="Com", Start="2021-07-20", Finish="2021-12-30"),
        ]
    )
    fig2 = px.timeline(df, x_start="Start", x_end="Finish", y="Disc")
    fig2.update_yaxes(autorange="reversed")
    fig2.update_layout(
        title={"text": "Main dates", "x": 0.5},
        plot_bgcolor="#eef9ea",
        paper_bgcolor="#eef9ea",
        font={"color": "#008080", "family": "Georgia"},
        height=340,
        width=550,
        margin=dict(l=51, r=5, b=10, t=50),
    )
    fig2.update_traces(marker_color="#17A2B8", selector=dict(type="bar"))
    return fig2


def plot_calendar_heatmap(
    cidade="AFONSO CLAUDIO", tipo="NOVOS CASOS", mes_analise=1, ano_analise=2021
):
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
    # print('###################################################################')
    # print('Calendar Heatmap')
    # t = time()

    COLUMNS = [
        "Municipio",
        "Classificacao",
        "DataDiagnostico",
        "DataCadastro",
        "DataEncerramento",
    ]

    # --------- FILTRANDO DF PARA CIDADES DO ES ---------
    filtro_es = [
        "AGUIA BRANCA",
        "ALTO RIO NOVO",
        "ARACRUZ",
        "BAIXO GUANDU",
        "COLATINA",
        "GOVERNADOR LINDENBERG",
        "IBIRACU",
        "JOAO NEIVA",
        "LINHARES",
        "MANTENOPOLIS",
        "MARILANDIA",
        "PANCAS",
        "RIO BANANAL",
        "SAO DOMINGOS DO NORTE",
        "SAO GABRIEL DA PALHA",
        "SAO ROQUE DO CANAA",
        "SOORETAMA",
        "VILA VALERIO",
        "AFONSO CLAUDIO",
        "BREJETUBA",
        "CARIACICA",
        "CONCEICAO DO CASTELO",
        "DOMINGOS MARTINS",
        "FUNDAO",
        "GUARAPARI",
        "IBATIBA",
        "ITAGUACU",
        "ITARANA",
        "LARANJA DA TERRA",
        "MARECHAL FLORIANO",
        "SANTA LEOPOLDINA",
        "SANTA MARIA DE JETIBA",
        "SANTA TERESA",
        "SERRA",
        "VENDA NOVA DO IMIGRANTE",
        "VIANA",
        "VILA VELHA",
        "VITORIA",
        "AGUA DOCE DO NORTE",
        "BARRA DE SAO FRANCISCO",
        "BOA ESPERANCA",
        "CONCEICAO DA BARRA",
        "ECOPORANGA",
        "JAGUARE",
        "MONTANHA",
        "MUCURICI",
        "NOVA VENECIA",
        "PEDRO CANARIO",
        "PINHEIROS",
        "PONTO BELO",
        "SAO MATEUS",
        "VILA PAVAO",
        "ALEGRE",
        "ALFREDO CHAVES",
        "ANCHIETA",
        "APIACA",
        "ATILIO VIVACQUA",
        "BOM JESUS DO NORTE",
        "CACHOEIRO DE ITAPEMIRIM",
        "CASTELO",
        "DIVINO DE SAO LOURENCO",
        "DORES DO RIO PRETO",
        "GUACUI",
        "IBITIRAMA",
        "ICONHA",
        "IRUPI",
        "ITAPEMIRIM",
        "IUNA",
        "JERONIMO MONTEIRO",
        "MARATAIZES",
        "MIMOSO DO SUL",
        "MUNIZ FREIRE",
        "MUQUI",
        "PIUMA",
        "PRESIDENTE KENNEDY",
        "RIO NOVO DO SUL",
        "SAO JOSE DO CALCADO",
        "VARGEM ALTA",
    ]

    # --------- BUSCANDO DF ---------
    df = datasets.microdados(columns=COLUMNS, field="Municipio", value=filtro_es)
    # df = datasets.microdados(columns=COLUMNS)
    # df = df[df['Municipio']==filtro_es]

    # --------- CRIANDO DF_CALENDAR_NEW(CASOS NOVOS) E DF_CALENDAR_CLOSED(CASOS FECHADOS) ---------
    # df_calendar_new -> filtrar pacientes com covid confirmados; groupby(Municipio, DataDiagnostico); contar ocorrencias
    df_calendar_new = (
        df[df["Classificacao"] == "Confirmados"]
        .groupby(["Municipio", "DataDiagnostico"])["DataCadastro"]
        .size()
        .reset_index(name="count_new")
    )

    # renomendo coluna DataDiagnostico
    df_calendar_new.rename(columns={"DataDiagnostico": "date"}, inplace=True)

    # transformando o dtype na coluna 'date' para datetime
    df_calendar_new["date"] = df_calendar_new["date"].astype("datetime64[ns]")

    # df_calendar_closed -> filtrar pacientes com covid confirmados; groupby(Municipio, DataEncerramento); contar ocorrencias
    df_calendar_closed = (
        df[df["Classificacao"] == "Confirmados"]
        .groupby(["Municipio", "DataEncerramento"])["DataCadastro"]
        .size()
        .reset_index(name="count_closed")
    )

    # --- ATENCAO!!! --- DataEncerramento NAO esta sendo transformada automaticamente, por isso vamos forçar essa transformação aqui
    # após corrigido, retirar esse pedaço de código
    # transformando DataEncerramento em datatype
    # df_calendar_closed['DataEncerramento'] = pd.to_datetime(df_calendar_closed['DataEncerramento'], format='%Y-%m-%d')

    # transformando valores de casos fechados em negativo
    df_calendar_closed["count_closed"] = df_calendar_closed["count_closed"] * -1

    # renomendo coluna DataEncerramento
    df_calendar_closed.rename(columns={"DataEncerramento": "date"}, inplace=True)

    # transformando o dtype na coluna 'date' para datetime
    df_calendar_closed["date"] = df_calendar_closed["date"].astype("datetime64[ns]")

    # --------- MERGE ENTRE OS DOIS DFs CRIADOS ---------
    df_calendar = pd.merge(
        df_calendar_new,
        df_calendar_closed,
        how="outer",
        left_on=["Municipio", "date"],
        right_on=["Municipio", "date"],
    )

    # --------- TRABLHANDO O NOVO DF ---------
    # organizando por cidade/data
    df_calendar = df_calendar.sort_values(["Municipio", "date"]).reset_index()

    # preenchendo Nan com zero(0)
    for i in ["count_new", "count_closed"]:
        df_calendar[i] = df_calendar[i].fillna(0)

    # criando coluna acumulado por cidade
    municipios = df_calendar["Municipio"].unique()
    acum = []
    for idx, i in enumerate(df_calendar["date"]):
        if df_calendar["Municipio"].iloc[idx] == df_calendar["Municipio"].iloc[idx - 1]:
            try:
                acum.append(
                    acum[idx - 1]
                    + df_calendar["count_new"].iloc[idx]
                    + df_calendar["count_closed"].iloc[idx]
                )
            except:
                acum.append(
                    df_calendar["count_new"].iloc[idx]
                    + df_calendar["count_closed"].iloc[idx]
                )
        else:
            acum.append(
                0
                + df_calendar["count_new"].iloc[idx]
                + df_calendar["count_closed"].iloc[idx]
            )

    df_calendar["acum"] = acum

    # criando colunas de dia/semana/dia_da_semana/mes/ano
    df_calendar["day"] = [i.day for i in df_calendar["date"]]
    df_calendar["week"] = [i.week for i in df_calendar["date"]]
    df_calendar["weekday"] = [i.weekday() for i in df_calendar["date"]]
    df_calendar["month"] = [i.month for i in df_calendar["date"]]
    df_calendar["year"] = [i.year for i in df_calendar["date"]]

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

    # aplicando filtros
    if tipo == "NOVOS CASOS":
        df_calendar_display = (
            df_calendar[
                (df_calendar["Municipio"] == cidade)
                & (df_calendar["month"] == mes_analise)
                & (df_calendar["year"] == ano_analise)
            ][
                [
                    "Municipio",
                    "date",
                    "day",
                    "week",
                    "weekday",
                    "month",
                    "year",
                    "count_new",
                ]
            ]
            .sort_values(by=["day"])
            .reset_index()
            .drop(columns=["index"])
        )
    else:
        df_calendar_display = (
            df_calendar[
                (df_calendar["Municipio"] == cidade)
                & (df_calendar["month"] == mes_analise)
                & (df_calendar["year"] == ano_analise)
            ][["Municipio", "date", "day", "week", "weekday", "month", "year", "acum"]]
            .sort_values(by=["day"])
            .reset_index()
            .drop(columns=["index"])
        )

    # criando listagem com a contagem de casos para cada dia do mes e as informações da semana do ano e dia da semana
    # preenchendo com zero os dias em que nao tiveram registros
    info_dia = []
    contador = 0
    for i in range(1, n_dias + 1):
        if i == df_calendar_display["day"].iloc[contador]:
            dia = i
            numero_casos = int(df_calendar_display.iloc[contador, -1])
            semana_do_ano = df_calendar_display["week"].iloc[contador]
            dia_da_semana = df_calendar_display["weekday"].iloc[contador]
            if contador < len(df_calendar_display) - 1:
                contador = contador + 1
        else:
            dia = i
            numero_casos = 0
            semana_do_ano = int(datetime(ano_analise, mes_analise, i).strftime("%W"))
            dia_da_semana = datetime(ano_analise, mes_analise, i).weekday()

        info_dia.append([dia, numero_casos, semana_do_ano, dia_da_semana])

    # separando essa lista em outras 4
    dias, n_casos, semana, dia_semana = zip(*info_dia)

    # criando lista com o numero de casos de cada dia do mes e separado em lista por semana
    final_casos = []
    parcial_casos = []
    for i, week in enumerate(semana):
        if i == 0:
            parcial_casos.append(n_casos[i])
        elif i == n_dias - 1:
            parcial_casos.append(n_casos[i])
            final_casos.append(parcial_casos)
        else:
            if week == semana[i - 1]:
                parcial_casos.append(n_casos[i])
            else:
                final_casos.append(parcial_casos)
                parcial_casos = []
                parcial_casos.append(n_casos[i])

    # calculando o valor maximo da quantidade de casos para servir como ponto maximo da escala de cores
    max_value = []
    for i in range(len(final_casos)):
        max_value.append(max(final_casos[i]))

    max_value = max(max_value)

    # preenchendo valores relativos aos dias que completam as semanas com menos de 7 dias (inicio/final)
    # o max_value serve para ajustar a cor (branco) que vai ser printado no heatmap para esses valores de preenchimento
    while len(final_casos[0]) < 7:
        final_casos[0].insert(0, 0.001 * max_value)

    while len(final_casos[-1]) < 7:
        final_casos[-1].append(0.001 * max_value)

    # transformando valores a serem pintados em cinza, em negativo
    for i in range(len(final_casos)):
        for j in range(len(final_casos[i])):
            if final_casos[i][j] > 0 and final_casos[i][j] < 1:
                final_casos[i][j] = final_casos[i][j] * -1

    # tranformando dias de int para str
    dias = list(map(str, dias))

    # preenchendo lista de acordo com o exigido para o plot (lista de listas para cada semana do mes)
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

    # preenchendo as semanas que ficaram com menos de 7 dias com os dias do mes anterior e subsequente
    if mes_analise in [1, 2, 4, 6, 8, 9, 11]:
        contador = 0
        while len(final_dias[0]) < 7:
            final_dias[0].insert(0, str(31 - contador))
            contador += 1
        contador = 0
        while len(final_dias[-1]) < 7:
            final_dias[-1].append(str(contador + 1))
            contador += 1
    elif mes_analise == 3 and ano_analise != 2020:
        contador = 0
        while len(final_dias[0]) < 7:
            final_dias[0].insert(0, str(28 - contador))
            contador += 1
        contador = 0
        while len(final_dias[-1]) < 7:
            final_dias[-1].append(str(contador + 1))
            contador += 1
    elif mes_analise == 3 and ano_analise == 2020:
        contador = 0
        while len(final_dias[0]) < 7:
            final_dias[0].insert(0, str(29 - contador))
            contador += 1
        contador = 0
        while len(final_dias[-1]) < 7:
            final_dias[-1].append(str(contador + 1))
            contador += 1
    elif mes_analise in [5, 7, 10, 12]:
        contador = 0
        while len(final_dias[0]) < 7:
            final_dias[0].insert(0, str(30 - contador))
            contador += 1
        contador = 0
        while len(final_dias[-1]) < 7:
            final_dias[-1].append(str(contador + 1))
            contador += 1

    # criando os labels das semanas
    y_label = []
    for i in range(len(final_dias)):
        y_label.append("Semana " + str(i + 1))

    # --------- CALENDAR HEATMAP PLOT ---------

    # plot do heatmap estilo calendario (com a quantida de casos por dia)

    import plotly.figure_factory as ff

    z = final_casos[::-1]

    x = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sabado", "Domingo"]
    y = y_label[::-1]

    z_text = final_dias[::-1]

    fig1 = ff.create_annotated_heatmap(
        z,
        x=x,
        y=y,
        annotation_text=z_text,
        colorscale=[
            [0.0, "rgb(235, 236, 240)"],  # valores negativos
            [0.00001, "rgb(255,255,255)"],
            [0.1, "rgb(255,245,240)"],
            [0.2, "rgb(252,201,180)"],
            [0.4, "rgb(251,136,104)"],
            [0.6, "rgb(242,67,49)"],
            [0.8, "rgb(187,19,25)"],
            [1.0, "rgb(115,2,23)"],
        ],
        showscale=True,
    )

    # titulo plot
    meses = [
        "Janeiro",
        "Feveireiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro",
    ]
    mes_plot = meses[mes_analise - 1]
    if tipo == "NOVOS CASOS":
        fig1.update_layout(
            title_text="Casos Novos por dia - "
            + cidade.title()
            + " - "
            + mes_plot
            + " "
            + str(ano_analise),
            title_x=0.5,
        )
    else:
        fig1.update_layout(
            title_text="Casos Acumulados - "
            + cidade.title()
            + " - "
            + mes_plot
            + " "
            + str(ano_analise),
            title_x=0.5,
        )

    # fig1.update_layout({
    # 'plot_bgcolor': 'rgba(0,0,0,0)',
    # 'paper_bgcolor': 'rgba(0,0,0,0)'})

    # print("Tempo decorrido: " + str( time() - t) + " s.")
    # print('###################################################################')

    return fig1


def plot_comp_tributos_cidades(
    list_cidades=["ARACRUZ", "ANCHIETA", "CARIACICA", "GUARAPARI", "LINHARES", "PIUMA"]
):
    # import pandas as pd
    # import datetime

    # ##########################################
    # Obtendo os dados
    # DB's PARA IMPORTAR: transfestadomunicipios e populacao
    # ==========================================
    # fonte: https://dados.es.gov.br/dataset/portal-da-transparencia-transferencias-para-municipios
    transf_2018 = datasets.transfestadomunicipios_2018()
    transf_2019 = datasets.transfestadomunicipios_2019()
    transf_2020 = datasets.transfestadomunicipios_2020()
    transf_2021 = datasets.transfestadomunicipios_2021()

    # juntando informacoes em 1 dataset
    # ==========================================
    transferencias = pd.concat(
        [transf_2018, transf_2019, transf_2020, transf_2021], ignore_index=True
    )

    # Mudando os codigos municipais errados das tres cidades com homonimos
    # ====================================================================
    # * Boa Esperança (MG - 3107109) -> (ES - 3201001)
    # * Presidente Keneddy (TO - 1718402) -> (ES - 3204302)
    # * Viana (MA - 2112803) -> (ES - 3205101)

    for i in range(len(transferencias)):
        # Boa Esperança
        if transferencias.loc[i, "CodMunicipio"] == 3107109:
            transferencias.loc[i, "CodMunicipio"] = 3201001
        elif transferencias.loc[i, "CodMunicipio"] == 1718402:
            transferencias.loc[i, "CodMunicipio"] = 3204302
        elif transferencias.loc[i, "CodMunicipio"] == 2112803:
            transferencias.loc[i, "CodMunicipio"] = 3205101

    # Transformando colunas pertinentes em numbers
    # ====================================================================
    calumns_to_num = ["IcmsTotal", "Ipi", "Ipva", "FundoReducaoDesigualdades"]
    for x in calumns_to_num:
        transferencias[x] = [
            round(float(transferencias[x].iloc[i].replace(",", ".")), 2)
            for i in range(len(transferencias))
        ]

    # Criando coluna de totais
    # ====================================================================
    transferencias["TotalRepassado"] = (
        transferencias[calumns_to_num[0]]
        + transferencias[calumns_to_num[1]]
        + transferencias[calumns_to_num[2]]
        + transferencias[calumns_to_num[3]]
    )

    # Criando coluna com datatype
    # ====================================================================
    transferencias["Data"] = [
        datetime.datetime(
            transferencias["Ano"].iloc[i], transferencias["Mes"].iloc[i], 28
        )
        for i in range(len(transferencias))
    ]

    # ##############################################################################################################################################################################
    COLUMNS = ["UF", "COD. UF", "COD. MUNIC", "NOME DO MUNICÍPIO", "POPULAÇÃO ESTIMADA"]
    populacao_2018 = datasets.populacao_2018(columns=COLUMNS)
    populacao_2019 = datasets.populacao_2019(columns=COLUMNS)
    populacao_2020 = datasets.populacao_2020(columns=COLUMNS)
    populacao_2021 = datasets.populacao_2021(columns=COLUMNS)

    populacao_es_2018 = populacao_2018[populacao_2018["UF"] == "ES"]
    populacao_es_2019 = populacao_2019[populacao_2019["UF"] == "ES"]
    populacao_es_2020 = populacao_2020[populacao_2020["UF"] == "ES"]
    populacao_es_2021 = populacao_2021[populacao_2021["UF"] == "ES"]

    # ATENCAO ARRUMAR CODIGO PARA AS 3 CIDADES CITADAS
    # Criando coluna código
    ano = 2018
    for x in [
        populacao_es_2018,
        populacao_es_2019,
        populacao_es_2020,
        populacao_es_2021,
    ]:
        x["COD.GERAL"] = [
            int(
                str(int(x["COD. UF"].iloc[i]))
                + "00"
                + str(int(x["COD. MUNIC"].iloc[i]))
            )
            if len(str(int(x["COD. MUNIC"].iloc[i]))) < 4
            else int(
                str(int(x["COD. UF"].iloc[i])) + "0" + str(int(x["COD. MUNIC"].iloc[i]))
            )
            for i in range(len(x))
        ]
        x["ANO"] = ano
        ano += 1

    populacao_es = pd.concat(
        [populacao_es_2018, populacao_es_2019, populacao_es_2020, populacao_es_2021],
        ignore_index=True,
    )
    populacao_es["POPULAÇÃO ESTIMADA"] = [
        int(i.replace(",", "")) for i in populacao_es["POPULAÇÃO ESTIMADA"]
    ]

    boolean_series = transferencias["NomeMunicipio"].isin(list_cidades)
    df_repasse = transferencias[boolean_series][
        ["NomeMunicipio", "CodMunicipio", "TotalRepassado", "Data", "Ano"]
    ]

    codigos = []
    for i in list_cidades:
        cod = transferencias[transferencias["NomeMunicipio"] == i]["CodMunicipio"].iloc[
            0
        ]
        codigos.append(cod)

    boolean_series = populacao_es["COD.GERAL"].isin(codigos)
    df_pop = populacao_es[boolean_series][["COD.GERAL", "POPULAÇÃO ESTIMADA", "ANO"]]

    # merge
    df = df_repasse.merge(
        df_pop,
        how="inner",
        left_on=["CodMunicipio", "Ano"],
        right_on=["COD.GERAL", "ANO"],
    )
    df = df.drop(columns=["COD.GERAL"])

    # column arrec_percapita
    df["RepassPercapita"] = [
        round(df["TotalRepassado"].iloc[i] / df["POPULAÇÃO ESTIMADA"].iloc[0], 2)
        for i in range(len(df))
    ]

    # plot percapita
    import plotly.graph_objects as go

    fig = go.Figure()
    for i in range(len(list_cidades)):
        fig.add_trace(
            go.Scatter(
                y=df[df["NomeMunicipio"] == list_cidades[i]]["RepassPercapita"],
                x=df[df["NomeMunicipio"] == list_cidades[i]]["Data"],
                mode="lines",
                name=list_cidades[i],
            )
        )
    return fig


gapminder = px.data.gapminder()


def plot_slider_bubbles(df=gapminder):
    fig = px.scatter(
        df,
        x="gdpPercap",
        y="lifeExp",
        animation_frame="year",
        animation_group="country",
        size="pop",
        color="continent",
        hover_name="country",
        log_x=True,
        size_max=55,
        range_x=[100, 100000],
        range_y=[25, 90],
    )

    fig["layout"].pop("updatemenus")

    return fig
