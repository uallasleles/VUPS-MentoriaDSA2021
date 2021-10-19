# -*- encoding: utf-8 -*-
"""
Programa de Mentoria DSA 2021
"""

from app import db
from app.home.vups import datasets
from app.base.models import Microdados
from flask import Response, stream_with_context

def importar():
    print("Importando Dataset...")
    data = datasets.microdados()

    def generate():
        total = data.shape[0]
        inc = 100 / total
        x = 0
        # yield str(total)
        try:
            print("Transferindo registros para a database...")
            for col in data.itertuples():
                # print("Adicionando registro para sessão! Nº {}".format(col.Index+1))
                # print(col)
                record = Microdados(
                    **{
                        "DataNotificacao": col[1],
                        "DataCadastro": col[2],
                        "DataDiagnostico": col[3],
                        "DataColeta_RT_PCR": col[4],
                        "DataColetaTesteRapido": col[5],
                        "DataColetaSorologia": col[6],
                        "DataColetaSorologiaIGG": col[7],
                        "DataEncerramento": col[8],
                        "DataObito": col[9],
                        "Classificacao": col[10],
                        "Evolucao": col[11],
                        "CriterioConfirmacao": col[12],
                        "StatusNotificacao": col[13],
                        "Municipio": col[14],
                        "Bairro": col[15],
                        "FaixaEtaria": col[16],
                        "IdadeNaDataNotificacao": col[17],
                        "Sexo": col[18],
                        "RacaCor": col[19],
                        "Escolaridade": col[20],
                        "Gestante": col[21],
                        "Febre": col[22],
                        "DificuldadeRespiratoria": col[23],
                        "Tosse": col[24],
                        "Coriza": col[25],
                        "DorGarganta": col[26],
                        "Diarreia": col[27],
                        "Cefaleia": col[28],
                        "ComorbidadePulmao": col[29],
                        "ComorbidadeCardio": col[30],
                        "ComorbidadeRenal": col[31],
                        "ComorbidadeDiabetes": col[32],
                        "ComorbidadeTabagismo": col[33],
                        "ComorbidadeObesidade": col[34],
                        "FicouInternado": col[35],
                        "ViagemBrasil": col[36],
                        "ViagemInternacional": col[37],
                        "ProfissionalSaude": col[38],
                        "PossuiDeficiencia": col[39],
                        "MoradorDeRua": col[40],
                        "ResultadoRT_PCR": col[41],
                        "ResultadoTesteRapido": col[42],
                        "ResultadoSorologia": col[43],
                        "ResultadoSorologia_IGG": col[44],
                        "TipoTesteRapido": col[45],
                    }
                )
                x = x + inc
                yield "data:" + "{:.4f}".format(x) + "\n\n"
                db.session.add(record)
                db.session.flush()
                db.session.commit()
                # time.sleep(2)
        except:
            print("Houve uma exceção! Revertendo as alterações!")
            db.session.rollback()  # Rollback the changes on error

        finally:
            print("Fechando a conexão")
            db.session.close()  # Close the connection

    return Response(stream_with_context(generate()), mimetype="text/event-stream")