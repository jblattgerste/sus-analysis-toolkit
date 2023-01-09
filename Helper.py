import base64
import copy
import random
from dataclasses import dataclass
# noinspection PyProtectedMember
from bs4 import UnicodeDammit
import pandas as pd
from dash import html, dcc
import io
from dash.dash_table.Format import Format, Scheme

import ChartLayouts
from Result import Result
from SUSDataset import SUSDataset
from SUSStud import SUSStud
import numpy as np


def parseDataFrameToSUSDataset(dataFrame, singleStudy=False):
    """Parses through DataFrame and creates and returns a list with SUSStuds from it."""

    # Set with each individual study.
    studySet = set(dataFrame['System'])

    # Container for SUSStuds
    SUSStudies = []

    for singleStudy in studySet:
        # All the Study results, which belong to the current singleStudy
        resultsRawString = dataFrame.loc[dataFrame['System'] == singleStudy].values.tolist()
        # remove first and last element, as they are the index and System-String in the dataframe
        for result in resultsRawString:
            result.pop()

        # Container for the current Results
        results = []

        # Create result objects and add them to container.
        for idx, result in enumerate(resultsRawString):
            results.append(Result(result, idx))

        # Create SUSStuds-instances and append to list
        SUSStudies.append(SUSStud(results, singleStudy))

    return SUSStudies


def decodeContentToCSV(contents):
    content_type, csvData = contents.split(',')
    decoded = base64.b64decode(csvData)

    # Tries to encoding format of uploaded file
    suggestion = UnicodeDammit(decoded)
    csvData = pd.read_csv(io.StringIO(decoded.decode(suggestion.original_encoding, errors="strict")), sep=';')

    return csvData


def stringListToFloat(stringList):
    """Converts a list with strings into a list with floats."""
    return [float(singleFloatResult) for singleFloatResult in stringList]


def downloadChartContentSingleStudy(fig):
    fig = copy.copy(fig)
    fig.update_layout(
        paper_bgcolor='rgba(255,255,255,255)',
        font=dict(
            size=20),
        xaxis=dict(title_font_size=20),
        xaxis3=dict(title_font_size=20),
        yaxis3=dict(title_font_size=20),
        xaxis2=dict(
            title_font_size=20,
        ),
        yaxis2=dict(
            title_font_size=20,
        ),

    )
    img_bytes = fig.to_image(format="png", width=1530, height=1048)

    encoding = base64.b64encode(img_bytes).decode()
    img_b64 = "data:image/png;base64," + encoding

    downloadChart = [
        html.A(html.Button('Download this chart', className='button1'), href=img_b64, download='plot')
    ]
    return downloadChart


def downloadChartContent(downloadType, fig, customWidth=None, customHeight=None, customFontSize=None):

    if downloadType == 'customSize':
        fig.update_layout(
            paper_bgcolor='rgba(255,255,255,255)',
            font=dict(
                size=customFontSize)
        )
        img_bytes = fig.to_image(format="png", width=customWidth,
                                 height=customHeight)
    else:
        fig.update_layout(
            paper_bgcolor='rgba(255,255,255,255)',
            font=dict(
                size=plotSettings[downloadType].fontSize)
        )
        img_bytes = fig.to_image(format="png", width=plotSettings[downloadType].width,
                                 height=plotSettings[downloadType].height)
    return img_bytes


def downloadChartContent_orientation(fig, download_format, orientation):
    fig = copy.copy(fig)
    fig.update_layout(
        paper_bgcolor='rgba(255,255,255,255)',
    )
    if orientation == 'vertical':
        if download_format == "narrowPlot":
            img_bytes = fig.to_image(format="png", width=1300, height=500)
        elif download_format == "dynamicPlot":
            img_bytes = fig.to_image(format="png")
        elif download_format == "widePlot":
            img_bytes = fig.to_image(format="png", width=1600, height=500)
        else:
            img_bytes = fig.to_image(format="png", width=1300, height=500)
    else:
        if download_format == "singleColumn":
            img_bytes = fig.to_image(format="png", width=900, height=500)
        elif download_format == "doubleColumn":
            img_bytes = fig.to_image(format="png", width=900, height=700)
        elif download_format == "wideFigurePresentationStyle":
            img_bytes = fig.to_image(format="png", width=900, height=400)
        else:
            img_bytes = fig.to_image(format="png", width=900, height=700)

    encoding = base64.b64encode(img_bytes).decode()
    img_b64 = "data:image/png;base64," + encoding

    downloadChart = [
        html.A(html.Button('Download this chart', className='button1'), href=img_b64, download='plot')
    ]
    return downloadChart


def checkUploadFile(csvData, isSingleStudy):
    if isSingleStudy:
        if 'System' not in csvData:
            csvData['System'] = 'System'
        if len(csvData['System'].unique()) != 1:
            raise WrongUploadFileException(
                'This csv-file contained multiple systems. Try a csv file with only one system or use the multi study upload.')
        columns = csvData.columns.values
        if len(columns) != 11:
            raise WrongUploadFileException('Wrong amount of columns in CSV-File')
        if True in np.nditer(csvData.isnull()):
            raise WrongUploadFileException('There is a NaN value in the dataframe')
    else:
        if 'System' not in csvData:
            raise WrongUploadFileException('There must be System column in the CSV-File')
        columns = csvData.columns.values
        if len(columns) != 11:
            raise WrongUploadFileException('Wrong amount of columns in CSV-File')
        if True in np.nditer(csvData.isnull()):
            raise WrongUploadFileException('There is a NaN value in the dataframe')
    return csvData


class WrongUploadFileException(Exception):
    pass


scaleInfoTexts = {
    'adjectiveScale': html.P(children=[
        'The adjective scale contextualizes SUS study scores on descriptive adjectives ranging from \"Worst Imaginable\" to \"Best Imaginable\". It is based on ',
        html.A('Sauro et al. 2018', href='https://measuringu.com/interpret-sus-score', target="_blank"),
        '\'s interpretation of the primary data by ',
        html.A('Bangor et al. 2009',
               href='https://scholar.google.de/citations?view_op=view_citation&hl=de&user=BD7BLDgAAAAJ&citation_for_view=BD7BLDgAAAAJ:d1gkVwhDpl0C',
               target="_blank"),
        '.'
    ]),
    'gradeScale': html.P(
        children=[
            'The grade scale contextualizes SUS study scores on school grades ranging from \"F\" to \"A\".  This scale is based on the data from ',
            html.A('Sauro et al. 2016',
                   href='https://scholar.google.de/citations?view_op=view_citation&hl=de&user=rmiLIsYAAAAJ&citation_for_view=rmiLIsYAAAAJ:Mojj43d5GZwC',
                   target="_blank"),
            '. Note: There is multiple interpretations of the grade scale, e.g. the one proposed by ',
            html.A('Bangor et al. 2009',
                   href='https://scholar.google.de/citations?view_op=view_citation&hl=de&user=BD7BLDgAAAAJ&citation_for_view=BD7BLDgAAAAJ:d1gkVwhDpl0C',
                   target="_blank"),
            ' uses different ranges.'
        ]),
    'quartileScale': html.P(
        children=['The quartile scale was developed by splitting a dataset of 3500 SUS scores into four quartiles (',
                  html.A('Bangor et al. 2009',
                         href='https://scholar.google.de/citations?view_op=view_citation&hl=de&user=BD7BLDgAAAAJ&citation_for_view=BD7BLDgAAAAJ:d1gkVwhDpl0C',
                         target="_blank"),
                  '). It can be used to contextualize and compare SUS study scores against the scores in the dataset.']),
    'acceptabilityScale': html.P(children=[
        'The acceptability scale contextualizes SUS study scores on descriptions ranging from \"Not Acceptable\" over \"Marginally accaptable\" to \"Acceptable\". This scale is based on data from ',
        html.A('Bangor et al. 2008',
               href='https://scholar.google.de/citations?view_op=view_citation&hl=de&user=BD7BLDgAAAAJ&citation_for_view=BD7BLDgAAAAJ:u5HHmVD_uO8C',
               target="_blank"),
        ' and derived from implications of the grading and adjective scales.']),
    'promoterScale': html.P(children=[
        'The Net Promoter score scale describes how likely users of a product are to recommend the System to others. It is based on data from ',
        html.A('Sauro et al. 2012', href='https://measuringu.com/nps-sus/', target="_blank"),
        '.']),
    'industryBenchmarkScale': html.P(children=[
        'This non-empirical scale is derived from ', html.A('Lewis et al. 2018',
                                                    href='https://scholar.google.de/citations?view_op=view_citation&hl=de&user=rmiLIsYAAAAJ&citation_for_view=rmiLIsYAAAAJ:a9-T7VOCCH8C',
                                                    target="_blank"),
        '. It is based on the idea that 68 is the average SUS study score but a SUS score of 80 is commonly observed to be an “industrial benchmark” to reach as evidence of an above average user experience.']),
    'none': ""
}

plotStyleInfoTexts = {
    'mainplot': "Displays SUS study scores as boxplots.",
    'per-question-chart': "Displays the SUS study score on bar charts with standard deviation.",
    'notched': "Displays SUS study scores as notched boxplots. The notches can help identifying skewed distributions of data.",
}

SUSQuestions = ['Question 1', 'Question 2', 'Question 3', 'Question 4', 'Question 5', 'Question 6',
                'Question 7', 'Question 8', 'Question 9',
                'Question 10']

SUSQuestionsTexts = ['I think that I would like to use this system frequently.',
                     'I found the system unnecessarily complex.',
                     'I thought the system was easy to use.',
                     'I think that I would need the support of a technical person to be able to use this system.',
                     'I found the various functions in this system were well integrated.',
                     'I thought there was too much inconsistency in this system.',
                     'I would imagine that most people would learn to use this system very quickly.',
                     'I found the system very cumbersome to use.',
                     'I felt very confident using the system.',
                     'I needed to learn a lot of things before I could get going with this system.']

ConclusivenessValues = dict({0: '0%',
                             6: '35%',
                             7: '55%',
                             8: '75%',
                             9: '78%',
                             10: '80%',
                             11: '98%',
                             12: '100%',
                             13: '100%',
                             14: '100%'
                             })


def filterSUSStuds(SUSData, systemsToPlot):
    studies = SUSData.SUSStuds
    SUSData.SUSStuds = list(filter(lambda study: study.name in systemsToPlot, studies))
    return SUSData


def getAdjectiveValue(score):
    if score < 25.1:
        return "Worst Imaginable"
    if score < 51.7:
        return "Poor"
    if score < 71.1:
        return "OK"
    if score < 80.7:
        return "Good"
    if score < 84:
        return "Excellent"
    else:
        return "Best Imaginable"


def getGradeScaleValue(score):
    if score < 51.6:
        return "F"
    if score < 62.6:
        return "D"
    if score < 72.5:
        return "C"
    if score < 78.8:
        return "B"
    else:
        return "A"


def getQuartileScaleValue(score):
    if score < 62.5:
        return "1st"
    if score < 71:
        return "2nd"
    if score < 78:
        return "3rd"
    else:
        return "4th"


def getAcceptabilityValue(score):
    if score < 51.7:
        return "Not Acceptable"
    if score < 72.6:
        return "Marginal"
    else:
        return "Acceptable"


def getNPSValue(score):
    if score < 62.5:
        return "Detractor"
    if score < 78.8:
        return "Passive"
    else:
        return "Promoter"


def getIndustryBenchmarkValue(score):
    if score < 68:
        return "Below Average"
    if score < 80:
        return "Above Average"
    else:
        return "Above Industry Standard"


def getConclusiveness(study):
    sampleSize = len(study.Results)
    if sampleSize < 6:
        return '0%'
    elif sampleSize < 15:
        return ConclusivenessValues.get(sampleSize)
    else:
        return '100%'


def tableDataIsInvalid(table_data):
    # Check whether table is empty
    if table_data:
        for row in table_data:
            cells = list(row.values())
            if all([cell != '' for cell in cells]) and all([cell is not None for cell in cells]) and all(
                    [0 < int(cell) < 6 for cell in cells[0:9]]):
                continue
            else:
                return True
    else:
        return True


def conditionalFormattingEditableDataTable(columnNames):
    style_data_conditional = []
    for name in columnNames[0:10]:
        style_data_conditional.extend([
            {
                'if': {
                    'filter_query': '{' + '{name}'.format(name=name) + '}< 1 ||' + '{' + '{name}'.format(
                        name=name) + '} > 5',
                    'column_id': '{name}'.format(name=name)
                },
                'backgroundColor': 'tomato',
                'color': 'white'
            },
            {
                'if': {
                    'filter_query': '{' + '{name}'.format(name=name) + '} is blank',
                    'column_id': '{name}'.format(name=name)
                },
                'backgroundColor': 'tomato',
                'color': 'white'
            },
        ]
        )
    style_data_conditional.append(
        {
            'if': {
                'filter_query': '{' + '{name}'.format(name=columnNames[10]) + '} is blank',
                'column_id': '{name}'.format(name=columnNames[10])
            },
            'backgroundColor': 'tomato',
            'color': 'white'
        },
    )
    return style_data_conditional


# Generates an example dataframe with random SUS values
def createExampleDataFrame(singleStudy=False):
    if singleStudy:
        df = pd.read_csv('assets/singleStudyData.csv', sep=';')
    else:
        df = pd.read_csv('assets/studyData.csv', sep=';')
    return df
    # Random data generation... deprecated for now
    # exampleData = {}
    # for i in range(1, 11):
    #     exampleData['Question {qNumber}'.format(qNumber=i)] = [random.randint(1, 5), random.randint(1, 5)]
    # # Only Multi Study table has a system column
    # if singleStudy is False:
    #     exampleData['System'] = ['Example System A', 'Example System B']
    # else:
    #     exampleData['System'] = ['Example System', 'Example System']
    # dataframe = pd.DataFrame(data=exampleData)
    # return dataframe


dataframeQuartileConditions = [
    {
        'if': {
            'column_id': 'SUS Score (mean) '
        },
        'fontWeight': 'bold'
    },
    {
        'if': {'row_index': 'odd'},
        'backgroundColor': 'rgb(248, 248, 248)'
    },
    {
        'if': {
            'filter_query': '{SUS Score (mean) } < 100.1',
            # 'column_id': 'SUS Score (mean) '
        },
        'color': 'black',
        'backgroundColor': '#CEE741'
    },
    {
        'if': {
            'filter_query': '{SUS Score (mean) } < 78',
            # 'column_id': 'SUS Score (mean) '
        },
        'color': 'black',
        'backgroundColor': '#FEF445'
    },
    {
        'if': {
            'filter_query': '{SUS Score (mean) } < 71',
            # 'column_id': 'SUS Score (mean) '
        },
        'color': 'black',
        'backgroundColor': '#FAC710'
    },
    {
        'if': {
            'filter_query': '{SUS Score (mean) } < 62.5',
            # 'column_id': 'SUS Score (mean) '
        },
        'color': 'black',
        'backgroundColor': '#F24726'
    }
]

dataframeAcceptabilityConditions = [
    {
        'if': {
            'column_id': 'SUS Score (mean) '
        },
        'fontWeight': 'bold'
    },
    {
        'if': {'row_index': 'odd'},
        'backgroundColor': 'rgb(248, 248, 248)'
    },
    {
        'if': {
            'filter_query': '{SUS Score (mean) } < 100.1',
            # 'column_id': 'SUS Score (mean) '
        },
        'color': 'black',
        'backgroundColor': '#8FD14F'
    },
    {
        'if': {
            'filter_query': '{SUS Score (mean) } < 72.6',
            # 'column_id': 'SUS Score (mean) '
        },
        'color': 'black',
        'backgroundColor': '#FEF445'
    },
    {
        'if': {
            'filter_query': '{SUS Score (mean) } < 51.7',
            # 'column_id': 'SUS Score (mean) '
        },
        'color': 'black',
        'backgroundColor': '#F24726'
    },
]

dataframeGradeConditions = [
    {
        'if': {
            'column_id': 'SUS Score (mean) '
        },
        'fontWeight': 'bold'
    },
    {
        'if': {'row_index': 'odd'},
        'backgroundColor': 'rgb(248, 248, 248)'
    },
    {
        'if': {
            'filter_query': '{SUS Score (mean) } < 100.1',
            # 'column_id': 'SUS Score (mean) '
        },
        'color': 'black',
        'backgroundColor': '#8FD14F'
    },
    {
        'if': {
            'filter_query': '{SUS Score (mean) } < 78.8',
            # 'column_id': 'SUS Score (mean) '
        },
        'color': 'black',
        'backgroundColor': '#CEE741'
    },
    {
        'if': {
            'filter_query': '{SUS Score (mean) } < 72.5',
            # 'column_id': 'SUS Score (mean) '
        },
        'color': 'black',
        'backgroundColor': '#FEF445'
    },
    {
        'if': {
            'filter_query': '{SUS Score (mean) } < 62.6',
            # 'column_id': 'SUS Score (mean) '
        },
        'color': 'black',
        'backgroundColor': '#FAC710'
    },
    {
        'if': {
            'filter_query': '{SUS Score (mean) } < 51.6',
            # 'column_id': 'SUS Score (mean) '
        },
        'color': 'black',
        'backgroundColor': '#F24726'
    },
]

dataframeAdjectiveConditions = [
    {
        'if': {
            'column_id': 'SUS Score (mean) '
        },
        'fontWeight': 'bold'
    },
    {
        'if': {'row_index': 'odd'},
        'backgroundColor': 'rgb(248, 248, 248)'
    },
    {
        'if': {
            'filter_query': '{SUS Score (mean) } < 100.1',
            # 'column_id': 'SUS Score (mean) '
        },
        'color': 'white',
        'backgroundColor': '#008000'
    },
    {
        'if': {
            'filter_query': '{SUS Score (mean) } < 84.1',
            # 'column_id': 'SUS Score (mean) '
        },
        'color': 'black',
        'backgroundColor': '#8FD14F'
    },
    {
        'if': {
            'filter_query': '{SUS Score (mean) } < 80.8',
            # 'column_id': 'SUS Score (mean) '
        },
        'color': 'black',
        'backgroundColor': '#CEE741'
    },
    {
        'if': {
            'filter_query': '{SUS Score (mean) } < 71.1',
            # 'column_id': 'SUS Score (mean) '
        },
        'color': 'black',
        'backgroundColor': '#FEF445'
    },
    {
        'if': {
            'filter_query': '{SUS Score (mean) } < 51.7',
            # 'column_id': 'SUS Score (mean) '
        },
        'color': 'black',
        'backgroundColor': '#FAC710'
    },
    {
        'if': {
            'filter_query': '{SUS Score (mean) } < 25.0',
            # 'column_id': 'SUS Score (mean) '
        },
        'color': 'black',
        'backgroundColor': '#F24726'
    }
]

dataframeNPSConditions = [
    {
        'if': {
            'column_id': 'SUS Score (mean) '
        },
        'fontWeight': 'bold'
    },
    {
        'if': {'row_index': 'odd'},
        'backgroundColor': 'rgb(248, 248, 248)'
    },
    {
        'if': {
            'filter_query': '{SUS Score (mean) } < 100.1',
            # 'column_id': 'SUS Score (mean) '
        },
        'color': 'black',
        'backgroundColor': '#8FD14F'
    },
    {
        'if': {
            'filter_query': '{SUS Score (mean) } < 78.8',
            # 'column_id': 'SUS Score (mean) '
        },
        'color': 'black',
        'backgroundColor': '#FEF445'
    },
    {
        'if': {
            'filter_query': '{SUS Score (mean) } < 62.5',
            # 'column_id': 'SUS Score (mean) '
        },
        'color': 'black',
        'backgroundColor': '#F24726'
    },
]

industryBenchmarkConditions = [
    {
        'if': {
            'column_id': 'SUS Score (mean) '
        },
        'fontWeight': 'bold'
    },
    {
        'if': {'row_index': 'odd'},
        'backgroundColor': 'rgb(248, 248, 248)'
    },
    {
        'if': {
            'filter_query': '{SUS Score (mean) } < 100.1',
            # 'column_id': 'SUS Score (mean) '
        },
        'color': 'black',
        'backgroundColor': '#8FD14F'
    },
    {
        'if': {
            'filter_query': '{SUS Score (mean) } < 80',
            # 'column_id': 'SUS Score (mean) '
        },
        'color': 'black',
        'backgroundColor': '#FEF445'
    },
    {
        'if': {
            'filter_query': '{SUS Score (mean) } < 68',
            # 'column_id': 'SUS Score (mean) '
        },
        'color': 'black',
        'backgroundColor': '#F24726'
    },
]

dataFrameNoScale = [
    {
        'if': {
            'column_id': 'SUS Score (mean) '
        },
        'fontWeight': 'bold'
    },
    {
        'if': {'row_index': 'odd'},
        'backgroundColor': 'rgb(248, 248, 248)'
    }
]

editableTableTypeFormatting = {
    'type': 'numeric',
    'format': Format(
        precision=0,
        scheme=Scheme.fixed,
    ),
}

dataFrameConditions = {'acceptabilityScale': dataframeAcceptabilityConditions,
                       'adjectiveScale': dataframeAdjectiveConditions,
                       'gradeScale': dataframeGradeConditions,
                       'quartileScale': dataframeQuartileConditions,
                       'promoterScale': dataframeNPSConditions,
                       'industryBenchmarkScale': industryBenchmarkConditions,
                       'none': dataFrameNoScale
                       }

percentileIntoText = html.P(children=[
    'SUS study scores do not follow a uniform or normal distribution. Bar charts and boxplots can therefore sometimes be deceiving for comparing the difference between SUS scores. The percentile curve, derived from over 5000 SUS study scores by ',
    html.A('Sauro et al. 2016',
           href='https://scholar.google.de/citations?view_op=view_citation&hl=de&user=rmiLIsYAAAAJ&citation_for_view=rmiLIsYAAAAJ:Mojj43d5GZwC',
           target="_blank"),
    ', visualizes SUS study scores on the cumulative percentile curve of the dataset.'
])

conclusivenessInfoText = html.P(children=[
    'The conclusiveness chart visualizes how conclusive each system/variables SUS study score is based on the number of participants. This graph is based on data from ',
    html.A('Tullis et al. 2006',
           href='https://scholar.google.de/citations?view_op=view_citation&hl=de&user=TXoUczoAAAAJ&citation_for_view=TXoUczoAAAAJ:PyEswDtIyv0C',
           target="_blank"),
    '.'
])


@dataclass
class ImageDownloadSettings:
    width: float
    height: float
    fontSize: float


defaultPlotSettings = ImageDownloadSettings(1200, 487, 15)
widePlotSettings = ImageDownloadSettings(1530, 510, 15)
narrowPlotSettings = ImageDownloadSettings(1025, 805, 15)

plotSettings = {'defaultPlot': defaultPlotSettings,
                'narrowPlot': narrowPlotSettings,
                'widePlot': widePlotSettings}


def imageDownloadLabelFactory(idSubstring):
    return html.Div([
        html.Label([
        "Download ",
        dcc.Dropdown(id='download-type-' + idSubstring,
                     options=ChartLayouts.download_layouts,
                     value='defaultPlot',
                     style={'font-weight': 'normal',
                            'margin-top': '10px',
                            'font-size': '.8rem'
                            }
                     ),
    ],
        style={'display': 'block',
               'font-weight': 'bold',
               'padding': '10px 10px 10px 10px'
               },
    ),
    html.Label([
        'Download Image Width:', html.Br(),
        dcc.Input(id='image-width-' + idSubstring + '',
                  type="number",
                  debounce=True,
                  style={'font-weight': 'normal',
                         'margin-top': '10px',
                         }
                  ), html.Br(),
        'Download Image Length:', html.Br(),
        dcc.Input(id='image-height-' + idSubstring,
                  type="number",
                  debounce=True,
                  style={'font-weight': 'normal',
                         'margin-top': '10px',
                         }
                  ), html.Br(),
        'Download Image Font Size":', html.Br(),
        dcc.Input(id='image-font-size-' + idSubstring,
                  type="number",
                  value=25,
                  debounce=True,
                  style={'font-weight': 'normal',
                         'margin-top': '10px',
                         }
                  ), html.Br(),
    ],
        id='custom-image-size-' + idSubstring,
        style={'display': 'None',
               'font-weight': 'bold',
               'padding': '10px 10px 10px 10px'
               },
    )])

