import pandas as pd
import numpy as np
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from dash.dependencies import Input, Output
import dash_table as dt
import  psycopg2
from psycopg2 import Error
from datetime import date
from datetime import timedelta
import os
from flask import Flask, send_from_directory
import dash
import dash_html_components as html
from app_test import telechargement
import collect
from apscheduler.schedulers.background import BackgroundScheduler

tl = telechargement('niger')

UPLOAD_DIRECTORY = "history/niger/app_uploaded_files"


if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)



df = pd.read_csv('data/inventory.csv')
df['cost_price'] = df['cost_price'].round(2)
df = df[df['country']=='Niger']
df.fillna(0,inplace=True)

df_1 = df.groupby(['product_type','etat','cost_price', 'stock_type'],as_index=False).sum({'quantite':'sum'})
df_1['cost_price'] = df_1['cost_price'].round(2)
df_final = df_1.copy()
df_final = df_final[(df_final['etat'] =='waste')|(df_final['etat'] =='Neuf')]
df_final['Cout Total'] = (df_final['quantite']*df_final['cost_price']).round(2)
# df_final.rename(columns={'serial':'Quantite'},inplace=True)

df_ko = df_final[df_final['etat'] =='waste']
df_neuf = df_final[df_final['etat'] =='Neuf']


def job2():
    yesterday = date.today() - timedelta(days=1)
    if int(date.today().day) == 1:
        ko = UPLOAD_DIRECTORY +'/'+ yesterday.strftime('%B')+'_stock_ko.csv'
        neuf = UPLOAD_DIRECTORY +'/'+ yesterday.strftime('%B')+'_stock_neuf.csv'

        df_ko.to_csv(ko,index = False)
        df_neuf.to_csv(neuf,index = False)
        print('Files successfully downloaded')
        return ''


job2()

scheduler = BackgroundScheduler(daemon=True)
scheduler.add_job(func=collect.get_data, trigger="interval", minutes=60)
scheduler.add_job(func=job2, trigger="interval", minutes=7200)
scheduler.start()


tabel_colunm = ['product_type','etat','cost_price','quantite','Cout Total']


table_header_style = {
    "backgroundColor": "rgb(2,21,70)",
    "color": "white",
    "textAlign": "center",
    'fontSize': 20
}
server = Flask(__name__)
app = dash.Dash(server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])


@server.route("/download/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(UPLOAD_DIRECTORY, path, as_attachment=True)


app.layout = html.Div([
        dcc.Interval(
                id='interval-component',
                interval=144000*1000, # in milliseconds
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
                                 }, )], href='http://212.47.246.218:8888/'),
                ],width={'size': 2}),
            dbc.Col(html.H1('Inventaire Du Stock Niger',
                            style={
                                'textAlign': 'center',
                                'color': 'white'
                                }),
                width={'size': 4, 'offset': 3}, ),
            dbc.Col(html.P(id ='refresh' ,children='Last update  :  ' f'{date.today()}',
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

                    dcc.Dropdown(id = 'stock',multi=True,
                            options=[{'label':x, 'value':x} for x in df['stock_type'].unique()],
                            placeholder="Select stock type",
                            className='form-dropdown',
                            style={'width':'200px'}
                    ),

                    html.Br(style={'heigh': '500 px'}),
                    html.Br(style={'heigh': '300 px'}),

                    dcc.Dropdown(id = 'product',multi=True,
                        options=[{'label':x, 'value':x} for x in df['product_type'].unique()],
                        placeholder="Select a product",
                        className='form-dropdown',
                        style={'width':'200px'},
                    ),
                    html.Br(style={'heigh': '500 px'}),
                    html.Br(style={'heigh': '500 px'}),
                    html.Br(style={'heigh': '300 px'}),
                    html.Div(
                        [
                        html.H5("Historical Data", className="display-4",style={'width':'150px'}),
                            html.Hr(style={'width':'200px','textAlign': 'center'}),
                            html.Br(style={'heigh': '300 px'}),
                            html.Br(style={'heigh': '300 px'}),
                        html.Ul(id="file-list",
                                children=tl.update_output(),
                        style ={'color': 'white'}),
                        ],
                        style={"max-width": "700px", 'color': 'white'},
                        # className="card_container two columns"
                    ),
                ],width={'size': 2, 'offset':0}
                )
                    ],className="card_container two columns"
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
                            html.P(id='q_n',#f"{df_neuf['quantite'].sum():,.0f}",
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
                            html.P(id='v_n',#f"{df_ko['quantite'].sum():,.0f}",
                                   style={
                                       'textAlign': 'center',
                                       'color': 'green',
                                       'fontSize': 50}
                                   ),
                            ], className= "card_container six columns" "offset-by-one.column"),
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
                ],width={'size': 4,'offset':0},
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
                    html.P(id='q_k',#f"{df_ko['quantite'].sum():,.0f}",
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
                    html.P(id='v_k',#f"{df_ko['quantite'].sum():,.0f}",
                           style={
                               'textAlign': 'center',
                               'color': 'red',
                               'fontSize': 50}
                           ),
                    ], className= "card_container six columns" "offset-by-one.column"),
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
            ],width={'size': 5,'offset':0},
            )
        ]),
        html.Div(
            id='update-connection'
        )
])


@app.callback(
    Output('q_n', 'children'),
    Output('v_n', 'children'),
    Output('q_k', 'children'),
    Output('v_k', 'children'),
    [Input('product', 'value'),
     Input('stock', 'value')])
def update_table(select_product,select_stock):
    if not select_product and not select_stock:
        return f"{df_neuf['quantite'].sum():,.0f}   ",f"{df_neuf['Cout Total'].sum():,.0f} CFA" , f"{df_ko['quantite'].sum():,.0f} ", f"{df_ko['Cout Total'].sum():,.2f} CFA"
    elif select_product and not select_stock:
        tab1 = df_neuf[df_neuf['product_type'].isin(select_product)]
        tab2 = df_ko[df_ko['product_type'].isin(select_product)]
        return f"{tab1['quantite'].sum():,.0f} ",f"{tab1['Cout Total'].sum():,.0f}  CFA", f"{tab2['quantite'].sum():,.0f} ", f"{tab2['Cout Total'].sum():,.2f} CFA"
    elif select_stock and not select_product:
        tab1 = df_neuf[df_neuf['stock_type'].isin(select_stock)]
        tab2 = df_ko[df_ko['stock_type'].isin(select_stock)]
        return f"{tab1['quantite'].sum():,.0f} ", f"{tab1['Cout Total'].sum():,.0f} CFA", f"{tab2['quantite'].sum():,.0f}" , f"{tab2['Cout Total'].sum():,.2f}  CFA"
    else:
        tab1 = df_neuf[df_neuf['product_type'].isin(select_product) & df_neuf['stock_type'].isin(select_stock)]
        tab2 = df_ko[df_ko['product_type'].isin(select_product) & df_ko['stock_type'].isin(select_stock)]
        return f"{tab1['quantite'].sum():,.0f} ", f"{tab1['Cout Total'].sum():,.0f}  CFA" , f"{tab2['quantite'].sum():,.0f} ", f"{tab2['Cout Total'].sum():,.2f}  CFA"


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


@app.callback(
    Output('update-connection', 'children'),
    Output('refresh', 'children'),
    Input('interval-component', 'n_intervals'))
def update_connection(n):
    global df
    global df_1
    global df_final
    global df_ko
    global df_neuf

    if n >0 :
        df = pd.read_csv('data/inventory.csv')
        df['cost_price'] = df['cost_price'].round(2)
        df = df[df['country'] == 'Niger']
        df.fillna(0, inplace=True)

        df_1 = df.groupby(['product_type', 'etat', 'cost_price', 'stock_type'], as_index=False).sum({'quantite': 'sum'})
        df_1['cost_price'] = df_1['cost_price'].round(2)
        df_final = df_1.copy()
        df_final = df_final[(df_final['etat'] == 'waste') | (df_final['etat'] == 'Neuf')]
        df_final['Cout Total'] = (df_final['quantite'] * df_final['cost_price']).round(2)
        # df_final.rename(columns={'serial':'Quantite'},inplace=True)

        df_ko = df_final[df_final['etat'] == 'waste']
        df_neuf = df_final[df_final['etat'] == 'Neuf']

        collect.get_data()
        yesterday = date.today() - timedelta(days=1)
        if int(date.today().day) == 1:
            ko = UPLOAD_DIRECTORY + '/' + yesterday.strftime('%B') + '_stock_ko.csv'
            neuf = UPLOAD_DIRECTORY + '/' + yesterday.strftime('%B') + '_stock_neuf.csv'

            df_ko.to_csv(ko, index=False)
            df_neuf.to_csv(neuf, index=False)

        print('data have been updated')

        return ''


if __name__ == '__main__':
    app.run_server(debug=True,dev_tools_ui=False, host='0.0.0.0', port=8085)
