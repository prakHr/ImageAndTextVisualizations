from dash import Dash, dcc, html, Input, Output, State, callback
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, ALL
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

import re
app = Dash(__name__)
app.config.suppress_callback_exceptions=True

app.layout = html.Div([
    html.Div(dcc.Input(id='input-on-submit', type='text')),
    html.Button('Submit', id='submit-val', n_clicks=0),
    html.Div(id='container-button-basic',
             children='Enter a value and press submit'),
    html.Div(id = 'output-regex',children = ""),
    # dcc.Store stores the intermediate value
    dcc.Store(id='intermediate-value'),
    html.Br(),
    html.Div(id='container-button-basic-2',
             children='Enter a regex output value 2 and press submit'),
  
     html.Div(id = 'output-api-call',children = ""),

    # html.Button('Submit-2', id='submit-val-2', n_clicks=0),
    
    dbc.Button(id='btn-scrape',
                           children=["Download  ", html.I(className="fa fa-download mr-1")],
                           color="primary",
                           className="mt-1"
                           ),
    html.Hr(),

    
    html.Hr(),
    dbc.Col([
        dcc.Loading(
            id='loading-1',
            type='circle',
            children=[
                dash_table.DataTable(
                    id='datatable-paging',
                    data=[{}],
                    editable=True,
                    style_cell={
                        'whiteSpace': 'normal',
                        'lineHeight': 'auto',
                        'height': 'auto',
                        'fontSize': 12},
                    page_current=0,
                    page_size=10,
                    page_action='native'),
                dcc.Download(id='download-table')
            ]),
    ])
])


@app.callback(
    
        
    [
        Output('intermediate-value', 'data'),
        Output('container-button-basic', 'children'), 
        Output('output-regex','children'),
    ],
    State('output-regex','children'),
    Input('submit-val', 'n_clicks'),
    State('input-on-submit', 'value'),
    prevent_initial_call=True
)
def update_output(children,n_clicks, value):
    def generate_inputs(shortName):
        return dbc.Input(id={
                        'type': 'dynamic-textbox',
                        'index': shortName
                    },
                     type='text',
                     placeholder=str(shortName),
                     style={"margin-bottom": "5px"})

    pattern  = r'\{\{.*?\}\}'
    matches = re.finditer(pattern, value)
    # print(matches)
    children = []
    iterr = 1
    json_data = {}
    # matches_lst = [i.group(0) for i in matches]
    for matchNum, match in enumerate(matches, start=1):
        text = str(match.group(0)).strip()
        # print(text)
        json_data[text[2:-2]] = text[2:-2]
        children.append(generate_inputs(text[2:-2]))
        # children.append(html.Div(text[2:-2]))
        # children.append(html.Textarea(id=f"regex-{iterr}"))
        iterr+=1

        # print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    # children.append(html.Button('Submit-2', id='submit-val-2', n_clicks=0))
    return json_data,'The input value was "{}" and the button has been clicked {} times'.format(
        value,
        n_clicks
    ),dbc.Col(children = children)

'''
App callback: Scraping data from eurlex using the XmlScraper Class
'''
@app.callback(
    [
        Output('datatable-paging', 'data'),
        Output('output-api-call','children'),
    ],
    [
        Input('intermediate-value', 'data'),
        Input('btn-scrape', 'n_clicks'),
    ],
    State({'type': 'dynamic-textbox', 'index': ALL}, 'value'),
    prevent_initial_call=True
)
def update_output(json_data,n_clicks, value):

    if n_clicks is None:
        return json_data,""
    else:
        # print(value)
        # print(json_data)
        # json_data = json_data[0]
        json_keys = [k.strip() for k in list(json_data.keys())]
        json_dict = {k:v for k,v in zip(json_keys,value)}
        children = "Human Role: What is the message for user when supplied with naive information like "
        i = 0
        for k,v in json_dict.items():
                if i!=len(json_keys)-1:
                    children+=f"{k} is {v} and "
                else:
                    children+=f"{k} is {v}."
                i+=1
        return json_data,children

if __name__ == '__main__':
    app.run(debug=True)
