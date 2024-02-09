import dash
from dash import html, dcc, callback, Input, Output
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback

import base64
import datetime
import io

import pandas as pd
import plotly.express as px
dash.register_page(__name__)


layout = html.Div([
    html.H1('Two Dimensional Scatter Plot'),
    html.Div([
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            # Allow multiple files to be uploaded
            multiple=True
        ),
        html.Div(id='output-data-upload'),
        dcc.Graph(id="scatter-plot"),
    ]),
    # html.Div([
    #     "Select a city: ",
    #     dcc.RadioItems(
    #         options=['New York City', 'Montreal', 'San Francisco'],
    #         value='Montreal',
    #         id='analytics-input'
    #     )
    # ]),
    html.Br(),
    html.Div(id='dd-output-container'),
    html.Button(id="submit-btn", children="Submit feature choice"),
    # html.Div(id='analytics-output'),
])



# @callback(
#     Output('analytics-output', 'children'),
#     Input('analytics-input', 'value')
# )
# def update_city_selected(input_value):
#     return f'You selected: {input_value}'

    
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xlsx' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded),engine = 'openpyxl')
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ]),pd.DataFrame()
    # df.select_dtypes(include='number')
    
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    newdf = df.select_dtypes(include=numerics)
    numeric_cols = list(newdf.columns)
    # newdf.to_csv("temp.csv")
    return html.Div([
        dcc.Dropdown(
                        numeric_cols, 
                        id='feature-1-dropdown',
                        # persistence=True,
                        # persistence_type="session"
                    ),
        dcc.Dropdown(numeric_cols, 
                        id='feature-2-dropdown',
                        # persistence=True,
                        # persistence_type="session"
                    ),
        
        # html.H5(filename),
    #     html.H6(datetime.datetime.fromtimestamp(date)),

    #     dash_table.DataTable(
    #         df.to_dict('records'),
    #         [{'name': i, 'id': i} for i in df.columns]
    #     ),

    #     html.Hr(),  # horizontal line

    #     # For debugging, display the raw contents provided by the web browser
    #     html.Div('Raw Content'),
    #     html.Pre(contents[0:200] + '...', style={
    #         'whiteSpace': 'pre-wrap',
    #         'wordBreak': 'break-all'
    #     })
    ]),newdf

@callback([
              Output('output-data-upload', 'children'),
              Output("current-data", "data")
    ],
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        x= [parse_contents(c, n, d)[0] for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        children = x
        newdf = [parse_contents(c, n, d)[1] for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        newdf = newdf[0]
        return children,newdf.reset_index().to_json(orient="split")
    return [],pd.DataFrame().reset_index().to_json(orient="split")

@callback(
    [
        Output('dd-output-container', 'children'),
        Output("scatter-plot", "figure")
    ], 
    [
        Input("submit-btn", "n_clicks"),
        # State('feature-1-dropdown', 'feature1'),
        # State('feature-2-dropdown', 'feature2'),
        State('output-data-upload', 'children'),
        State("current-data", "data"),
        
    ],
    prevent_initial_call=True

)
def update_chart(n_clicks,children,data):
    # print(children)
    # print(feature2)
    if children is not None:
        children = children[0]
        from pprint import pprint
        # pprint(children)
        # newdf = pd.read_csv("temp.csv")
        newdf = pd.read_json(data,orient="split")
        # print(newdf.head(10))
        feature1 = children['props']['children'][0]['props']['value']
        feature2 = children['props']['children'][1]['props']['value']
        fig = px.scatter(newdf, x=feature1, y=feature2)
        return [],fig
    else:
        return f'You have selected {None} and {None}'