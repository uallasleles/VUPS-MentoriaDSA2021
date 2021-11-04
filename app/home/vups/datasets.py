# -*- encoding: utf-8 -*-
"""
******************************************************************************
* MÓDULO: datasets
******************************************************************************
"""

# IMPORTAÇÕES ****************************************************************
import json
from typing import Iterable
from tqdm.gui import tqdm_gui
from app.home.vups import const, data, utils
import os, sys, validators, requests, time, pandas as pd, inspect
from clint.textui import progress
from pathlib import Path
import pandas as pd
import tqdm
import typer
# ****************************************************************************

# @utils.print_caller_name(4)
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
    name=None,
    format=None
):
    """FUNÇÃO CENTRAL PARA OBTENÇÃO DE DADOS
    ----------------------------------------------------------------------
    - BUSCA O DATASET POR ORDEM DE PRECEDÊNCIA DO TIPO DE ARMAZENAMENTO.
        PRECEDÊNCIA: PARQUET < CSV < URL
    - TENTA IMPORTAR O DATASET SOLICITADO DE PARQUET FILE PARA DATAFRAME DO PANDAS, CASO O PARQUET EXISTA.
    - SENÃO, TENTA IMPORTAR DE CSV PARA DATAFRAME DO PANDAS, TRATA OS DADOS E FAZ O CAST PARA PARQUET, UTILIZANDO POR FIM O PARQUET
    - CASO NÃO ENCONTRE O DATASET EM CSV, RECORRE AS URLS NO REGISTRO DO DATASET
    AS URLS (CSV) SÃO IMPORTADAS PARA DATAFRAME DO PANDAS, OS DADOS SÃO TRATADOS, 
    CONVERTIDO PARA PARQUET, O ARQUIVO É GRAVADO EM DISCO, POR FIM O PARQUET É UTILIZADO.
    """
    
    filename, file_extension = os.path.splitext(os.path.basename(filepath_or_buffer[0][1]))
    chunk_size = 1024

    if validators.url(filepath_or_buffer[0][1]):
        print("Baixando {} de URL ...".format(filename))

        filepath = []
        for url in filepath_or_buffer:
            filename = url[0]
            if validators.url(url[1]):
                r = requests.get(url[1], stream=True)

                # CRIA UM PATH PARA GRAVAR O ARQUIVO BAIXADO E, ADICIONA O PATH A UMA LISTA
                DATENAME = time.strftime("%Y%m%d-%H%M%S")
                filepath.append(
                    os.path.join(
                        const.DATATMP, 
                        "{}-{}{}".format(DATENAME, filename.upper(), format)
                        )
                    )

                # GRAVA CADA DATASET BAIXADO, PARA DEPOIS ... 
                # ... CONCATENÁ-LOS, TRANSFORMAR OS TIPOS DE DADOS E CONVERTER O DATASET UNIFICADO EM PARQUET
               
                with open(filepath[-1], 'wb') as fd:
                    print("Obtendo o comprimento dos dados ...")
                    total_length = int(r.headers.get('content-length'))

                    print("Gravando os dados em disco ...")
                    for chunk in progress.bar(r.iter_content(chunk_size=chunk_size), expected_size=(total_length/chunk_size) + 1):
                        if chunk:
                            fd.write(chunk)
                            fd.flush()

        # OS DATASETS BAIXADOS SÃO IMPORTADOS NOVAMENTE DOS ARQUIVOS EM DISCO
        ds_lst = []
        for f in filepath:
            _PARAMS = {
                "filepath_or_buffer": f,
                "iterator": True,
                "chunksize": chunk_size,
                "usecols": usecols,
                "sep": sep,
                "nrows": nrows,
                "encoding": encoding,
                "warn_bad_lines": warn_bad_lines,
                "error_bad_lines": error_bad_lines,
                # "parse_dates": True,
                # "dtype": dtype,
                "memory_map": memory_map
            }
            iter = pd.read_csv(**_PARAMS)
            subset = pd.concat(iter, ignore_index=True)
            # (CHAMO CADA CONJUNTO QUE COMPÕE O MESMO DATASET DE "SUBSET")

            # OS "SUBSETS" SÃO ADICIONADOS EM UMA LISTA PARA SEREM CONCATENADOS
            ds_lst.append(subset)

        print("Concatenando arquivos, caso sejam múltiplos datasets...")
        dataset = pd.concat(ds_lst, ignore_index=True)

        # AGORA É A HORA DO TRATAMENTO E TRANSFORMAÇÃO DOS DADOS, PARA NO FIM GRAVAR UM PARQUET TIPADO
        # --------------------------------------------------------------------------------------------

        # USO O DTYPE MAP QUE FOI DECLARADO NO REGISTRO DO DATASET
        if mapa is not None:
            print("Realizando transformações de dados no dataset consolidado...")
            dataset = data.dtype_transform(dataset, mapa)
        else:
            # CASO NÃO EXISTA O DTYPE MAP, UM INICIAL É CRIADO PARA FUTURAMENTE SER CONFIGURADO E O TRATAMENTO REPROCESSADO
            print("Inicializando mapeamento de tipos de dados...")
            data.create_dtype_map(dataset, name)
        
        # APÓS O TRATAMENTO E TRANSFORMAÇÃO DOS DADOS, UM ARQUIVO PARQUET É CRIADO, PASSANDO A SER O DATASET OFICIAL
        print("Convertendo para PARQUET o dataset com os tipos de dados já tratados...")
        filepath_or_buffer = data.convert_to_parquet([dataset], name)
        file_extension = ".parquet"

        # LIMPA O DIRETÓRIO DE DADOS TEMPORÁRIOS    # ALTERNATIVA
        # for f in os.listdir(const.DATATMP):         # for f in filepath:
        #     file = os.path.join(const.DATATMP, f)   #     REMOVE APENAS OS ARQUIVOS USADOS NESTA IMPORTAÇÃO
        #     os.remove(file)                         #     os.remove(f)

    if file_extension == ".csv":
        # print("Importando {} de CSV...".format(filename))

        _PARAMS = {
            "filepath_or_buffer": filepath_or_buffer[0][1],
            "iterator": True,
            "chunksize": chunk_size,
            "usecols": usecols,
            "sep": sep,
            "nrows": nrows,
            "encoding": encoding,
            "warn_bad_lines": warn_bad_lines,
            "error_bad_lines": error_bad_lines,
            # "parse_dates": True,
            # "dtype": dtype,
            "memory_map": memory_map,
            "low_memory": False
        }

        dataset = progress_read_csv(**_PARAMS)
        # iter = progress_read_csv(**_PARAMS)
        # dataset = pd.concat(iter, ignore_index=True)
        
        if mapa is not None:
            # print("Realizando transformações de dados no dataset CSV unificado...")
            # print("MAPA:", mapa)
            dataset = data.dtype_transform(dataset, mapa)
        else:
            # print("Inicializando as variáveis do mapeamento de tipos de dados...")
            # print("MAPA:", mapa)
            data.create_dtype_map(dataset, name)

        filepath_or_buffer = data.convert_to_parquet([dataset], name)
        file_extension = ".parquet"

    if file_extension == ".parquet":
        # print("Importando {} de PARQUET...".format(filename))

        _PARAMS = {
            "path": filepath_or_buffer[0][1],
            "columns": usecols,
        }
        dataset = pd.read_parquet(**_PARAMS)

        # PATH = const.METADIR
        # FILENAME = "DTYPEMAP_{}.json".format(name)
        # FILEPATH = os.path.join(PATH, FILENAME)
        
        # if not os.path.exists(FILEPATH):
        #     print("NÃO EXISTE MAPA!")
        #     data.create_dtype_map(dataset, name)
        # elif mapa != const.read_dtype_map(dataset):
        #     print("MAPAS DIFERENTES! REPROCESSANDO O TRATAMENTO DE DADOS ...")
        #     dataset = data.dtype_transform(dataset, mapa)
        #     print("ATUALIZANDO O ARQUIVO PARQUET ...")
        #     data.convert_to_parquet([dataset], name)

    # if filename.strip() != "":
    #     curframe = inspect.currentframe()
    #     calframe = inspect.getouterframes(curframe, 2)
    #     print("===================================================================")
    #     print("FILENAME:", filename)
    #     print("# FILE: {}".format(__file__))
    #     print("# NAME: {}".format(__name__))
    #     print("# OBJECT: {}".format(sys._getframe(  ).f_code.co_name))
    #     print("# CALLER:", calframe[1][3])
    #     print("-------------------------------------------------------------------")
    #     print(dataset.info())
    #     print("===================================================================")

    return dataset


class Datasets:
    """CLASSE QUE INTERMEDIA A PASSAGEM DE PARÂMETROS DOS DATASETS REGISTRADOS
    OS METADADOS E CONFIGURAÇÕES DE TODOS OS DATASETS SÃO ARMAZENADOS EM ARQUIVOS JSON
    OS ARQUIVOS JSON SÃO LIDOS PELO MÓDULO [vups.const]
    OS MÉTODOS DESTA CLASSE BUSCAM NO MÓDULO [vups.const] OS PARÂMETROS DO DATASET A SER IMPORTADO
    ENTÃO, REPASSA ESSES PARÂMETROS PARA O MÉTODO get_data()
    """

    # def __init__(self, name=None, usecols=None, nrows=None):
    #     self.name       = name
    #     self.usecols    = usecols
    #     self.nrows      = nrows

    # def to_json(self):
    #     pass

    def microdados(columns=None, nrows=None, dtype=None):
        """MÉTODO QUE BUSCA OS PARÂMETROS DO DATASET [microdados]"""

        name = sys._getframe(  ).f_code.co_name.upper()
        filepath_or_buffer = data.which_file_exists(name)
        mapa = getattr(const, name).get("MAP")
        format = getattr(const, name).get("FORMAT")

        return get_data(
            filepath_or_buffer=filepath_or_buffer,
            usecols=columns,
            nrows=nrows,
            sep=getattr(const, name).get("DELIMITER"),
            encoding=getattr(const, name).get("ENCODING"),
            warn_bad_lines=False,
            error_bad_lines=False,
            dtype=dtype,
            mapa=mapa,
            name=name,
            format=format
        )

    def microdados_bairros(columns=None, nrows=None, dtype=None):
        name = sys._getframe(  ).f_code.co_name.upper()
        filepath_or_buffer = data.which_file_exists(name)
        mapa = getattr(const, name).get("MAP")
        format = getattr(const, name).get("FORMAT")

        return get_data(
            filepath_or_buffer=filepath_or_buffer,
            usecols=columns,
            nrows=nrows,
            sep=getattr(const, name).get("DELIMITER"),
            encoding=getattr(const, name).get("ENCODING"),
            warn_bad_lines=False,
            error_bad_lines=False,
            dtype=dtype,
            mapa=mapa,
            name=name,
            format=format
        )

    def arrecadacao(columns=None, nrows=None, dtype=None):
        name = sys._getframe(  ).f_code.co_name.upper()
        filepath_or_buffer = data.which_file_exists(name)
        mapa = getattr(const, name).get("MAP")
        format = getattr(const, name).get("FORMAT")

        return get_data(
            filepath_or_buffer=filepath_or_buffer,
            usecols=columns,
            nrows=nrows,
            sep=getattr(const, name).get("DELIMITER"),
            encoding=getattr(const, name).get("ENCODING"),
            warn_bad_lines=False,
            error_bad_lines=False,
            dtype=dtype,
            mapa=mapa,
            name=name,
            format=format
        )

    def tipo_arrecadacao(columns=None, nrows=None, dtype=None):
        name = sys._getframe(  ).f_code.co_name.upper()
        filepath_or_buffer = data.which_file_exists(name)
        mapa = getattr(const, name).get("MAP")
        format = getattr(const, name).get("FORMAT")

        return get_data(
            filepath_or_buffer=filepath_or_buffer,
            usecols=columns,
            nrows=nrows,
            sep=getattr(const, name).get("DELIMITER"),
            encoding=getattr(const, name).get("ENCODING"),
            warn_bad_lines=False,
            error_bad_lines=False,
            dtype=dtype,
            mapa=mapa,
            name=name,
            format=format
        )

    def transferencias(columns=None, nrows=None, dtype=None):
        name = sys._getframe(  ).f_code.co_name.upper()
        filepath_or_buffer = data.which_file_exists(name)
        mapa = getattr(const, name).get("MAP")
        format = getattr(const, name).get("FORMAT")

        return get_data(
            filepath_or_buffer=filepath_or_buffer,
            usecols=columns,
            nrows=nrows,
            sep=getattr(const, name).get("DELIMITER"),
            encoding=getattr(const, name).get("ENCODING"),
            warn_bad_lines=False,
            error_bad_lines=False,
            dtype=dtype,
            mapa=mapa,
            name=name,
            format=format
        )

    def populacao(columns=None, nrows=None, dtype=None):
        name = sys._getframe(  ).f_code.co_name.upper()
        filepath_or_buffer = data.which_file_exists(name)
        mapa = getattr(const, name).get("MAP")
        format = getattr(const, name).get("FORMAT")

        return get_data(
            filepath_or_buffer=filepath_or_buffer,
            usecols=columns,
            nrows=nrows,
            sep=getattr(const, name).get("DELIMITER"),
            encoding=getattr(const, name).get("ENCODING"),
            warn_bad_lines=False,
            error_bad_lines=False,
            dtype=dtype,
            mapa=mapa,
            name=name,
            format=format
        )

def progress_read_csv(**_PARAMS):

    # read number of rows quickly
    filename = _PARAMS.get('filepath_or_buffer')
    length = sum1forline(filename)
    chunksize = _PARAMS.get('chunksize')

    # initiate a blank dataframe
    df = pd.DataFrame()

    # fancy logging with typer
    typer.secho(f"LENDO ARQUIVO: {filename}", fg="red", bold=True)
    typer.secho(f"TOTAL DE LINHAS: {length}", fg="green", bold=True)

    # tqdm context
    with tqdm.tqdm(total=length, desc="REGISTROS LIDOS") as bar:
        lst = []
        # enumerate chunks read without low_memory (it is massive for pandas to precisely assign dtypes)
        for i, chunk in enumerate(pd.read_csv(**_PARAMS)):
            
            # append it to df
            # df = df.append(chunk)
            lst.append(chunk)
            # update tqdm progress bar
            bar.update(chunksize)
    df = pd.concat(lst, ignore_index=True)
    print(df.info())

    # finally inform with a friendly message
    typer.secho("FIM DA LEITURA DOS REGISTROS...", fg=typer.colors.BRIGHT_RED)
    typer.secho(f"COMPRIMENTO:{len(df)}", fg="green", bold=True)
    return df

def sum1forline(filename):
    with open(filename) as f:
        return sum(1 for line in f)