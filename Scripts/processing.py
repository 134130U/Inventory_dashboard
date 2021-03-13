import pandas as pd
from datetime import date
from datetime import timedelta
import  psycopg2
from psycopg2 import Error

def update_connection(n):
    if n > 0:
        sql_file = open('../data/inventory.sql')
        sql_text = sql_file.read()
        # Connection to oolusolar database
        try:
            connection = psycopg2.connect(user='chartio_read_only_user',
                                          password='2ZVF01USUWTKV3K9JJFY',
                                          host='oolu-main-postgresql.cfa4plgxjs0u.eu-central-1.rds.amazonaws.com',
                                          port='5432',
                                          database='oolusolar_analytics')
            cursor = connection.cursor()
            cursor.execute("SELECT version();")
            record = cursor.fetchone()
            print('You are Successfully connected to - ', record, '\n')
        except (Exception, Error) as error:
            print(" Connection failed, try again", error)
            cursor.close()

        data = pd.read_sql_query(sql_text, connection)
        data.to_csv('data/inventory.csv',index= False)
        cursor.close()
        connection.close()
        print('data have been updated')

        return ''


# path = 'history/app_uploaded_files/'
#
#
# def job(df_ko,df_neuf):
#     yesterday = date.today() - timedelta(days=1)
#     if int(date.today().day) == 1:
#         ko = path + yesterday.strftime('%B') + '_stock_ko.csv'
#         neuf = path + yesterday.strftime('%B') + '_stock_neuf.csv'
#
#         df_ko.to_csv(ko, index=False)
#         df_neuf.to_csv(neuf, index=False)
#         print('Files successfully downloaded')
#         return 'hello babou'