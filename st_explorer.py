from pkg_resources import run_script
import streamlit as st
import pandas as pd
import numpy as np
from lib import vups


# TÍTULO
# ============================================================================
st.title('Clã VUPS')


# DADOS
# ============================================================================
DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache)")


# CHECKBOX - Se marcado, exibe os dados brutos
# ============================================================================
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)


# HISTOGRAMA
# ============================================================================
st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)


# Plotar dados em um mapa
# ============================================================================
# Usar um histograma com o conjunto de dados do Uber nos ajudou a determinar 
# quais são os horários de maior movimento para as coletas, 
# mas e se quiséssemos descobrir onde as coletas estavam concentradas na cidade. 
#
# Embora você possa usar um gráfico de barras para mostrar esses dados, 
# não seria fácil interpretá-los, a menos que você estivesse 
# intimamente familiarizado com as coordenadas latitudinais e longitudinais da cidade. 
#
# Para mostrar a concentração de captação, vamos usar a função st.map () do Streamlit 
# para sobrepor os dados em um mapa da cidade de Nova York.
# ----------------------------------------------------------------------------

# SLIDER
hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)