import os
from urllib.parse import quote as urlquote
# from flask import Flask, send_from_directory
import pandas as pd
import dash_html_components as html
import pathlib
from datetime import date
from datetime import timedelta



class telechargement(object):

    def __init__(self, country):
        self.country = country
        self.UPLOAD_DIRECTORY = "history/"+country.lower()+"/app_uploaded_files"
        self.PATH = pathlib.Path(__file__).parent
        self.DATA_PATH = self.PATH.joinpath("../Inventory_dashboard/data").resolve()
        self.data = pd.read_csv(self.DATA_PATH.joinpath("inventory.csv"))
        self.data['Cout Total'] = (self.data['quantite'] * self.data['cost_price']).round(2)

        self.df_ko = self.data[(self.data['etat'] == 'Endommagé') & (self.data['country'] == self.country)]
        self.df_neuf = self.data[(self.data['etat'] == 'Neuf') & (self.data['country'] == self.country)]

        if not os.path.exists(self.UPLOAD_DIRECTORY):
            os.makedirs(self.UPLOAD_DIRECTORY)

    def job2(self):
        yesterday = date.today() - timedelta(days=1)
        if int(date.today().day) == 1:

            self.df_ko.to_csv(self.UPLOAD_DIRECTORY + '/' + yesterday.strftime('%B') + '_stock_ko.csv', index=False)
            self.df_neuf.to_csv(self.UPLOAD_DIRECTORY + '/' + yesterday.strftime('%B') + '_stock_neuf.csv', index=False)
            print('Files successfully downloaded')
            return ''



    def uploaded_files(self):
        """List the files in the upload directory."""
        files = []
        for filename in os.listdir(self.UPLOAD_DIRECTORY):
            path = os.path.join(self.UPLOAD_DIRECTORY, filename)
            if os.path.isfile(path):
                files.append(filename)
        return files

    def file_download_link(self, filename):
        """Create a Plotly Dash 'A' element that downloads a file from the app."""
        location = "/download/{}".format(urlquote(filename))
        return html.A(filename, href=location)

    def update_output(self):
        """Save uploaded files and regenerate the file list."""

        files = self.uploaded_files()
        if len(files) == 0:
            return [html.Li("No files yet!")]
        else:
            return [html.Li(self.file_download_link(filename),style ={'color': 'orange'}) for filename in files]
print()
