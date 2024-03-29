import pandas as pd
from dash import html, dcc
from dash import dash_table
import styles

per_question_context = html.Div([
    html.Dl([
        html.Dt(html.B("Question 1")),
        html.Dd("I think that I would like to use this system frequently."),
        html.Dt(html.B("Question 2")),
        html.Dd("I found the system unnecessarily complex."),
        html.Dt(html.B("Question 3")),
        html.Dd("I thought the system was easy to use."),
        html.Dt(html.B("Question 4")),
        html.Dd("I think that I would need the support of a technical person to be able to use this system."),
        html.Dt(html.B("Question 5")),
        html.Dd("I found the various functions in this system were well integrated."),
        html.Dt(html.B("Question 6")),
        html.Dd("I thought there was too much inconsistency in this system."),
        html.Dt(html.B("Question 7")),
        html.Dd("I would imagine that most people would learn to use this system very quickly."),
        html.Dt(html.B("Question 8")),
        html.Dd("I found the system very cumbersome to use."),
        html.Dt(html.B("Question 9")),
        html.Dd("I felt very confident using the system."),
        html.Dt(html.B("Question 10")),
        html.Dd("I needed to learn a lot of things before I could get going with this system."),
    ])],
    style={
        'float': 'left'},
    id='per-question-context',
)

editable_table_editor_panel = html.Div([
    html.Label(
        ['This table shows the data that is currently plotted. You can add, change or delete data points.'
         ],
        style={'display': 'block',
               'padding': '10px 10px 0px 10px'
               },
    ),
    html.Label([
    ],
        style={'display': 'block',
               'padding': '10px 10px 10px 10px'
               },
    ),
    html.Div([
        html.Button('Download as CSV', id='csv-data-button', className='button1'),
        dcc.Download(id='download-csv-data')],
        style=styles.download_div_style
    ),
],
    className='editor'
)

editable_table_editor_panel_single = html.Div([
    html.Label(
        ['This table shows the data that is currently plotted. You can change entries or add additional data points.'
         ],
        style={'display': 'block',
               'padding': '10px 10px 0px 10px'
               },
    ),
    html.Label([
    ],
        style={'display': 'block',
               'padding': '10px 10px 10px 10px'
               },
    ),
    html.Div([
        html.Button('Download as CSV', id='csv-data-button-single', className='button1'),
        dcc.Download(id='download-csv-data-single')],
        style=styles.download_div_style
    ),
],
    className='editor'
)


def getMainContent(app, VERSION):
    main_Content = html.Div([
        html.Div(
            [html.Div(
                [
                    html.H1('System Usability Scale Analysis Toolkit',
                            style={
                                'text-align': 'center',
                                'color': 'white'
                            }),
                    html.Div(
                        html.A(html.Button(['Back to Startpage'], className='button2'), href='/'),
                        # html.A(html.Img(src=app.get_asset_url('home_white.png'), width='30', height='30'), href='/'),
                        style={'text-align': 'center'}),
                ],
                style={
                    'background-color': '#445262',
                    'padding': '50px',
                    'margin-top': '10px',
                    'margin-bottom': '10px',
                    'border-radius': '5px',
                    'box-shadow': '0 1rem 1rem -.5rem rgba(0, 0, 0, .4)'
                }
            ),
                html.Div(
                    [
                        html.Div([
                            html.Img(src=app.get_asset_url('SUSToolFlow.png'), style={'width': '75%'}),
                            html.Div(
                                html.Div([
                                    html.Div([
                                        html.Button(html.H1('Start Multi Variable Analysis'), id='start-tool-button',
                                                    className='startToolButton'),
                                        html.Div([
                                            html.H1('Or', style={'textAlign': 'center'}),
                                            dcc.Upload(
                                                id='upload-data-multi',
                                                children=html.Div([
                                                    html.H1(['Drag and Drop or ',
                                                             html.A('click here to select CSV-file.')], style={'font-size':'1vw'})
                                                ], style={'margin': '1em'}),
                                                style=styles.mainPageDownloadPanelStyle,
                                                # Allow multiple files to be uploaded
                                                multiple=False
                                            ),
                                        ],
                                            className='centre',
                                            style={'width': '90%'}),
                                    ],
                                        className='inline-div'
                                    ),
                                    html.Div([
                                        html.Button(html.H1('Start Single Variable Analysis'),
                                                    id='start-tool-button-single',
                                                    className='startToolButton'),
                                        html.Div([
                                            html.H1('Or', style={'textAlign': 'center'}),
                                            dcc.Upload(
                                                id='upload-data-single',
                                                children=html.Div([
                                                    html.H1(['Drag and Drop or ',
                                                             html.A('click here to select CSV-file.')],style={'font-size':'1vw'})
                                                ],style={'margin': '1em'}),
                                                style=styles.mainPageDownloadPanelStyle,
                                                # Allow multiple files to be uploaded
                                                multiple=False
                                            )
                                        ],
                                            className='centre',
                                            style={'width': '90%'}
                                        ),
                                    ],
                                        className='inline-div'
                                    )
                                ],
                                    className='centre',
                                    style={'width': '75%'},
                                )
                            ),
                        ], style={'textAlign': 'center', 'margin-top': '20px'}),
                        # html.H2('CSV-File Upload', style={'textAlign': 'center'}),
                        html.Div([

                        ], style={'text-align': 'center',
                                  'width:': '75%'}),
                        html.P([
                            html.Details([html.Summary('What is the System Usability Scale (SUS)?',
                                                       style=styles.mainPageSummaryHeaderStyle, className="mainPage"),
                                          'The ',
                                          html.A('System Usability Scale by John Brooke',
                                                 href='https://scholar.google.de/citations?view_op=view_citation&hl=de&user=qjAGPUcAAAAJ&alert_preview_top_rm=2&citation_for_view=qjAGPUcAAAAJ:u5HHmVD_uO8C'),
                                          ' is a popular questionnaire to measure perceived usability. It consists of 10 likert-scale'
                                          ' questions, where participants responses range from \'Strongly disagree\' to '
                                          '\'Strongly agree\'. The results are then calculated into a single 0 - 100 score called the SUS score. Multiple SUS scores represent the SUS study score.'
                                          ' It is simple to apply, validated through years of its application, easy to understand for participants, ',html.A('available in multiple languages', href='https://jblattgerste.github.io/sus-pdf-generator'), ' and can be used for any system that requires human interaction.',
                                          ], open=False, className="mainPage")], style=styles.mainPageSummaryParagraph),
                        html.P([
                            html.Details([html.Summary(
                                'What is the "SUS Analysis Toolkit"?', style=styles.mainPageSummaryHeaderStyle,
                                className="mainPage"),
                                'The SUS Analysis Toolkit is an ',
                                html.A('open source', href='https://github.com/jblattgerste/sus-analysis-toolkit'),
                                ' web-based toolkit for the analysis of single- and multivariable SUS usability studies developed by the ',
                                html.A('Mixality Research Group', href='https://mixality.de/sus-analysis-toolkit/'),
                                '. The toolkit provides a compilation of useful insights and contextualisation approaches based on findings from the scientific literature for the System Usability Scale questionnaire. It allows researchers and practisionaires to easily calculate and plot comparative, iterative and single variable SUS usability study datasets. Furthermore, it provides utility to contextualize the meaning of calculated scores, compare them against scores gathered in meta-analyses, calculate SUS scores conclusiveness and analysing the contribution of specific questions of the 10-item questionnaire towards the SUS study scores. A particular focus lies on producing camera-ready scientific figures and calculations to be directly used in scientific publications and presentations. ',
                                html.Br(),
                            ], open=False, className="mainPage")], style=styles.mainPageSummaryParagraph),
                        html.P([html.Details([
                            html.Summary(
                                'How can i use the "SUS Analysis Toolkit"?', style=styles.mainPageSummaryHeaderStyle,
                                className="mainPage"
                            ),
                            'After conducting either an iterative, comparative or singular SUS study, questionnaire results have to be converted into a CSV file that consists of one column for each of the 10 questionnaire items in their original order'
                            ' and the last column as the identifier for the variable.',
                            ' Therefore, each row contains the results of one filled out questionnaire and the associated variable. For the single variable analysis, there can either be only one variable present or the column for the variable can be deleted.'
                            ' Values for the individual questionnaire items in the CSV file have to be between 1 (Strongly Disagree) and 5 (Strongly Agree). Other or empty values can not be processed. ',
                            '(Exemplary CSV templates are provided for the multi variable CSV file: ',
                            html.A('Download', href=app.get_asset_url('studyData.csv'), download='studyData.csv'),
                            ' and the single variable CSV file: ',
                            html.A('Download', href=app.get_asset_url('singleStudyData.csv'), download='studyData.csv'),
                            '. You can utilize them using a text editor or CSV editors like: ',
                            html.A('CsvTextEditor', href='https://github.com/WildGums/CsvTextEditor'),
                            ', ',
                            html.A('CSV-Editor', href='https://github.com/ritsrivastava01/CSV-Editor'),
                            ' or ',
                            html.A('Table Tool', href='https://github.com/jakob/TableTool'),
                            ' on macOS). ',
                            'After the successfull upload, SUS scores, per-item contribution, the studies conclusiveness and contextualization onto meta-analysis are calcualted and plotted. The interactive plots can be viewed and customized with a multitude of available options. After the analysis and customization, individual charts, tables or the whole analysis can be downloaded and used.',
                            ' Alternatively, since version 1.0.1, SUS questionnaire values can also be added in the tool directly and downloaded as a CSV for reuse.'
                        ], open=False, className="mainPage")], style=styles.mainPageSummaryParagraph),

                        html.P([
                            html.Details([html.Summary(
                                'Licensing and Acknowledgement', style=styles.mainPageSummaryHeaderStyle,
                                className="mainPage"
                            ),
                                ''
                                ' The open source SUS Analysis Toolkit is licensed under the MIT license and can be used, extended and redistributed for commercial and non-commercial applications without attribtution. The ownership of generated calculations, interpretations, tables, and plots fully remain with the user of the tool. '
                                'If you use this toolkit in the scientific context, we would appreciate an acknowledgement in form of a ',
                                html.A('citation to our tool', href=app.get_asset_url('BibTex.txt'),
                                       download='BibTex.txt'),
                                ' and recommend citing the primary sources for the insights utilized.',
                                html.Br(),
                            ], open=False, className="mainPage")], style=styles.mainPageSummaryParagraph),
                        html.P([

                        ]),
                        html.P([

                        ]),

                    ], id='landing-page', style={'display': 'block',
                                                 'margin-left': 'auto',
                                                 'margin-right': 'auto'}),

                html.Div(id='graph-content', style=styles.graph_div_style, children=[

                    html.Div([
                        dcc.Download(id='download-all-charts-data'),

                        dcc.Tabs([
                            dcc.Tab(id='editable-table-tab',
                                    value='editable-table-tab',
                                    label='Raw SUS Data',
                                    children=[
                                        html.Div([
                                            html.Div([
                                                html.Div(id='table-error-icon', className='tooltip', children=[
                                                    html.Img(src=app.get_asset_url('exclamation-mark.png'),
                                                             style={'height': '2em'}), html.Span(
                                                        'You\'ve either entered a value that is not between 1 and 5, or there are empty cells. The plots will not update until this is fixed.',
                                                        className='tooltiptext')],
                                                         style=styles.tableErrorIconDefaultStyle),
                                                dash_table.DataTable(
                                                    id='editable-table',
                                                    editable=True,
                                                    row_deletable=True,
                                                    style_table={'overflowX': 'auto'}
                                                ),
                                                html.Button('Add SUS Data Entry', className='button1', id='add-row-button',style={'margin-bottom':'10px'},
                                                            n_clicks=0),
                                            ],
                                                style=styles.main_content_style),
                                            editable_table_editor_panel],
                                            style=styles.graph_editor_container),
                                    ],
                                    selected_style=styles.tab_selected_style,
                                    ),
                            dcc.Tab(id='main-plot-tab',
                                    label='SUS Score',
                                    selected_style=styles.tab_selected_style),
                            dcc.Tab(id='percentile-plot-tab',
                                    label='SUS Score on Percentile-Curve',
                                    selected_style=styles.tab_selected_style
                                    ),
                            dcc.Tab(id='per-item-tab',
                                    label='Per Item Chart',
                                    selected_style=styles.tab_selected_style
                                    ),
                            dcc.Tab(id='conclusiveness-tab',
                                    label='Conclusiveness Chart',
                                    selected_style=styles.tab_selected_style
                                    ),
                        ],
                            value='editable-table-tab')
                    ],
                        id='multi-study-content',
                        style={'display': 'none'}),
                    html.Div([dcc.Tabs([
                        dcc.Tab(id='single-study-editable-table',
                                label='Raw SUS Data',
                                children=[html.Div([
                                    html.Div([
                                        html.Div(id='table-error-icon-single', className='tooltip', children=[
                                            html.Img(src=app.get_asset_url('exclamation-mark.png'),
                                                     style={'height': '2em'}), html.Span(
                                                'You\'ve either entered a value that is not between 1 and 5, or there are empty cells. The plots will not update until this is fixed.',
                                                className='tooltiptext')],
                                                 style=styles.tableErrorIconDefaultStyle),
                                        dash_table.DataTable(
                                            id='editable-table-single',
                                            editable=True,
                                            row_deletable=True,
                                            style_table={'overflowX': 'auto'}
                                        ),
                                        html.Button('Add SUS Data Entry', className='button1', id='add-row-button-single',
                                                    n_clicks=0),
                                    ],
                                        style=styles.main_content_style),
                                    editable_table_editor_panel_single],
                                    style=styles.graph_editor_container),
                                ],
                                selected_style=styles.tab_selected_style),
                        dcc.Tab(id='single-study-tab',
                                label='SUS Dashboard Plot',
                                selected_style=styles.tab_selected_style),

                    ])],
                        id='single-study-content',
                        style={'display': 'none',
                               }
                    )
                ]),

                # This stores the session data
                dcc.Store(id='sessionPlotData-multi'),
                dcc.Store(id='sessionPlotData-single'),
            ],
            style={
                'margin-right': 'auto',
                # 'position': 'absolute',
                # 'left': '50%',
                # 'margin-right': '-50%',
                'margin-left': 'auto',
                'width': '80%'
                # 'transform': 'translate(-50%)',
            }
        ),
        html.Div([VERSION], className='bottomright')]
    )
    return main_Content


def CreateDataTableLayout(df=pd.DataFrame()):
    return [dash_table.DataTable(
        id='editable-table',
        data=df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df.columns],
        editable=True
    )]
