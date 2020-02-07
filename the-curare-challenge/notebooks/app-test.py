import pandas as pd
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.dashboard_objs as dashboard
import IPython.display
from IPython.display import Image
plotly.__version__

#pip install dash-table==3.1.11
#import dash
#import dash_table
#import pandas as pd

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import datetime
import json
import timeit
import buttons_CurareGrame as b_curaregame


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

colors = {
    'background': '#111111',
    'text': '#171c42'
}

def match_EvaluateEffort():
    return html.Div([

            html.H3(children='Evaluate Effort', 
                             style={
                            #'textAlign': 'center',
                            'color': colors['text'],
                            'fontFamily': 'Helvetica',
                           # 'marginLeft': 65,
                            'marginRight':80,
                            }),

                   dcc.Slider(id = 'slider-input-container',
                            min=0,
                            max=4,
                            marks={
                                1: {'label': 'Low', 'style': {'color': '#111111', 'fontSize': 15, 'fontFamily':'Helvetica'}},
                                2: {'label': 'Regular', 'style': {'color': '#111111', 'fontSize': 15, 'fontFamily':'Helvetica'}},
                                3: {'label': 'High', 'style': {'color': '#f50', 'fontSize': 15, 'fontFamily':'Helvetica'}}
                            },
                            step=0.50,
                            value=0,
                            updatemode = 'mouseup',
                            dots = True,
                ),
                html.Div(id='slider-output-container')
               ], style={'columnCount': 1, 'color': 'black', 'marginLeft': 65, 'marginRight':80})


def chronometre():
    return html.Div([
                        html.Button('Start', id='btn-1', n_clicks_timestamp='0'),
                        html.Button('Stop', id='btn-2', n_clicks_timestamp='0'),
                        html.Div(id='container-button-timestamp'),
                        ])

def define_question(question):
    return html.H3(children= question, 
                         style={
                        'textAlign': 'center',
                        'color': colors['text'],
                        'fontFamily': 'Helvetica'
                        })

def define_radioMultipleOptions(inputId, outputId, radio_options):
    return html.Div([html.Div([dcc.RadioItems( id = inputId,
                            options= radio_options,
                            value=''
                            )], style={'color': 'black', 'fontSize': 18, 'fontFamily': 'Helvetica'}),
              html.Div(id= outputId )
             ], style={'columnCount': 1, 'marginBottom': 25, 'marginTop': 25, 'marginLeft': 65}
            )
#------------------------------------------------------------------------------------------------------------------------------------------#
#------------------------------------------------------- Effort questions -----------------------------------------------------------------#
effortW = b_curaregame.collect_QuestionEffort()
timeLblW = b_curaregame.collect_ResponseTime()
q_answers = []
elapsed_time = 0

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.config['suppress_callback_exceptions']=True

app.layout = html.Div([
    html.Div([
                html.H1(children='The CURARE Challenge', 
                        style={
                        'textAlign': 'center',
                        'color': colors['text'],
                        'fontFamily': 'Helvetica'
                        }),

                html.H2(children='Match 1: exploring raw Stack Overflow data collections', 
                         style={
                        'textAlign': 'center',
                        'color': colors['text'],
                        'fontFamily': 'Helvetica'
                        }),
                ]),
    html.Div([
                   
                    #html.H3(children='Q1. Which release has the most number of records?', 
                    #     style={
                    #    'textAlign': 'center',
                    #    'color': colors['text'],
                    #    'fontFamily': 'Helvetica'
                    #    }),
                    define_question('Q1. Which release has the most number of records?'),
                    chronometre()
              
                    #html.Div([
                    #html.Button('Start', id='btn-1', n_clicks_timestamp='0'),
                    #html.Button('Stop', id='btn-2', n_clicks_timestamp='0'),
                    #html.Div(id='container-button-timestamp'),
                    #])
              ], style={'columnCount': 2}),
  #  html.Div([html.Div([dcc.RadioItems( id = 'q1-choice-input',
  #                          options=[
  #                              {'label': 'January 1rst 2018', 'value': 'R1'},
  #                              {'label': 'January 2nd 2018', 'value': 'R2'},
  #                              {'label': 'January 3rd 2018', 'value': 'R3'}
  #                          ],
  #                          value=''
  #                          )], style={'color': 'black', 'fontSize': 18, 'fontFamily': 'Helvetica'}),
  #            html.Div(id='q1-choice-output')
  #           ], style={'columnCount': 1, 'marginBottom': 25, 'marginTop': 25, 'marginLeft': 65}
  #          ),
    define_radioMultipleOptions('q1-choice-input', 'q1-choice-output', [
                                {'label': 'January 1rst 2018', 'value': 'R1'},
                                {'label': 'January 2nd 2018', 'value': 'R2'},
                                {'label': 'January 3rd 2018', 'value': 'R3'}
                            ]),
    match_EvaluateEffort()
   
    #html.Div([
   # dcc.Input(id='input-1-state', type='text', value='Montreal'),
  #  dcc.Input(id='input-2-state', type='text', value='Canada'),
  #  html.Button(id='submit-button', n_clicks=0, children='Submit'),
  #  html.Div(id='output-state')
#]),
  #  html.Div([
        
  #      html.H3(children='Evaluate Effort', 
  #                       style={
                        #'textAlign': 'center',
  #                      'color': colors['text'],
  #                     'fontFamily': 'Helvetica',
                       # 'marginLeft': 65,
  #                      'marginRight':80,
  #                      }),
        
              
   #            dcc.Slider(id = 'slider-input-container',
   #                     min=0,
   #                     max=4,
   #                     marks={
   #                         1: {'label': 'Low', 'style': {'color': '#111111', 'fontSize': 15, 'fontFamily':'Helvetica'}},
   #                         2: {'label': 'Regular', 'style': {'color': '#111111', 'fontSize': 15, 'fontFamily':'Helvetica'}},
   #                         3: {'label': 'High', 'style': {'color': '#f50', 'fontSize': 15, 'fontFamily':'Helvetica'}}
   #                     },
    #                    step=0.50,
    #                    value=0,
    #                    updatemode = 'mouseup',
    #                    dots = True,
    #        ),
    #        html.Div(id='slider-output-container')
    #       ], style={'columnCount': 1, 'color': 'black', 'marginLeft': 65, 'marginRight':80})
])

@app.callback(Output('container-button-timestamp', 'children'),
             [Input('btn-1', 'n_clicks_timestamp'),
               Input('btn-2', 'n_clicks_timestamp')
              ])
def displayClick(btn1, btn2):
    if int(btn1) > int(btn2):
        #timeLblW.append(0)
        elapsed_time = 0
        msg = 'Top chronometer'
    elif int(btn2) > int(btn1):
        #timeLblW.append( ((int(btn2) - int(btn1))/1000))
        elapsed_time = (int(btn2) - int(btn1))/1000
        timeLblW.append(elapsed_time)
        msg = ('Elapsed time: ' + str(elapsed_time))
    else:
        msg = ''
    return html.Div([
                    html.H4(msg)
                    ],  style={'columnCount': 1, 'fontFamily':'Helvetica'})


@app.callback(
    Output(component_id ='slider-output-container', component_property ='children'),
    [Input(component_id = 'slider-input-container', component_property = 'value')]
)
def update_output(value):
    if value == 0:
        msg = ''
    else: 
        effortW.append(value)
        if value == 1:
            effort = "Low"
        elif value == 2:
            effort = "Regular"
        elif value == 3:
            effort = "High"
        msg = ('You have selected: ' + effort)
    return html.Div([
                    html.H4(msg)
               ], style={'columnCount': 1, 'fontFamily':'Helvetica'})


@app.callback(
    Output(component_id = 'q1-choice-output', component_property = 'children'),
    [Input(component_id = 'q1-choice-input', component_property = 'value')]
)
def callback_b(dropdown_value): 
        if dropdown_value == '':
            msg = ''
        else:
            q_answers.append(dropdown_value)
            msg = ('Choice you\'ve selected: ' + str(dropdown_value))
        return html.Div([
                            html.H4(msg)
                        ], style={'columnCount': 1, 'fontFamily':'Helvetica'}
                        )


    

    
#@app.callback(Output('output-state', 'children'),
#              [Input('submit-button', 'n_clicks')],
#              [State('input-1-state', 'value'),
#               State('input-2-state', 'value')])
#def update_output(n_clicks, input1, input2):
#    return u'''
#        The Button has been pressed {} times,
#        Input 1 is "{}",
#        and Input 2 is "{}"
#    '''.format(n_clicks, input1, input2)



if __name__ == '__main__':
    app.run_server(debug=True)
    
#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

#app = dash.Dash(__name__)

#app.layout = dash_table.DataTable(
#    id='table',
#    columns=[{"name": i, "id": i} for i in df.columns],
#    data=df.to_dict("rows"),
#)

#if __name__ == '__main__':
#    app.run_server(debug=True)