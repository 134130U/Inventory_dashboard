import pandas as pd
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_table as dt
from datetime import date
from datetime import timedelta
import os
from flask import Flask, send_from_directory
import dash
import dash_html_components as html
from app_test import telechargement
import collect
from apscheduler.schedulers.background import BackgroundScheduler


# from main import app


tabel_colunm = ['product_type','etat','cost_price','quantite','Cout Total']


table_header_style = {
    "backgroundColor": "rgb(2,21,70)",
    "color": "white",
    "textAlign": "center",
    'fontSize': 20
}
data = pd.read_csv('data/inventory.csv')

server = Flask(__name__)
app = dash.Dash(server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

# tl = telechargement('Senegal')
# tl.job2()
# df_neuf = tl.df_neuf
# df_ko = tl.df_ko

app.layout =  html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Interval(
        id='interval-component',
        interval=144000 * 1000,  # in milliseconds
        n_intervals=0
    ),
    dbc.Row([
        dbc.Col([
            html.A([html.Img(src=app.get_asset_url('oolu.png'),
                             id='oolu-logo',
                             style={
                                 "height": "60px",
                                 "width": "auto",
                                 "margin-bottom": "25px",
                             }, )], href='/'),
        ], width={'size': 2}),
        dbc.Col(html.H1(id ='titre',children='',
                        style={
                            'textAlign': 'center',
                            'color': 'white'
                        }),
                width={'size': 4, 'offset': 3}, ),
        dbc.Col(html.P(id='refresh', children='Last update  :  ' f'{date.today()}',
                       style={
                           'textAlign': 'right',
                           'color': 'orange',
                           'fontSize': 16}),
                width={'size': 2, 'offset': 0},
                ),
    ]),

    #
    html.Div([]),
    dbc.Row([html.Div([
        dbc.Col([

            dcc.Dropdown(id='stock', multi=True,
                         options=[{'label': x, 'value': x} for x in data['stock_type'].unique()],
                         placeholder="Select stock type",
                         className='form-dropdown',
                         style={'width': '200px'}
                         ),

            html.Br(style={'heigh': '500 px'}),
            html.Br(style={'heigh': '300 px'}),

            dcc.Dropdown(id='product', multi=True,
                         options=[{'label': x, 'value': x} for x in data['product_type'].unique()],
                         placeholder="Select a product",
                         className='form-dropdown',
                         style={'width': '200px'},
                         ),
            html.Br(style={'heigh': '500 px'}),
            html.Br(style={'heigh': '500 px'}),
            html.Br(style={'heigh': '300 px'}),
            html.Div(
                [
                    html.H5("Historical Data", className="display-4", style={'width': '150px'}),
                    html.Hr(style={'width': '200px', 'textAlign': 'center'}),
                    html.Br(style={'heigh': '300 px'}),
                    html.Br(style={'heigh': '300 px'}),
                    html.Ul(id="file-list",
                            children='',
                            style={'color': 'white'}),
                ],
                style={"max-width": "700px", 'color': 'white'},
                # className="card_container two columns"
            ),
        ], width={'size': 2, 'offset': 0}
        )
    ], className="card_container two columns"
    ),
        dbc.Col([
            html.P('Systémes Neufs',
                   style={
                       'textAlign': 'center',
                       'color': 'white',
                       'fontSize': 40}
                   ),
            html.Div([
                html.H4(children='Total Stock Neuf',
                        style={
                            'textAlign': 'center',
                            'color': 'white'}
                        ),
                html.P(id='q_n',
                       style={
                           'textAlign': 'center',
                           'color': 'green',
                           'fontSize': 50}
                       ),
            ], className="card_container six columns" "offset-by-one.column"),
            html.Div([
                html.H4(children='Cout du Stock neuf',
                        style={
                            'textAlign': 'center',
                            'color': 'white'}
                        ),
                html.P(id='v_n',  # f"{df_ko['quantite'].sum():,.0f}",
                       style={
                           'textAlign': 'center',
                           'color': 'green',
                           'fontSize': 50}
                       ),
            ], className="card_container six columns" "offset-by-one.column"),
            dt.DataTable(
                id='table',
                style_header=table_header_style,
                columns=[{'name': i, 'id': i} for i in tabel_colunm],
                # style_table={'height': '600px', 'overflowY': 'auto'}
                style_table={'height': '450px', 'overflowY': 'auto', "font-family": "Montserrat"},
                style_cell={'minWidth': '0px', 'maxWidth': '100px', 'width': '50px', 'fontSize': 14,
                            'backgroundColor': '#1f2c56', 'color': 'white',
                            'textAlign': 'center', "font-family": "Montserrat"}

            ),
        ], width={'size': 4, 'offset': 0},
        ),

        dbc.Col([
            html.P('Systémes Endommagés',
                   style={
                       'textAlign': 'center',
                       'color': 'white',
                       'fontSize': 40}
                   ),
            html.Div([
                html.H4(children='Total Stock KO',
                        style={
                            'textAlign': 'center',
                            'color': 'white'}
                        ),
                html.P(id='q_k',  # f"{df_ko['quantite'].sum():,.0f}",
                       style={
                           'textAlign': 'center',
                           'color': 'red',
                           'fontSize': 50}
                       ),
            ], className="card_container six columns" "offset-by-one.column"),
            html.Div([
                html.H4(children='Cout du Stock KO',
                        style={
                            'textAlign': 'center',
                            'color': 'white'}
                        ),
                html.P(id='v_k',  # f"{df_ko['quantite'].sum():,.0f}",
                       style={
                           'textAlign': 'center',
                           'color': 'red',
                           'fontSize': 50}
                       ),
            ], className="card_container six columns" "offset-by-one.column"),
            dt.DataTable(
                id='table2',
                style_header=table_header_style,
                columns=[{'name': i, 'id': i} for i in tabel_colunm],
                # style_table={'height': '600px', 'overflowY': 'auto'}
                style_table={'height': '450px', 'overflowY': 'auto', "font-family": "Montserrat"},
                style_cell={'minWidth': '0px', 'maxWidth': '100px', 'width': '50px', 'fontSize': 14,
                            'backgroundColor': '#1f2c56', 'color': 'white',
                            'textAlign': 'center', "font-family": "Montserrat"}

            ),
        ], width={'size': 5, 'offset': 0},
        )
    ]),
    html.Div(
        id='update-connection'
    )
])

@app.callback(
    Output('titre','children'),
    Output("file-list",'children'),
    Output('q_n', 'children'),
    Output('v_n', 'children'),
    Output('q_k', 'children'),
    Output('v_k', 'children'),
    [Input('url','pathname'),
    Input('product', 'value'),
    Input('stock', 'value')])
def update_table(pathname,select_product,select_stock):
    global tl
    global df_ko
    global df_neuf
    global UPLOAD_DIRECTORY



    p = pathname.split('/')[-1]
    titre = 'Inventaire Du Stock '+ p
    tl = telechargement(p)
    df_neuf = tl.df_neuf
    df_ko = tl.df_ko
    UPLOAD_DIRECTORY = tl.UPLOAD_DIRECTORY
    tl.job2()
    if not select_product and not select_stock:
        upload = tl.update_output()
        return titre,upload,f"{df_neuf['quantite'].sum():,.0f}   ",f"{df_neuf['Cout Total'].sum():,.0f} CFA" , f"{df_ko['quantite'].sum():,.0f} ", f"{df_ko['Cout Total'].sum():,.2f} CFA"
    elif select_product and not select_stock:
        tab1 = df_neuf[df_neuf['product_type'].isin(select_product)]
        tab2 = df_ko[df_ko['product_type'].isin(select_product)]
        upload = tl.update_output()
        return titre,upload , f"{tab1['quantite'].sum():,.0f} ",f"{tab1['Cout Total'].sum():,.0f}  CFA", f"{tab2['quantite'].sum():,.0f} ", f"{tab2['Cout Total'].sum():,.2f} CFA"
    elif select_stock and not select_product:
        tab1 = df_neuf[df_neuf['stock_type'].isin(select_stock)]
        tab2 = df_ko[df_ko['stock_type'].isin(select_stock)]
        upload = tl.update_output()
        return titre,upload, f"{tab1['quantite'].sum():,.0f} ", f"{tab1['Cout Total'].sum():,.0f} CFA", f"{tab2['quantite'].sum():,.0f}" , f"{tab2['Cout Total'].sum():,.2f}  CFA"
    else:
        tab1 = df_neuf[df_neuf['product_type'].isin(select_product) & df_neuf['stock_type'].isin(select_stock)]
        tab2 = df_ko[df_ko['product_type'].isin(select_product) & df_ko['stock_type'].isin(select_stock)]
        upload = tl.update_output()
        return titre,upload, f"{tab1['quantite'].sum():,.0f} ", f"{tab1['Cout Total'].sum():,.0f}  CFA" , f"{tab2['quantite'].sum():,.0f} ", f"{tab2['Cout Total'].sum():,.2f}  CFA"


@app.callback(
    Output('table', 'data'),
    Output('table2', 'data'),
    [Input('product', 'value'),
     Input('stock', 'value')])
def update_table(select_product,select_stock):
    if not select_product and not select_stock:
        data_table1 = df_neuf
        data_table2 = df_ko
    elif select_product and not select_stock:
        data_table1 = df_neuf[df_neuf['product_type'].isin(select_product)]
        data_table2 = df_ko[df_ko['product_type'].isin(select_product)]
    elif select_stock and not select_product:
        data_table1 = df_neuf[df_neuf['stock_type'].isin(select_stock)]
        data_table2 = df_ko[df_ko['stock_type'].isin(select_stock)]
    else:
        data_table1 = df_neuf[df_neuf['product_type'].isin(select_product) & df_neuf['stock_type'].isin(select_stock)]
        data_table2 = df_ko[df_ko['product_type'].isin(select_product) & df_ko['stock_type'].isin(select_stock)]

    table1 = data_table1.groupby(['product_type','etat','cost_price'],as_index=False).sum({'quantite':'sum','Cout Total':'sum'})
    table2 = data_table2.groupby(['product_type', 'etat', 'cost_price'],as_index=False).sum({'quantite':'sum','Cout Total':'sum'})
    return table1.to_dict('records'),table2.to_dict('records')


@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


if __name__ == "__main__":
    app.run_server(debug=True,dev_tools_ui=False,host='0.0.0.0', port=8881)