import streamlit as st
import pandas as pd
import numpy as np
import s3fs
import os

'''
Este guia explica como acessar com segurança os arquivos no 
AWS S3 do compartilhamento Streamlit ou Streamlit for Teams. 
Ele usa a biblioteca s3fs e o gerenciamento de segredos do Streamlit.
'''

# 1. Crie um S3 bucket e adicione um arquivo.
#
#   1.1 Primeiro, inscreva-se no AWS ou faça login. 
#       Vá para o Console S3 e crie um novo bucket:
#
#   1.2 Navegue até a seção de upload do seu novo bucket:
#
#   1.3 E faça upload do seguinte arquivo CSV, que contém alguns dados de exemplo:


# 2. Crie chaves de acesso.
#
#   2.1 Vá para o console da AWS, crie chaves de acesso.
#   2.2 Copie a “ID da chave de acesso” e a “Chave de acesso secreta”.

#       # As chaves de acesso criadas como um usuário root têm permissões abrangentes. 
#       # Para tornar sua conta da AWS mais segura, 
#       # você deve considerar a criação de uma conta IAM com permissões restritas 
#       # e o uso de suas chaves de acesso.


# 3. Adicione a chave aos segredos do seu aplicativo local

# # .streamlit/secrets.toml
# AWS_ACCESS_KEY_ID = "xxx"
# AWS_SECRET_ACCESS_KEY = "xxx"

#   3.1 Seu aplicativo Streamlit local lerá segredos de um arquivo 
#       .streamlit/secrets.toml no diretório raiz do seu aplicativo. 
#       
#       Crie este arquivo se ele ainda não existir e 
#       adicione a chave de acesso a ele.


# 4. Copie os segredos do seu aplicativo para a nuvem
#
#   4.1 Como o arquivo secrets.toml acima não está comprometido com o Github, 
#       você precisa passar seu conteúdo para seu aplicativo implantado 
#       (no compartilhamento Streamlit ou Streamlit for Teams) separadamente.

#       Vá para o painel do aplicativo e no menu suspenso do aplicativo, 
#       clique em Editar segredos. 
#       Copie o conteúdo de secrets.toml para a área de texto.


# 5. Adicione s3fs ao seu arquivo de requisitos

# # requirements.txt
# s3fs==x.x.x

#   5.1 Adicione o pacote s3fs ao seu arquivo requirements.txt, 
#   de preferência fixando sua versão 
#   (basta substituir x.x.x pela versão que você deseja instalar).


# 6. Escreva seu aplicativo Streamlit

#   6.1 Copie o código abaixo para o seu aplicativo Streamlit e execute-o. 
#       Certifique-se de adaptar o nome do seu intervalo e arquivo. 
#       Observe que o Streamlit transforma automaticamente as chaves de acesso do seu arquivo secrets 
#       em variáveis ​​de ambiente, onde o s3fs procura por elas por padrão.


    # # streamlit_app.py

    # import streamlit as st
    # import s3fs
    # import os

    # # Create connection object.
    # # `anon=False` means not anonymous, i.e. it uses access keys to pull data.
    # fs = s3fs.S3FileSystem(anon=False)

    # # Retrieve file contents.
    # # Uses st.cache to only rerun when the query changes or after 10 min.
    # @st.cache(ttl=600)
    # def read_file(filename):
    #     with fs.open(filename) as f:
    #         return f.read().decode("utf-8")

    # content = read_file("testbucket-jrieke/myfile.csv")

    # # Print results.
    # for line in content.strip().split("\n"):
    #     name, pet = line.split(",")
    #     st.write(f"{name} has a :{pet}:")


# Viu st.cache acima? 
# Sem ele, o Streamlit executaria a consulta sempre que o aplicativo fosse executado novamente 
# (por exemplo, em uma interação de widget). 
# Com st.cache, ele só é executado quando a consulta muda ou após 10 minutos (é para isso que serve o ttl). 
# 
# Cuidado: se o seu banco de dados é atualizado com mais frequência, 
# você deve adaptar o ttl ou remover o cache para que os visualizadores sempre vejam os dados mais recentes. 
# 

# streamlit_app.py

# Create connection object.
# `anon=False` means not anonymous, i.e. it uses access keys to pull data.
fs = s3fs.S3FileSystem(anon=False)

# Retrieve file contents.
# Uses st.cache to only rerun when the query changes or after 10 min.
#@st.cache(ttl=600)
def read_file(filename):
    with fs.open(filename) as f:
        return f.read().decode("utf-8")

content = read_file("https:\\\\vups.s3.sa-east-1.amazonaws.com\\myfile.csv")

# Print results.
for line in content.strip().split("\n"):
    name, pet = line.split(",")
    st.write(f"{name} has a :{pet}:")