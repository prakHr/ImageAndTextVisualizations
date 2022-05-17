import dash
from dash import dcc, callback, Output, State, Input, dash_table # pip install dash
import dash_labs as dl  # pip install dash-labs
import dash_bootstrap_components as dbc # pip install dash-bootstrap-components
from dash import html
import plotly.express as px
import pandas as pd
import os


def get_app():
    cwd = os.getcwd()
    #df = px.data.tips()
    dummy_dict = {'key 1': 'value 1', 'key 2': 'value 2', 'key 3': 'value 3'}
    df = pd.DataFrame([dummy_dict])
    df.to_csv("temp_df.csv")
    #print(df.head())
    #print("Here")
    # convert dataframe to list of dictionaries because dcc.Store
    # accepts dict | list | number | string | boolean

    all_cols = list(df.columns)
    df = df.to_dict('records')

    app = dash.Dash(
        __name__, plugins=[dl.plugins.pages], external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True
    )

    navbar = dbc.NavbarSimple(
        dbc.DropdownMenu(
            [
                dbc.DropdownMenuItem(page["name"], href=page["path"])
                for page in dash.page_registry.values()
                if page["module"] != "pages.not_found_404"
            ],
            nav=True,
            label="More Pages",
        ),
        brand="Multi Page App Visualization Automated one",
        color="primary",
        dark=True,
        className="mb-2",
    )
    

    input_text_tag = html.Div([
            dcc.Input(id='username', value='key 1', type='text'),
            html.Button(id='submit-button', type='submit', children='Submit column name'),
            html.Div(id='output_div')
    ])

    input_text_tag_for_filepath = html.Div([
            dcc.Input(id='username-2', value=os.path.join(cwd,"temp_df.csv"), type='text'),
            html.Button(id='submit-button-2', type='submit', children='submit csv file path'),
            html.Div(id='output_div-2')
    ])
    create = html.Div(
        [
            html.Div(id="dropdown-container", children=[],style= {'display': 'none'} ),
            # html.Div(id="dropdown-container-0", children=[]),
            #html.Div(id="bar-container", children=[]),
        ]
    )

    app.layout = dbc.Container(
        [navbar,
         input_text_tag,
         input_text_tag_for_filepath,
         create,
         dcc.Store(id="stored-data", data=df),
         dcc.Store(id="store-dropdown-value", data=None),
         dl.plugins.page_container],
        fluid=True,
    )


    return app
# @app.callback(Output('output_div', 'children'),
#                   [Input('submit-button', 'n_clicks')],
#                   [State('username', 'value')])
# def update_output(clicks, input_value):
#     if clicks is not None:
#         if input_value in all_cols:
#             #print(input_value)
#             print("column is in df")
#             print("-"*50)
#         else:
#             print("column is not in df")
#             print("-"*50)
#         #print(clicks, input_value)
#         #print(type(input_value))


if __name__ == "__main__":
    
    app=get_app()
    app.run_server(debug=True, port=8003)
