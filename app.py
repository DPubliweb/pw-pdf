import pandas as pd
from flask import Flask, flash, request, redirect, render_template, send_file, url_for, make_response, after_this_request, session
from fileinput import filename
from werkzeug.utils import secure_filename
import os
from datetime import datetime


app = Flask(__name__)

@app.route("/")
def home():
  return render_template('index.html')

@app.route("/pdf_upload", methods=['GET','POST'])
def pdf_creator():
    if request.method == "POST":
        file = request.files["file"]
        if file.filename.endswith(".csv"):
            data = pd.read_csv(file)
        elif file.filename.endswith(".xlsx"):
            data = pd.read_excel(file)
        elif file.filename.endswith(".txt"):
            data = pd.read_csv(file, sep=",")
        else:
            return "File format not supported"
        return render_template("pdf.html", date=datetime.now().strftime("%d-%m-%Y"), data=data.to_html(index=False, justify='center'))
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host = '0.0.0.0',port = 8080, debug = False)
