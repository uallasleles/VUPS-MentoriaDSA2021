# -*- encoding: utf-8 -*-
"""
Programa de Mentoria DSA 2021
"""

import pandas as pd
import string
import unicodedata


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