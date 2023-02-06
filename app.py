import pandas as pd
from flask import Flask, flash, request, redirect, render_template, send_file, url_for, make_response, after_this_request, session
import pdfkit
from fileinput import filename
from werkzeug.utils import secure_filename
import os
from datetime import datetime


app = Flask(__name__)
app.secret_key = "12345678"
styles = [
    dict(selector="tr:hover",
                props=[("background", "#f4f4f4")]),
    dict(selector="th", props=[("color", "#fff"),
                               ("border", "1px solid #eee"),
                               ("padding", "12px 35px"),
                               ("border-collapse", "collapse"),
                               ("background", "#535353"),
                               ("text-transform", "uppercase"),
                               ("font-size", "18px"),
                               ("text-align", "center")
                               ]),
    dict(selector="td", props=[("color", "#999"),
                               ("border", "1px solid #eee"),
                               ("padding", "12px 35px"),
                               ("border-collapse", "collapse"),
                               ("font-size", "15px"),
                               ("text-align", "center")
                               ]),
    dict(selector="table", props=[
                                    ("font-family" , 'Arial'),
                                    ("margin" , "25px auto"),
                                    ("border-collapse" , "collapse"),
                                    ("border" , "1px solid #eee"),
                                    ("border-bottom" , "2px solid #00cccc"),   
                                    ("width", "100%")                                 
                                      ]),
    dict(selector="caption", props=[("caption-side", "bottom")])
]


@app.route("/")
def home():
  return render_template('index.html')

@app.route("/pdf_upload", methods=['GET','POST'])
def pdf_creator():
    if request.method == "POST":
        file = request.files["file"]
        civilite =  request.form['civilite']
        name = request.form['name']
        societe = request.form['societe']
        session['civilite'] = civilite
        session['name'] = name
        session['societe'] = societe
        if file.filename.endswith(".csv"):
            data = pd.read_csv(file)
        elif file.filename.endswith(".xlsx"):
            data = pd.read_excel(file)
        elif file.filename.endswith(".txt"):
            data = pd.read_csv(file, sep=",")
        else:
            return "File format not supported"
        
        data = data.style.set_table_styles(styles).render() 
        session['data'] = data
 

        return render_template("pdf.html", date=datetime.now().strftime("%d-%m-%Y"), data=data, civilite=civilite, name=name, societe=societe)
    return render_template("index.html")

@app.route("/pdf_download")
def pdf_download():
    data = session.get('data')
    civilite = session.get('civilite')
    name = session.get('name')
    societe = session.get('societe')
    if not data:
        return "No data to download"
    
    html = render_template("pdf.html", date=datetime.now().strftime("%d-%m-%Y"), data=data,  civilite=civilite, name=name, societe=societe)
    pdf = pdfkit.from_string(html, False)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=devis_{}.pdf'.format(datetime.now().strftime("%d-%m-%Y"))
    return response


if __name__ == "__main__":
    app.run(host = '0.0.0.0',port = 8080, debug = False)
