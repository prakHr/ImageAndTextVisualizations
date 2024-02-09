import dash
from dash import html
import pandas as pd
import dash_mantine_components as dmc
dash.register_page(__name__, path='/')

################################
kpath = r'./pages/data/phoneNos.xlsx'
kirana_df = pd.read_excel(kpath,engine='openpyxl')
phonenos = kirana_df['phone Numbers'].tolist()
gradients = [
    {"from": "indigo", "to": "cyan"},
    {"from": "teal", "to": "lime", "deg": 105},
    {"from": "teal", "to": "blue", "deg": 60},
    {"from": "orange", "to": "red"},
    {"from": "grape", "to": "pink", "deg": 35},
]
phone_children = []
for i in range(len(phonenos)):
    component = dmc.Badge(f"{phonenos[i]}",variant = "gradient",gradient = gradients[i%len(gradients)],size="xl")
    phone_children.append(html.Br())
    phone_children.append(html.Br())
    phone_children.append(component)
#######################################

################################
gpath = r"./pages/data/generalInfo.xlsx"
availableInfoDf = pd.read_excel(gpath,engine='openpyxl')
availableInfocols = list(availableInfoDf.columns)
components = []
for index, row in availableInfoDf.iterrows():
    rr = row.tolist()
    items  = list(eval(rr[-1]))
    # print(items)
    ss = html.Div(dmc.Select(
            label="Select item",
            placeholder="Select one",
            id="kiranaItem-select",
            value="ng",
            data=[
                {"value":item.lower(),"label":item.lower().title()}
                for item in items
                
            ],
            style={"width": 200, "marginBottom": 10},
        )
    )
    component = html.Div([dmc.Badge(f"{c}",size="xl") for c in rr[:-1]])
    components.append(component)
    components.append(ss)
    components.append(html.Br())
################################

layout = html.Div([
    html.H1('General Info of Kirana Users'),
    html.Div('This is our available users phoneNos.'),
    html.Div(phone_children),
    html.Div(components)
])