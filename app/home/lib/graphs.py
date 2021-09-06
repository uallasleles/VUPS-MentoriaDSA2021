import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from app.home.lib import const
import os

def plot_kpi_percentage_progress():
    """
    Global Actual Progress
    Baseline 46%
    """
    fig_c1 = go.Figure(go.Indicator(
        mode="number+delta",
        value=35,
        number={'suffix': "%", "font": {"size": 40, 'color': "#008080", 'family': "Arial"}},
        delta={'position': "bottom", 'reference': 46, 'relative': False},
        domain={'x': [0, 1], 'y': [0, 1]}))
    fig_c1.update_layout(autosize=False,
                        width=350, height=90, margin=dict(l=20, r=20, b=20, t=30),
                        paper_bgcolor="#fbfff0", font={'size': 20})
    return fig_c1

def plot_kpi_spend_hours():
    """
    Global Spend Hours
    Baseline 92.700
    """
    fig_c2 = go.Figure(go.Indicator(
        mode="number+delta",
        value=73500,
        number={'suffix': " HH", "font": {"size": 40, 'color': "#008080", 'family': "Arial"}, 'valueformat': ',f'},
        delta={'position': "bottom", 'reference': 92700},
        domain={'x': [0, 1], 'y': [0, 1]}))
    fig_c2.update_layout(autosize=False,
                            width=350, height=90, margin=dict(l=20, r=20, b=20, t=30),
                            paper_bgcolor="#fbfff0", font={'size': 20})
    fig_c2.update_traces(delta_decreasing_color="#3D9970",
                            delta_increasing_color="#FF4136",
                            delta_valueformat='f',
                            selector=dict(type='indicator'))
    return fig_c2

def plot_kpi_tcpi():
    """
    TPCI - To Complete Performance Index ≤ 1.00
    """
    fig_c3 = go.Figure(go.Indicator(
        mode="number+delta",
        value=1.085,
        number={"font": {"size": 40, 'color': "#008080", 'family': "Arial"}},
        delta={'position': "bottom", 'reference': 1, 'relative': False},
        domain={'x': [0, 1], 'y': [0, 1]}))
    fig_c3.update_layout(
        autosize=False,
        width=350, height=90, margin=dict(l=20, r=20, b=20, t=30),
        paper_bgcolor="#fbfff0", font={'size': 20})
    fig_c3.update_traces(
        delta_decreasing_color="#3D9970",
        delta_increasing_color="#FF4136",
        delta_valueformat='.3f',
        selector=dict(type='indicator'))
    return fig_c3

def plot_small_bar_percentage_progress():
    x = ['Actual', 'Previous', 'Average', 'Planned']
    y = [5.5, 4.2, 6.3, 8.5]
    fig_m_prog = go.Figure([go.Bar(x=x, y=y, text=y, textposition='auto')])
    fig_m_prog.update_layout(
        paper_bgcolor="#fbfff0", plot_bgcolor="#fbfff0",
        font={'color': "#008080", 'family': "Arial"}, height=100, width=250,
        margin=dict(l=15, r=1, b=4, t=4))
    fig_m_prog.update_yaxes(title='y', visible=False, showticklabels=False)
    fig_m_prog.update_traces(marker_color='#17A2B8', selector=dict(type='bar'))
    return fig_m_prog

def plot_small_bar_spend_hours():
    x = ['Δ vs Prev', 'Δ vs Aver', 'Δ vs Plan']
    y = [10, 12, 8]
    fig_m_hh = go.Figure([go.Bar(x=x, y=y, text=y, textposition='auto')])
    fig_m_hh.update_layout(
        paper_bgcolor="#fbfff0", plot_bgcolor="#fbfff0",
        font={'color': "#008080", 'family': "Arial"}, height=100, width=250,
        margin=dict(l=15, r=1, b=1, t=1))
    fig_m_hh.update_yaxes(title='y', visible=False, showticklabels=False)
    fig_m_hh.update_traces(marker_color='#17A2B8', selector=dict(type='bar'))
    return fig_m_hh

data=pd.read_excel(os.path.join(const.DATADIR + 'curva.xlsx'))

def plot_line_progress_actual_planned():
    y = data.loc[data.Activity_name == 'Total']
    # Create traces
    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=y['Date'], y=y['Progress'],
                                mode='lines',
                                name='Progress',
                                marker_color='#FF4136'))
    fig3.add_trace(go.Scatter(x=y['Date'], y=y['Baseline'],
                                mode='lines',
                                name='Baseline',
                                marker_color='#17A2B8'))
    fig3.update_layout(title={'text': "Actual Progress vs Planned", 'x': 0.5}, paper_bgcolor="#fbfff0",
                        plot_bgcolor="#fbfff0", font={'color': "#008080", 'size': 12, 'family': "Georgia"}, height=220,
                        width=540,
                        legend=dict(orientation="h",
                                    yanchor="top",
                                    y=0.99,
                                    xanchor="left",
                                    x=0.01),
                        margin=dict(l=1, r=1, b=1, t=30))
    fig3.update_xaxes(showline=True, linewidth=1, linecolor='#F7F7F7', mirror=True, nticks=6, rangemode="tozero",
                        showgrid=False, gridwidth=0.5, gridcolor='#F7F7F7')
    fig3.update_yaxes(showline=True, linewidth=1, linecolor='#F7F7F7', mirror=True, nticks=10, rangemode="tozero",
                        showgrid=True, gridwidth=0.5, gridcolor='#F7F7F7')
    fig3.layout.yaxis.tickformat = ',.0%'
    return fig3

def plot_widget_cost_variance():
    fig_cv = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=1.05,
        number={"font": {"size": 22, 'color': "#008080", 'family': "Arial"}, "valueformat": "#,##0"},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [None, 1.5], 'tickwidth': 1, 'tickcolor': "black"},
            'bar': {'color': "#06282d"},
            'bgcolor': "white",
            'steps': [
                {'range': [0, 1], 'color': '#FF4136'},
                {'range': [1, 1.5], 'color': '#3D9970'}]}))

    fig_cv.update_layout(paper_bgcolor="#fbfff0", font={'color': "#008080", 'family': "Arial"}, height=135, width=250,
                            margin=dict(l=10, r=10, b=15, t=20))
    return fig_cv

def plot_widget_schedule_variance():
    fig_sv = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=0.95,
        number={"font": {"size": 22, 'color': "#008080", 'family': "Arial"}, "valueformat": "#,##0"},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [None, 1.5], 'tickwidth': 1, 'tickcolor': "black"},
            'bar': {'color': "#06282d"},
            'bgcolor': "white",
            'steps': [
                {'range': [0, 1], 'color': '#FF4136'},
                {'range': [1, 1.5], 'color': '#3D9970'}]}))
    fig_sv.update_layout(paper_bgcolor="#fbfff0", font={'color': "#008080", 'family': "Arial"}, height=135, width=250,
                            margin=dict(l=10, r=10, b=15, t=20))
    return fig_sv

def plot_bar_hours_spend_planned():
    y = data.loc[data.Activity_name == 'Total']
    y = data.loc[data.Activity_name == 'Total']
    fig_hh = go.Figure()
    fig_hh.add_trace(go.Bar(
        x=y['Date'],
        y=y['Spend_Hours'],
        name='Spend Hours',
        marker_color='#FF4136'
    ))
    fig_hh.add_trace(go.Bar(
        x=y['Date'],
        y=y['Planned_Hours'],
        name='Planned Hours',
        marker_color='#17A2B8'
    ))
    fig_hh.update_layout(barmode='group', title={'text': 'Spend Hours vs Planned', 'x': 0.5}, paper_bgcolor="#fbfff0",
                            plot_bgcolor="#fbfff0", font={'color': "#008080", 'family': "Georgia"}, height=250, width=540,
                            legend=dict(orientation="h",
                                        yanchor="top",
                                        y=0.99,
                                        xanchor="left",
                                        x=0.01),
                            margin=dict(l=5, r=1, b=1, t=25))
    fig_hh.update_xaxes(showline=True, linewidth=1, linecolor='#F7F7F7', mirror=True, nticks=6, rangemode="tozero",
                        showgrid=False, gridwidth=0.5, gridcolor='#F7F7F7')
    fig_hh.update_yaxes(showline=True, linewidth=1, linecolor='#F7F7F7', mirror=True, nticks=10, rangemode="tozero",
                        showgrid=False, gridwidth=0.5, gridcolor='#F7F7F7')
    return fig_hh

def plot_gantt():
    # *******Gantt Chart
    df = pd.DataFrame([
        dict(Disc="Civ", Start='2021-01-04', Finish='2021-08-10'),
        dict(Disc="Mec", Start='2021-03-05', Finish='2021-09-15'),
        dict(Disc="Pip", Start='2021-04-20', Finish='2021-11-30'),
        dict(Disc="Ele", Start='2021-05-20', Finish='2021-12-05'),
        dict(Disc="Ins", Start='2021-06-20', Finish='2021-12-20'),
        dict(Disc="Com", Start='2021-07-20', Finish='2021-12-30')
    ])
    fig2 = px.timeline(df, x_start="Start", x_end="Finish", y='Disc')
    fig2.update_yaxes(autorange="reversed")
    fig2.update_layout(title={'text': "Main dates", 'x': 0.5}, plot_bgcolor="#eef9ea", paper_bgcolor="#eef9ea",
                        font={'color': "#008080", 'family': "Georgia"}, height=340, width=550, margin=dict(
            l=51, r=5, b=10, t=50))
    fig2.update_traces(marker_color='#17A2B8', selector=dict(type='bar'))
    return fig2