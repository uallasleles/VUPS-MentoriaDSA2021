# -*- encoding: utf-8 -*-
"""
Programa de Mentoria DSA 2021
"""

# IMPORTAÇÕES ****************************************************************
import pandas as pd
import warnings


# AJUSTES ********************************************************************

# Ignorando mensagens de avisos.
warnings.filterwarnings("ignore")

# Formata ponto flutuante como string com 2 casas decimais
pd.options.display.float_format = '{:.2f}'.format

__all__ = [
    "const",
    "data",
    "datasets",
    "graphs",
    "utils",
]