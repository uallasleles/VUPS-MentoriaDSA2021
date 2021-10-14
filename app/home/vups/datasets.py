# -*- encoding: utf-8 -*-
"""
Programa de Mentoria DSA 2021
"""

# IMPORTAÇÕES ****************************************************************
from app.home.vups import const
import os, sys, validators, requests, time, pandas as pd
# ############################################################################

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
    """
        FUNÇÃO CENTRAL PARA OBETENÇÃO DE DADOS
        ----------------------------------------------------------------
        BUSCA O DATASET POR ORDEM DE PRECEDÊNCIA DO TIPO DE ARMAZENAMENTO.
            PRECEDÊNCIA: PARQUET < CSV < URL
        - TENTA IMPORTAR O DATASET SOLICITADO DE ARQUIVO PARQUET PARA DATAFRAME DO PANDAS, CASO O PARQUET EXISTA
        - SENÃO, TENTA IMPORTAR DE CSV PARA DATAFRAME DO PANDAS, TRATA OS DADOS E FAZ O CAST PARA PARQUET, UTILIZANDO POR FIM O PARQUET
        - CASO NÃO ENCONTRE O DATASET EM CSV, RECORRE AS URLS NO REGISTRO DO DATASET
        AS URLS (CSV) SÃO IMPORTADAS PARA DATAFRAME DO PANDAS, OS DADOS SÃO TRATADOS 
        ENTÃO, É FEITO UM CAST PARA PARQUET, O ARQUIVO É GRAVADO EM DISCO, POR FIM O PARQUET É UTILIZADO
    """
    
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

        print(mapa)
        if mapa != "{}":
            print("Realizando transformações de dados no dataset consolidado...")
            dataset = data.dtype_transform(dataset, mapa)
        else:
            print("Inicializando mapeamento de tipos de dados...")
            data.field_map(dataset, name)
        
        print("Convertendo para PARQUET o dataset com os tipos de dados já tratados...")
        file_extension = data.convert_to_parquet([dataset], name)

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
        
        print(mapa)
        if mapa != "{}":
            print("Realizando transformações de dados no dataset consolidado...")
            dataset = data.dtype_transform(dataset, mapa)
        else:
            print("Inicializando mapeamento de tipos de dados...")
            data.dump.field_map(dataset, name)

        dataset = data.dtype_transform(dataset, mapa)
        file_extension = data.convert_to_parquet([dataset], name)
        filepath_or_buffer = data.which_file_exists(name)
        
    if file_extension == ".parquet":
        print("Realizando importação de arquivo PARQUET.")
        _PARAMS = {
            "path": filepath_or_buffer[0][1],
            "columns": usecols
        }
        dataset = pd.read_parquet(**_PARAMS)
            
    return dataset

class datasets:
    """
    CLASSE QUE INTERMEDIA A PASSAGEM DE PARÂMETROS DOS DATASETS REGISTRADOS
    OS METADADOS E CONFIGURAÇÕES DE TODOS OS DATASETS SÃO ARMAZENADOS EM ARQUIVOS JSON
    OS ARQUIVOS JSON SÃO LIDOS PELO MÓDULO [vups.const]
    OS MÉTODOS DESTA CLASSE BUSCAM NO MÓDULO [vups.const] OS PARÂMETROS DO DATASET A SER IMPORTADO
    ENTÃO, REPASSA ESSES PARÂMETROS PARA O MÉTODO get_data()
    """
    
    def microdados(columns=None, nrows=None, dtype=None):
        """
        MÉTODO QUE BUSCA OS PARÂMETROS DO DATASET [microdados]
        """

        # SHOW DE BOLA ESSA PASSAGEM DINÂMICA DE NAMESPACES! ^^
        name = sys._getframe(  ).f_code.co_name.upper()
        filepath_or_buffer = data.which_file_exists(name)

        mapa = getattr(const, name).get("MAP")
        print(mapa)

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
            name=name
        )

    def microdados_bairros(columns=None, nrows=None, dtype=None):
        name = sys._getframe(  ).f_code.co_name.upper()
        filepath_or_buffer = data.which_file_exists(name)
        mapa = getattr(const, name).get("MAP")

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
            name=name
        )

    def arrecadacao(columns=None, nrows=None, dtype=None):
        name = sys._getframe(  ).f_code.co_name.upper()
        filepath_or_buffer = data.which_file_exists(name)
        mapa = getattr(const, name).get("MAP")

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
            name=name
        )

    def tipo_arrecadacao(columns=None, nrows=None, dtype=None):
        name = sys._getframe(  ).f_code.co_name.upper()
        filepath_or_buffer = data.which_file_exists(name)
        mapa = getattr(const, name).get("MAP")

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
            name=name
        )

    def transferencias(columns=None, nrows=None, dtype=None):
        name = sys._getframe(  ).f_code.co_name.upper()
        filepath_or_buffer = data.which_file_exists(name)
        mapa = getattr(const, name).get("MAP")

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
            name=name
        )

    def populacao(columns=None, nrows=None, dtype=None):
        name = sys._getframe(  ).f_code.co_name.upper()
        filepath_or_buffer = data.which_file_exists(name)
        mapa = getattr(const, name).get("MAP")

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
            name=name
        )