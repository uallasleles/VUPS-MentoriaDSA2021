from typing import Text
from numpy import genfromtxt

from time import time
from datetime import datetime

from app.base.models import Microdados
from app.home import vups
# from app import db
from tqdm import tqdm
from flask import Response

def getData_fromTXT(file_name):
    data = genfromtxt(file_name, delimiter=',', skip_header=1, converters={0: lambda s: str(s)})
    return data.tolist()

# for i in data:
#     record = Microdados(**{
#         'date' : datetime.strptime(i[0], '%d-%b-%y').date(),
#         'opn' : i[1],
#         'hi' : i[2],
#         'lo' : i[3],
#         'close' : i[4],
#         'vol' : i[5]

# def importer(data=vups.datasets.microdados(nrows=100)): 
    try:
        print("Importando Dataset")
        print("Informações sobre o Dataset importado:")
        print("===============================================================")
        print(data.info())
        print("===============================================================")
        
        print("Iterando registros")
        for col in tqdm(data.itertuples(), total=data.shape[0]):
            record = Microdados(**{
                'DataNotificacao' : col[1],
                'DataCadastro' : col[2],
                'DataDiagnostico' : col[3],
                'DataColeta_RT_PCR' : col[4],
                'DataColetaTesteRapido' : col[5],
                'DataColetaSorologia' : col[6],
                'DataColetaSorologiaIGG' : col[7],
                'DataEncerramento' : col[8],
                'DataObito' : col[9],
                'Classificacao' : col[10],
                'Evolucao' : col[11],
                'CriterioConfirmacao' : col[12],
                'StatusNotificacao' : col[13],
                'Municipio' : col[14],
                'Bairro' : col[15],
                'FaixaEtaria' : col[16],
                'IdadeNaDataNotificacao' : col[17],
                'Sexo' : col[18],
                'RacaCor' : col[19],
                'Escolaridade' : col[20],
                'Gestante' : col[21],
                'Febre' : col[22],
                'DificuldadeRespiratoria' : col[23],
                'Tosse' : col[24],
                'Coriza' : col[25],
                'DorGarganta' : col[26],
                'Diarreia' : col[27],
                'Cefaleia' : col[28],
                'ComorbidadePulmao' : col[29],
                'ComorbidadeCardio' : col[30],
                'ComorbidadeRenal' : col[31],
                'ComorbidadeDiabetes' : col[32],
                'ComorbidadeTabagismo' : col[33],
                'ComorbidadeObesidade' : col[34],
                'FicouInternado' : col[35],
                'ViagemBrasil' : col[36],
                'ViagemInternacional' : col[37],
                'ProfissionalSaude' : col[38],
                'PossuiDeficiencia' : col[39],
                'MoradorDeRua' : col[40],
                'ResultadoRT_PCR' : col[41],
                'ResultadoTesteRapido' : col[42],
                'ResultadoSorologia' : col[43],
                'ResultadoSorologia_IGG' : col[44],
                'TipoTesteRapido' : col[45]
            })
            print("Adicionando registro para sessão! %{}%".format(col.Index))
            # db.session.add(record)
            # db.session.flush()
            # db.session.commit()

    except:
        print("Houve uma exceção! Revertendo as alterações!")
        # db.session.rollback() # Rollback the changes on error
    
    finally:
        print("Fechando a conexão")
        # db.session.close() # Close the connection