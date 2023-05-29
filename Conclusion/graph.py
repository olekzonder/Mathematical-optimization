import random
from point import Point
import numpy as np
import plotly.graph_objs as go

def plot_graph(points=False, unopt=False, pareto=False, optimal=False,most_optimal=False,ideal = False):
    x = np.linspace(0,50,1000)
    y = np.linspace(0,50,1000)
    X,Y = np.meshgrid(x,y)
    mask = (X**2)/2304 + (Y-24)**2/576 <= 1 & (-X+Y <= 24) & (X+Y >= 48)
    fig = go.Figure()
    if points:
        fig.add_trace(go.Scatter(x=[point.f1 for point in points],y=[point.f2 for point in points], mode='markers',name='Точки'))
    
    if unopt:
        fig.add_trace(go.Scatter(x=[point.f1 for point in unopt],y=[point.f2 for point in unopt], mode='markers', marker=dict(color='red'),name='Заведомо не эффективные точки'))
    
    if pareto:
        fig.add_trace(go.Scatter(x=[point.f1 for point in pareto],y=[point.f2 for point in pareto], mode='markers', marker=dict(color='green'),name='Множество Парето'))
    
    if optimal:
        fig.add_trace(go.Scatter(x=[point.f1 for point in optimal],y=[point.f2 for point in optimal], mode='markers', marker=dict(color='blue'),name='Оптимальный проект'))
    if most_optimal:
        fig.add_trace(go.Scatter(x=[point.f1 for point in most_optimal],y=[point.f2 for point in most_optimal], mode='markers', marker=dict(color='cyan'),name='Наиболее оптимальный проект'))
    if ideal:
        fig.add_trace(go.Scatter(x=[point.f1 for point in ideal],y=[point.f2 for point in ideal], mode='markers', marker=dict(color='magenta'),name='Идеальная точка'))
    fig.update_layout(xaxis_title='F1', yaxis_title='F2')
    fig.update_xaxes(range=[0, 50])
    fig.update_yaxes(range=[0, 50])
    fig.update_traces(showlegend=False)
    fig.update_layout(height=800)
    fig.update_layout(
    xaxis=dict(
        showgrid=True,
        gridcolor='rgb(200, 200, 200)',
        dtick=5
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='rgb(200, 200, 200)',
        dtick=5
    ),
    )
    arrowx_dict = [dict(x=0, y=50, ax=0, ay=675, showarrow=True, xref='x', yref='y', arrowhead=5, arrowsize=1.5, arrowwidth=1)]
    arrowy_dict = [dict(x=50, y=0, ax=-1500, ay=0, showarrow=True, xref='x', yref='y', arrowhead=5, arrowsize=1.5, arrowwidth=1)]
    fig.update_layout(annotations=arrowx_dict+arrowy_dict)
    return fig
