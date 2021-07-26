import os
import pandas as pd
import plotly.express as px


def get_data(filename='MICRODADOS.csv', warn_bad_lines=True, test=False):
    if not test:
        BASEDIR = os.path.abspath('')
        DATADIR = os.path.join(BASEDIR + '\\data\\')
        DATASET = filename
        SEP = ";"
        DATADIC = 'dictionary.md'

        PATH = os.path.join(DATADIR + DATASET)

        dataset = pd.read_csv(
            PATH, 
            sep=SEP, 
            error_bad_lines=False, 
            encoding='latin1',
            warn_bad_lines=warn_bad_lines)
    else:
        # dataset = pd.DataFrame({
        #     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        #     "Amount": [4, 1, 2, 2, 4, 5],
        #     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
        # })
        dataset = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')

    return dataset

def plot_qtd_pessoas_x_sintomas(df):
    # Tratamento de dados
    from itertools import compress
    import matplotlib.pyplot as plt
    plt.style.use('seaborn-talk')
    
    df3 = df[['Classificacao', 'Febre', 'DificuldadeRespiratoria', 'Tosse', 'Coriza', 'DorGarganta', 'Diarreia', 'Cefaleia',
        'ComorbidadePulmao', 'ComorbidadeCardio', 'ComorbidadeRenal', 'ComorbidadeDiabetes', 'ComorbidadeTabagismo',
        'ComorbidadeObesidade', 'DataObito']].dropna()

    df3['Sintomas'] = df3[['Febre', 'DificuldadeRespiratoria', 'Tosse', 'Coriza', 'DorGarganta', 'Diarreia', 'Cefaleia',
        'ComorbidadePulmao', 'ComorbidadeCardio', 'ComorbidadeRenal', 'ComorbidadeDiabetes', 'ComorbidadeTabagismo',
        'ComorbidadeObesidade']].values.tolist()

    sintomas = ['Febre', 'DificuldadeRespiratoria', 'Tosse', 'Coriza', 'DorGarganta', 'Diarreia', 'Cefaleia',
        'ComorbidadePulmao', 'ComorbidadeCardio', 'ComorbidadeRenal', 'ComorbidadeDiabetes', 'ComorbidadeTabagismo',
        'ComorbidadeObesidade']

    df3['Sintomas'] = df3['Sintomas'].apply(lambda x: [True if item=='Sim' else False for item in x])

    df3['Sintomas'] = df3['Sintomas'].apply(lambda x: list(compress(sintomas, x)))

    df3['Qntd_sintomas'] = df3['Sintomas'].apply(lambda x: len(x))

    df3['Classificacao'].value_counts()

    # df2.iloc[df3[df3['Qntd_sintomas']==0].index].head()
    confirmados = df3[df3['Classificacao']=='Confirmados']
    descartados = df3[df3['Classificacao']=='Descartados']
    suspeitos = df3[df3['Classificacao']=='Suspeitos']
    #confirmados['DataObito'] = pd.to_datetime(confirmados['DataObito'])
    #descartados['DataObito'] = pd.to_datetime(descartados['DataObito'])
    #suspeitos['DataObito'] = pd.to_datetime(suspeitos['DataObito'])

    confirmados['Assintomatico'] = confirmados['Sintomas'].apply(lambda x:  'sim' if x==[] else 'nao')

    dic = {}
    
    for i in confirmados['Sintomas'].apply(lambda x: x):
        for j in i:
            dic[j] = dic.get(j, 0) + 1
    
    sintomas = pd.Series(dic)
    sintomas_prop = round(sintomas / sintomas.sum() * 100, ndigits=2)
    sintomas_prop.sort_values()
    
    pd.DataFrame({'Qntd': sintomas}).sort_values('Qntd').plot.barh(legend=False, figsize=(12,10))
    plt.xlabel('# de pessoas com o sintoma', fontsize=12)
    return 

def plot_bar(df):
    df = ''
    return

def plot_bar(df):
    return px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

def plot_scatter(df, selected_year):
    
    filtered_df = df[df.year == selected_year]

    fig = px.scatter(filtered_df, x="gdpPercap", y="lifeExp",
                     size="pop", color="continent", hover_name="country",
                     log_x=True, size_max=55)

    fig.update_layout(transition_duration=500)

    return fig

def generate_table(df, max_rows=10):
    import dash_html_components as html

    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in df.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(df.iloc[i][col]) for col in df.columns
            ]) for i in range(min(len(df), max_rows))
        ])
    ]
)

def plot_uallas(df):
    return