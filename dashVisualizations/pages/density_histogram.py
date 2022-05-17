import dash

dash.register_page(__name__)

from dash import Dash, dcc, html, Input, State, Output, callback, dash_table
import plotly.express as px
import pandas as pd

from plotly.subplots import make_subplots


layout = html.Div(
    [
        html.Div(id="density-container", children=[]),
    ]
)
# @callback(
#     [Output("table-container", "children"),
#     Output("store-dropdown-value", "data")],
#     [Input("dropdown", "value"),
#      State("stored-data", "data")]
# )
# @callback(
#     [Output("table-container", "children"),
#     Output("store-dropdown-value", "data")],
#    [Input("dropdown", "value"),
#      State("stored-data", "data")]     
# )
# def graph_and_table(dropdown_day, data):
#     dff = pd.DataFrame(data)
#     print("Here graph can be made now according to dropdown")
#     dff = dff[dff["day"] == dropdown_day]
#     fig = px.bar(dff, x="sex", y="total_bill", color="smoker", barmode="group")
#     return dcc.Graph(figure=fig), dropdown_day


@callback(
    Output("density-container", "children"),
          [
          State("density-container",'children'),
          Input("stored-data", "data")]
          )
def populate_checklist(children, data):
    df = pd.DataFrame(data)
    cols = list(df.columns)
    counter = 1 

    for i,c in enumerate(cols):
        for j,c2 in enumerate(cols):
            if j>=i:
                continue
            try:
                fig = px.density_heatmap(df, x=c, y=c2, marginal_x="histogram", marginal_y="histogram")
                el = html.Div(
                    [
                        html.Div(id=f"heading_{counter}",children=[dcc.Graph(figure=fig)])
                    ],id=f"heading_element_{counter}"
                    )
                children.append(el)  
                counter+=1
            
            except Exception as e:
                # print(str(e))
                continue

    return children