import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
from lib import vups
from lib import const

st.title('Meu primeiro App Streamlit!')

st.write('## **Teste markdown!**')


microdados = vups.datasets.microdados(nrows=1000)
st.dataframe(microdados)
fig1 = vups.plot_bar()
fig2 = vups.plot_year_taxs()
fig2
# Desenhe um gráfico de linha
# ============================================================================
# Você pode adicionar facilmente um gráfico de linha ao seu aplicativo com st.line_chart (). 
# Vamos gerar uma amostra aleatória usando Numpy e, em seguida, traçá-la.
# ----------------------------------------------------------------------------

chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['a', 'b', 'c'])

st.line_chart(chart_data)


# Desenhe um mapa
# ============================================================================
# Com st.map () você pode exibir pontos de dados em um mapa. 
# Vamos usar o Numpy para gerar alguns dados de amostra e 
# plotá-los em um mapa de San Francisco.
# ----------------------------------------------------------------------------

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(map_data)


# Use as caixas de seleção para mostrar / ocultar dados
# ============================================================================
# Um caso de uso para as caixas de seleção é ocultar ou mostrar um gráfico ou seção específica em um aplicativo. 
# st.checkbox () recebe um único argumento, que é o rótulo do widget. 
# Neste exemplo, a caixa de seleção é usada para alternar uma instrução condicional.
# ----------------------------------------------------------------------------

if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])

    chart_data


# Use uma caixa de seleção para opções
# ============================================================================
# Use st.selectbox para escolher entre uma série. 
# Você pode escrever as opções desejadas ou passar por uma matriz ou coluna de quadro de dados. 
# Vamos usar o quadro de dados df que criamos anteriormente.
# ----------------------------------------------------------------------------

df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})

# option = st.selectbox(
#     'Which number do you like best?',
#      df['first column'])

# 'You selected: ', option


# Organize seu aplicativo
# ============================================================================
# Para uma aparência mais limpa, você pode mover seus widgets para uma barra lateral. 
# Isso mantém seu aplicativo no centro, enquanto os widgets são fixados à esquerda. 
# Vamos dar uma olhada em como você pode usar st.sidebar em seu aplicativo.
# ----------------------------------------------------------------------------

option = st.sidebar.selectbox(
    'Which number do you like best?',
     df['first column'])

'You selected:', option

# A maioria dos elementos que você pode colocar em seu aplicativo 
# também podem ser colocados em uma barra lateral usando esta sintaxe: 
#   st.sidebar.[Element_name]()
# 
# Aqui estão alguns exemplos que mostram como ele é usado: 
#   st.sidebar.markdown(), 
#   st.sidebar.slider(), 
#   st.sidebar.line_chart().
# 
# Você também pode usar st.columns para dispor os widgets lado a lado ou 
# st.expander para economizar espaço ocultando um conteúdo grande.

left_column, right_column = st.columns(2)
pressed = left_column.button('Press me?')
if pressed:
    right_column.write("Woohoo!")

expander = st.expander("FAQ")
expander.write("Here you could put in some really, really long explanations...")


# Mostrar progresso
# ============================================================================
# Ao adicionar cálculos de longa execução a um aplicativo, 
# você pode usar st.progress () para exibir o status em tempo real.
# Primeiro, vamos importar o tempo. 
# Vamos usar o método time.sleep () para simular um cálculo de longa execução:
# ----------------------------------------------------------------------------

import time

# Agora, vamos criar uma barra de progresso:

'Starting a long computation...'

# Add a placeholder
latest_iteration = st.empty()
bar = st.progress(0)

for i in range(100):
  # Update the progress bar with each iteration.
  latest_iteration.text(f'Iteration {i+1}')
  bar.progress(i + 1)
  time.sleep(0.1)

'...and now we\'re done!'

# Compartilhe seu aplicativo
# ============================================================================
# Depois de criar um aplicativo Streamlit, é hora de compartilhá-lo!
# Para mostrá-lo ao mundo, você pode usar o compartilhamento Streamlit para implantar, 
# gerenciar e compartilhar seu aplicativo gratuitamente. 
# No momento, o compartilhamento do Streamlit é apenas para convidados, 
# então solicite um convite e receberemos um em breve!
# ----------------------------------------------------------------------------

# Funciona em 3 etapas simples: 
#   - Coloque seu aplicativo em um repositório público do Github (e certifique-se de que ele tenha um requirements.txt!) 
#   - Faça login em share.streamlit.io 
#   - Clique em "Implementar um aplicativo" e cole no URL do GitHub

# ----------------------------------------------------------------------------

st.text('This will appear first')
# Appends some text to the app.

my_slot1 = st.empty()
# Appends an empty slot to the app. We'll use this later.

my_slot2 = st.empty()
# Appends another empty slot.

st.text('This will appear last')
# Appends some more text to the app.

my_slot1.text('This will appear second')
# Replaces the first empty slot with a text string.

my_slot2.line_chart(np.random.randn(20, 2))
# Replaces the second empty slot with a chart.
