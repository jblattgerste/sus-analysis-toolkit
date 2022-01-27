import statistics
from collections import Counter
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import Annotations
import plotly.io as pio
from plotly.subplots import make_subplots

import Helper

pio.templates.default = 'seaborn'

plotSize = {0: 500,
            1: 500,
            2: 600,
            3: 700,
            4: 800,
            5: 900,
            'horizontal': 900}


def CreateRadarChart(SUSData, questionsTicked, SUSIds):
    fig = go.Figure()
    set_PaperBGColor(fig)
    questions = ['Question 1', 'Question 2', 'Question 3', 'Question 4', 'Question 5', 'Question 6',
                 'Question 7', 'Question 8', 'Question 9',
                 'Question 10']

    hovertext = ['I think that I would like to use this system frequently.',
                 'I found the system unnecessarily complex.',
                 'I thought the system was easy to use.',
                 'I think that I would need the support of a technical person to be able to use this system.',
                 'I found the various functions in this system were well integrated.',
                 'I thought there was too much inconsistency in this system.',
                 'I would imagine that most people would learn to use this system very quickly.',
                 'I found the system very cumbersome to use.',
                 'I felt very confident using the system.',
                 'I needed to learn a lot of things before I could get going with this system.']

    removeIdxs = []

    for idx, question in enumerate(questions):
        if question not in questionsTicked:
            removeIdxs.append(idx)

    for study in SUSData.SUSStuds:
        if study.name in SUSIds:
            plotData = []

            for questionScore in study.avgScorePerQuestion:
                plotData.append(questionScore)
            filteredPlotData = [i for j, i in enumerate(plotData) if j not in removeIdxs]
            filteredQuestions = [i for j, i in enumerate(questions) if j not in removeIdxs]
            filteredHover = [i for j, i in enumerate(hovertext) if j not in removeIdxs]
            # Have to add the data for the last point twice, so the radar chart appears closed
            filteredQuestions.append(filteredQuestions[0])
            filteredHover.append(filteredHover[0])
            filteredPlotData.append(filteredPlotData[0])
            fig.add_trace(go.Scatterpolar(
                r0=90,
                dr=10,
                r=filteredPlotData,
                theta=filteredQuestions,
                fill='toself',
                name=study.name,
                hovertext=filteredHover,

            ))

    fig.update_layout(
        margin=dict(
            l=12,
            r=12,
            b=40,
            t=40,
        ),
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            ),
            angularaxis=dict(
                direction="clockwise")
        ))

    return fig


def CreateLikertChart(SUSData, questionsTicked, colorizeByMeaning):

    questions = ['Question 1', 'Question 2', 'Question 3', 'Question 4', 'Question 5', 'Question 6',
                 'Question 7', 'Question 8', 'Question 9',
                 'Question 10']

    y_data = [{'question': 'I think that I would like to<br> use this system frequently.',
               'positiveWording': True},
              {'question': 'I found the system <br>unnecessarily complex.',
               'positiveWording': False},
              {'question': 'I thought the system was easy to use.',
               'positiveWording': True},
              {
                  'question': 'I think that I would need the support<br>of a technical person to be able to<br>use this system.',
                  'positiveWording': False},
              {'question': 'I found the various functions in<br> this system were well integrated.',
               'positiveWording': True},
              {'question': 'I thought there was too much <br>inconsistency in this system.',
               'positiveWording': False},
              {'question': 'I would imagine that most people<br> would learn to use this system very quickly.',
               'positiveWording': True},
              {'question': 'I found the system very <br>cumbersome to use.',
               'positiveWording': False},
              {'question': 'I felt very confident<br> using the system.',
               'positiveWording': True},
              {'question': 'I needed to learn a lot of things before<br> I could get going with this system.',
               'positiveWording': False}]

    top_labels = ['Strongly<br>agree', 'Agree', 'Neutral', 'Disagree',
                  'Strongly<br>disagree']

    colors = ['#8FD14F', '#CEE741',
              '#FEF445', '#FAC710',
              '#F24726']

    x_data = [[],
              [],
              [],
              [],
              [],
              [],
              [],
              [],
              [],
              []]

    removeIdxs = []

    for idx, question in enumerate(questions):
        if question not in questionsTicked:
            removeIdxs.append(idx)

    for i, questionResults in enumerate(SUSData.rawResultPerQuestion):
        for j in range(1, 6):
            x_data[i].append(questionResults.count(j) / len(SUSData.rawResultPerQuestion[0]) * 100)
        # x_data_strings[i].append(round(questionResults.count(j)/len(questionResults)*100))

    x_data = [i for j, i in enumerate(x_data) if j not in removeIdxs]
    y_data = [i for j, i in enumerate(y_data) if j not in removeIdxs]

    # x_data_strings.reverse()
    x_data.reverse()
    y_data.reverse()

    fig = go.Figure()

    for i in range(0, len(x_data[0])):
        j = 0
        for xd, yd in zip(x_data, y_data):
            if yd['positiveWording'] != 0 or colorizeByMeaning == 'regular':
                fig.add_trace(go.Bar(
                    x=[xd[i]], y=[yd['question']],
                    orientation='h',
                    marker=dict(
                        color=colors[i],
                        line=dict(color='rgb(248, 248, 249)', width=1)
                    )
                ))
            else:
                fig.add_trace(go.Bar(
                    x=[xd[i]], y=[yd['question']],
                    orientation='h',
                    marker=dict(
                        color=colors[4 - i],
                        line=dict(color='rgb(248, 248, 249)', width=1)
                    )
                ))
            j += 1

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
            domain=[0.15, 1],
            range=[0, 100]
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        barmode='stack',
        paper_bgcolor='#FAFAFA',
        plot_bgcolor='#FAFAFA',
        showlegend=False,
        margin=dict(
            l=150,
            r=12,
            b=12,
        ),
    )

    annotations = []
    labelPos = 10
    label_offset = 20

    for yd, xd in zip(y_data, x_data):
        # labeling the y-axis
        annotations.append(dict(xref='paper', yref='y',
                                x=0.14, y=yd['question'],
                                xanchor='right',
                                text=str(yd['question']),
                                font=dict(family='Arial', size=10,
                                          color='rgb(67, 67, 67)'),
                                showarrow=False, align='right'))
        # labeling the first percentage of each bar (x_axis)
        percentage = round(xd[0])
        if percentage != 0:
            annotations.append(dict(xref='x', yref='y',
                                    x=xd[0] / 2, y=yd['question'],
                                    text=str(round(xd[0])) + '%',
                                    font=dict(family='Arial', size=14),
                                    showarrow=False))
        # labeling the first Likert scale (on the top)
        if yd == y_data[-1]:
            annotations.append(dict(xref='x', yref='paper',
                                    x=labelPos, y=1.15,
                                    text=top_labels[0],
                                    font=dict(family='Arial', size=14,
                                              color='rgb(67, 67, 67)'),
                                    showarrow=False))
        space = xd[0]
        for i in range(1, len(xd)):
            # labeling the rest of percentages for each bar (x_axis)
            percentage = round(xd[i])
            if percentage != 0:
                annotations.append(dict(xref='x', yref='y',
                                        x=space + (xd[i] / 2), y=yd['question'],
                                        text=str(round(xd[i])) + '%',
                                        font=dict(family='Arial', size=14),
                                        showarrow=False))
            # labeling the Likert scale
            if yd == y_data[-1]:
                labelPos += label_offset
                annotations.append(dict(xref='x', yref='paper',
                                        x=labelPos, y=1.15,
                                        text=top_labels[i],
                                        font=dict(family='Arial', size=14,
                                                  color='rgb(67, 67, 67)'),
                                        showarrow=False))
            space += xd[i]

    fig.update_layout(annotations=annotations)
    return fig


def CreateMainplot(SUSData, boxpoints, scaleValue, orientationValue, plotStyle, mean_sdValue, axis_title):

    mean_sdValue = determineMean_sdValue(mean_sdValue)
    fig = go.Figure()
    set_PaperBGColor(fig)

    if plotStyle == 'notched':
        notchedValue = True
    else:
        notchedValue = False

    if boxpoints == 'False':
        boxpoints = False

    if orientationValue == 'vertical':
        for study in SUSData.SUSStuds:
            if plotStyle == 'mainplot' or plotStyle == 'notched':
                fig.add_trace(
                    go.Box(y=study.getAllSUSScores(), name=study.name, boxpoints=boxpoints, boxmean=mean_sdValue,
                           notched=notchedValue))
            elif plotStyle == 'per-question-chart':
                fig.add_trace(
                    go.Bar(y=[study.Score], name=study.name, x=[study.name],
                           error_y=dict(type='data', array=[study.standardDevOverall])))

        if scaleValue == 'none':
            fig.update_layout(
                yaxis_range=[0, 100],
                xaxis_title=axis_title,
                yaxis_title="SUS Score",
                uniformtext=dict(mode="show", minsize=9),
                margin=dict(
                    l=0,
                    r=0,
                    b=12,
                    t=12,
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
            )
        else:
            fig.update_layout(
                yaxis_range=[0, 100],
                xaxis_title=axis_title,
                yaxis_title="SUS Score",
                uniformtext=dict(mode="show", minsize=9),
                margin=dict(
                    l=0,
                    r=0,
                    b=12,
                    t=12,
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                barmode='stack',
                xaxis=dict(
                    domain=[0, 0.9],
                ),
                yaxis=dict(
                    domain=[0, 1],
                    range=[0, 100]
                ),
                xaxis2=dict(
                    domain=[0.9, 1],
                    anchor='y2',
                    range=[-0.5, 0.5],
                    showgrid=False,
                    showticklabels=False
                ),
                yaxis2=dict(
                    domain=[0, 1],
                    anchor='x2',
                    showgrid=False,
                    range=[0, 100],
                    showticklabels=False
                ),
            )

        fig.layout.yaxis.fixedrange = True
    else:
        for study in SUSData.SUSStuds:
            if plotStyle == 'mainplot' or plotStyle == 'notched':
                fig.add_trace(
                    go.Box(x=study.getAllSUSScores(), name=study.name, boxpoints=boxpoints, boxmean=mean_sdValue,
                           notched=notchedValue))
            elif plotStyle == 'per-question-chart':
                fig.add_trace(
                    go.Bar(x=[study.Score], name=study.name, y=[study.name], orientation='h',
                           error_x=dict(type='data', array=[study.standardDevOverall])))

        if scaleValue == 'none':
            fig.update_layout(
                yaxis_title=axis_title,
                xaxis_title="SUS Score",
                xaxis_range=[0, 100],
                barmode='stack',
                margin=dict(
                    l=0,
                    r=0,
                    b=12,
                    t=12,
                ),
                xaxis=dict(
                    domain=[0, 1],
                    range=[0, 100],
                    tickmode='linear',
                    tick0=0,
                    dtick=10,
                )
            )
        else:
            fig.update_layout(
                yaxis_title=axis_title,
                xaxis_title="SUS Score",
                xaxis_range=[0, 100],
                barmode='stack',
                margin=dict(
                    l=0,
                    r=0,
                    b=12,
                    t=12,
                ),
                yaxis=dict(
                    domain=[0, 0.8],
                ),
                xaxis=dict(
                    domain=[0, 1],
                    range=[0, 100],
                    tickmode='linear',
                    tick0=0,
                    dtick=10,
                ),
                yaxis2=dict(
                    domain=[0.8, 1],
                    anchor='x2',
                    range=[-0.5, 0.5],
                    showgrid=False,
                    showticklabels=False
                ),
                xaxis2=dict(
                    domain=[0, 1],
                    anchor='y2',
                    showgrid=False,
                    range=[0, 100],
                    showticklabels=False
                ),
            )
        fig.layout.xaxis.fixedrange = True

    # If enabled, add contextualization Scales
    if scaleValue != 'none':
        fig.add_traces(scales[scaleValue](orientationValue))

    return fig


def CreatePerQuestionChart(SUSData, questionsTicked, SUSIds, orientationValue):
    fig = go.Figure()
    set_PaperBGColor(fig)
    questions = ['Question 1', 'Question 2', 'Question 3', 'Question 4', 'Question 5', 'Question 6',
                 'Question 7', 'Question 8', 'Question 9',
                 'Question 10']

    hovertext = ['I think that I would like to use this system frequently.',
                 'I found the system unnecessarily complex.',
                 'I thought the system was easy to use.',
                 'I think that I would need the support of a technical person to be able to use this system.',
                 'I found the various functions in this system were well integrated.',
                 'I thought there was too much inconsistency in this system.',
                 'I would imagine that most people would learn to use this system very quickly.',
                 'I found the system very cumbersome to use.',
                 'I felt very confident using the system.',
                 'I needed to learn a lot of things before I could get going with this system.']

    removeIdxs = []

    for idx, question in enumerate(questions):
        if question not in questionsTicked:
            removeIdxs.append(idx)

    if orientationValue == 'vertical':
        for study in SUSData.SUSStuds:
            if study.name in SUSIds:
                plotData = []

                for questionScore in study.avgScorePerQuestion:
                    plotData.append(questionScore)
                filteredErrorBars = [i for j, i in enumerate(study.standardDevPerQuestion) if j not in removeIdxs]
                filteredQuestions = [i for j, i in enumerate(questions) if j not in removeIdxs]
                filteredHover = [i for j, i in enumerate(hovertext) if j not in removeIdxs]
                fig.add_trace(go.Bar(name=study.name, y=plotData, x=filteredQuestions, hovertext=filteredHover,
                                     error_y=dict(type='data', array=filteredErrorBars)))

        fig.update_layout(
            xaxis_title="System",
            yaxis_title="SUS Score",
            yaxis_range=[0, 10],
            margin=dict(
                l=12,
                r=12,
                b=12,
                t=12,
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
    else:
        for study in SUSData.SUSStuds:
            if study.name in SUSIds:
                plotData = []

                for questionScore in study.avgScorePerQuestion:
                    plotData.append(questionScore)

                filteredErrorBars = [i for j, i in enumerate(study.standardDevPerQuestion) if j not in removeIdxs]
                filteredQuestions = [i for j, i in enumerate(questions) if j not in removeIdxs]
                filteredHover = [i for j, i in enumerate(hovertext) if j not in removeIdxs]
                fig.add_trace(
                    go.Bar(name=study.name, x=plotData, y=filteredQuestions, hovertext=filteredHover, orientation='h',
                           error_x=dict(type='data', array=filteredErrorBars)))

        fig.update_layout(
            yaxis_title="System",
            xaxis_title="SUS Score",
            xaxis_range=[0, 10],
            margin=dict(
                l=12,
                r=12,
                b=12,
                t=12,
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
        )

    return fig


def CreateConclusivenessChart(SUSData):
    yVal = [35, 75, 80, 100, 100]
    xVal = [6, 8, 10, 12, 14]
    studySampleSizes = dict()

    for study in SUSData.SUSStuds:
        if len(study.Results) > 14:
            sampleSize = 14
        else:
            sampleSize = len(study.Results)

        studySampleSizes[study.name] = sampleSize

    studySamples = []
    annotations = []
    for idx, study in enumerate(studySampleSizes):
        studySamples.append(studySampleSizes[study])
        occurrences = Counter(studySamples)
        annotations.append(Annotations.generateConclusivenessAnnotation(studySampleSizes[study], study,
                                                                        occurrences[studySampleSizes[study]] * 5))

    fig = go.Figure()
    set_PaperBGColor(fig)
    fig.add_trace(go.Scatter(x=xVal, y=yVal))
    fig.update_layout(
        margin=dict(
            l=0,
            r=0,
            b=12,
            t=12,
        ),
        annotations=annotations,
        xaxis_title="Sample Size",
        yaxis_title="Conclusiveness Percentage",
        #yaxis=dict(
       #     tickmode='array',
       #     tickvals=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
       #     ticktext=['10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%', '100%']
        #)
    )
    return fig


def CreatePercentilePlot(SUSData, systems):
    x = np.linspace(0, 100, 100)
    y = parametrizePercentile(x)
    fig = go.Figure()
    set_PaperBGColor(fig)

    defaultPlotlyColors = ['#1f77b4', ' #ff7f0e', '#2ca02c', ' #d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
                           '#bcbd22', '#17becf']

    fig.update_layout(dict(
        xaxis_title='SUS Score',
        yaxis_title='Percentile Value',
        margin=dict(
            l=0,
            r=0,
            b=12,
            t=12,
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        colorway=['#1f77b4', ' #ff7f0e', '#2ca02c', ' #d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22',
                  '#17becf']
    ))
    fig.layout.yaxis.fixedrange = True

    fig.add_trace(go.Scatter(x=x, y=y, showlegend=False))
    for i, study in enumerate(SUSData.SUSStuds):
        if study.name in systems:
            fig.add_trace(go.Scatter(x=[study.Score], y=[parametrizePercentile(study.Score)],
                                     marker=dict(size=12, color=defaultPlotlyColors[i]),
                                     mode='markers',
                                     name=study.name))
    return fig


def parametrizePercentile(x):
    a1 = 106.3
    b1 = 118
    c1 = 46.32
    a2 = 33.06
    b2 = 81.58
    c2 = 15.92

    return a1 * np.exp(-((x - b1) / c1) ** 2) + a2 * np.exp(-((x - b2) / c2) ** 2)


def update_Datapoints(figure, datapointValues):
    if datapointValues == 'False':
        datapointValues = False
    for element in figure['data']:
        element['boxpoints'] = datapointValues
    return figure


def set_PaperBGColor(fig):
    fig.update_layout(
        paper_bgcolor='#FAFAFA'
    )


def determineMean_sdValue(mean_sdValue):
    if mean_sdValue == 'neither':
        return False
    if mean_sdValue == 'mean':
        return True
    return mean_sdValue


def parseDataForTable(SUSData):
    mins = ["Min"]
    firstQuartiles = ["First Quartile"]
    medians = ["Median"]
    thirdQuartiles = ["Third Quartile"]
    maxs = ["Max"]
    OverallScores = ["Score (mean)"]
    standardDeviation = ["Standard Dev."]

    for study in SUSData.SUSStuds:
        OverallScores.append(round(study.Score, 2))
        susScores = study.getAllSUSScores()
        mins.append(min(susScores))
        try:
            firstQuartiles.append(statistics.quantiles(susScores)[0])
        except statistics.StatisticsError:
            firstQuartiles.append('-')
        try:
            medians.append(statistics.median(susScores))
        except statistics.StatisticsError:
            medians.append('-')
        try:
            thirdQuartiles.append(statistics.quantiles(susScores)[2])
        except statistics.StatisticsError:
            thirdQuartiles.append('-')
        maxs.append(max(susScores))
        standardDeviation.append(round(study.standardDevOverall, 2))

    data = {
        'Min': mins,
        'First Quartile': firstQuartiles,
        'Median': medians,
        'Overall Score (mean)': OverallScores,
        'Standard Deviation': standardDeviation,
        'Third Quartile': thirdQuartiles,
        'Max': maxs,
    }
    df = pd.DataFrame(data)
    return df


# noinspection PyTypeChecker
def getAdjectiveScaleTraces(orientation, xaxis='x2', yaxis='y2'):
    if orientation == 'vertical':
        traces = [
            go.Bar(y=[25], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip',
                   text="Worst<br>Imagineable",
                   marker_color='#F24726', insidetextanchor='middle'),
            go.Bar(y=[26.7], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='Poor',
                   marker_color='#FAC710', insidetextanchor='middle'),
            go.Bar(y=[19.3], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='OK',
                   marker_color='#FEF445', insidetextanchor='middle'),
            go.Bar(y=[9.7], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='Good',
                   marker_color='#CEE741', insidetextanchor='middle'),
            go.Bar(y=[3.3], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='Excellent',
                   marker_color='#8FD14F', insidetextanchor='middle'),
            go.Bar(y=[16], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip',
                   text='Best<br>Imagineable',
                   marker_color='#E6E6E6', insidetextanchor='middle')
        ]
    else:
        traces = [
            go.Bar(x=[25], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip',
                   text="Worst<br>Imagineable",
                   marker_color='#F24726', insidetextanchor='middle'),
            go.Bar(x=[26.7], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='Poor',
                   marker_color='#FAC710', insidetextanchor='middle'),
            go.Bar(x=[19.3], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='OK',
                   marker_color='#FEF445', insidetextanchor='middle'),
            go.Bar(x=[9.7], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='Good',
                   marker_color='#CEE741', insidetextanchor='middle'),
            go.Bar(x=[3.3], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='Excellent',
                   marker_color='#8FD14F', insidetextanchor='middle'),
            go.Bar(x=[16], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip',
                   text='Best<br>Imagineable',
                   marker_color='#E6E6E6', insidetextanchor='middle')
        ]
    return traces


# noinspection PyTypeChecker
def getGradeScaleTraces(orientation, xaxis='x2', yaxis='y2'):
    if orientation == 'vertical':
        traces = [
        go.Bar(y=[51.6], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='F',
               marker_color='#F24726', insidetextanchor='middle'),
        go.Bar(y=[11], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='D',
               marker_color='#FAC710', insidetextanchor='middle'),
        go.Bar(y=[9.9], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='C',
               marker_color='#FEF445', insidetextanchor='middle'),
        go.Bar(y=[6.3], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='B',
               marker_color='#CEE741', insidetextanchor='middle'),
        go.Bar(y=[21.2], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='A',
               marker_color='#8FD14F', insidetextanchor='middle')]
    else:
        traces = [
            go.Bar(x=[51.6], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='F',
                   marker_color='#F24726', insidetextanchor='middle'),
            go.Bar(x=[11], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='D',
                   marker_color='#FAC710', insidetextanchor='middle'),
            go.Bar(x=[9.9], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='C',
                   marker_color='#FEF445', insidetextanchor='middle'),
            go.Bar(x=[6.3], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='B',
                   marker_color='#CEE741', insidetextanchor='middle'),
            go.Bar(x=[21.2], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='A',
                   marker_color='#8FD14F', insidetextanchor='middle')
        ]
    return traces


# noinspection PyTypeChecker
def getAcceptabilityScaleTraces(orientation, xaxis='x2', yaxis='y2'):
    if orientation == 'vertical':
        traces = [
            go.Bar(y=[51.6], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip',
                   text='Not<br>Acceptable',
                   marker_color='#F24726', insidetextanchor='middle'),
            go.Bar(y=[20.9], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='Marginal',
                   marker_color='#FEF445', insidetextanchor='middle'),
            go.Bar(y=[27.5], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='Acceptable',
                   marker_color='#8FD14F', insidetextanchor='middle'),
        ]
    else:
        traces = [
            go.Bar(x=[51.6], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip',
                   text='Not<br>Acceptable',
                   marker_color='#F24726', insidetextanchor='middle'),
            go.Bar(x=[20.9], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='Marginal',
                   marker_color='#FEF445', insidetextanchor='middle'),
            go.Bar(x=[27.5], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='Acceptable',
                   marker_color='#8FD14F', insidetextanchor='middle')
        ]
    return traces


# noinspection PyTypeChecker
def getPromoterScaleTraces(orientation, xaxis='x2', yaxis='y2'):
    if orientation == 'vertical':
        traces = [
            go.Bar(y=[62.5], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='Detractor',
                   marker_color='#F24726', insidetextanchor='middle'),
            go.Bar(y=[16.3], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='Passive',
                   marker_color='#FEF445', insidetextanchor='middle'),
            go.Bar(y=[21.2], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='Promoter',
                   marker_color='#8FD14F', insidetextanchor='middle')
        ]
    else:
        traces = [
            go.Bar(x=[62.5], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='Detractor',
                   marker_color='#F24726', insidetextanchor='middle'),
            go.Bar(x=[16.3], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='Passive',
                   marker_color='#FEF445', insidetextanchor='middle'),
            go.Bar(x=[21.2], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='Promoter',
                   marker_color='#8FD14F', insidetextanchor='middle')
        ]
    return traces


def getEmptyScaleTraces(orientation):
    return []


# noinspection PyTypeChecker
def getQuartileScaleTraces(orientation, xaxis='x2', yaxis='y2'):
    if orientation == 'vertical':
        traces = [
            go.Bar(y=[62.5], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='1st Quartile',
                   marker_color='#F24726', insidetextanchor='middle'),
            go.Bar(y=[8.5], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='2nd Quartile',
                   marker_color='#FAC710', insidetextanchor='middle'),
            go.Bar(y=[7], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='3nd Quartile',
                   marker_color='#FEF445', insidetextanchor='middle'),
            go.Bar(y=[22], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='4th Quartile',
                   marker_color='#CEE741', insidetextanchor='middle'),
        ]
    else:
        traces = [
            go.Bar(x=[62.5], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='1st Quartile',
                   marker_color='#F24726', insidetextanchor='middle'),
            go.Bar(x=[8.5], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='2nd Quartile',
                   marker_color='#FAC710', insidetextanchor='middle'),
            go.Bar(x=[7], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='3nd Quartile',
                   marker_color='#FEF445', insidetextanchor='middle'),
            go.Bar(x=[22], xaxis=xaxis, yaxis=yaxis, width=1, showlegend=False, hoverinfo='skip', text='4th Quartile',
                   marker_color='#CEE741', insidetextanchor='middle'),
        ]
    return traces


# Traces for the various vertical contextualization scales
# noinspection PyTypeChecker
scales = {
    'adjectiveScale': getAdjectiveScaleTraces,
    'gradeScale': getGradeScaleTraces,
    'acceptabilityScale': getAcceptabilityScaleTraces,
    'promoterScale': getPromoterScaleTraces,
    'quartileScale': getQuartileScaleTraces,
    'none': getEmptyScaleTraces
}
