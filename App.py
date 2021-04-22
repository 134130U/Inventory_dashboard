import pandas as pd
from datetime import date
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import collect
import plotly.express as px
from apscheduler.schedulers.background import BackgroundScheduler
import senegal,mali,nigeria,niger,burkina,cameroun

collect.get_data()

scheduler = BackgroundScheduler()
scheduler.add_job(func=collect.get_data, trigger="interval", minutes=180)
scheduler.start()



data = pd.read_csv('data/inventory.csv')

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": '#1f2c56',
    'color':'white'
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    # 'color':'white',
}

sidebar = html.Div(
    [
        html.Img(src=app.get_asset_url('oolu.png'),
                 id='oolu-logo',
                 style={
                     "height": "60px",
                     "width": "auto",
                     "margin-bottom": "30px",},
                 ),
        html.Br(style={"height": "400px"}),
        html.H2("Pays", className="display-4"),
        html.Hr(),
        html.P(
            "Veuillez choisir votre pays ", className="lead"
        ),
        html.Br(style={"height": "400px"}),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Senegal", href="http://212.47.246.218:8081/", active="exact"),
                dbc.NavLink("Mali", href="http://212.47.246.218:8082/", active="exact"),
                dbc.NavLink("Burkina", href="http://212.47.246.218:8087/", active="exact"),
                dbc.NavLink("Nigeria", href="http://212.47.246.218:8084/", active="exact"),
                dbc.NavLink("Cameroun", href="http://212.47.246.218:8086/", active="exact"),
                dbc.NavLink("Niger", href="http://212.47.246.218:8085/", active="exact")

            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

fig1 = px.sunburst(data, path=['country','etat'], values='quantite',
                  color='etat',width=600, height=500)
fig1.update_layout(
    margin=dict(l=20, r=20, t=20, b=20),
    paper_bgcolor='#1f2c56',)

# fig.show()
df_hist = data.groupby(['country','etat'],as_index=False).sum({'quantite':'sum'})
fig2 = px.bar(df_hist, x="country", y="quantite",color='etat',width=300, height=300,)
fig2.update_layout(
    margin=dict(l=20, r=20, t=20, b=20),
    paper_bgcolor='#1f2c56',)
# fig2.show()

content = html.Div([
                    dcc.Interval(
                        id='interval-component',
                        interval=144000*1000, # in milliseconds
                        n_intervals=0
                    ),
                    dbc.Row([
                        dbc.Col(html.H1('Inventaire Du Stock',
                                style={
                                    'textAlign': 'center',
                                    'color': 'white'
                                    }),
                            width={'size': 4, 'offset': 4}, ),
                        dbc.Col(html.P(id ='refresh' ,children='Last update  :  ' f'{date.today()}',
                               style={
                                       'textAlign': 'right',
                                       'color': 'orange',
                                       'fontSize': 14}),
                            width={'size': 2, 'offset': 2},
                        ),
                    ]),
            dbc.Row([
                dbc.Col(html.Div(),width={'size': 3},),
                html.Div([
                    html.H4(children='Global Stocks',
                            style={
                                'textAlign': 'center',
                                'color': 'white'}
                            ),
                    html.P(f"{data['quantite'].sum():,.0f}",
                           style={
                               'textAlign': 'center',
                               'color': 'orange',
                               'fontSize': 40}
                           ),
                    ], className="card_container two columns",
                ),
            html.Div([
                html.H4(children='Stock Neuf',
                        style={
                            'textAlign': 'center',
                            'color': 'white'}
                        ),
                html.P(f"{data['quantite'][data['etat'] =='Neuf'].sum():,.0f}",
                       style={
                           'textAlign': 'center',
                           'color': 'green',
                           'fontSize': 40}
                       ),
                ], className="card_container two columns",
            ),
            html.Div([
                html.H4(children='Stock KO',
                        style={
                            'textAlign': 'center',
                            'color': 'white'}
                        ),
                html.P(f"{data['quantite'][data['etat'] =='Endommagé'].sum():,.0f}",
                       style={
                           'textAlign': 'center',
                           'color': 'red',
                           'fontSize': 40}
                       ),
                ], className="card_container two columns",
            ),
            ]),

    dbc.Row([
    dbc.Col(html.Div(html.H4(children='Repartition du stock par pays et etat des produits',
                        style={
                            'textAlign': 'center',
                            'color': 'white'}
            ),),width={'size': 6,'offset': 3},),

        dbc.Col([

            dcc.Graph(figure=fig1, style={"background-color": '#1f2c56'}),
        ],width={'size': 4,'offset': 4},),
    ]),
    html.Div(
            id='update-connection'
        )
])
@app.callback(
    Output('update-connection', 'children'),
    Output('refresh', 'children'),
    Input('interval-component', 'n_intervals'))
def update_connection(n):
    global data

    if n > 0:
        data = pd.read_csv('data/inventory.csv')
        collect.get_data()
        print('data have been updated')

        return ''


app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


if __name__ == "__main__":
    app.run_server(debug=True,dev_tools_ui=False, host='0.0.0.0', port=8888)