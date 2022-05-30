import io
import time

from flask import Flask,request,render_template
from Bio import Entrez
import mysql.connector

conn = mysql.connector.connect(
    host="ensembldb.ensembl.org",
    user="anonymous",
    database="homo_sapiens_core_95_38"
)

app = Flask(__name__)

@app.route('/',methods=["POST", "GET"])
def start():
    return render_template("start.html")

@app.route('/Homepage',methods=["POST", "GET"])
def hello_world():
    if request.method == "POST":
        if 'file' not in request.files:
            error = "File not selected"
            return render_template("Homepage.html", error=error)
        file = request.files['file']
        email = request.form.get("email","")
        print(email)
        filename = file.filename
        print(filename)
        if email == "":
            print("no email is needed")
        else:
            print(email)
        if filename == '':
            error = "Filename is empty"
            return render_template("Homepage.html", error=error)
        if filename.endswith(".xlsx") == False:
            error = "This file is not allowed"
            return render_template("Homepage.html", error=error)
        else:
            return render_template("Homepage.html", error="")
    else:
        return render_template("Homepage.html")

@app.route('/About',methods=["POST", "GET"])
def info():
    return render_template("About.html")

@app.route('/Results2',methods=["POST", "GET"])
def results2():
    return render_template("Results2.html")

@app.route('/Results',methods=["POST", "GET"])
def results():
    if request.method == "POST":
        mainOption = request.form['org_pro']
        supOpt1 = request.form.getlist('z-scores')
        supOpt2 = request.form.getlist('patients')
        supOpt3 = request.form.getlist('diseases')
        supOpt4 = request.form.getlist('articles')
        supOpt5 = request.form.getlist('meta')
        z_score_neg = request.form['zscoreNeg']
        z_score_pos = request.form['zscorePos']

        # Zet de gemaakte keuzes in een lijst en maakt er vervolgens een string van via de functie opbouw_keuzes
        keuzes = ["".join(supOpt2), "".join(supOpt3), "".join(supOpt5), "".join(supOpt1),
                  "".join(supOpt4)]
        keuze = opbouw_keuzes(keuzes)
        search = request.form.get('answer')
        output = search_queri(mainOption, keuzes,z_score_neg,z_score_pos,search)
        print(keuze.split(",")) #["getal","type","analysis_id","gene_id"]

        return render_template("Results.html",output=output,keuze=keuze.split(","),answer=search)
    else:
        return render_template("Results.html")

@app.errorhandler(404)
def not_found(e):
    return render_template("errorPage.html")

def search_queri(mainOpt,keuzes,neg,pos,zoek):
    if keuzes == "":
        keuzes = "*"

    mainOpt = "gene"
    keuzes = "gene_id,biotype,analysis_id,gene_id"
    cursor = conn.cursor()
    cursor = conn.cursor()
    sql = f"select {keuzes} from {mainOpt} " \
          f"limit 10"
#f"where z_score < {neg} or z_score > {pos}" \
    # sql = f"select {zoek} from blast where {keuze_2} like '%{orga}%'"
    cursor.execute(sql)
    row = cursor.fetchall()
    regels = []
    for item in list(row):
        # regel = str(item).strip("'()''").replace(",", " ").replace("'", "")
        # regels.append(regel[0:len(regel)])
        regels.append(item)
    conn.commit()
    print(regels)
    return regels

def get_email(reciever):
    import smtplib
    # SERVER = "localhost"
    FROM = 'monty@python.com'
    msg = "lets test this"
    # Send the mail
    smtp = smtplib.SMTP('localhost')
    smtp.sendmail(FROM, reciever, msg)
    smtp.quit()

def opbouw_keuzes(keus):
    search = ""
    for item in keus:
        if item != "":
            search = search + str(item) + ","
    return search[0:len(search) - 1]

if __name__ == '__main__':
    app.run()
