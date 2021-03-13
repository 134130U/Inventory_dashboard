import os
from urllib.parse import quote as urlquote
# from flask import Flask, send_from_directory
# import dash
import dash_html_components as html


class telechargement(object):

    def __init__(self, country):
        self.country = country
        self.UPLOAD_DIRECTORY = "history/"+country+"/app_uploaded_files"

        if not os.path.exists(self.UPLOAD_DIRECTORY):
            os.makedirs(self.UPLOAD_DIRECTORY)

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
