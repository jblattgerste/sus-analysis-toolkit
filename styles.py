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

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#445262',
    'color': 'white',
    'padding': '6px'
}

graph_style = {'height': '50vh'
               }

single_study_graph_style = {'width': '100%', 'height': '80vh'}

graph_editor_container = {'width': '100%',
                          'display': 'flex',
                          'justify-content': 'center',
                          'flex-wrap': 'wrap'
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

main_content_style = {'width': '70%'
                      }

single_study_main_content_style = {'width': '70%'}

per_item_main_content_style = {'display': 'block',
                               'width': '70%'}

mainPageDownloadPanelStyle = {

                                        'height': '10em',
                                        'width':'98%',
                                        'line-height':'10em',
                                        'borderWidth': '1px',
                                        'borderStyle': 'dashed',
                                        'borderRadius': '5px',
                                        'display': 'inline-block',
                                        'textAlign': 'center',
                                        'background-color': '#FFFFFF',
                                        'box-shadow': '0 .5rem 1rem -.5rem rgba(0, 0, 0, .4)',
                                        'font-weight': 'bold',
                                        'font-size': 'x-large',
                                        'color': 'black',
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
