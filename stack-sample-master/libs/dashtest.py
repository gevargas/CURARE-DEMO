from IPython import display
# def show_app(app,  # type: dash.Dash
#              port=9999,
#              width=700,
#              height=350,
#              offline=True,
#              style=True,
#              **dash_flask_kwargs):
#     """
#     Run the application inside a Jupyter notebook and show an iframe with it
#     :param app:
#     :param port:
#     :param width:
#     :param height:
#     :param offline:
#     :return:
#     """
#     url = 'http://localhost:%d' % port
#     iframe = '<iframe src="{url}" width={width} height={height}></iframe>'.format(url=url,
#                                                                                   width=width,
#                                                                                   height=height)
#     display.display_html(iframe, raw=True)
#     if offline:
#         app.css.config.serve_locally = True
#         app.scripts.config.serve_locally = True
#     if style:
#         external_css = ["https://fonts.googleapis.com/css?family=Raleway:400,300,600",
#                         "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
#                         "http://getbootstrap.com/dist/css/bootstrap.min.css", ]

#         for css in external_css:
#             app.css.append_css({"external_url": css})

#         external_js = ["https://code.jquery.com/jquery-3.2.1.min.js",
#                        "https://cdn.rawgit.com/plotly/dash-app-stylesheets/a3401de132a6d0b652ba11548736b1d1e80aa10d/dash-goldman-sachs-report-js.js",
#                        "http://getbootstrap.com/dist/js/bootstrap.min.js"]

#         for js in external_js:
#             app.scripts.append_script({"external_url": js})

#     return app.run_server(debug=False,  # needs to be false in Jupyter
#                           port=port,
#                           **dash_flask_kwargs)



# import dash
# import dash_core_components as dcc
# import dash_html_components as html

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# app.layout = html.Div(children=[
#     html.H1(children='Hello Dash'),

#     html.Div(children='''
#         Dash: A web application framework for Python.
#     '''),

#     dcc.Graph(
#         id='example-graph',
#         figure={
#             'data': [
#                 {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
#                 {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montreal'},
#             ],
#             'layout': {
#                 'title': 'Dash Data Visualization'
#             }
#         }
#     )
# ])

import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Hello Dash',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(children='Dash: A web application framework for Python.', style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='example-graph-2',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'Saltillo'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Chihuahua'},
            ],
            'layout': {
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

#show_app(app)
