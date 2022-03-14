import base64
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import ChartLayouts
import Charts
import pandas as pd
import Helper
from dash.exceptions import PreventUpdate

import SingleStudyCharts
from SUSDataset import SUSDataset
import Layouts
import styles
import zipfile
import tempfile

app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
app.layout = Layouts.getMainContent(app)

debugMode = True


@app.callback(
    Output('graph-content', component_property='children'),
    Output('landing-page', 'style'),
    Output("sessionPlotData-multi", 'children'),
    Output("sessionPlotData-single", "data"),
    Input('upload-data-multi', 'contents'),
    Input('upload-data-single', 'contents')
)
def init_main_page(contents_multi, contents_single):
    ctx = dash.callback_context
    upload_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if upload_id == 'upload-data-multi':
        try:
            if contents_multi is None:
                raise PreventUpdate
            csvData = Helper.decodeContentToCSV(contents_multi)
            csvData = Helper.checkUploadFile(csvData, False)
            SUSData = SUSDataset(Helper.parseDataFrameToSUSDataset(csvData))
            systemList = SUSData.getAllStudNames()
            graph = [
                html.Div([
                    dcc.Download(id='download-all-charts-data'),

                    dcc.Tabs([
                        dcc.Tab(label='System Usability Scale',
                                children=ChartLayouts.CreateMainPlotLayout(SUSData, systemList),
                                selected_style={'border-top': '3px solid #445262'}),
                        dcc.Tab(label='SUS Score on Percentile-Curve',
                                children=ChartLayouts.CreatePercentilePlotLayout(SUSData, systemList),
                                selected_style={'border-top': '3px solid #445262'}
                                ),
                        dcc.Tab(label='Per Item Chart',
                                children=ChartLayouts.CreatePerQuestionChartLayout(SUSData, systemList),
                                selected_style={'border-top': '3px solid #445262'}
                                ),
                        dcc.Tab(label='Conclusiveness Chart',
                                children=ChartLayouts.CreateCocnlusivenessChartLayout(SUSData),
                                selected_style={'border-top': '3px solid #445262'}
                                ),
                    ])
                ])
            ]
            return graph, {'display': 'none'}, csvData.to_json(date_format='iso', orient='split'), dash.no_update
        except Helper.WrongUploadFileException as e:
            print(e)
            errorMessage = [html.Div(children=[
                'There was an error processing this file: ' + str(e),
                html.P(['Please refer to this ',
                        html.A('template', href=app.get_asset_url('singleStudyData.csv'), download='singleStudyData.csv'),
                        ' for help. ', ]),

                html.P([html.A('Refresh', href='/'), ' the page to try again.'])
            ])]
            return errorMessage, {'display': 'none'}, dash.no_update, dash.no_update
        except Exception as e:
            print(e)
            errorMessage = [html.Div(children=[
                'There was an error processing this file. ',
                html.P(['Please refer to this ',
                        html.A('template', href=app.get_asset_url('singleStudyData.csv'),
                               download='singleStudyData.csv'),
                        ' for help. ', ]),

                html.P([html.A('Refresh', href='/'), ' the page to try again.'])
            ])]
            return errorMessage, {'display': 'none'}, dash.no_update, dash.no_update
    else:
        if contents_single is None:
            raise PreventUpdate
        try:
            csvData = Helper.decodeContentToCSV(contents_single)
            csvData = Helper.checkUploadFile(csvData, True)
            SUSData = SUSDataset(Helper.parseDataFrameToSUSDataset(csvData))
            graph = [ChartLayouts.CreateSingleStudyChartLayout(SUSData)]
            return graph, {'display': 'none'}, dash.no_update, csvData.to_json(date_format='iso', orient='split')
        except Helper.WrongUploadFileException as e:
            print(e)
            errorMessage = [html.Div(children=[
                'There was an error processing this file: ' + str(e),
                html.P(['Please refer to this ',
                        html.A('template', href=app.get_asset_url('singleStudyData.csv'), download='singleStudyData.csv'),
                        ' for help. ', ]),

                html.P([html.A('Refresh', href='/'), ' the page to try again.'])
            ])]
            return errorMessage, {'display': 'none'}, dash.no_update, dash.no_update
        except Exception as e:
            print(e)
            errorMessage = [html.Div(children=[
                'There was an error processing this file. ',
                html.P(['Please refer to this ',
                        html.A('template', href=app.get_asset_url('singleStudyData.csv'),
                               download='singleStudyData.csv'),
                        ' for help. ', ]),

                html.P([html.A('Refresh', href='/'), ' the page to try again.'])
            ])]
            return errorMessage, {'display': 'none'}, dash.no_update, dash.no_update


@app.callback(
    Output('download-single-study-chart', 'children'),
    Output('single-study-chart', 'figure'),
    Input('sessionPlotData-single', 'data'),
    Input('preset-single-study', 'value'),
)
def update_SingleStudyMainplot(data_single, presetValue):
    df = pd.read_json(data_single, orient='split')
    SUSData = SUSDataset(Helper.parseDataFrameToSUSDataset(df))
    fig = SingleStudyCharts.singleStudyPresetDict[presetValue](SUSData.SUSStuds[0])
    return Helper.downloadChartContentSingleStudy(fig), fig


@app.callback(
    Output('mainplot', 'figure'),
    # Output('mainplot', 'style'),
    Output('download-mainplot', 'children'),
    Output('datapoints-label', 'style'),
    Output('mean_sdValue-label', 'style'),
    Output('scaletype-info', 'children'),
    Output('plotstyle-info', 'children'),
    Output('mainplot-table-div', 'children'),
    Input('systems-mainplot', 'value'),
    Input('sessionPlotData-multi', 'children'),
    Input('datapoints-mainplot', 'value'),
    Input('scale-mainplot', 'value'),
    Input('orientation-mainplot', 'value'),
    Input('plotstyle-mainplot', 'value'),
    Input('mean_sd-mainplot', 'value'),
    Input('axis-title-mainplot', 'value'),
    Input('download-type-mainplot', 'value'),
    Input('sort-by-mainplot', 'value')
)
def update_Mainplot(systemsToPlot, data, datapointsValues, scaleValue, orientationValue, plotStyle, mean_sdValue,
                    axis_title, download_format, sort_value):
    df = pd.read_json(data, orient='split')
    SUSData = SUSDataset(Helper.parseDataFrameToSUSDataset(df))
    SUSData.sortBy(sort_value)

    filteredSUSData = Helper.filterSUSStuds(SUSData, systemsToPlot)
    mainplot_table = ChartLayouts.createMainplotTable(filteredSUSData, scaleValue)
    fig = Charts.CreateMainplot(filteredSUSData, datapointsValues, scaleValue, orientationValue, plotStyle,
                                mean_sdValue, axis_title)
    if plotStyle == 'per-question-chart':
        datapointsLabelStyle = styles.disabledStyle
        mean_sdValueLabelStyle = styles.disabledStyle
    else:
        datapointsLabelStyle = styles.defaultEditorLabel
        mean_sdValueLabelStyle = styles.defaultEditorLabel

    return fig, Helper.downloadChartContent(fig, download_format), datapointsLabelStyle, mean_sdValueLabelStyle, \
           Helper.scaleInfoTexts[scaleValue], Helper.plotStyleInfoTexts[plotStyle], mainplot_table


@app.callback(
    Output('per-question-chart', 'figure'),
    Output('download-per-question-chart', 'children'),
    Output('orientation-label', 'style'),
    Output('colorize-by-meaning-label', 'style'),
    Output('systems-label', 'style'),
    Output('sort-by-label', 'style'),
    Output('per-question-context', 'style'),
    Output('systems-label-radio', 'style'),
    Input('systems-per-question-chart', 'value'),
    Input('questions-per-question-chart', 'value'),
    Input('sessionPlotData-multi', 'children'),
    Input('orientation-per-question-chart', 'value'),
    Input('plotstyle-per-question-chart', 'value'),
    Input('download-type-perquestion', 'value'),
    Input('sort-by-perquestion', 'value'),
    Input('colorize-by-meaning', 'value'),
    Input('systems-per-question-chart-radio', 'value'),
)
def update_PerQuestionChart(systemsToPlot, questionsTicked, data, orientationValue, plotStyle, download_format,
                            sort_value, colorizeByMeaning, systemToPlotRadio):
    df = pd.read_json(data, orient='split')
    SUSData = SUSDataset(Helper.parseDataFrameToSUSDataset(df))
    SUSData.sortBy(sort_value)

    colorizeByMeaningLabelStyle = {'display': 'none'}
    orientationLabelStyle = {'display': 'none'}
    systemsLabelStyle = {'display': 'none'}
    sortByLabelStyle = {'display': 'none'}
    perQuestionContextStyle = {'float': 'left'}
    systemsLabelRadioStyle = {'display': 'none'}

    if plotStyle == 'per-question-chart':
        fig = Charts.CreatePerQuestionChart(SUSData, questionsTicked, systemsToPlot, orientationValue)
        orientationLabelStyle = {'display': 'block',
                                 'font-weight': 'bold',
                                 'padding': '10px 10px 10px 10px'}
        systemsLabelStyle = {'display': 'block',
                             'font-weight': 'bold',
                             'padding': '10px 10px 10px 10px'}
        sortByLabelStyle = {'display': 'block',
                            'font-weight': 'bold',
                            'padding': '10px 10px 10px 10px'}
    elif plotStyle == 'radar':
        fig = Charts.CreateRadarChart(SUSData, questionsTicked, systemsToPlot)
        systemsLabelStyle = {'display': 'block',
                             'font-weight': 'bold',
                             'padding': '10px 10px 10px 10px'}
        sortByLabelStyle = {'display': 'block',
                            'font-weight': 'bold',
                            'padding': '10px 10px 10px 10px'}
    elif plotStyle == 'likert':
        systemsLabelRadioStyle = {'display': 'block',
                                  'font-weight': 'bold',
                                  'padding': '10px 10px 10px 10px',
                                  }
        perQuestionContextStyle = {'display': 'none'}
        colorizeByMeaningLabelStyle = {'display': 'block',
                                       'font-weight': 'bold',
                                       'padding': '10px 10px 10px 10px'}
        fig = Charts.CreateLikertChart(SUSData.getIndividualStudyData(systemToPlotRadio), questionsTicked,
                                       colorizeByMeaning)

    downloadChart = Helper.downloadChartContent(fig, download_format)
    return fig, downloadChart, orientationLabelStyle, colorizeByMeaningLabelStyle, systemsLabelStyle, sortByLabelStyle, perQuestionContextStyle, systemsLabelRadioStyle


@app.callback(
    Output('percentilePlot', 'figure'),
    Output('download-percentilePlot', 'children'),
    Input('systems-percentilePlot', 'value'),
    Input('sessionPlotData-multi', 'children'),
    Input('download-type-percentile', 'value'),
    Input('sort-by-percentile', 'value')
)
def update_PercentilePlot(systems, data, download_format, sort_value):
    df = pd.read_json(data, orient='split')
    SUSData = SUSDataset(Helper.parseDataFrameToSUSDataset(df))
    SUSData.sortBy(sort_value)
    fig = Charts.CreatePercentilePlot(SUSData, systems)

    downloadPercentilePlot = Helper.downloadChartContent(fig, download_format)
    return fig, downloadPercentilePlot


@app.callback(
    Output('conclusivenessPlot', 'figure'),
    Output('download-conclusiveness', 'children'),
    Input('systems-percentilePlot', 'value'),
    Input('sessionPlotData-multi', 'children'),
    Input('download-type-conclusiveness', 'value')
)
def update_Conclusiveness(systems, data, download_format):
    df = pd.read_json(data, orient='split')
    SUSData = SUSDataset(Helper.parseDataFrameToSUSDataset(df))
    fig = Charts.CreateConclusivenessChart(SUSData)

    downloadConclusivenessChart = Helper.downloadChartContent(fig, download_format)
    return fig, downloadConclusivenessChart


@app.callback(
    Output('main-plot-dataframe', 'style_data_conditional'),
    Input('scale-mainplot', 'value')
)
def update_mainplot_table(scaleValue):
    return Helper.dataFrameConditions[scaleValue]


@app.callback(
    Output("download-all-charts-data", "data"),
    Input("download-all-per-question-button", "n_clicks"),
    Input("download-all-mainplot-button", "n_clicks"),
    Input("download-all-percentile-button", "n_clicks"),
    Input("download-all-conclusiveness-button", "n_clicks"),
    State('mainplot', 'figure'),
    State('per-question-chart', 'figure'),
    State('percentilePlot', 'figure'),
    State('conclusivenessPlot', 'figure'),
    State('sessionPlotData-multi', 'children'),
    prevent_initial_call=True,
)
def download_all_charts(n_clicks, n_clicks_2, n_clicks_3, n_clicks_4, mainplot, per_question, percentile,
                        conclusiveness, data):
    # Create Data Frames for the .csv files
    df = pd.read_json(data, orient='split')
    systemList = set(df['System'])
    SUSData = SUSDataset(Helper.parseDataFrameToSUSDataset(df))

    # Mainplot Dataframe
    df_mainplot = ChartLayouts.createMainplotDataframe(SUSData, systemList)

    # Per Question Dataframe
    df_per_question = ChartLayouts.createPerItemDataFrame(SUSData)

    # Percentile Dataframe
    df_percentile = ChartLayouts.createPercentilePlotDataFrame(SUSData, systemList)

    # Conclusiveness Dataframe
    df_conclusiveness = ChartLayouts.CreateConclusivenessPlotDataFrame(SUSData, systemList)

    # Create png-images from figures

    # Mainplot
    mainplot_fig = go.Figure(mainplot)
    mainplot_fig.update_layout(
        paper_bgcolor='rgba(255,255,255,255)',
    )
    img_mainplot = mainplot_fig.to_image(format="png", width=mainplot_fig.layout.width,
                                         height=mainplot_fig.layout.height)
    # Per Question
    per_question_fig = go.Figure(per_question)
    per_question_fig.update_layout(
        paper_bgcolor='rgba(255,255,255,255)',
    )
    img_per_question = per_question_fig.to_image(format="png", width=per_question_fig.layout.width,
                                                 height=per_question_fig.layout.height)
    # Percentile
    percentile_fig = go.Figure(percentile)
    percentile_fig.update_layout(
        paper_bgcolor='rgba(255,255,255,255)',
    )
    img_percentile = percentile_fig.to_image(format="png", width=percentile_fig.layout.width,
                                             height=percentile_fig.layout.height)
    # Conclusiveness
    conclusiveness_fig = go.Figure(conclusiveness)
    conclusiveness_fig.update_layout(
        paper_bgcolor='rgba(255,255,255,255)',
    )
    img_conclusiveness = conclusiveness_fig.to_image(format="png", width=conclusiveness_fig.layout.width,
                                                     height=conclusiveness_fig.layout.height)

    # Write images in zip file
    zip_tf = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
    zf = zipfile.ZipFile(zip_tf, mode='w', compression=zipfile.ZIP_DEFLATED)

    zf.writestr("main_plot.png", img_mainplot)
    zf.writestr("per_item_plot.png", img_per_question)
    zf.writestr("percentile_plot.png", img_percentile)
    zf.writestr("conclusiveness_plot.png", img_conclusiveness)

    # Write .csv to zip files
    zf.writestr("mainplot.csv", df_mainplot.to_csv(encoding='utf-8-sig', index=False))
    zf.writestr("per-question.csv", df_per_question.to_csv(encoding='utf-8', index=False))
    zf.writestr("percentile.csv", df_percentile.to_csv(encoding='utf-8', index=False))
    zf.writestr("conclusiveness.csv", df_conclusiveness.to_csv(encoding='utf-8', index=False))

    # Close zip file
    zf.close()
    zip_tf.flush()
    zip_tf.seek(0)

    return dcc.send_file(zip_tf.name, filename="my_plots.zip")


@app.callback(
    Output('download-csv-mainplot', 'data'),
    Input('csv-mainplot-button', 'n_clicks'),
    State('sessionPlotData-multi', 'children'),
    prevent_initial_call=True
)
def download_csv_mainplot(n_clicks, data):
    df = pd.read_json(data, orient='split')
    systemList = set(df['System'])
    SUSData = SUSDataset(Helper.parseDataFrameToSUSDataset(df))
    df = ChartLayouts.createMainplotDataframe(SUSData, systemList)
    return dcc.send_data_frame(df.to_csv, "mainplot.csv", index=False)


@app.callback(
    Output('download-csv-per-question', 'data'),
    Input('csv-per-question-button', 'n_clicks'),
    State('sessionPlotData-multi', 'children'),
    prevent_initial_call=True
)
def download_csv_per_question(n_clicks, data):
    df = pd.read_json(data, orient='split')
    SUSData = SUSDataset(Helper.parseDataFrameToSUSDataset(df))
    df = ChartLayouts.createPerItemDataFrame(SUSData)
    return dcc.send_data_frame(df.to_csv, "per_question.csv", index=False)


@app.callback(
    Output('download-csv-percentile', 'data'),
    Input('csv-percentile-button', 'n_clicks'),
    State('sessionPlotData-multi', 'children'),
    prevent_initial_call=True
)
def download_csv_percentile(n_clicks, data):
    df = pd.read_json(data, orient='split')
    SUSData = SUSDataset(Helper.parseDataFrameToSUSDataset(df))
    systemList = set(df['System'])
    df = ChartLayouts.createPercentilePlotDataFrame(SUSData, systemList)
    return dcc.send_data_frame(df.to_csv, "percentile.csv", index=False)


@app.callback(
    Output('download-csv-conclusiveness', 'data'),
    Input('csv-conclusiveness-button', 'n_clicks'),
    State('sessionPlotData-multi', 'children'),
    prevent_initial_call=True
)
def download_csv_conclusiveness(n_clicks, data):
    df = pd.read_json(data, orient='split')
    SUSData = SUSDataset(Helper.parseDataFrameToSUSDataset(df))
    systemList = set(df['System'])
    df = ChartLayouts.CreateConclusivenessPlotDataFrame(SUSData, systemList)
    return dcc.send_data_frame(df.to_csv, "conclusiveness.csv", index=False)


if __name__ == '__main__':
    if debugMode:
        app.run_server(port=80,host='0.0.0.0', debug=True)
    else:
        app.run_server(port=80,host='0.0.0.0')
