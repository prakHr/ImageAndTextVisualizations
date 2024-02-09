import dash
from dash import html
import pandas as pd
from dash import dash_table
from dash import html, dcc, callback, Input, Output
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback

dash.register_page(__name__)

kpath1 = r'./pages/data/kiranaItems.xlsx'
kirana_df1 = pd.read_excel(kpath1,engine='openpyxl')

kpath2 = r'./pages/data/kiranaBarcodes.xlsx'
kirana_df2 = pd.read_excel(kpath2,engine='openpyxl')


kirana_df1[' index'] = range(1, len(kirana_df1) + 1)
kirana_df2[' index'] = range(1, len(kirana_df2) + 1)

PAGE_SIZE = 5
layout = html.Div([
    html.H1('This is our Archive page'),
    html.Div('Here is kirana archive present!'),
    dash_table.DataTable(
        id='datatable-paging-1',
        columns=[
            {"name": i, "id": i} for i in sorted(kirana_df1.columns)
        ],
        page_current=0,
        page_size=PAGE_SIZE,
        page_action='custom'
    ),
    dash_table.DataTable(
        id='datatable-paging-2',
        columns=[
            {"name": i, "id": i} for i in sorted(kirana_df2.columns)
        ],
        page_current=0,
        page_size=PAGE_SIZE,
        page_action='custom'
    )



])
@callback(
    Output('datatable-paging-1', 'data'),
    Input('datatable-paging-1', "page_current"),
    Input('datatable-paging-1', "page_size"))
def update_table(page_current,page_size):
    return kirana_df1.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')

@callback(
    Output('datatable-paging-2', 'data'),
    Input('datatable-paging-2', "page_current"),
    Input('datatable-paging-2', "page_size"))
def update_table(page_current,page_size):
    return kirana_df2.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')
