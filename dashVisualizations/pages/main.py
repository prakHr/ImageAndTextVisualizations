import dash

dash.register_page(__name__, path="/")

from dash import Dash, dcc, html, Input, Output, State, callback, dash_table
import plotly.express as px
import pandas as pd


layout = html.Div(
    [
        html.P("Choose Classes:"),
        html.Div(id="dropdown-container", children=[]),
        # html.Div(id="dropdown-container-0", children=[]),
        #html.Div(id="bar-container", children=[]),
    ]
)
@callback(
           [ Output("dropdown-container", "children")],
            [Output("stored-data", "data")],
                  [Input('submit-button', 'n_clicks')],
                  [State('username', 'value')],
                  [State('username-2', 'value')],
                  Input("stored-data", "data"))
def populate_dropdownvalues_0(clicks,input_value,file_path,data):
    dff=pd.read_csv(file_path,encoding = 'unicode_escape')
    #dff=pd.DataFrame(data)
    #print("dff")

    all_cols = list(dff.columns)
    # print(all_cols)
    # print(input_value)
    if input_value in all_cols:
            # print(input_value)
            # print("column is in df")

            return dcc.Dropdown(
                id="dropdown",
                options=[{"label": x, "value": x} for x in dff[input_value].unique()],
                value=dff[input_value].unique()[0],
                clearable=False,
                style={"width": "50%"},
                persistence=True,
                persistence_type="session"
            ),dff.to_dict("records")
    #print(input_value)
    return dcc.Dropdown(
            id="dropdown",
            options=[{"label": "Incorrect Value", "value": "Incorrect Value"}],
            value="Please select a correct value",
            clearable=False,
            style={"width": "50%"},
            persistence=True,
            persistence_type="session"
        ),{"error":"You have inputted wrong column name and it does not exists"}


# @callback(Output("dropdown-container", "children"), Input("stored-data", "data"))
# def populate_dropdownvalues(data):
#     dff = pd.DataFrame(data)
#     return dcc.Dropdown(
#         id="dropdown",
#         options=[{"label": x, "value": x} for x in dff.day.unique()],
#         value=dff.day.unique()[0],
#         clearable=False,
#         style={"width": "50%"},
#         persistence=True,
#         persistence_type="session"
#     ),


# @callback(
#     [Output("bar-container", "children"),
#     Output("store-dropdown-value", "data")],
#     [Input("dropdown", "value"),
#      State("stored-data", "data")]
# )
# def graph_and_table(dropdown_day, data):
#     dff = pd.DataFrame(data)
#     dff = dff[dff["day"] == dropdown_day]
#     fig = px.bar(dff, x="sex", y="total_bill", color="smoker", barmode="group")
#     return dcc.Graph(figure=fig), dropdown_day

@callback(
    Output("store-dropdown-value", "data"),
    Input("dropdown", "value")
)
def graph_and_table(dropdown_day):
    return dropdown_day

