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
app.title = 'SUS Analysis Toolkit'
app._favicon = ("assets/favicon.ico")
app.config.suppress_callback_exceptions = True
app.layout = Layouts.getMainContent(app)

debugMode = True


@app.callback(
    Output('multi-study-content', 'style'),
    Output('single-study-content', 'style'),
    Output('landing-page', 'style'),
    Input('upload-data-multi', 'contents'),
    Input('start-tool-button', 'n_clicks'),
    Input('upload-data-single', 'contents'),
    Input('start-tool-button-single', 'n_clicks'),
)
def init_main_page(contents_multi, contents_single, nclicks_multi, nclicks_single):
    ctx = dash.callback_context
    upload_id = ctx.triggered[0]['prop_id'].split('.')[0]
    # When the multi study upload is triggered
    if upload_id == 'upload-data-multi' or upload_id == 'start-tool-button':
        return {'display':'block'}, dash.no_update, {'display':'none'}
    # Single study upload trigger
    elif upload_id == 'upload-data-single' or upload_id == 'start-tool-button-single':
        return dash.no_update, {'display': 'block'}, {'display': 'none'}
    # On changes to the editable table
    else:
        if contents_single is None and contents_multi is None:
            raise PreventUpdate


@app.callback(
    Output('main-plot-tab','children'),
    Output('percentile-plot-tab', 'children'),
    Output('per-item-tab', 'children'),
    Output('conclusiveness-tab', 'children'),
    Output("sessionPlotData-multi", 'data'),
    Output('editable-table', 'data'),
    Output('editable-table', 'columns'),
    Output('table-error-icon', 'style'),
    Output('editable-table', 'style_data_conditional'),
    Output('multi-study-content', 'children'),
    Input('upload-data-multi', 'contents'),
    Input('editable-table', 'data'),
    Input('editable-table', 'columns'),
    Input('add-row-button', 'n_clicks'),
    Input('start-tool-button', 'n_clicks'),
)
def update_multi_study(contents_multi, table_data, table_columns, add_row_button_nclicks, start_tool_button_nclicks):

    ctx = dash.callback_context
    input_trigger = ctx.triggered[0]['prop_id'].split('.')[0]

    if input_trigger == 'upload-data-multi':
        try:
            if contents_multi is None:
                raise PreventUpdate
            # decode the upload data and convert it to pandas data frame
            csvData = Helper.decodeContentToCSV(contents_multi)
            # check if the upload file is correctly formated, has no null values etc.
            Helper.checkUploadFile(csvData, False)
            # Parse pandas dataframe to SUSDataset
            SUSData = SUSDataset(Helper.parseDataFrameToSUSDataset(csvData))
            systemList = SUSData.getAllStudNames()
            # Apply the formatting rules to the editable data table
            columns = [{"name": i, "id": i} for i in csvData.columns]
            for column in columns[0:10]:
                column.update(Helper.editableTableTypeFormatting)
            style_data_conditional = (Helper.conditionalFormattingEditableDataTable(csvData.columns.values.tolist()))
            return ChartLayouts.CreateMainPlotLayout(SUSData, systemList), ChartLayouts.CreatePercentilePlotLayout(SUSData, systemList), ChartLayouts.CreatePerQuestionChartLayout(SUSData, systemList), ChartLayouts.CreateCocnlusivenessChartLayout(SUSData),  csvData.to_json(
                date_format='iso', orient='split'), csvData.to_dict(
                'records'), columns, dash.no_update, style_data_conditional, dash.no_update
        # If something is wrong with the upload file, print the reason on the page.
        except Helper.WrongUploadFileException as e:
            print(e)
            errorMessage = [html.Div(children=[
                'There was an error processing this file: ' + str(e),
                html.P(['Please refer to this ',
                        html.A('template', href=app.get_asset_url('singleStudyData.csv'),
                               download='singleStudyData.csv'),
                        ' for help. ', ]),

                html.P([html.A('Refresh', href='/'), ' the page to try again.'])
            ])]
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update,errorMessage
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
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update ,errorMessage
    elif 'start-tool-button' == input_trigger:
        exampleData = Helper.createExampleDataFrame()
        # Create SUSDataset from example dataframe
        SUSData = SUSDataset(Helper.parseDataFrameToSUSDataset(exampleData))
        systemList = SUSData.getAllStudNames()
        # Apply the formatting rules to the editable data table
        columns = [{"name": i, "id": i} for i in exampleData.columns]
        for column in columns[0:10]:
            column.update(Helper.editableTableTypeFormatting)
        return ChartLayouts.CreateMainPlotLayout(SUSData, systemList), ChartLayouts.CreatePercentilePlotLayout(SUSData, systemList), ChartLayouts.CreatePerQuestionChartLayout(SUSData, systemList), ChartLayouts.CreateCocnlusivenessChartLayout(SUSData), exampleData.to_json(date_format='iso',
                                                                                                orient='split'), exampleData.to_dict(
            'records'), columns, dash.no_update, (Helper.conditionalFormattingEditableDataTable(exampleData.columns.values.tolist())), dash.no_update
    elif input_trigger == 'editable-table':
        # Checks whether all entries in the table are viable. If not the error overlay of the data table is enabled.
        if Helper.tableDataIsInvalid(table_data):
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, table_data,  dash.no_update, styles.tableErrorIconEnabledStyle, dash.no_update, dash.no_update
        # Collecting the table heads for each of the columns of the table.
        columns = []
        for item in table_columns:
            columns.append(item.get("name"))
        # Creating the dataframe from the table entries
        table_df = pd.DataFrame(data=table_data, columns=columns)
        #  parsing it to SUS Dataset, so all the graphs can be updated
        SUSData = SUSDataset(Helper.parseDataFrameToSUSDataset(table_df))
        systemList = SUSData.getAllStudNames()
        return ChartLayouts.CreateMainPlotLayout(SUSData, systemList), ChartLayouts.CreatePercentilePlotLayout(SUSData, systemList), ChartLayouts.CreatePerQuestionChartLayout(SUSData, systemList), ChartLayouts.CreateCocnlusivenessChartLayout(SUSData), table_df.to_json(date_format='iso', orient='split'), dash.no_update,dash.no_update, styles.tableErrorIconDefaultStyle, dash.no_update,dash.no_update
    # On Press of the add-row button
    elif input_trigger == 'add-row-button':
        if add_row_button_nclicks > 0:
            table_data.append({c['id']: '' for c in table_columns})
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update,  dash.no_update, table_data, dash.no_update, dash.no_update, dash.no_update, dash.no_update
    else:
        if contents_multi is None:
            raise PreventUpdate


@app.callback(
    Output('single-study-tab','children'),
    Output("sessionPlotData-single", 'data'),
    Output('editable-table-single', 'data'),
    Output('editable-table-single', 'columns'),
    Output('table-error-icon-single', 'style'),
    Output('editable-table-single', 'style_data_conditional'),
    Output('single-study-content', 'children'),
    Input('upload-data-single', 'contents'),
    Input('editable-table-single', 'data'),
    Input('editable-table-single', 'columns'),
    Input('add-row-button-single', 'n_clicks'),
    Input('start-tool-button-single', 'n_clicks'),
)
def update_single_study(contents_single, table_data, table_columns, add_row_button_nclicks, start_tool_button_nclicks):
    ctx = dash.callback_context
    input_trigger = ctx.triggered[0]['prop_id'].split('.')[0]

    if input_trigger == 'upload-data-single':
        try:
            csvData = Helper.decodeContentToCSV(contents_single)
            csvData = Helper.checkUploadFile(csvData, True)
            SUSData = SUSDataset(Helper.parseDataFrameToSUSDataset(csvData))
            # The columns for the editable table. The system column is dropped, since the editable table isn't supposed to have it.
            columns = [{"name": i, "id": i} for i in csvData.drop('System', axis=1).columns]
            for column in columns:
                column.update(Helper.editableTableTypeFormatting)
            style_data_conditional = (Helper.conditionalFormattingEditableDataTable(csvData.columns.values.tolist()))
            graph = [ChartLayouts.CreateSingleStudyChartLayout(SUSData)]
            return graph, csvData.to_json(date_format='iso',
                                                                    orient='split'), csvData.drop('System', axis=1).to_dict(
                'records'), columns, dash.no_update, style_data_conditional, dash.no_update
        except Helper.WrongUploadFileException as e:
            print(e)
            errorMessage = [html.Div(children=[
                'There was an error processing this file: ' + str(e),
                html.P(['Please refer to this ',
                        html.A('template', href=app.get_asset_url('singleStudyData.csv'), download='singleStudyData.csv'),
                        ' for help. ', ]),

                html.P([html.A('Refresh', href='/'), ' the page to try again.'])
            ])]
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, errorMessage
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
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, errorMessage
    elif input_trigger == 'editable-table-single':
        # Checks whether all entries in the table are viable. If not the error overlay of the data table is enabled.
        if Helper.tableDataIsInvalid(table_data):
            return dash.no_update, dash.no_update, table_data,  dash.no_update, styles.tableErrorIconEnabledStyle, dash.no_update, dash.no_update
        # Collecting the table heads for each of the columns of the table.
        columns = []
        for item in table_columns:
            columns.append(item.get("name"))
        # Creating the dataframe from the table entries
        table_df = pd.DataFrame(data=table_data, columns=columns)
        table_df = Helper.checkUploadFile(table_df, True)
        #  parsing it to SUS Dataset, so all the graphs can be updated
        SUSData = SUSDataset(Helper.parseDataFrameToSUSDataset(table_df))
        graph = [ChartLayouts.CreateSingleStudyChartLayout(SUSData)]
        return graph, table_df.to_json(date_format='iso',
                               orient='split'), dash.no_update, dash.no_update, styles.tableErrorIconDefaultStyle,  dash.no_update, dash.no_update
    elif input_trigger == 'start-tool-button-single':
        exampleData = Helper.createExampleDataFrame(singleStudy=True)
        # Create SUSDataset from example dataframe
        SUSData = SUSDataset(Helper.parseDataFrameToSUSDataset(exampleData))
        # The columns for the editable table. The system column is dropped, since the editable table isn't supposed to have it.
        columns = [{"name": i, "id": i} for i in exampleData.drop('System', axis=1).columns]
        graph = [ChartLayouts.CreateSingleStudyChartLayout(SUSData)]
        # Apply the formatting rules to the editable data table
        style_data_conditional = (Helper.conditionalFormattingEditableDataTable(exampleData.columns.values.tolist()))
        for column in columns[0:10]:
            column.update(Helper.editableTableTypeFormatting)
        return graph, exampleData.to_json(date_format='iso',
                               orient='split'), exampleData.drop('System', axis=1).to_dict(
            'records'), columns, dash.no_update, style_data_conditional, dash.no_update
    elif input_trigger == 'add-row-button-single':
        if add_row_button_nclicks > 0:
            table_data.append({c['id']: '' for c in table_columns})
            return dash.no_update, dash.no_update,  table_data, dash.no_update,  dash.no_update,  dash.no_update,  dash.no_update
    else:
        if contents_single is None:
            raise PreventUpdate



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
    Input('sessionPlotData-multi', 'data'),
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
    df = pd.read_json(data, orient='split', dtype='int16')
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
    Output('per-item-table-div', 'children'),
    Input('systems-per-question-chart', 'value'),
    Input('questions-per-question-chart', 'value'),
    Input('sessionPlotData-multi', 'data'),
    Input('orientation-per-question-chart', 'value'),
    Input('plotstyle-per-question-chart', 'value'),
    Input('download-type-perquestion', 'value'),
    Input('sort-by-perquestion', 'value'),
    Input('colorize-by-meaning', 'value'),
    Input('systems-per-question-chart-radio', 'value'),
)
def update_PerQuestionChart(systemsToPlot, questionsTicked, data, orientationValue, plotStyle, download_format,
                            sort_value, colorizeByMeaning, systemToPlotRadio):
    df = pd.read_json(data, orient='split', dtype='int16')
    SUSData = SUSDataset(Helper.parseDataFrameToSUSDataset(df))
    SUSData.sortBy(sort_value)

    colorizeByMeaningLabelStyle = {'display': 'none'}
    orientationLabelStyle = {'display': 'none'}
    systemsLabelStyle = {'display': 'none'}
    sortByLabelStyle = {'display': 'none'}
    perQuestionContextStyle = {'float': 'left'}
    systemsLabelRadioStyle = {'display': 'none'}

    perItemTable = ChartLayouts.createPerItemTable(Helper.filterSUSStuds(SUSData, systemsToPlot), questionsTicked)

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
    return fig, downloadChart, orientationLabelStyle, colorizeByMeaningLabelStyle, systemsLabelStyle, sortByLabelStyle, perQuestionContextStyle, systemsLabelRadioStyle, perItemTable


@app.callback(
    Output('percentilePlot', 'figure'),
    Output('download-percentilePlot', 'children'),
    Output('percentile-plot-table-div', 'children'),
    Input('systems-percentilePlot', 'value'),
    Input('sessionPlotData-multi', 'data'),
    Input('download-type-percentile', 'value'),
    Input('sort-by-percentile', 'value')
)
def update_PercentilePlot(systems, data, download_format, sort_value):
    df = pd.read_json(data, orient='split', dtype='int16')
    SUSData = SUSDataset(Helper.parseDataFrameToSUSDataset(df))
    SUSData.sortBy(sort_value)
    table = ChartLayouts.createPercentilePlotTable(Helper.filterSUSStuds(SUSData, systems))
    fig = Charts.CreatePercentilePlot(SUSData, systems)

    downloadPercentilePlot = Helper.downloadChartContent(fig, download_format)
    return fig, downloadPercentilePlot, table


@app.callback(
    Output('conclusivenessPlot', 'figure'),
    Output('download-conclusiveness', 'children'),
    Output('conclusiveness-plot-table-div', 'children'),
    Input('systems-conclusivenessPlot', 'value'),
    Input('sessionPlotData-multi', 'data'),
    Input('download-type-conclusiveness', 'value')
)
def update_Conclusiveness(systems, data, download_format):
    df = pd.read_json(data, orient='split', dtype='int16')
    SUSData = SUSDataset(Helper.parseDataFrameToSUSDataset(df))
    filteredSUSData = Helper.filterSUSStuds(SUSData, systems)
    fig = Charts.CreateConclusivenessChart(filteredSUSData)
    table = ChartLayouts.CreateConclusivenessPlotTable(filteredSUSData, systems)

    downloadConclusivenessChart = Helper.downloadChartContent(fig, download_format)
    return fig, downloadConclusivenessChart, table


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
    State('sessionPlotData-multi', 'data'),
    prevent_initial_call=True
)
def download_all_charts(n_clicks, n_clicks_2, n_clicks_3, n_clicks_4, mainplot, per_question, percentile,
                        conclusiveness, data):

    # This is needed because prevent_initial_call=True doesnt't work, if the input component is generated by another callback
    if n_clicks is None and n_clicks_2 is None and n_clicks_3 is None and n_clicks_4 is None:
        return dash.no_update

    # Create Data Frames for the .csv files
    df = pd.read_json(data, orient='split')
    systemList = set(df['System'])
    SUSData = SUSDataset(Helper.parseDataFrameToSUSDataset(df))

    # Mainplot Dataframe
    df_mainplot = ChartLayouts.createMainplotDataframe(SUSData)

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
    State('sessionPlotData-multi', 'data'),
    prevent_initial_call=True
)
def download_csv_mainplot(n_clicks, data):
    df = pd.read_json(data, orient='split')
    systemList = set(df['System'])
    SUSData = SUSDataset(Helper.parseDataFrameToSUSDataset(df))
    df = ChartLayouts.createMainplotDataframe(SUSData)
    return dcc.send_data_frame(df.to_csv, "mainplot.csv", index=False)


@app.callback(
    Output('download-csv-per-question', 'data'),
    Input('csv-per-question-button', 'n_clicks'),
    State('sessionPlotData-multi', 'data'),
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
    State('sessionPlotData-multi', 'data'),
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
    State('sessionPlotData-multi', 'data'),
    prevent_initial_call=True
)
def download_csv_conclusiveness(n_clicks, data):
    df = pd.read_json(data, orient='split')
    SUSData = SUSDataset(Helper.parseDataFrameToSUSDataset(df))
    systemList = set(df['System'])
    df = ChartLayouts.CreateConclusivenessPlotDataFrame(SUSData, systemList)
    return dcc.send_data_frame(df.to_csv, "conclusiveness.csv", index=False)


@app.callback(
    Output('download-csv-data', 'data'),
    Input('csv-data-button', 'n_clicks'),
    State('editable-table', 'data'),
    State('editable-table', 'columns'),
    prevent_initial_call=True
)
def download_csv_data_multi(nclicks, data, table_columns):
    columns = []
    for item in table_columns:
        columns.append(item.get("name"))
    # Creating the dataframe from the table entries
    table_df = pd.DataFrame(data=data, columns=columns)
    return dcc.send_data_frame(table_df.to_csv, "studyData.csv", index=False, sep=';')


@app.callback(
    Output('download-csv-data-single', 'data'),
    Input('csv-data-button-single', 'n_clicks'),
    State('editable-table-single', 'data'),
    State('editable-table-single', 'columns'),
    prevent_initial_call=True
)
def download_csv_data_single(nclicks, data, table_columns):
    columns = []
    for item in table_columns:
        columns.append(item.get("name"))
    # Creating the dataframe from the table entries
    table_df = pd.DataFrame(data=data, columns=columns)
    return dcc.send_data_frame(table_df.to_csv, "studyData.csv", index=False,sep=';')


if __name__ == '__main__':
    if debugMode:
        app.run_server(port=80,host='0.0.0.0',debug=True)
    else:
        app.run_server(port=80,host='0.0.0.0')
