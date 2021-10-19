# -*- encoding: utf-8 -*-
"""
Programa de Mentoria DSA 2021
"""

import pandas as pd
import os, string
import unicodedata
import datetime
from app.home.vups import const

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

def print_caller_name(stack_size=3):
    def wrapper(fn):
        def inner(*args, **kwargs):
            import inspect
            stack = inspect.stack()

            modules = [(index, inspect.getmodule(stack[index][0]))
                       for index in reversed(range(1, stack_size))]
            module_name_lengths = [len(module.__name__)
                                   for _, module in modules]

            s = '{index:>5} : {module:^%i} : {name}' % (
                max(module_name_lengths) + 4)
            callers = ['',
                       s.format(index='level', module='module', name='name'),
                       '-' * 50]

            for index, module in modules:
                callers.append(s.format(index=index,
                                        module=module.__name__,
                                        name=stack[index][3]))

            callers.append(s.format(index=0,
                                    module=fn.__module__,
                                    name=fn.__name__))
            callers.append('')
            print('\n'.join(callers))

            fn(*args, **kwargs)
        return inner
    return wrapper


def tratando_transferencias_estaduais(transferencias):

    # fonte: https://dados.es.gov.br/dataset/portal-da-transparencia-transferencias-para-municipios

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
        transferencias[x] = [round(float(transferencias[x].iloc[i].replace(
            ',', '.')), 2) for i in range(len(transferencias))]

    # criando coluna de totais
    transferencias['TotalRepassado'] = transferencias[calumns_to_num[0]] + \
        transferencias[calumns_to_num[1]] + \
        transferencias[calumns_to_num[2]] + transferencias[calumns_to_num[3]]

    # criando coluna com datatype
    transferencias['Data'] = [datetime.datetime(
        transferencias['Ano'].iloc[i], transferencias['Mes'].iloc[i], 28) for i in range(len(transferencias))]

    path = os.path.join(const.DATADIR, 'transf_estadual_tratado.parquet')
    
    transferencias.to_parquet(path)
