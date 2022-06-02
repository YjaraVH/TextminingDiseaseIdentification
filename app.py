import io
import time

from flask import Flask,request,render_template
from Bio import Entrez
import mysql.connector
import fileReader
import textmining2

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
            #to obtain all information in file

           ##### data = fileReader.readFile(file)

            # to obtain metabolieten for textmining


            ######metabolieten = fileReader.getMetabolites(data)
            ######textmining2.get_ids_all_pubmed(metabolieten,True)
            return render_template("Homepage.html", error="")
    else:
        return render_template("Homepage.html")

@app.route('/About',methods=["POST", "GET"])
def info():
    return render_template("About.html")

@app.route('/Resultspatient',methods=["POST", "GET"])
def resultspatient():
    patients = ["piet","jan","iphone"]                                         #Needs query to get all the patient ID's
    if request.method == "POST":
        patient = request.form.get('patientC')
        zscoreP = request.form.getlist('zscorePos')
        zscoreN = request.form.getlist('zscoreNeg')
        print(f"patient:{patient}, z-scorep:{zscoreP}, z-scoren:{zscoreN}")
        return render_template("Resultspatient.html",patients=patients)
    else:
        return render_template("Resultspatient.html", patients=patients)

@app.route('/ResultsGlobal',methods=["POST", "GET"])
def resultsGlobal():
    metabolieten = ["dirk","jan","iphone"]                                         #Needs query to get all the metabolietes names
    if request.method == "POST":
        metaboliet = request.form.get('Metabolites')
        print(f"patient:{metaboliet}")
        return render_template("ResultsGlobal.html",Metabolites=metabolieten)
    else:
        return render_template("ResultsGlobal.html",Metabolites=metabolieten)

@app.route('/Results',methods=["POST", "GET"])
def results():
    if request.method == "POST":
        # Patient or Metabolite
        mainOption = request.form['org_pro']
        order_desc_asc = request.form['order']

        # Name metabolite or patient iD
        search = request.form.get('answer')
        if mainOption == "patient":
            z_score_neg = request.form['zscoreNeg']
            z_score_pos = request.form['zscorePos']
                                                                                # functie oproepen queri met alle nodige informatie, zie header tabel, onderstaande is een functie voor mezelf om te checken of alles werkt
            print(f"main otion:{mainOption}, zscoreNeg:{z_score_neg}, zscorePos:{z_score_pos}, id_patient:{search}, order:{order_desc_asc}")
            output = search_queri(mainOption,z_score_neg, z_score_pos,6)
            headers = ["Metabolite","Z-score","Disease(s)"]                     # Zou nice zijn als er per disease een top 3 gevonden ziektes kan woorden, nog beter ook met score, kan ik nog een colomn voor bij maken. Laat maar weten
        else:
            order_by = request.form['order_type']
            print(f"mainOption:{mainOption}, order_by:{order_by}, metaboliteName:{search}, order:{order_desc_asc}")
                                                                                # functie oproepen queri met alle nodige informatie, zie header tabel, onderstaande is een functie voor mezelf om te checken of alles werkt
            output = search_queri(mainOption,2,3,9)
            headers = ["Name","Origin","Description","HMBD_code","Relevance"]

        return render_template("Results.html", output=output, headers=headers)
    else:
        return render_template("Results.html")

@app.errorhandler(404)
def not_found(e):
    return render_template("errorPage.html")

def search_queri(mainOpt,keuzes,neg,pos):
    if keuzes == "":
        keuzes = "*"

    mainOpt = "gene"
    keuzes = "gene_id,biotype,analysis_id"
    cursor = conn.cursor()
    cursor = conn.cursor()
    sql = f"select {keuzes} from {mainOpt} " \
          f"limit 50"
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
