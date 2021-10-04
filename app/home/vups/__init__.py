# -*- encoding: utf-8 -*-
"""
Programa de Mentoria DSA 2021
"""

import os
import sys
import pandas as pd

# from pandas.io.formats.format import CategoricalFormatter
import plotly.express as px
from . import const, utils

import datetime
import plotly.figure_factory as ff
import plotly.graph_objects as go
import warnings
import validators
import requests
import time

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
    memory_map=True,
    name=None
):
    filename, file_extension = os.path.splitext(os.path.basename(filepath_or_buffer[0][1]))
    print("Importando o dataset {}...".format(filename))

    if validators.url(filepath_or_buffer[0][1]):
        print("Buscando dataset de URL...")
        file_extension = '.csv'
        filepath = []
        for url in filepath_or_buffer:
            filename = url[0]
            if validators.url(url[1]):
                r = requests.get(url[1], stream=True)

                DATENAME = time.strftime("%Y%m%d-%H%M%S")
                filepath.append(os.path.join(const.DATADIR, "{}-{}{}".format(DATENAME, filename.upper(), file_extension)))
                print("Gravando os dados em disco...")
                with open(filepath[-1], 'wb') as fd:
                    for chunk in r.iter_content(chunk_size=128):
                        fd.write(chunk)

        ds_lst = []
        for f in filepath:
            _PARAMS = {
                "filepath_or_buffer": f,
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
            subset = pd.concat(iter, ignore_index=True)
            ds_lst.append(subset)

        print("Concatenando arquivos, caso sejam múltiplos datasets...")
        dataset = pd.concat(ds_lst, ignore_index=True)
        print("Realizando transformações de dados no dataset consolidado...")
        dataset = dtype_transform(dataset, mapa)
        print("Convertendo para PARQUET o dataset com os tipos de dados já tratados...")
        file_extension = convert_to_parquet([dataset], name)

        filepath_or_buffer = {"filepath": {"ext": os.path.join(const.DATADIR, "{}{}".format(name.upper(), file_extension))}}
        filepath_or_buffer = list(filepath_or_buffer.get("filepath").items())

    if file_extension == ".csv":

        _PARAMS = {
            "filepath_or_buffer": filepath_or_buffer[0][1],
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
        file_extension = convert_to_parquet([dataset], name)
        filepath_or_buffer = which_file_exists(name)
        # filepath_or_buffer[0][1] = os.path.join(const.DATADIR, "{}{}".format(name.upper(), file_extension))

    if file_extension == ".parquet":
        print("Realizando importação de arquivo PARQUET.")
        _PARAMS = {
            "path": filepath_or_buffer[0][1],
            "columns": usecols
        }
        dataset = pd.read_parquet(**_PARAMS)
            
    return dataset

def convert_to_parquet(lst_dfs: list, filename=None):
    if len(lst_dfs) > 1:
        df = pd.concat(lst_dfs, ignore_index=True)
    else:
        df = lst_dfs[0]

    filepath_pqt = os.path.join(const.DATADIR, "{}.parquet".format(filename))
    
    # CRIA O ARQUIVO PARQUET
    try:
        print("Salvando em disco o arquivo convertido para PARQUET.")
        df.to_parquet(filepath_pqt)
    except:
        print("O dataset {} no foi convertido para Parquet. \nCaminho utilizado:{}".format(filename, filepath_pqt))
    
    # Verificação
    resp = '.parquet' if os.path.exists(filepath_pqt) else '.csv'
    
    return resp

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
    numeric_cols = fn_number_cols(df)

    df = utils.remove_espaco(df, date_cols + numeric_cols)

    for c in date_cols:
        try:
            df[c] = pd.to_datetime(df[c], infer_datetime_format=True, errors='coerce')
        except:
            pass

    cat_cols = list(df.select_dtypes(include="object").columns)
    for c in cat_cols:
        try:
            df[c] = df[c].astype("category")
        except:
            pass

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

def which_file_exists(name):
    extensions = [".parquet", ".csv"]
    
    for ext in extensions:
        # CRIA UM PATH DO ARQUIVO PARA CADA EXTENSÃO
        path = os.path.join(const.DATADIR, "{}{}".format(name, ext))
        filepath = {"filepath": {"ext": path}}
        filepath = list(filepath.get("filepath").items())

        # TESTA SE O ARQUIVO EXISTE
        if os.path.exists(filepath[0][1]):
            return filepath

    filepath = list(getattr(const, name).get("URLS").items())

    return filepath

class datasets:
    def microdados(columns=None, nrows=None, dtype=None):
        # SHOW DE BOLA ESSA PASSAGEM DINÂMICA DE NOMES! ^^
        name = sys._getframe(  ).f_code.co_name.upper()
        filepath_or_buffer = which_file_exists(name)
        mapa = getattr(const, name).get("MAP")

        return get_data(
            filepath_or_buffer=filepath_or_buffer,
            usecols=columns,
            nrows=nrows,
            sep=";",
            encoding="ISO-8859-1",
            warn_bad_lines=False,
            error_bad_lines=False,
            dtype=dtype,
            mapa=mapa,
            name=name
        )

    def microdados_bairros(columns=None, nrows=None, dtype=None):
        name = sys._getframe(  ).f_code.co_name.upper()
        filepath_or_buffer = which_file_exists(name)
        mapa = getattr(const, name).get("MAP")

        return get_data(
            filepath_or_buffer=filepath_or_buffer,
            usecols=columns,
            nrows=nrows,
            sep=",",
            encoding="ISO-8859-1",
            warn_bad_lines=False,
            error_bad_lines=False,
            dtype=dtype,
            mapa=mapa,
            name=name
        )

    def arrecadacao(columns=None, nrows=None, dtype=None):
        name = sys._getframe(  ).f_code.co_name.upper()
        filepath_or_buffer = which_file_exists(name)
        mapa = getattr(const, name).get("MAP")

        return get_data(
            filepath_or_buffer=filepath_or_buffer,
            usecols=columns,
            nrows=nrows,
            sep=",",
            encoding="utf-8",
            warn_bad_lines=False,
            error_bad_lines=False,
            dtype=dtype,
            mapa=mapa,
            name=name
        )

    def tipo_arrecadacao(columns=None, nrows=None, dtype=None):
        name = sys._getframe(  ).f_code.co_name.upper()
        filepath_or_buffer = which_file_exists(name)
        mapa = getattr(const, name).get("MAP")

        return get_data(
            filepath_or_buffer=filepath_or_buffer,
            usecols=columns,
            nrows=nrows,
            sep=",",
            encoding="utf-8",
            warn_bad_lines=False,
            error_bad_lines=False,
            dtype=dtype,
            mapa=mapa,
            name=name
        )

    def transferencias(columns=None, nrows=None, dtype=None):
        name = sys._getframe(  ).f_code.co_name.upper()
        filepath_or_buffer = which_file_exists(name)
        mapa = getattr(const, name).get("MAP")

        return get_data(
            filepath_or_buffer=filepath_or_buffer,
            usecols=columns,
            nrows=nrows,
            sep=";",
            encoding="UTF-8",
            warn_bad_lines=False,
            error_bad_lines=False,
            dtype=dtype,
            mapa=mapa,
            name=name
        )

    def populacao(columns=None, nrows=None, dtype=None):
        name = sys._getframe(  ).f_code.co_name.upper()
        filepath_or_buffer = which_file_exists(name)
        mapa = getattr(const, name).get("MAP")

        return get_data(
            filepath_or_buffer=filepath_or_buffer,
            usecols=columns,
            nrows=nrows,
            sep=",",
            encoding="UTF-8",
            warn_bad_lines=False,
            error_bad_lines=False,
            dtype=dtype,
            mapa=mapa,
            name=name
        )