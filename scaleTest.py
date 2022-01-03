import plotly.graph_objects as go
import numpy as np

if __name__ == '__main__':
    traces = []

    layout = go.Layout(
        barmode='stack',
        xaxis=dict(
            domain=[0, 0.9],
            side='top'
        ),
        yaxis=dict(
            domain=[0, 1],
            range=[0, 100]
        ),
        xaxis2=dict(
            domain=[0.9, 1],
            anchor='y2',
            range=[0, 1],
            showgrid=False,
            showticklabels=False
        ),
        yaxis2=dict(
            domain=[0, 1],
            anchor='x2',
            showgrid=False,
            range=[0, 100]
        ),
    )
    y0 = np.random.rand(1000)*100
    y1 = [25,25,20,25,15]
    traces.append(go.Box(y=y0))
    traces.append(go.Box(y=y0))
    traces.append(go.Box(y=y0))
    traces.append(go.Bar(y=[y1[0]], xaxis='x2', yaxis='y2', width=2, showlegend=False, hoverinfo='skip'))
    traces.append(go.Bar(y=[y1[1]], xaxis='x2', yaxis='y2', width=2, showlegend=False, hoverinfo='skip'))
    traces.append(go.Bar(y=[y1[2]], xaxis='x2', yaxis='y2', width=2, showlegend=False, hoverinfo='skip'))
    traces.append(go.Bar(y=[y1[3]], xaxis='x2', yaxis='y2', width=2, showlegend=False, hoverinfo='skip'))
    traces.append(go.Bar(y=[y1[4]], xaxis='x2', yaxis='y2', width=2, showlegend=False, hoverinfo='skip'))
    fig = go.Figure(data=traces, layout=layout)
    fig.show()