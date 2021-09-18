# -*- encoding: utf-8 -*-
"""
Programa de Mentoria DSA 2021
"""

from flask_login import UserMixin
from sqlalchemy import Binary, Column, Integer, String, Date
from app import db, login_manager
from app.base.util import hash_pass


class User(db.Model, UserMixin):

    __tablename__ = 'User'

    id          = Column(Integer, primary_key=True)
    username    = Column(String, unique=True)
    email       = Column(String, unique=True)
    password    = Column(Binary)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            # dependendo se o valor é iterável ou não, 
            # devemos descompactar seu valor.
            # (quando ** kwargs é request.form, 
            # alguns valores serão uma lista de 1 elemento).
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                # o, = desempacotar de um singleton falha no PEP8 (teste travis flake8)
                value = value[0]

            if property == 'password':
                value = hash_pass( value ) # precisamos de bytes aqui (não str simples)
                
            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)


class Microdados(db.Model):
    
    __tablename__ = 'Microdados'

    id = Column(Integer, primary_key=True, nullable=False)

    DataNotificacao         = Column(String) # 01
    DataCadastro            = Column(String) # 02
    DataDiagnostico         = Column(String) # 03
    DataColeta_RT_PCR       = Column(String) # 04
    DataColetaTesteRapido   = Column(String) # 05
    DataColetaSorologia     = Column(String) # 06
    DataColetaSorologiaIGG  = Column(String) # 07
    DataEncerramento        = Column(String) # 08
    DataObito               = Column(String) # 09
 
    Classificacao           = Column(String) # 10
    Evolucao                = Column(String) # 11
    CriterioConfirmacao     = Column(String) # 12
    StatusNotificacao       = Column(String) # 13
    Municipio               = Column(String) # 14
    Bairro                  = Column(String) # 15
    FaixaEtaria             = Column(String) # 16
    IdadeNaDataNotificacao  = Column(String) # 17
    Sexo                    = Column(String) # 18
    RacaCor                 = Column(String) # 19
    Escolaridade            = Column(String) # 20
    Gestante                = Column(String) # 21
    Febre                   = Column(String) # 22
    DificuldadeRespiratoria = Column(String) # 23
    Tosse                   = Column(String) # 24
    Coriza                  = Column(String) # 25
    DorGarganta             = Column(String) # 26
    Diarreia                = Column(String) # 27
    Cefaleia                = Column(String) # 28

    ComorbidadePulmao       = Column(String) # 29
    ComorbidadeCardio       = Column(String) # 30
    ComorbidadeRenal        = Column(String) # 31
    ComorbidadeDiabetes     = Column(String) # 32
    ComorbidadeTabagismo    = Column(String) # 33
    ComorbidadeObesidade    = Column(String) # 34

    FicouInternado          = Column(String) # 35
    ViagemBrasil            = Column(String) # 36
    ViagemInternacional     = Column(String) # 37
    ProfissionalSaude       = Column(String) # 38
    PossuiDeficiencia       = Column(String) # 39
    MoradorDeRua            = Column(String) # 40
    ResultadoRT_PCR         = Column(String) # 41
    ResultadoTesteRapido    = Column(String) # 42
    ResultadoSorologia      = Column(String) # 43
    ResultadoSorologia_IGG  = Column(String) # 44
    TipoTesteRapido         = Column(String) # 45

    def __init__(self, **kwargs):
        for property, value in kwargs.items():

            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]
    
            setattr(self, property, value)

    # def __str__(self):
    #     return f'Caso: \
    #         Classificação - {self.Classificacao},\
    #         Municipio - {self.Municipio}, \
    #         Notificação - {self.DataNotificacao})'

    # def __repr__(self):
    #     return f'Caso(\
    #         Classificacao={self.Classificacao},\
    #         Municipio={self.Municipio}, \
    #         DataNotificacao={self.DataNotificacao})'


@login_manager.user_loader
def user_loader(id):
    return User.query.filter_by(id=id).first()

@login_manager.request_loader
def request_loader(request):
    username = request.form.get('username')
    user = User.query.filter_by(username=username).first()
    return user if user else None

