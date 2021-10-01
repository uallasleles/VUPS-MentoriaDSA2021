# -*- encoding: utf-8 -*-
"""
Programa de Mentoria DSA 2021
"""

import os
import io
import pandas as pd

# from pandas.io.formats.format import CategoricalFormatter
import plotly.express as px
from . import const
import folium
import datetime
import plotly.figure_factory as ff
import plotly.graph_objects as go
import warnings
import validators
import requests

# Ignorando mensagens de avisos.
warnings.filterwarnings("ignore")

# Formata ponto flutuante como string com 2 casas decimais
pd.options.display.float_format = '{:.2f}'.format


def get_data(
    filepath_or_buffer=None,
    usecols=None,
    nrows=None,
    sep=None,
    encoding=None,
    warn_bad_lines=None,
    error_bad_lines=None,
    dtype=None,
    mapa=None,
    memory_map=True
):

    filename, file_extension = os.path.splitext(os.path.basename(filepath_or_buffer))
    
    if file_extension == ".csv":
        # for url in filepath_or_buffer:
        #     pass

        if validators.url(filepath_or_buffer):
            r = requests.get(filepath_or_buffer, stream=True)
            
            filepath_or_buffer = os.path.join(const.DATADIR, "{}.{}".format(filename.upper(), file_extension))
            with open(filepath_or_buffer, 'wb') as fd:
                for chunk in r.iter_content(chunk_size=128):
                    fd.write(chunk)

        _PARAMS = {
            "filepath_or_buffer": filepath_or_buffer,
            "iterator": True,
            "chunksize": 128,
            "usecols": usecols,
            "sep": sep,
            "nrows": nrows,
            "encoding": encoding,
            "warn_bad_lines": warn_bad_lines,
            "error_bad_lines": error_bad_lines,
            "parse_dates": True,
            "dtype": dtype,
            "memory_map": memory_map
        }

        iter = pd.read_csv(**_PARAMS)
        dataset = pd.concat(iter, ignore_index=True)
            
        dataset = dtype_transform(dataset, mapa)
        file_extension = convert_to_parquet([dataset], filename)
        filepath_or_buffer = os.path.join(const.DATADIR, "{}.{}".format(filename.upper(), file_extension))

    if file_extension == ".parquet":
        _PARAMS = {
            "path": filepath_or_buffer, 
            "columns": usecols
        }
        dataset = pd.read_parquet(**_PARAMS)
            
    return dataset


def convert_to_parquet(lst_dfs: list, filename=None):
    if len(lst_dfs) > 1:
        df = pd.concat(lst_dfs, ignore_index=True)
    else:
        df = lst_dfs[0]

    filepath_pqt = const.DATADIR + "{}.parquet".format(filename)
    
    df.to_parquet(filepath_pqt)
    resp = '.parquet' if os.path.exists(filepath_pqt) else '.csv'
    
    return resp


def plot_bar():
    df = pd.DataFrame(
        {
            "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
            "Amount": [4, 1, 2, 2, 4, 5],
            "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"],
        }
    )
    return px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")


def generate_table(df, max_rows=10):
    import dash_html_components as html

    return html.Table(
        [
            html.Thead(html.Tr([html.Th(col) for col in df.columns])),
            html.Tbody(
                [
                    html.Tr([html.Td(df.iloc[i][col]) for col in df.columns])
                    for i in range(min(len(df), max_rows))
                ]
            ),
        ]
    )


def plot_sexo_idade(df):
    fig = px.bar(df, x="Sexo", y="IdadeNaDataNotificacao")
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

    fig = px.scatter(
        filtered_df,
        x="gdpPercap",
        y="lifeExp",
        size="pop",
        color="continent",
        hover_name="country",
        log_x=True,
        size_max=55,
    )

    fig.update_layout(transition_duration=500)

    return fig


def plot_map_folium():
    map = folium.Map(location=[-16.3722412, -39.5757040], zoom_start=10)
    map.save("map.html")


def fn_date_cols(df):
    import re

    date_patern1 = re.compile(
        r"(19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])"
    )
    date_patern2 = re.compile(
        r"(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](19|20)\d\d"
    )

    lst_cols = []

    for n in list(df.columns):
        i = df.columns.get_loc(n)  # ÍNDICE DA COLUNA
        v = df.iloc[:, i]  # VALOR NA LINHA ZERO
        try:
            if (re.search(date_patern1, v) is not None) or (
                re.search(date_patern2, v) is not None
            ):
                lst_cols.append(n)
        except:
            pass

    return lst_cols


def fn_number_cols(df):
    lst_cols = []

    for n in list(df.columns):
        i = df.columns.get_loc(n)  # ÍNDICE DA COLUNA
        v = df.iloc[:, i]  # VALOR NA LINHA ZERO
        try:
            if float(n):  # SE PASSAR, É UM NÚMERO (Tenta converter para float)
                lst_cols.append(n)
        except:
            pass

    return lst_cols


def dtype_transform(df, mapa):

    if mapa is not None:
        date_cols = mapa.get('date_cols')
    else:
        date_cols = fn_date_cols(df)

    for c in date_cols:
        try:
            df[c] = df[c].astype("datetime64[ns]")
        except:
            pass

    cat_cols = list(df.select_dtypes(include="object").columns)
    for c in cat_cols:
        try:
            df[c] = df[c].astype("category")
        except:
            pass

    numeric_cols = fn_number_cols(df)

    for c in numeric_cols:
        i = df.columns.get_loc(c)  # ÍNDICE DA COLUNA
        v = df.iloc[:0, i]  # VALOR NA LINHA ZERO
        try:
            if float(v) and not v.isdecimal():
                try:
                    df[c] = df[c].astype("float64")
                except:
                    pass
            else:  # isdecimal() - SE NÃO PASSAR, É UM NÚMERO INTEIRO (Verifica se todos os caracteres no Unicode são decimais)
                try:
                    df[c] = df[c].astype("int64")
                except:
                    pass
        except:
            pass

    return(df)


class datasets:
    def microdados(columns=None, nrows=None, dtype={"DataObito": "object"}, field=None, value=None):
        name = "MICRODADOS"
        url = "https://bi.s3.es.gov.br/covid19/MICRODADOS.csv"
        partial_path = os.path.join(const.DATADIR, name)
        filepath_pqt = "{}.parquet".format(partial_path)
        filepath_csv = "{}.csv".format(partial_path)

        if os.path.exists(filepath_pqt):
            filepath_or_buffer = filepath_pqt
        elif os.path.exists(filepath_csv):
            filepath_or_buffer = filepath_csv
        else:
            filepath_or_buffer = url

        mapa = const.mapa_microdados

        return get_data(
            filepath_or_buffer=filepath_or_buffer,
            usecols=columns,
            nrows=nrows,
            sep=";",
            encoding="ISO-8859-1",
            warn_bad_lines=True,
            error_bad_lines=True,
            dtype=dtype,
            mapa=mapa
        )

    def microdados_bairros(columns=None, nrows=None, error_bad_lines=False, dtype=None):
        url = "https://bi.s3.es.gov.br/covid19/MICRODADOS_BAIRROS.csv"
        name = "MICRODADOS_BAIRROS"

        partial_path = os.path.join(const.DATADIR, name)
        filepath_pqt = "{}.parquet".format(partial_path)
        filepath_csv = "{}.csv".format(partial_path)

        if os.path.exists(filepath_pqt):
            filepath_or_buffer = filepath_pqt
        elif os.path.exists(filepath_csv):
            filepath_or_buffer = filepath_csv
        else:
            filepath_or_buffer = url

        mapa = None

        return get_data(
            filepath_or_buffer=filepath_or_buffer,
            usecols=columns,
            nrows=nrows,
            sep=",",
            encoding="ISO-8859-1",
            warn_bad_lines=True,
            error_bad_lines=True,
            dtype=dtype,
            mapa=mapa
        )

    def arrecadacao(columns=None, nrows=None, dtype=None):
        name = "ARRECADACAO"
        lst_urls = [] # list(const.ARRECADACAO["URLS"].values())
        
        partial_path = os.path.join(const.DATADIR, name)
        filepath_pqt = "{}.parquet".format(partial_path)
        filepath_csv = "{}.csv".format(partial_path)

        if os.path.exists(filepath_pqt):
            filepath_or_buffer = filepath_pqt
        elif os.path.exists(filepath_csv):
            filepath_or_buffer = filepath_csv
        else:
            filepath_or_buffer = lst_urls

        mapa = None

        return get_data(
            filepath_or_buffer=filepath_or_buffer,
            usecols=columns,
            nrows=nrows,
            sep=";",
            encoding="ISO-8859-1",
            warn_bad_lines=True,
            error_bad_lines=True,
            dtype=dtype,
            mapa=mapa
        )

    def arrecadacao_1998_a_2001(columns=None, nrows=None, dtype=None):
        filename = "Arrecadacao_01-01-1998_a_31-12-2001.csv"
        filepath = os.path.join(const.DATADIR + filename)
        return get_data(
            filepath_or_buffer=filepath,
            usecols=columns,
            nrows=nrows,
            sep=",",
            encoding="utf-8",
            dtype=dtype,
        )

    def arrecadacao_2002_a_2005(columns=None, nrows=None, dtype=None):
        filename = "Arrecadacao_01-01-2002_a_31-12-2005.csv"
        filepath = os.path.join(const.DATADIR + filename)
        return get_data(
            filepath_or_buffer=filepath,
            usecols=columns,
            nrows=nrows,
            sep=",",
            encoding="utf-8",
            dtype=dtype,
        )

    def arrecadacao_2006_a_2009(columns=None, nrows=None, dtype=None):
        filename = "Arrecadacao_01-01-2006_a_31-12-2009.csv"
        filepath = os.path.join(const.DATADIR + filename)
        return get_data(
            filepath_or_buffer=filepath,
            usecols=columns,
            nrows=nrows,
            sep=",",
            encoding="utf-8",
            dtype=dtype,
        )

    def arrecadacao_2010_a_2013(columns=None, nrows=None, dtype=None):
        filename = "Arrecadacao_01-01-2010_a_31-12-2013.csv"
        filepath = os.path.join(const.DATADIR + filename)
        return get_data(
            filepath_or_buffer=filepath,
            usecols=columns,
            nrows=nrows,
            sep=",",
            encoding="utf-8",
            dtype=dtype,
        )

    def arrecadacao_2014_a_2017(columns=None, nrows=None, dtype=None):
        filename = "Arrecadacao_01-01-2014_a_31-12-2017.csv"
        filepath = os.path.join(const.DATADIR + filename)
        return get_data(
            filepath_or_buffer=filepath,
            usecols=columns,
            nrows=nrows,
            sep=",",
            encoding="utf-8",
            dtype=dtype,
        )

    def arrecadacao_2018_a_2020(columns=None, nrows=None, dtype=None):
        filename = "Arrecadacao_01-01-2018_a_09-12-2020.csv"
        filepath = os.path.join(const.DATADIR + filename)
        return get_data(
            filepath_or_buffer=filepath,
            usecols=columns,
            nrows=nrows,
            sep=",",
            encoding="utf-8",
            dtype=dtype,
        )

    # TIPO ARRECADACAO
    def tipo_arrecadacao(columns=None, nrows=None, dtype=None):
        filename = "TIPO_ARRECADACAO.parquet"
        filepath = os.path.join(const.DATADIR + filename)
        return get_data(
            filepath_or_buffer=filepath,
            usecols=columns,
            nrows=nrows,
            sep=",",
            encoding="utf-8",
            dtype=dtype,
        )

    # TRANSFERÊNCIAS Estados-Municipios
    def transferencias(columns=None, nrows=None, dtype=None):
        filename = "TRANSFERENCIAS.parquet"
        filepath = os.path.join(const.DATADIR + filename)
        return get_data(
            filepath_or_buffer=filepath,
            usecols=columns,
            nrows=nrows,
            sep=";",
            encoding="utf-8",
            dtype=dtype,
        )

    def transfestadomunicipios_2018(columns=None, nrows=None, dtype=None):
        filename = "transfestadomunicipios-2018.csv"
        filepath = os.path.join(const.DATADIR + filename)
        return get_data(
            filepath_or_buffer=filepath,
            usecols=columns,
            nrows=nrows,
            sep=";",
            encoding="utf-8",
            dtype=dtype,
        )

    def transfestadomunicipios_2019(columns=None, nrows=None, dtype=None):
        filename = "transfestadomunicipios-2019.csv"
        filepath = os.path.join(const.DATADIR + filename)
        return get_data(
            filepath_or_buffer=filepath,
            usecols=columns,
            nrows=nrows,
            sep=";",
            encoding="utf-8",
            dtype=dtype,
        )

    def transfestadomunicipios_2020(columns=None, nrows=None, dtype=None):
        filename = "transfestadomunicipios-2020.csv"
        filepath = os.path.join(const.DATADIR + filename)
        return get_data(
            filepath_or_buffer=filepath,
            usecols=columns,
            nrows=nrows,
            sep=";",
            encoding="utf-8",
            dtype=dtype,
        )

    def transfestadomunicipios_2021(columns=None, nrows=None, dtype=None):
        filename = "transfestadomunicipios-2021.csv"
        filepath = os.path.join(const.DATADIR + filename)
        return get_data(
            filepath_or_buffer=filepath,
            usecols=columns,
            nrows=nrows,
            sep=";",
            encoding="utf-8",
            dtype=dtype,
        )

    # POPULAÇÃO
    def populacao(columns=None, nrows=None, dtype=None):
        filename = "POPULACAO.parquet"
        filepath = os.path.join(const.DATADIR + filename)
        return get_data(
            filepath_or_buffer=filepath,
            usecols=columns,
            nrows=nrows,
            sep=",",
            encoding="utf-8",
            dtype=dtype,
        )

    def populacao_2018(columns=None, nrows=None, dtype=None):
        filename = "populacao_2018.csv"
        filepath = os.path.join(const.DATADIR + filename)
        return get_data(
            filepath_or_buffer=filepath,
            usecols=columns,
            nrows=nrows,
            sep=",",
            encoding="utf-8",
            dtype=dtype,
        )

    def populacao_2019(columns=None, nrows=None, dtype=None):
        filename = "populacao_2019.csv"
        filepath = os.path.join(const.DATADIR + filename)
        return get_data(
            filepath_or_buffer=filepath,
            usecols=columns,
            nrows=nrows,
            sep=",",
            encoding="utf-8",
            dtype=dtype,
        )

    def populacao_2020(columns=None, nrows=None, dtype=None):
        filename = "populacao_2020.csv"
        filepath = os.path.join(const.DATADIR + filename)
        return get_data(
            filepath_or_buffer=filepath,
            usecols=columns,
            nrows=nrows,
            sep=",",
            encoding="utf-8",
            dtype=dtype,
        )

    def populacao_2021(columns=None, nrows=None, dtype=None):
        filename = "populacao_2021.csv"
        filepath = os.path.join(const.DATADIR + filename)
        return get_data(
            filepath_or_buffer=filepath,
            usecols=columns,
            nrows=nrows,
            sep=",",
            encoding="utf-8",
            dtype=dtype,
        )


def group_by(df, col):
    """
    Função para agrupamento
    """
    # Agregação
    grouped = df.groupby(by=col, as_index=False).agg({"va_arrecadacao": "sum"})

    return(grouped)