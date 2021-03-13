import pandas as pd
import  psycopg2
from psycopg2 import Error

def get_data():

    # Connection to oolusolar base
    sql_file = open('data/inventory.sql')
    sql_text = sql_file.read()
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
    data.to_csv('data/inventory.csv', index=False)
    cursor.close()
    connection.close()

    return ''
