import statistics
import pandas as pd
import Charts as Charts
from dash import html, dcc
from dash import dash_table

import SingleStudyCharts
import styles
import Helper
import Layouts

download_layouts = [{'label': 'Default plot format' + ' (Width: ' + str(Helper.defaultPlotSettings.width) + ' Height: ' + str(Helper.defaultPlotSettings.height) + ' Font Size: ' + str(Helper.defaultPlotSettings.fontSize) + ')', 'value': 'defaultPlot'},
                    {'label': 'Narrow plot format' + ' (Width: ' + str(Helper.narrowPlotSettings.width) + ' Height: ' + str(Helper.narrowPlotSettings.height) + ' Font Size: ' + str(Helper.narrowPlotSettings.fontSize) + ')', 'value': 'narrowPlot'},
                    {'label': 'Wide plot format' + ' (Width: ' + str(Helper.widePlotSettings.width) + ' Height: ' + str(Helper.widePlotSettings.height) + ' Font Size: ' + str(Helper.widePlotSettings.fontSize) + ')', 'value': 'widePlot'},
                    {'label': 'Custom format', 'value': 'customSize'}
                    ]

sort_values = [{'label': 'Alphabetical order', 'value': 'alphabetically'},
               {'label': 'Mean', 'value': 'mean'},
               {'label': 'Median', 'value': 'median'}
               ]


def CreatePercentilePlotLayout(SUSData, systemList):
    options = []
    value = []

    for system in systemList:
        options.append({'label': system, 'value': system})
        value.append(system)

    fig = Charts.CreatePercentilePlot(SUSData, value)

    tableContent = createPercentilePlotTable(SUSData)

    graphContent = [
        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(
                        id='percentilePlot',
                        figure=fig,
                        style=styles.graph_style
                    ),
                ],
                    style=styles.graph_div_style),
                html.Div([tableContent], id='percentile-plot-table-div', style=styles.tableStyle),
            ],
                style=styles.main_content_style
            ),
            html.Div([
                html.Label([
                    Helper.percentileIntoText,
                ],
                    style={'display': 'block',
                           'padding': '10px 10px 0px 10px'
                           },
                ),
                html.Label([
                    "Show in plot: ",
                    dcc.Checklist(id='systems-percentilePlot',
                                  options=options,
                                  value=value,
                                  labelStyle={'display': 'block'},
                                  style={'font-weight': 'normal',
                                         }
                                  ),
                ],
                    style={'display': 'block',
                           'font-weight': 'bold',
                           'padding': '10px 10px 10px 10px',
                           },
                ),
                html.Label([
                    "Sort by: ",
                    dcc.Dropdown(id='sort-by-percentile',
                                 options=sort_values,
                                 value='alphabetically',
                                 style={'font-weight': 'normal',
                                        'margin-top': '10px',
                                        }
                                 ),
                ],
                    style={'display': 'block',
                           'font-weight': 'bold',
                           'padding': '10px 10px 10px 10px'
                           },
                ),
                Helper.imageDownloadLabelFactory('percentile'),
                dcc.Download(id='download-image-percentile'),
                dcc.Download(id='download-csv-percentile'),
                html.Div([

                    html.Button('Download this chart', id='image-percentile-button', className='button1'),
                ],
                    style=styles.download_div_style
                ),
                html.Div([html.Button('Download this data table', id='csv-percentile-button', className='button1'),
                          dcc.Download(id='download-csv-percentile')],
                         style=styles.download_div_style),
                html.Div([
                    html.Button('Download complete analysis', id='download-all-percentile-button',
                                className='button1')],
                    style=styles.download_div_style
                ),

            ],
                className='editor'
            )
        ],
            style=styles.graph_editor_container
        )
    ]
    return graphContent


def CreateMainPlotLayout(SUSData, systemList):
    options = []
    value = []

    for system in systemList:
        options.append({'label': system, 'value': system})
        value.append(system)
    fig = Charts.CreateMainplot(SUSData, 'outliers', 'adjectiveScale', 'vertical', 'mainplot', 'mean', "",'default-colors')
    #
    tableContent = createMainplotTable(SUSData, 'adjectiveScale')
    #
    # conclusivenessFigure = Charts.CreateConclusivenessChart(SUSData)

    graphContent = [
        html.Div([
            html.Div([
                html.Div(
                    [
                        dcc.Graph(id='mainplot',
                                  figure=fig,
                                  style=styles.graph_style
                                  )
                    ],
                    style=styles.graph_div_style
                ),
                html.Div([tableContent], id='mainplot-table-div', style=styles.tableStyle),

            ], style=styles.main_content_style
            ),
            # html.Img(src='/assets/adjective_scale.JPG'),
            html.Div([
                html.Label([
                    html.P(children=[
                        'Each System Usability Scale (SUS) study score represents an average perceived usability score between 0 - 100 calculated based on the formula from ',
                        html.A('Brooke et al. 1996',
                               href='https://scholar.google.de/citations?view_op=view_citation&hl=de&user=qjAGPUcAAAAJ&citation_for_view=qjAGPUcAAAAJ:u5HHmVD_uO8C',
                               target="_blank"),
                        '. SUS study scores can be compared against each other and on contextualization scales.'
                    ]),
                ],
                    style={'display': 'block',
                           'padding': '10px 10px 0px 10px'
                           },
                ),
                html.Label([
                    html.Details([
                    html.Summary("Plot type: "),
                    html.P(id="plotstyle-info",
                           children=[Helper.plotStyleInfoTexts['mainplot']],
                           style=styles.editorInfoTextStyle)], open=True),
                    dcc.Dropdown(id='plotstyle-mainplot',
                                 options=[{'label': 'Boxplot', 'value': 'mainplot'},
                                          {'label': 'Notched Boxplot', 'value': 'notched'},
                                          {'label': 'Bar chart', 'value': 'per-question-chart'}],
                                 value='mainplot',
                                 style={'font-weight': 'normal',
                                        }
                                 ),
                ],
                    style={'display': 'block',
                           'font-weight': 'bold',
                           'padding': '10px 10px 10px 10px',
                           },
                ),
                html.Label([
                    html.Details([html.Summary("Contextualization scale: "),
                    html.P(id="scaletype-info",
                           children=[Helper.scaleInfoTexts['adjectiveScale']],
                           style=styles.editorInfoTextStyle)], open=True),
                    dcc.Dropdown(id='scale-mainplot',
                                 options=[{'label': 'Adjective Scale', 'value': 'adjectiveScale'},
                                          {'label': 'Grade Scale', 'value': 'gradeScale'},
                                          {'label': 'Quartile Scale', 'value': 'quartileScale'},
                                          {'label': 'Acceptability Scale', 'value': 'acceptabilityScale'},
                                          {'label': 'Net Promoter Scale', 'value': 'promoterScale'},
                                          {'label': 'Industry Benchmark Scale', 'value': 'industryBenchmarkScale'},
                                          {'label': 'No Scale', 'value': 'none'}
                                          # {'label': 'Background Adjective Scale', 'value': 'BGAdjectiveScale'}
                                          ],
                                 value='adjectiveScale',
                                 style={'font-weight': 'normal',
                                        'margin-top': '10px',
                                        }
                                 ),
                ],
                    style={'display': 'block',
                           'font-weight': 'bold',
                           'padding': '10px 10px 10px 10px'
                           },
                ),

                html.Label([
                    'Colorize plot according to contextualization scale:',
                    dcc.Dropdown(id='colorize-by-scale',
                                options={'scale-colors': 'Colorize by scale',
                                         'default-colors': 'Default Colors'},
                                value='default-colors',
                                 style={'font-weight': 'normal',
                                        'margin-top': '10px',
                                        }
                                 ),
                ],
                    style={'display': 'block',
                           'font-weight': 'bold',
                           'padding': '10px 10px 10px 10px'
                           },
                ),

                html.Label([
                    "Show in plot: ",
                    dcc.Checklist(id='systems-mainplot',
                                  options=options,
                                  value=value,
                                  labelStyle={'display': 'block'},
                                  style={'font-weight': 'normal',
                                         'margin-top': '10px'}
                                  ),
                ],
                    style={'display': 'block',
                           'font-weight': 'bold',
                           'padding': '10px 10px 10px 10px',
                           },
                ),
                html.Label([
                    "Sort by: ",
                    dcc.Dropdown(id='sort-by-mainplot',
                                 options=sort_values,
                                 value='alphabetically',
                                 style={'font-weight': 'normal',
                                        'margin-top': '10px',
                                        }
                                 ),
                ],
                    style={'display': 'block',
                           'font-weight': 'bold',
                           'padding': '10px 10px 10px 10px'
                           },
                ),
                html.Label([
                    "Individual data points: ",
                    dcc.Dropdown(id='datapoints-mainplot',
                                 options=[{'label': 'Show outliers', 'value': 'outliers'},
                                          {'label': 'Show all datapoints', 'value': 'all'},
                                          {'label': 'Show no datapoints', 'value': 'False'}],
                                 value='outliers',
                                 style={'font-weight': 'normal',
                                        'margin-top': '10px',
                                        }
                                 ),
                ],
                    id='datapoints-label',
                    style={'display': 'block',
                           'font-weight': 'bold',
                           'padding': '10px 10px 10px 10px'
                           },
                ),
                html.Label([
                    "Mean and Standard Deviation: ",
                    dcc.Dropdown(id='mean_sd-mainplot',
                                 options=[{'label': 'Show Mean', 'value': 'mean'},
                                          {'label': 'Show Mean and SD', 'value': 'sd'},
                                          {'label': 'None', 'value': 'neither'}],
                                 value='mean',
                                 style={'font-weight': 'normal',
                                        'margin-top': '10px',
                                        }
                                 ),
                ],
                    id='mean_sdValue-label',
                    style={'display': 'block',
                           'font-weight': 'bold',
                           'padding': '10px 10px 10px 10px'
                           },
                ),
                html.Label([
                    "Plot orientation: ",
                    dcc.Dropdown(id='orientation-mainplot',
                                 options=[{'label': 'Vertical', 'value': 'vertical'},
                                          {'label': 'Horizontal', 'value': 'horizontal'}],
                                 value='vertical',
                                 style={'font-weight': 'normal',
                                        'margin-top': '10px',
                                        }
                                 ),
                ],
                    style={'display': 'block',
                           'font-weight': 'bold',
                           'padding': '10px 10px 10px 10px'
                           },
                ),
                html.Label([
                    "X-Axis label: ",
                    dcc.Input(id='axis-title-mainplot',
                              type="text",
                              debounce=True,
                              value="",
                              style={'font-weight': 'normal',
                                     'margin-top': '10px',
                                     }
                              ),
                ],
                    id='orientation-label',
                    style={'display': 'block',
                           'font-weight': 'bold',
                           'padding': '10px 10px 10px 10px'
                           },
                ),
                Helper.imageDownloadLabelFactory('mainplot'),
                dcc.Download(id='download-image-mainplot'),
                dcc.Download(id='download-csv-mainplot'),
                html.Div([

                    html.Button('Download this chart', id='image-mainplot-button', className='button1'),
                ],
                    style=styles.download_div_style
                ),
                html.Div([
                    html.Button('Download this data table', id='csv-mainplot-button', className='button1'),],
                    style=styles.download_div_style
                ),
                html.Div([
                    html.Button('Download complete analysis', id='download-all-mainplot-button', className='button1')],
                    style=styles.download_div_style
                ),
            ],
                className='editor'
            )
        ],
            style=styles.graph_editor_container),

    ]
    return graphContent


def CreatePerQuestionChartLayout(SUSData, systemList):
    options = []
    value = []

    for system in systemList:
        options.append({'label': system, 'value': system})
        value.append(system)

    questionOptions = [{'label': 'Question 1', 'value': 'Question 1'},
                       {'label': 'Question 2', 'value': 'Question 2'},
                       {'label': 'Question 3', 'value': 'Question 3'},
                       {'label': 'Question 4', 'value': 'Question 4'},
                       {'label': 'Question 5', 'value': 'Question 5'},
                       {'label': 'Question 6', 'value': 'Question 6'},
                       {'label': 'Question 7', 'value': 'Question 7'},
                       {'label': 'Question 8', 'value': 'Question 8'},
                       {'label': 'Question 9', 'value': 'Question 9'},
                       {'label': 'Question 10', 'value': 'Question 10'}]

    questionsTicked = ['Question 1', 'Question 2', 'Question 3', 'Question 4', 'Question 5', 'Question 6',
                       'Question 7', 'Question 8', 'Question 9',
                       'Question 10']

    fig = Charts.CreatePerQuestionChart(SUSData, questionsTicked, value, 'vertical')

    tableContent = createPerItemTable(SUSData, questionsTicked)

    graphContent = [
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        Layouts.per_question_context,
                    ],
                        style={'float': 'left',
                               'width': '40%'},
                    ),
                    dcc.Graph(id='per-question-chart',
                              figure=fig,
                              style=styles.graph_style_per_item),

                ],
                    style=styles.graph_div_style
                ),
                html.Div([tableContent], id='per-item-table-div', style=styles.tableStyle),

            ], style=styles.main_content_style
            ),
            html.Div([
                html.Label([
                    html.P(
                        'The per item chart visualizes the impact of participants answers to specific SUS questions. The per item values are normalized values between 0-10 representing their contribution to the SUS study scores and not the Likert scale values in the questionnaire where even numbered questions (2, 4, 6, 8, and 10) are formulated negatively.'),
                ],
                    style={'display': 'block',
                           'padding': '10px 10px 0px 10px'
                           },
                ),
                html.Label([
                    "Show in plot: ",
                    dcc.RadioItems(id='systems-per-question-chart-radio',
                                   options=options,
                                   value=value[0],
                                   labelStyle={'display': 'block'},
                                   style={'font-weight': 'normal',
                                          'margin-top': '10px'
                                          }
                                   ),
                ],
                    id='systems-label-radio',
                    style={'display': 'none',
                           'font-weight': 'bold',
                           'padding': '10px 10px 10px 10px',
                           },
                ),
                html.Label([
                    "Show in plot: ",
                    dcc.Checklist(id='systems-per-question-chart',
                                  options=options,
                                  value=value,
                                  labelStyle={'display': 'block'},
                                  style={'font-weight': 'normal',
                                         'margin-top': '10px'
                                         }
                                  ),
                ],
                    id='systems-label',
                    style={'display': 'block',
                           'font-weight': 'bold',
                           'padding': '10px 10px 10px 10px',
                           },
                ),
                html.Label([
                    "Sort by: ",
                    dcc.Dropdown(id='sort-by-perquestion',
                                 options=sort_values,
                                 value='alphabetically',
                                 style={'font-weight': 'normal',
                                        'margin-top': '10px',
                                        }
                                 ),
                ],
                    id='sort-by-label',
                    style={'display': 'block',
                           'font-weight': 'bold',
                           'padding': '10px 10px 10px 10px'
                           },
                ),
                html.Label([
                    "Show questionnaire items: ",
                    dcc.Checklist(id='questions-per-question-chart',
                                  options=questionOptions,
                                  value=questionsTicked,
                                  labelStyle={'display': 'block'},
                                  style={'font-weight': 'normal',
                                         'margin-top': '10px',
                                         }
                                  ),
                ],
                    style={'display': 'block',
                           'font-weight': 'bold',
                           'padding': '10px 10px 10px 10px'
                           },
                ),
                # For now depcrecated, might reuse later
                # html.Label([
                #     "Colorization: ",
                #     dcc.Dropdown(id='colorize-by-meaning',
                #                  options=[{'label': 'Regular colors', 'value': 'regular'},
                #                           {'label': 'Colorize by meaning', 'value': 'byMeaning'}],
                #                  value='byMeaning',
                #                  style={'font-weight': 'normal',
                #                         'margin-top': '10px',
                #                         }
                #                  ),
                # ],
                #     id='colorize-by-meaning-label',
                #     style={'display': 'none',
                #            'font-weight': 'bold',
                #            'padding': '10px 10px 10px 10px'
                #            },
                # ),

                html.Label([
                    "Plot type: ",
                    dcc.Dropdown(id='plotstyle-per-question-chart',
                                 options=[{'label': 'Bar chart', 'value': 'per-question-chart'},
                                          {'label': 'Radar chart', 'value': 'radar'},
                                          {'label': 'Stacked bar chart', 'value': 'likert'},
                                          {'label': 'Boxplot', 'value': 'boxplot'}],
                                 value='per-question-chart',
                                 style={'font-weight': 'normal',
                                        'margin-top': '10px',
                                        }
                                 ),
                ],
                    style={'display': 'block',
                           'font-weight': 'bold',
                           'padding': '10px 10px 10px 10px'
                           },
                ),
                html.Label([
                    "Plot orientation: ",
                    dcc.Dropdown(id='orientation-per-question-chart',
                                 options=[{'label': 'Vertical', 'value': 'vertical'},
                                          {'label': 'Horizontal', 'value': 'horizontal'}],
                                 value='vertical',
                                 style={'font-weight': 'normal',
                                        'margin-top': '10px',
                                        }
                                 ),
                ],
                    id='orientation-label',
                    style={'display': 'block',
                           'font-weight': 'bold',
                           'padding': '10px 10px 10px 10px'
                           },
                ),
                Helper.imageDownloadLabelFactory('perquestion'),
                dcc.Download(id='download-image-perquestion'),
                dcc.Download(id='download-csv-perquestion'),
                html.Div([

                    html.Button('Download this chart', id='image-perquestion-button', className='button1'),
                ],
                    style=styles.download_div_style
                ),
                dcc.Download(id='download-csv-per-question'),
                html.Div([
                    html.Button('Download this data table', id='csv-per-question-button', className='button1'),
                ],
                    style=styles.download_div_style
                ),
                html.Div([
                    html.Button('Download complete analysis', id='download-all-per-question-button',
                                className='button1'), ],
                    style=styles.download_div_style
                ),
            ],
                className='editor'
            ),
        ],
            style=styles.graph_editor_container,
        )
    ]
    return graphContent


def CreateCocnlusivenessChartLayout(SUSData):

    value = []
    options = []

    for study in SUSData.SUSStuds:
        options.append({'label': study.name, 'value': study.name})
        value.append(study.name)

    fig = Charts.CreateConclusivenessChart(SUSData)
    tableContent = CreateConclusivenessPlotTable(SUSData, SUSData.getAllStudNames())
    graphContent = [
        html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(id='conclusivenessPlot',
                              figure=fig,
                              style=styles.graph_style)
                ],
                    style=styles.graph_div_style),
                html.Div([tableContent], id='conclusiveness-plot-table-div', style=styles.tableStyle),
            ],
                style=styles.main_content_style
            ),
            # html.Img(src='/assets/adjective_scale.JPG'),
            html.Div([
                html.Label([
                    Helper.conclusivenessInfoText,
                ],
                    style={'display': 'block',
                           'padding': '10px 10px 0px 10px'
                           },
                ),
                html.Label([
                    "Show in plot: ",
                    dcc.Checklist(id='systems-conclusivenessPlot',
                                  options=options,
                                  value=value,
                                  labelStyle={'display': 'block'},
                                  style={'font-weight': 'normal',
                                         }
                                  ),
                ],
                    style={'display': 'block',
                           'font-weight': 'bold',
                           'padding': '10px 10px 10px 10px',
                           },
                ),
                Helper.imageDownloadLabelFactory('conclusiveness'),
                dcc.Download(id='download-image-conclusiveness'),
                dcc.Download(id='download-csv-conclusiveness'),
                html.Div([

                    html.Button('Download this chart', id='image-conclusiveness-button', className='button1'),
                ],
                    style=styles.download_div_style
                ),

                html.Div([
                    html.Button('Download this data table', id='csv-conclusiveness-button', className='button1'),
                    dcc.Download(id='download-csv-conclusiveness')],
                    style=styles.download_div_style
                ),
                html.Div([
                    html.Button('Download complete analysis', id='download-all-conclusiveness-button',
                                className='button1')],
                    style=styles.download_div_style
                ),

            ],
                className='editor'
            ),
        ],
            style=styles.graph_editor_container),
    ]
    return graphContent


def CreateSingleStudyChartLayout(SUSData):
    singleStudy = SUSData.SUSStuds[0]
    fig = SingleStudyCharts.singleStudyPresetDict['preset_1'](singleStudy)

    questionTable = []

    for i, questionScore in enumerate(singleStudy.avgScorePerQuestion):
        questionTable.append(
            html.Tr([html.Td('Question ' + str(i + 1) + ':'), html.Td(round(singleStudy.avgScorePerQuestion[i], 2))]))

    graphContent = html.Div([
        html.Div([
            html.Div([
                dcc.Graph(id='single-study-chart',
                          figure=fig,
                          style=styles.single_study_graph_style)
            ])
        ],
            style=styles.single_study_main_content_style
        ),

        html.Div([
            html.Label([
                "Plot type: ",
                dcc.Dropdown(id='preset-single-study',
                             clearable=False,
                             options=[{'label': 'Preset 1', 'value': 'preset_1'},
                                      {'label': 'Preset 2', 'value': 'preset_2'},
                                      {'label': 'Preset 3', 'value': 'preset_3'},
                                      {'label': 'Preset 4', 'value': 'preset_4'}],
                             value='preset_1',
                             style={'font-weight': 'normal',
                                    'margin-top': '10px',
                                    }
                             ),
            ],
                style={'display': 'block',
                       'font-weight': 'bold',
                       'padding': '10px 10px 10px 10px'
                       },
            ),
            html.Label([
                "Score and Interpretation: ",
                html.Table([
                    html.Tr([html.Td('SUS Study Score: '), html.Td(round(singleStudy.Score, 2))]),
                    html.Tr([html.Td('Median: '), html.Td(singleStudy.median)]),
                    html.Tr([html.Td('Standard Dev. '), html.Td(round(singleStudy.standardDevOverall, 2))]),
                    html.Tr([html.Td('Adjective: '), html.Td(Helper.getAdjectiveValue(singleStudy.Score))]),
                    html.Tr([html.Td('Grade: '), html.Td(Helper.getGradeScaleValue(singleStudy.Score))]),
                    html.Tr([html.Td('Acceptability: '), html.Td(Helper.getAcceptabilityValue(singleStudy.Score))]),
                    html.Tr([html.Td('Quartile: '), html.Td(Helper.getQuartileScaleValue(singleStudy.Score))]),

                ],
                    style={'cellspacing': '0',
                           'cellpadding': '0',
                           'font-weight': 'normal'}
                ),
            ],
                style={'display': 'block',
                       'font-weight': 'bold',
                       'padding': '10px 10px 10px 10px'
                       },
            ),
            html.Label([
                "Per Question Scores: ",
                html.P(
                    children=[
                        'The per item values are normalized values between 0-10 representing their contribution to the SUS study score and not the Likert scale values in the questionnaire where even numbered questions are formulated negatively.'],
                    style=styles.editorInfoTextStyle),
                html.Table(
                    questionTable
                    ,
                    style={'cellspacing': '0',
                           'cellpadding': '0',
                           'font-weight': 'normal'}
                ),
            ],
                style={'display': 'block',
                       'font-weight': 'bold',
                       'padding': '10px 10px 10px 10px'
                       },
            ),
            html.Label([
                "Conclusiveness ",
                html.Table([
                    html.Tr([html.Td('Conclusiveness: '), html.Td(Helper.getConclusiveness(singleStudy))]),
                ],
                    style={'cellspacing': '0',
                           'cellpadding': '0',
                           'font-weight': 'normal'}
                ),
            ],
                style={'display': 'block',
                       'font-weight': 'bold',
                       'padding': '10px 10px 10px 10px'
                       },
            ),
            html.Label([
                "Primary sources ",
                html.Details([html.Summary(['Adjective Scale'], style={'font-size': 'medium',
                                                                         'font-weight': 'normal'}),
                              html.P(Helper.scaleInfoTexts['adjectiveScale'],
                                     style=styles.editorInfoTextStyle)],
                             ),
                html.Details([html.Summary(['Grade Scale'], style={'font-size': 'medium',
                                                                         'font-weight': 'normal'}),
                              html.P(Helper.scaleInfoTexts['gradeScale'],
                                     style=styles.editorInfoTextStyle)],
                             ),
                html.Details([html.Summary(['Acceptability Scale'], style={'font-size': 'medium',
                                                                     'font-weight': 'normal'}),
                              html.P(Helper.scaleInfoTexts['acceptabilityScale'],
                                     style=styles.editorInfoTextStyle)],
                             ),
                html.Details([html.Summary(['Percentile-Curve'], style={'font-size': 'medium',
                                                                           'font-weight': 'normal'}),
                              html.P(Helper.percentileIntoText,
                                     style=styles.editorInfoTextStyle)],
                             ),
                html.Details([html.Summary(['Conslusiveness Chart'], style={'font-size': 'medium',
                                                                        'font-weight': 'normal'}),
                              html.P(Helper.conclusivenessInfoText,
                                     style=styles.editorInfoTextStyle)],
                             ),
            ],
                style={'display': 'block',
                       'font-weight': 'bold',
                       'padding': '10px 10px 10px 10px'
                       },
            ),
            html.Div(id="download-single-study-chart",
                     children=[],
                     style=styles.download_div_style, ),
        ],
            className='editor'
        ),
    ],
        style=styles.graph_editor_container)
    return graphContent


def createMainplotDataframe(SUSData):
    mins = []
    firstQuartiles = []
    medians = []
    thirdQuartiles = []
    maxs = []
    OverallScores = []
    standardDeviation = []
    adjectiveScale = []
    grade = []
    quartile = []
    acceptability = []
    systemList = []
    nps = []
    industryBenchmark = []

    for study in SUSData.SUSStuds:
        adjectiveScale.append(Helper.getAdjectiveValue(study.Score))
        grade.append(Helper.getGradeScaleValue(study.Score))
        quartile.append(Helper.getQuartileScaleValue(study.Score))
        acceptability.append(Helper.getAcceptabilityValue(study.Score))
        nps.append(Helper.getNPSValue(study.Score))
        industryBenchmark.append(Helper.getIndustryBenchmarkValue(study.Score))
        OverallScores.append(round(study.Score, 2))
        susScores = study.getAllSUSScores()
        mins.append(min(susScores))
        systemList.append(study.name)
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
        'Variable ': systemList,
        'SUS Score (mean) ': OverallScores,
        'SD ': standardDeviation,
        'Min ': mins,
        'Max ': maxs,
        '1. Quartile ': firstQuartiles,
        'Median ': medians,
        '3. Quartile ': thirdQuartiles,
        'Adjective Scale ': adjectiveScale,
        'Grade Scale ': grade,
        'Quartile Scale ': quartile,
        'Acceptability Scale ': acceptability,
        'NPS Scale': nps,
        'Industry Benchmark': industryBenchmark
    }
    # tableHeader = [" "].extend(systems)
    df = pd.DataFrame(data)
    df = df
    return df


def createMainplotTable(SUSData, scaleType):
    df = createMainplotDataframe(SUSData)
    dataframeConditions = Helper.dataFrameConditions[scaleType]
    table = dash_table.DataTable(
                id='main-plot-dataframe',
                columns=[{"name": i, "id": i} for i in df.columns],
                style_table={
                    'overflowX': 'auto'},
                data=df.to_dict('records'),
                style_cell={'textAlign': 'right',
                            },
                style_data_conditional=dataframeConditions,
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                }
            )
    return table


def createPerItemDataFrame(SUSData, questionsTicked=None):
    if questionsTicked is None:
        questionsTicked = []
    questions = ['Question 1', 'Question 2', 'Question 3', 'Question 4', 'Question 5', 'Question 6',
                 'Question 7', 'Question 8', 'Question 9',
                 'Question 10']
    standardDev = []

    removeIdxs = []
    for idx, question in enumerate(questions):
        if question not in questionsTicked:
            removeIdxs.append(idx)

    filteredQuestions = [i for j, i in enumerate(questions) if j not in removeIdxs]

    data = {'Items': filteredQuestions}

    for study in SUSData.SUSStuds:
        avgScorePerQuestion, scorePerQuestionValues = study.calcSUSScorePerQuestion(removeIdxs)
        standardDeviations = []
        for question in scorePerQuestionValues.values():
            try:
                standardDeviations.append(statistics.pstdev(question))
            except statistics.StatisticsError:
                standardDeviations.append(0)

        data[study.name + ' Contribution (SD)'] = [str(round(score, 2)) + ' (' + str(round(stdDev, 2)) + ')'
                                                   for score, stdDev in
                                                   zip(avgScorePerQuestion, standardDeviations)]
    df = pd.DataFrame(data)

    df.set_index('Items', inplace=True)
    df = df.transpose()
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'Variable'}, inplace=True)
    return df


def createPerItemTable(SUSData, questionsTicked=None):
    if questionsTicked is None:
        questionsTicked = []
    df = createPerItemDataFrame(SUSData, questionsTicked)
    table = dash_table.DataTable(
                columns=[{"name": str(i), "id": str(i)} for i in df.columns],
                data=df.to_dict('records'),
                style_table={'overflowX': 'auto'
                             },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    }
                ],
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                }
            )
    return table


def createPercentilePlotDataFrame(SUSData):
    data = {}
    studyScores = []
    percentileValues = []
    systemList = SUSData.getAllStudNames()
    for study in SUSData.SUSStuds:
        studyScores.append(round(study.Score, 2))
        percentileValues.append(round(Charts.parametrizePercentile(study.Score), 2))
    data['Variable'] = systemList
    data['SUS Score'] = studyScores
    data['Percentile'] = percentileValues
    df = pd.DataFrame(data)
    return df


def createPercentilePlotTable(SUSData):
    df = createPercentilePlotDataFrame(SUSData)
    table = dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                style_cell={'textAlign': 'right',
                            'width': '17%'
                            },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    }
                ],
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                }
            )
    return table


def CreateConclusivenessPlotDataFrame(SUSData, systems):
    sampleSizes = []
    conclusiveness = []

    yValues = dict({0: '0 %',
                    6: '35 %',
                    7: '55 %',
                    8: '75 %',
                    9: '78 %',
                    10: '80 %',
                    11: '98 %',
                    12: '100 %',
                    13: '100 %',
                    14: '100 %'
                    })

    for study in SUSData.SUSStuds:
        sampleSize = len(study.Results)
        sampleSizes.append(sampleSize)
        if sampleSize < 6:
            conclusiveness.append('0 %')
        elif sampleSize < 15:
            conclusiveness.append(yValues.get(sampleSize))
        else:
            conclusiveness.append('100 %')

    data = {'Variable': list(systems),
            'Sample Size': sampleSizes,
            'Conclusiveness': conclusiveness
            }

    # tableHeader = [" "].extend(systems)
    df = pd.DataFrame(data)
    return df


def CreateConclusivenessPlotTable(SUSData, systems):
    df = CreateConclusivenessPlotDataFrame(SUSData, systems)
    table = dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                style_cell={'textAlign': 'right',
                            'width': '17%'
                            },
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    }
                ],
                style_header={
                    'backgroundColor': 'rgb(230, 230, 230)',
                    'fontWeight': 'bold'
                }
            )
    return table
