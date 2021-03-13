import pandas as pd
import matplotlib.pyplot as plt
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from dash.dependencies import Input, Output
import dash_table as dt

data_path = '/home/aims/PycharmProjects/Inventory_dashboard/data/stock_data.csv'
df = pd.read_csv(data_path)
print(df.head())

