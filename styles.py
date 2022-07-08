import Charts

tabs_styles = {
    'height': '44px',
    'width': '50%'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {'border-top': '3px solid #445262'}

graph_content_style={'display': 'block', 'padding': '10px'}

graph_style = {'height': '50vh'
               }

single_study_graph_style = {'width': '100%', 'height': '80vh'}

graph_editor_container = {'width': '100%',
                          'display': 'flex',
                          'justify-content': 'center',
                          'flex-wrap': 'wrap',
                          'margin-top': '1.5em'
                          }

defaultEditorLabel = {'display': 'block',
                      'font-weight': 'bold',
                      'padding': '10px 10px 10px 10px'}

disabledStyle = {
    'display': 'none'
}

tableStyle = {'float': 'left',
              'width': '100%',
              'margin-top': '1em'}

tableStyle_next_to_plot = {'float': 'left',
                           'width': '30%',
                           'margin-top': '2em'
                           }


perItemTableStyle = {
    'max-width': '100%',
    'margin-right': '30px'}

mainPageSummaryHeaderStyle = {
                                'font-size': '1.2em',
                                'font-weight': 'bold',
                                'color': 'white'
                            }

mainPageSummaryParagraph = {'width':'75%', 'margin-left': 'auto', 'margin-right':'auto'}

editorInfoTextStyle = {'font-weight': 'normal',
                       'font-size': 'small'}

download_div_style_mainplot = {'display': 'block',
                               'float': 'left',
                               'padding': '10px 10px 10px 10px'

                               }

download_div_style = {'display': 'block',
                      'padding': '10px 10px 10px 10px'
                      }

graph_style_per_item = {
    'float': 'left',
    'width': '60%',
    'height': '50vh'
}

graph_div_style = {'width': '100%',
                   'float': 'left',
                   }

graph_div_style_with_table = {'width': '70%',
                              'float': 'left'}

graph_div_style_per_item = {'max-width': '100%',
                            'float': 'right'}

graph_div_style_with_table_row = {'max-width': '100%',
                                  'display': 'flex',
                                  'justify-content': 'center'}

main_content_style = {'width': '70%',
                      'display':'inline-block',
                      'float': 'left'
                      }

single_study_main_content_style = {
    'width': '70%'}

per_item_main_content_style = {'display': 'block',
                               'width': '70%'}

mainPageDownloadPanelStyle = {
                                        'align-items': 'center',
                                        'height': '10em',
                                        'borderWidth': '1px',
                                        'borderStyle': 'dashed',
                                        'borderRadius': '5px',
                                        'display': 'flex',
                                        'textAlign': 'center',
                                        'background-color': '#FFFFFF',
                                        'box-shadow': '0 .5rem 1rem -.5rem rgba(0, 0, 0, .4)',
                                        'color': 'black',
                                        'font-family': 'monospace',
                                    }

editableTableDataStyleError = {'border': '3px double #FF0033'}

editableTableDataStyleDefault = {'border': '1px double lightgray'}

tableErrorIconDefaultStyle = {'display':'none'}

tableErrorIconEnabledStyle = {'margin-left': 'auto', 'margin-right': 'auto', 'display':'block'}

tab_style_upload_panel = {
    'fontWeight': 'bold'
}

tab_selected_style_upload_panel = {
    'backgroundColor': '#445262',
    'color': 'white',
}

def changeGraphWidth(width):
    return {'max-width': '1000px',
            'width': '{}px'.format(width),
            'float': 'right',  #
            'height': '500px'}


# Workaround function for bug that changes the width and length of the graph div when changing tabs
def adjustGraphStyle(systemCount, orientationValue):
    if orientationValue == 'horizontal':
        return changeGraphWidth(Charts.plotSize.get(orientationValue))
    else:
        return changeGraphWidth(Charts.plotSize.get(systemCount))
