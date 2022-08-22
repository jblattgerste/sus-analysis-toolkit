import numpy as np
import plotly.graph_objects as go
import Annotations
import Charts
import Helper
import plotly.io as pio
pio.templates.default = 'seaborn'


def generateSingleStudyPreset1(singleStudy):
    # Add the traces for Boxplot and Radarchart
    traces = [getSingleStudyBoxPlotTraces(singleStudy), getSingleStudyRadarChartTraces(singleStudy)]
    # Defining the layout for the subplots
    singleStudyLayout = go.Layout(
        barmode='stack',
        xaxis=dict(
            domain=[0, 0.3],
            title='System Usability Scale Study Score',
            title_font_size=12,
            showticklabels=False
        ),
        yaxis=dict(
            domain=[0, 1],
            range=[0, 100],
        ),
        xaxis3=dict(
            domain=[0.55, 1],
            anchor='y3',
        ),
        yaxis3=dict(
            domain=[0, 0.45],
            anchor='x3',
        ),
        polar=dict(
            domain_x=[0.5, 1],
            domain_y=[0, 0.45],
            radialaxis=dict(
                visible=True,
                range=[0, 10],
            ),
            angularaxis=dict(
                direction="clockwise")
        ),
        xaxis2=dict(
            domain=[0.55, 1],
            anchor='y2',
            title='Number of Participants',
            title_font_size=12,
            title_standoff=0.1
        ),
        yaxis2=dict(
            domain=[0.55, 1],
            anchor='x2',
            title_font_size=12,
            title_standoff=0.1,
            title='Conclusiveness Percentange',
        ),
        xaxis4=dict(
            domain=[0.3, 0.367],
            range=[-0.5, 0.5],
            showgrid=False,
            showticklabels=False
        ),
        xaxis5=dict(
            domain=[0.367, 0.434],
            range=[-0.5, 0.5],
            showgrid=False,
            showticklabels=False
        ),
        xaxis6=dict(
            domain=[0.434, 0.5],
            range=[-0.5, 0.5],
            showgrid=False,
            showticklabels=False
        ),
    )

    perQuestionCharTittle = dict(
        x=0.5,
        y=0,
        text='Per Question Values',
        showarrow=False,
        yref='y3 domain',
        xref='x2 domain',
    )

    # Add trace for the conclusiveness Chart
    traces.append(getSingleStudyConclusivenessTraces('x2', 'y2'))

    # The comparison scales for the Box plot
    traces.extend(Charts.scales['adjectiveScale']('vertical', 'x4', 'y'))
    traces.extend(Charts.scales['gradeScale']('vertical', 'x5', 'y'))
    traces.extend(Charts.scales['acceptabilityScale']('vertical', 'x6', 'y'))
    # annotations = Annotations.getSingleScoreScale()

    # Define figure with traces
    fig = go.Figure(data=traces, layout=singleStudyLayout)
    fig.update_layout(
        showlegend=False,
        margin=dict(
            l=12,
            r=12,
            b=12,
            t=40,
        ),
    paper_bgcolor='#FAFAFA'
    )

    # Add Annotations of comparison scales as well as the marker for the conclusiveness chart.
    fig.add_annotation(Annotations.generateConclusivenessAnnotationSingleStudy(singleStudy, 'x2', 'y2'))
    # fig.add_annotation(perQuestionCharTittle)

    return fig


def generateSingleStudyPreset2(singleStudy):
    questions = ['Question 1', 'Question 2', 'Question 3', 'Question 4', 'Question 5', 'Question 6',
                 'Question 7', 'Question 8', 'Question 9',
                 'Question 10']
    traces = []

    tick_labels_likertScale = ['Strongly<br>disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly<br>agree']
    # Add the trace for the SUS Boxplot
    traces.append(getSingleStudyBoxPlotTraces(singleStudy))

    # Add the trace for the LikertScale
    likertScaleTraces, likertScaleAnnotaions = getSingleStudyLikertChartTraces(singleStudy, 'byMeaning')
    traces.extend(likertScaleTraces)
    # Defining the layout for the subplots
    singleStudyLayout = go.Layout(
        barmode='stack',
        xaxis=dict(
            domain=[0, 0.3],
            title='System Usability Scale Study Score',
            title_font_size=12,
            showticklabels=False
        ),
        yaxis=dict(
            domain=[0, 1],
            range=[0, 100],
        ),
        xaxis3=dict(
            domain=[0.6, 1],
            anchor='y3',
            showgrid=False,
            range=[0, 100],
            showticklabels=True,
            tickmode='array',
            ticktext=tick_labels_likertScale,
            tickvals=[10, 30, 50, 70, 90]
        ),
        yaxis3=dict(
            domain=[0, 0.45],
            anchor='x3',
            showgrid=False,
            showticklabels=True,
        ),
        xaxis2=dict(
            domain=[0.55, 1],
            anchor='y2',
            title_font_size=12,
            title_standoff=0.1,
            title='Number of participants'
        ),
        yaxis2=dict(
            domain=[0.55, 1],
            anchor='x2',
            title_font_size=12,
            title_standoff=0.1,
            title='Conclusiveness Percentange',
        ),
        xaxis4=dict(
            domain=[0.3, 0.367],
            range=[-0.5, 0.5],
            showgrid=False,
            showticklabels=False
        ),
        xaxis5=dict(
            domain=[0.367, 0.434],
            range=[-0.5, 0.5],
            showgrid=False,
            showticklabels=False
        ),
        xaxis6=dict(
            domain=[0.434, 0.5],
            range=[-0.5, 0.5],
            showgrid=False,
            showticklabels=False
        ),

    )
    # Add trace for the conclusiveness Chart
    traces.append(getSingleStudyConclusivenessTraces('x2', 'y2'))

    # The comparison scales for the Box plot
    traces.extend(Charts.scales['adjectiveScale']('vertical', 'x4', 'y'))
    traces.extend(Charts.scales['gradeScale']('vertical', 'x5', 'y'))
    traces.extend(Charts.scales['acceptabilityScale']('vertical', 'x6', 'y'))
    # annotations = Annotations.getSingleScoreScale()

    # Define figure with traces
    fig = go.Figure(data=traces, layout=singleStudyLayout)
    fig.update_layout(
        showlegend=False,
        margin=dict(
            l=12,
            r=12,
            b=12,
            t=40,
        ),
        paper_bgcolor='#FAFAFA',
    )

    # Add Annotations of comparison scales as well as the marker for the conclusiveness chart.
    fig.add_annotation(Annotations.generateConclusivenessAnnotationSingleStudy(singleStudy, 'x2', 'y2'))
    for annotation in likertScaleAnnotaions:
        fig.add_annotation(annotation)

    return fig


def generateSingleStudyPreset3(singleStudy):
    traces = []
    tick_labels_likertScale = ['Strongly<br>agree', 'Agree', 'Neutral', 'Disagree',
                               'Strongly<br>disagree']

    # Add the trace for the SUS Boxplot
    traces.append(getSingleStudyBoxPlotTraces(singleStudy))

    # Add the trace for the LikertScale
    likertScaleTraces, likertScaleAnnotaitons = getSingleStudyLikertChartTraces(singleStudy, 'byMeaning')
    traces.extend(likertScaleTraces)
    # Defining the layout for the subplots
    singleStudyLayout = go.Layout(
        barmode='stack',
        xaxis=dict(
            domain=[0, 0.3],
            title='System Usability Scale Study Score',
            title_font_size=12,
            showticklabels=False
        ),
        yaxis=dict(
            domain=[0, 1],
            range=[0, 100],
        ),
        xaxis3=dict(
            domain=[0.6, 1],
            anchor='y3',
            showgrid=False,
            range=[0, 100],
            showticklabels=True,
            tickmode='array',
            ticktext=tick_labels_likertScale,
            tickvals=[10, 30, 50, 70, 90]
        ),
        yaxis3=dict(
            domain=[0, 0.45],
            anchor='x3',
            showgrid=False,
            showticklabels=True
        ),
        xaxis2=dict(
            domain=[0.55, 1],
            anchor='y2',
            title_font_size=12,
            title_standoff=0.1,
            title='SUS Study Score'
        ),
        yaxis2=dict(
            domain=[0.55, 1],
            anchor='x2',
            title_font_size=12,
            title_standoff=0.1,
            title='Percentile Value'
        ),
        xaxis4=dict(
            domain=[0.3, 0.367],
            range=[-0.5, 0.5],
            showgrid=False,
            showticklabels=False
        ),
        xaxis5=dict(
            domain=[0.367, 0.434],
            range=[-0.5, 0.5],
            showgrid=False,
            showticklabels=False
        ),
        xaxis6=dict(
            domain=[0.434, 0.5],
            range=[-0.5, 0.5],
            showgrid=False,
            showticklabels=False
        ),
    )

    # Add trace for the conclusiveness Chart
    traces.extend(getSingleStudyPercentilePlotTraces(singleStudy, 'x2', 'y2'))

    # The comparison scales for the Box plot
    traces.extend(Charts.scales['adjectiveScale']('vertical', 'x4', 'y'))
    traces.extend(Charts.scales['gradeScale']('vertical', 'x5', 'y'))
    traces.extend(Charts.scales['acceptabilityScale']('vertical', 'x6', 'y'))
    # annotations = Annotations.getSingleScoreScale()

    # Define figure with traces
    fig = go.Figure(data=traces, layout=singleStudyLayout)
    fig.update_layout(
        showlegend=False,
        margin=dict(
            l=12,
            r=12,
            b=12,
            t=40,
        ),
        paper_bgcolor='#FAFAFA',
    )

    # Add Annotations of comparison scales as well as the marker for the conclusiveness chart.
    for annotation in likertScaleAnnotaitons:
        fig.add_annotation(annotation)

    return fig


def generateSingleStudyPreset4(singleStudy):
    traces = []

    # Add the trace for the SUS Boxplot
    traces.append(getSingleStudyBoxPlotTraces(singleStudy))

    # Add the trace for the conclusiveness Chart
    traces.append(getSingleStudyConclusivenessTraces('x2', 'y2'))

    # Defining the layout for the subplots
    singleStudyLayout = go.Layout(
        barmode='stack',
        xaxis=dict(
            domain=[0, 0.3],
            title='System Usability Scale Study Score',
            title_font_size=12,
            showticklabels=False
        ),
        yaxis=dict(
            domain=[0, 1],
            range=[0, 100],
        ),
        xaxis3=dict(
            domain=[0.55, 1],
            anchor='y3',
            title_font_size=12,
            title_standoff=0.1,
            title='SUS Study Score'
        ),
        yaxis3=dict(
            domain=[0.55, 1],
            anchor='x3',
            title_font_size=12,
            title_standoff=0.1,
            title='Percentile Value'
        ),
        xaxis2=dict(
            domain=[0.55, 1],
            anchor='y2',
            title_font_size=12,
            title_standoff=0.1,
            title='Number of participants'
        ),
        yaxis2=dict(
            domain=[0, 0.45],
            anchor='x2',
            title_font_size=12,
            title_standoff=0.1,
            title='Conclusiveness Percentange',
        ),
        xaxis4=dict(
            domain=[0.3, 0.367],
            range=[-0.5, 0.5],
            showgrid=False,
            showticklabels=False
        ),
        xaxis5=dict(
            domain=[0.367, 0.434],
            range=[-0.5, 0.5],
            showgrid=False,
            showticklabels=False
        ),
        xaxis6=dict(
            domain=[0.434, 0.5],
            range=[-0.5, 0.5],
            showgrid=False,
            showticklabels=False
        ),
    )

    # Add trace for the percentile Chart
    traces.extend(getSingleStudyPercentilePlotTraces(singleStudy, 'x3', 'y3'))

    # The comparison scales for the Box plot
    traces.extend(Charts.scales['adjectiveScale']('vertical', 'x4', 'y'))
    traces.extend(Charts.scales['gradeScale']('vertical', 'x5', 'y'))
    traces.extend(Charts.scales['acceptabilityScale']('vertical', 'x6', 'y'))
    # annotations = Annotations.getSingleScoreScale()

    # Define figure with traces
    fig = go.Figure(data=traces, layout=singleStudyLayout)
    fig.update_layout(
        showlegend=False,
        margin=dict(
            l=12,
            r=12,
            b=12,
            t=40,
        ),
        paper_bgcolor='#FAFAFA',
    )

    # Add Annotations of comparison scales as well as the marker for the conclusiveness chart.
    fig.add_annotation(Annotations.generateConclusivenessAnnotationSingleStudy(singleStudy, 'x2', 'y2'))
    return fig


def getSingleStudyBoxPlotTraces(singleStudy):
    return go.Box(y=singleStudy.getAllSUSScores(), name=singleStudy.name, boxmean='sd', boxpoints='all')


def getSingleStudyPercentilePlotTraces(singleStudy, xaxis, yaxis):
    x = np.linspace(0, 100, 100)
    y = Charts.parametrizePercentile(x)
    traces = [go.Scatter(x=x, y=y, showlegend=False, xaxis=xaxis, yaxis=yaxis, hoverinfo='skip'),
              go.Scatter(x=[singleStudy.Score], y=[Charts.parametrizePercentile(singleStudy.Score)],
                         marker=dict(size=12), mode='markers', xaxis=xaxis, yaxis=yaxis,
                         hovertemplate='%{y:d}th Percentile' + '<extra></extra>',
                         )]
    return traces


def getSingleStudyRadarChartTraces(singleStudy):
    plotData = []
    questions = Helper.SUSQuestions
    questions.append(Helper.SUSQuestions[0])
    questionText = Helper.SUSQuestionsTexts
    questionText.append(Helper.SUSQuestionsTexts[0])
    for questionScore in singleStudy.avgScorePerQuestion:
        plotData.append(questionScore)
    plotData.append(plotData[0])
    return go.Scatterpolar(
        r0=90,
        dr=10,
        r=plotData,
        theta=questions,
        fill='toself',
        name=singleStudy.name,
        hovertext=questionText,
    )


def getSingleStudyConclusivenessTraces(xaxis, yaxis):
    yVal = [35, 75, 80, 100, 100]
    xVal = [6, 8, 10, 12, 14]
    return go.Scatter(x=xVal, y=yVal, xaxis=xaxis, yaxis=yaxis,  hoverinfo='skip')


def getSingleStudyLikertChartTraces(singleStudy, colorizeByMeaning):
    traces = []

    y_data = [{'question': 'Question 1',
               'positiveWording': True},
              {'question': 'Question 2',
               'positiveWording': False},
              {'question': 'Question 3',
               'positiveWording': True},
              {
                  'question': 'Question 4',
                  'positiveWording': False},
              {'question': 'Question 5',
               'positiveWording': True},
              {'question': 'Question 6',
               'positiveWording': False},
              {'question': 'Question 7',
               'positiveWording': True},
              {'question': 'Question 8',
               'positiveWording': False},
              {'question': 'Question 9',
               'positiveWording': True},
              {'question': 'Question 10',
               'positiveWording': False}]

    colors = ['#8FD14F', '#CEE741', '#FEF445', '#FAC710', '#F24726']
    top_labels = ['Strongly<br>disagree', 'Disagree', 'Neutral', 'Agree', 'Strongly<br>agree']

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

    for i, questionResults in enumerate(singleStudy.rawResultPerQuestion):
        for j in range(1, 6):
            x_data[i].append(questionResults.count(j) / len(singleStudy.rawResultPerQuestion[0]) * 100)
        # x_data_strings[i].append(round(questionResults.count(j)/len(questionResults)*100))

    # x_data_strings.reverse()
    x_data.reverse()
    y_data.reverse()

    for i in range(0, len(x_data[0])):
        j = 0
        for xd, yd in zip(x_data, y_data):
            if yd['positiveWording'] != 0 or colorizeByMeaning == 'regular':
                traces.append(go.Bar(
                    xaxis='x3',
                    yaxis='y3',
                    hovertemplate='%{x:d}%, ' + '%{text}<extra></extra>',
                    text=[top_labels[i]],
                    x=[xd[i]], y=[yd['question']],
                    textposition="none",
                    orientation='h',
                    marker=dict(
                        color=colors[4-i],
                        line=dict(color='rgb(248, 248, 249)', width=1)
                    )
                ))
            else:
                traces.append(go.Bar(
                    hovertemplate='%{x:d}%, ' + '%{text}<extra></extra>',
                    text=[top_labels[i]],
                    xaxis='x3',
                    yaxis='y3',
                    x=[xd[i]], y=[yd['question']],
                    textposition="none",
                    orientation='h',
                    marker=dict(
                        color=colors[i],
                        line=dict(color='rgb(248, 248, 249)', width=1)
                    )
                ))
            j += 1

    annotations = []
    for yd, xd in zip(y_data, x_data):
        percentage = round(xd[0])
        if percentage != 0:
            annotations.append(dict(xref='x3', yref='y3',
                                    x=xd[0] / 2, y=yd['question'],
                                    text=str(round(xd[0])) + '%',
                                    font=dict(family='Arial', size=14),
                                    showarrow=False))
        # labeling the first Likert scale (on the top)
        space = xd[0]
        for i in range(1, len(xd)):
            # labeling the rest of percentages for each bar (x_axis)
            percentage = round(xd[i])
            if percentage != 0:
                annotations.append(dict(xref='x3', yref='y3',
                                        x=space + (xd[i] / 2), y=yd['question'],
                                        text=str(round(xd[i])) + '%',
                                        font=dict(family='Arial', size=14),
                                        showarrow=False))
            space += xd[i]
    return traces, annotations


singleStudyPresetDict = {
    'preset_1': generateSingleStudyPreset1,
    'preset_2': generateSingleStudyPreset2,
    'preset_3': generateSingleStudyPreset3,
    'preset_4': generateSingleStudyPreset4
}
