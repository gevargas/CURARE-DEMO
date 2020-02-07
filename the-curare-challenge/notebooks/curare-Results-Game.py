import pandas as pd

import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.dashboard_objs as dashboard

import IPython.display
from IPython.display import Image
plotly.__version__

import dash
import dash_core_components as dcc
import dash_html_components as html


# - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . 
#  Page style definition
# - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . 


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

colors = {
    'background': '#111111',
    'text': '#171c42'
}


######################## Scatter polar: SCORE comparison in Matches 1 - 2 ########################

# - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . 
# Get scores from Match 1 - 2 
# - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . 
results_m1 = pd.read_csv('../results/match1.csv')
#na_values=':', usecols=['qid', 'score', 'time', 'user_effort', 'calculated_effort', 'execution_time'])

results_m2 = pd.read_csv('../results/match2.csv')#,
                         #na_values=':', usecols=['qid', 'score', 'time', 'user_effort', 'calculated_effort', 'execution_time'])


r = list(results_m1['score'])
rmax = max(r)
deltar = rmax+(rmax*0.1)

r2 = list(results_m2['score'])
rmax2 = max(r2)
deltar2 = rmax2+(rmax2*0.1)

# - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . 
# Define Scatter polar Data: score of answers questions per match
# - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . 
data_scatter_polar = [
    
    go.Scatterpolar(
                        r = r,
                        theta = results_m1['qid'],
                        fill = 'toself',
                        name = 'Score Match 1'
                    ),
    go.Scatterpolar(
                      r = r2,
                      theta = results_m2['qid'],
                      fill = 'toself',
                      name = 'Score Match 2'
                    )
]

# - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . 
# Define Scatter polar Layout: response time to questions Match 1 - 2
# - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . 
layout = go.Layout(
                      polar = dict(
                                      radialaxis = dict(
                                                          visible = True,
                                                          range = [0, max(deltar,deltar2)]
                                                        )
                                  ),
                      showlegend = True
                    )


data_Scatter_bis = [
                        go.Scatterpolar(
                                          r = r,
                                          theta = results_m1['qid'],
                                          fill = 'toself',
                                          name = 'Time Match 1'
                                        ),
                        go.Scatterpolar(
                          r = r2,
                          theta = results_m2['qid'],
                          fill = 'toself',
                          name = 'Time Match 2'
                        )
]

trace1 = go.Bar(
                    x = results_m1['qid'],
                    y=results_m1['time'],
                    name='Response time using raw data',
                    marker=dict(
                                color='rgb(55, 83, 109)'
                               )
                )

trace2 = go.Bar(
                    x = results_m2['qid'],
                    y = results_m2['time'],
                    name='Response time Using views',
                    marker=dict(
                                color='rgb(26, 118, 255)'
                                )
                )

data_scatter_polar_traces = [trace1, trace2]

layout = go.Layout(
                    title='Time to answer challenge queries',
                    xaxis=dict(
                                    tickfont=dict(
                                    size=16,
                                    color='rgb(107, 107, 107)'
                                    )
                                ),
                    yaxis=dict(
                                    title='Time (seconds)',
                                    titlefont=dict(
                                    size=16,
                                    color='rgb(107, 107, 107)'
                               ),
                    tickfont=dict(
                                    size=16,
                                    color='rgb(107, 107, 107)'
                                  )
                ),
legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
            ),
barmode='group',
bargap=0.12,
bargroupgap=0.1
)



########################  Pie chart: Effort in Matches 1 - 2 ########################

effort_groups1 = results_m1.groupby('user_effort').count().qid;effort_groups1
effort_groups2 = results_m2.groupby('user_effort').count().qid;effort_groups2

# - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . 
#  Effort in Matches 1: exploring raw data
# - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . 


fig1 = {
    "data": [
        {
            "values": effort_groups1,
            "labels": ['Low','Regular','High'],
            "marker": {
                        "line": {
                                    "color": "#FFFFFF",
                                    "width": 2
                                },
                        "colors": [
                                    "rgb(178, 62, 39)",
                                    "rgb(119, 123, 132)",
                                    "rgb(21, 52, 140)"
                                  ]
                      },
            "insidetextfont": {
                                "color": "#FFFFFF"
                                },
            #"domain": {"x": [0, .48]},
            "name": "User Effort Group",
            "hoverinfo":"label+percent+name",
            "hole": .4,
            "type": "pie"
        }],
    "layout": {
            "title":"User effort perception exploring raw data",
            "annotations": [
                            {
                                "font": {
                                            "size": 20
                                        },
                                "showarrow": False,
                                "text": "Match 1",
                                "x": 0.5,
                                "y": 0.5
                            }
                           ]
                }
     
}


# - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . 
#  Effort in Matches 2: exploring views
# - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . 

fig2 = {
    "data": [
        {
            "values": effort_groups2,
            "labels": ['Low','Regular','High'],
            "marker": {
                "line": {
                            "color": "#FFFFFF",
                            "width": 2
                        },
                "colors": [
                            "rgb(178, 62, 39)",
                            "rgb(119, 123, 132)",
                            "rgb(21, 52, 140)"
                            ]
                        },
            "insidetextfont": {
                                "color": "#FFFFFF"
                                },
            "name": "User Effort Group",
            "hoverinfo":"label+percent+name",
            "hole": .4,
            "type": "pie"
        }],
    "layout": {
                "title":"User effort perception exploring views",
                "annotations": [
                                    {
                                        "font": {
                                                    "size": 20
                                                },
                                        "showarrow": False,
                                        "text": "Match 2",
                                        "x": 0.5,
                                        "y": 0.5
                                    }
                                ]
                }
     
}

########################  Radar chart: Effort in Matches 1 - 2 ########################
# - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . 
# Define radar  Data: score of answers questions per match
# - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . - . 
# Create traces
radar_trace0 = go.Barpolar(
 #   x = results_m1['qid'],
    r = results_m1['calculated_effort'],
    text = results_m1['qid'],
   # mode = 'lines+markers',
    name = 'Exploring raw data',
    marker=dict(
        color='rgb(106,81,163)'
    )
)

radar_trace1 = go.Barpolar(
 #   x = results_m1['qid'],
    r = results_m2['calculated_effort'],
    text = results_m2['qid'],
   # mode = 'lines+markers',
    name = 'Exploring views',
    marker=dict(
        color='rgb(203,201,226)'
    )
)

#trace1 = go.Barpolar(
#    r=[77.5, 72.5, 70.0, 45.0, 22.5, 42.5, 40.0, 62.5],
#    text=['North', 'N-E', 'East', 'S-E', 'South', 'S-W', 'West', 'N-W'],
#    name='11-14 m/s',
#    marker=dict(
#        color='rgb(106,81,163)'
#    )
#)

#radar_layout = dict(title = 'Calculated effort (time/core ratio)',
#              yaxis = dict(zeroline = False),
#              xaxis = dict(zeroline = False)
#             )

radar_layout = go.Layout(
    title='Perceived effort in answering questions Match 1 - 2',
    font=dict(
        size=16
    ),
    legend=dict(
        font=dict(
            size=16
        )
    ),
    radialaxis=dict(
        ticksuffix='%'
    ),
    orientation=270
)

radar_data = [radar_trace0, radar_trace1]

radar_fig = dict(data= radar_data, layout = radar_layout)


######################## ****************** Main ********************** ########################

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

########################################################################################################################

app.layout = html.Div(children=[
    html.H1(children='The CURARE Challenge', 
            style={
            'textAlign': 'center',
            'color': colors['text']
            }),

    html.Div(children='Effort results Matches 1 & 2', 
             style={
            'textAlign': 'center',
            'color': colors['text']
            }),
    
    
# . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - . 
# Score bar chart for Matches 1 - 2    
# . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .     
    
html.Div([  
dcc.Graph(
        figure=go.Figure(
                        data=[
                            go.Bar(
                                x=results_m1['qid'],
                                y=[219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
                                   350, 430, 474, 526, 488, 537, 500, 439],
                                name='Score exploring raw data collections',
                                marker=go.bar.Marker(
                                    color='rgb(55, 83, 109)'
                                )
                            ),
                            go.Bar(
                                x=results_m2['qid'],
                                y=[16, 13, 10, 11, 28, 37, 43, 55, 56, 88, 105, 156, 270,
                                   299, 340, 403, 549, 499],
                                name='Score using views',
                                marker=go.bar.Marker(
                                color='rgb(26, 118, 255)'
                                )
                            )
                        ],
                        layout=go.Layout(
                                title='Measuring SCORE exploring Stack Overflow collections by hand & using views',
                                showlegend=True,
                                legend=go.layout.Legend(
                                x=0,
                                y=2.0
                            ),
                        margin=go.layout.Margin(l=40, r=0, t=40, b=30)
                    )
    ),
    style={'height': 290},
    id ='score-bar-chart'
),
    
dcc.Graph(   
    figure = go.Figure(data=data_scatter_polar_traces, layout=layout),
    id ='my-scatter-polar-traces'
),

], style={'columnCount': 2}),

# . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - . 
# Scatter Polar  chart for Matches 1 - 2    
# . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .     
 
html.Div([    
dcc.Graph(   
  
   figure = go.Figure(data = data_scatter_polar, layout=layout),
   id='my-polar-graph-1'
),
    
dcc.Graph(   
  
   figure = go.Figure(data= radar_data, 
                      layout = go.Layout(
                                            title='Perceived effort in answering questions Match 1 - 2',
                                             showlegend=True,
                                            font=dict(
                                                size=16
                                            ),
                                            legend=dict(
                                                font=dict(
                                                    size=16
                                                )
                                            ),
                                            radialaxis=dict(
                                                ticksuffix='%'
                                            ),
                                            orientation=270
                                        )

                    ),
                    id='my-radar-graph-2'
),
], style={'columnCount': 2}),
    
# . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - . 
# Pie  chart for Matches 1 - 2    
# . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .     
 html.Div([
 dcc.Graph(
             id='example-pie-chart1',
             figure= fig1
 ),
 
dcc.Graph(
             id='example-pie-chart2',
             figure= fig2
 ),
          ], style={'columnCount': 2}),
    
    
])  

# . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - . 
# Start server
# . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .  . - .     
 
if __name__ == '__main__':
    app.run_server(debug=True)