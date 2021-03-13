import pandas as pd
from datetime import date
import schedule
import  psycopg2
from psycopg2 import Error

# print()
# sql_file = open('../data/inventory.sql')
#
# sql_text = sql_file.read()

data_path = '/home/aims/PycharmProjects/Inventory_dashboard/data/stock_data.csv'
data = pd.read_csv(data_path)
df_ko = data[data['etat'] == 'Endommagé']
df_neuf = data[data['etat'] == 'Neuf']

def job():
        # ko = 'historic/ko'+date.today().strftime('%B')+'.csv'
        # neuf = 'historic/neuf'+date.today().strftime('%B')+'.csv'
        #
        # pd.to_csv(ko,index = False)
        # pd.to_csv(neuf,index = False)


        print('monthly downloading successfull')

    # actual job body

schedule.every(10).seconds.do(job)
