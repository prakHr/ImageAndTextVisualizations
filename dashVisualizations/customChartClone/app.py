import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True, use_pages=True)

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
    

app.layout = html.Div([
    html.H1('Multi-page app with Dash Pages'),
    # html.Div([
    #     html.Div(
    #         dcc.Link(f"{page['name']} - {page['path']}", href=page["relative_path"])
    #     ) for page in dash.page_registry.values()
    # ]),
    navbar,
    dcc.Store(id="current-data"),
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True)