# Clã VUPS - Mentoria DSA 2021
Projeto elaborado durante o Programa de Mentoria entre Alunos da **Data Science Academy**.

![DSA](https://github.com/uallasleles/VUPS-MentoriaDSA2021/blob/76c2293beb6e3df1a377bf5fdc7784dc3b082f9b/app/base/static/assets/img/icons/banner-dsa.jpg)

# Sobre a análise de dados.

## Tópicos
- Problema de Negócio
- Contexto
- Datasets
- Variáveis
- Ranking
   - PCA
      - Sinais Variáveis
      - Teste Estatístico
      - Escolha dos Fatores
      - Calculo da Puntuação
- Visualizações
   - Comparação de Repasses
   - Poder de Compra do Município
   - Calendário de Casos
   - Resumo COVID
   - Mapa com Ranking

## Problema de Negócio
---
Quais Municípios estão se saindo melhor em relação ao combate ao COVID-19?

## Contexto
---
Foi definido que iríamos focar nossa análise em um único estado brasileiro, dado o tamnho continetal
do nosso país. Como sugestão do nosso Mentor, original do estado do Espírito Santo, resolvemos delimitar
escomo do nosso trabalho aos municípios do ES.

Uma vez decidido os limites geográficos, definimos o escopo temporal do projeto. Por conta do tempo para conclusão
do trabalho, decidimos que uma avaliação mensal do desempenho do municípios seria a melhor estratêgia.

## Datasets
---
Datasets utilizados:
* Dados hitóricos COVID (fonte: )
* Dados históricos Vacinação COVID (fonte: )
* Dados Populacionais (fonte: )
* Repasses Estaduais (fonte: )

## Ranking
---
Para avaliar o desempenho no combate à pendemia, decidimos criar um ranking dos municípios. O desafio era criar
um sistema de avaliação que eliminasse a ponderação arbitrária. Para isso, usamos a soma do produto entre os fatores
oriundos de uma PCA e suas variancias compartilhadas.

#### Variáveis
As variáveis analisadas foram:
* Quantidade de casos (per capita) por mês;
* Quantidade de óbitos (per capita) por mês;
* Quantidade de casos recuperados (per capita) por mês;
* Quantidade de doses de vacina (per capita) por mês;
* Quantidade em dinheiro repassada pelo estado (per capita) por mês;

#### Teste Estatístico
Foi rodado o teste de esfericidade de Bartlett que apontou adequação estatística global do dataset para o modelo.

#### Escolha dos Fatores
Como o dataset era pequeno e não requeria muito poder computacional, decidimos por incluir todos os fatores no modelo,
de maneira que as comunalidades de cada variável tiveram valor final igual a 1.

#### Calculo da Puntuação
O calculo da pontuação se deu pela soma do produto entre os fatores e a variancia compartilhada

## Visualizações
---

### Comparação de Repasses
Criamos uma visualização que fizesse com que o usuário podesse comparar os repasses dos municípios de maneira simples
e objetiva. Duas formas de comparação foram criadas:
* Comparação Nominal: valor bruto recebido pelos municípios
* Comparação de variabilidade: quanto cada repasse variou de mês a més

### Poder de Compra do Município
Visualização que compara o valor recebido com a variação do indice IPCA. De maneira que o primeiro mês de análise
serviu como base de calculo para os mêses subsequentes. Com essa informação, o usuário pode ter uma noção melhor do
poder economico do município em relação ao combate da pandemia.

### Calendário de Casos
Visualização em forma de heatmap com formato de calendário. Tem com objetivo entender padrões de contagio do vírus.
É interessante observar, por exemplo, a quantidade de casos novos 1 semana após feriados municipais (como em AFONSO
CALUDIO no dia 20 de JANEIRO -> valores default da função).
### Resumo COVID
Visualização em linha com o numero de casos totais, obitos, recuperados e ativos, no tempo.

### Mapa com Ranking
Mapa com as divisões domunicípios e coloração referente ao posicionamento das cidades no ranking.


# Sobre a ignição do projeto

Para acelerar o processo de desenvolvimento da aplicação utilizamos um tema bootstrap desenvolvido por Themesberg.
> Bootstrap é o framework CSS mais popular do mundo. É um conjunto de componentes da web que ajudam a construir interfaces de usuário rápidas e modernas sem ter que configurar o código clichê para elementos básicos.

Desta forma podemos nos concentrar em personalizar o site usando as variáveis ​​Sass para alterar cores, fontes, tamanhos, e adicionar novos recursos.

Vantagens de usar um modelo

> 1. *Qualidade*. Base de código sólida e que funciona na maioria dos dispositivos e navegadores.
> 2. *Responsividade*. Site responsivo e acessívei em vários dispositivos.

<br>

Principais recursos frontend utilizados:
- Framework Bootstrap
- Ferramenta de fluxo de trabalho GULP
- Pré-processador CSS SASS

<br />

Com relação a estrutura base para o backend utilizamos o seguinte:

- Design modular com **Blueprints**
- Autenticação baseada em sessão (via **flask_login**) e formulários de validação.
- DBMS: SQLite
- DB Tools: SQLAlchemy ORM, Flask-Migrate (schema migrations)
- Amazon Web Service para deploy da aplicação

<br />

## Como usá-lo

```bash
# Obter o código
$ git clone https://github.com/uallasleles/VUPS-MentoriaDSA2021.git
```

```bash
# Instalar o Virtualenv

# Sistemas baseados em Unix
$ virtualenv env
$ source env/bin/activate

# Sistemas baseados em Windows
> virtualenv env
> .\env\Scripts\activate
```

```bash
# Instalar os pacotes Python necessários para o App
$ pip3 install -r requirements.txt
```

Para inicializar a aplicação é necessário definir as variáveis de ambiente FLASK_APP e FLASK_ENV.  
A variável FLASK_APP é usada para especificar como carregar o aplicativo.  
A variável FLASK_ENV define o ambiente em que o aplicativo Flask é executado (production ou development).  
Porém, utilizamos o dotenv do Flask para definir variáveis ​​de ambiente automaticamente, em vez de configurarmos cada vez que inicializamos a aplicação.

As declarações manuais referente as instruções que foram automatizadas são as seguintes:
```bash
# Configurar a variável de ambiente FLASK_APP

# (Unix/Mac) 
$ export FLASK_APP=run.py

# Windows (CMD) 
> set FLASK_APP=run.py

# Windows (Powershell) 
$ env:FLASK_APP = ".\run.py"
```

```bash
# Configurar o ambiente para DEBUG (opcional)

# (Unix/Mac) 
$ export FLASK_ENV=production

# Windows (CMD) 
> set FLASK_ENV=production

# Windows (Powershell) 
> env:FLASK_ENV = "production"
```

Após estas configurações você pode inicializar a aplicação.
```bash
# Iniciar o Dashboard App 

# Opções: 

# Modo de Desenvolvimento
# --host=0.0.0.0 - expõe o aplicativo em todas as interfaces de rede (padrão 127.0.0.1)
# --port=5000    - Especifique a porta do aplicativo (padrão 5000)

$ flask run --host=0.0.0.0 --port=5000

# Acesse o Dashboard App em seu browser: http://127.0.0.1:5000/
```

> Nota: Para usar o aplicativo, acesse a página de registro e crie um novo usuário. Após a autenticação, o aplicativo irá desbloquear as páginas privadas.

<br />

## Estrutura do código base

O projeto é codificado usando blueprints, app factory pattern, perfil de configuração dual (desenvolvimento e produção), com a seguinte estrutura:

<br />

> Árvore de Diretórios

```bash
< PROJECT ROOT >
   |
   |-- app/                                      # Implementa a lógica do aplicativo
   |   __init__.py                               # Inicialize o aplicativo
   |    |-- home/                                # Home Blueprint - serve páginas do app (área privada)
   |         |-- templates/                      # UI Kit Pages
   |              |
   |              |-- index.html                 # Página Início
   |              |-- Dashboard.html             # Página Dashboard
   |              |-- page-404.html              # Error 404 - mandatory page
   |              |-- page-500.html              # Error 500 - mandatory page
   |              |-- page-403.html              # Error 403 - mandatory page
   |
   |    |-- base/                                # Base Blueprint - lida com a autenticação
   |         |-- vups/                           # Biblioteca com os modulos customizados
   |         |    |-- __init__                   # Inicializa a biblioteca
   |         |    |-- const.py                   # Constantes e registros para o aplicativo
   |         |    |-- graphs.py                  # Módulo com as funções para plot de gráficos
   |         |    |-- utils.py                   # Módulo com métodos acessários e utilitários
   |         |    |-- data.py                    # Módulo para acesso a dados
   |         |-- static/
   |         |    |-- <css, JS, images>          # CSS files, Javascripts files
   |         |
   |         |-- templates/                      # Modelos usados ​​para renderizar páginas
   |              |
   |              |-- includes/                  #
   |              |    |-- navigation.html       # Componente do menu superior
   |              |    |-- sidebar.html          # Componente da barra lateral
   |              |    |-- footer.html           # Rodapé do aplicativo
   |              |    |-- scripts.html          # Scripts comuns a todas as páginas
   |              |
   |              |-- layouts/                   # Páginas mestre
   |              |    |-- base-fullscreen.html  # Usado por páginas de autenticação
   |              |    |-- base.html             # Usado por páginas comuns
   |              |
   |              |-- accounts/                  # Páginas de autenticação
   |                   |-- login.html            # Página de login
   |                   |-- register.html         # Página de registro
   |
   |-- requirements.txt                          # Pacotes Python necessários
   |
   |-- .env                                      # Configuração de injeção via ambiente
   |-- config.py                                 # Configura o aplicativo
   |-- run.py                                    # Inicia o aplicativo - gateway WSGI
   |
   |-- ************************************************************************
```

<br />

## Deploy

O deploy do projeto foi feito na [Amazon Web Service](https://aws.amazon.com/). Instanciamos uma máquina virtual na nuvem e nela implantamos e configuramos o projeto.

Link: http://ec2-18-220-57-143.us-east-2.compute.amazonaws.com:5000/ 
<br />

---