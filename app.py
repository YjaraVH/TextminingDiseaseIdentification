import io
import time

import psycopg2
from flask import Flask,request,render_template
from Bio import Entrez
import mysql.connector
import plotly.express as px
import psycopg2
import sunburstplot
import fileReader
import textmining2


conns = mysql.connector.connect(
    host="ensembldb.ensembl.org",
    user="anonymous",
    database="homo_sapiens_core_95_38"
)

conn = psycopg2.connect(host="postgres.biocentre.nl", user="BI2_PG1", password="blaat1234",
                            database="bio_jaar_2_pg_1", port="5900")

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
        tijd = request.form['fileT']

        # Name of file with metabolites, z-scores, patients etc
        filename = file.filename

        """ For further upgrades
        email = request.form.get("email","")
        if email == "":
            print("no email is needed")
        else:
            print(email)
            get_email(email)
        """

        if filename == '':
            error = "Filename is empty"
            return render_template("Homepage.html", error=error)
        if filename.endswith(".xlsx") == False:
            error = "This file is not allowed"
            return render_template("Homepage.html", error=error)
        else:
            #file request.form['org_pro']
            #to obtain all information in file
            #data = fileReader.readFile(file)
            #to obtain metabolieten for textmining
            #metabolieten = fileReader.getMetabolites(data)
            #textmining2.get_ids_all_pubmed(metabolieten,True)
            return render_template("Homepage.html", error="")
    else:
        return render_template("Homepage.html")

@app.route('/About',methods=["POST", "GET"])
def info():
    return render_template("About.html")

@app.route('/Resultspatient',methods=["POST", "GET"])
def resultspatient():
    #patients = ["piet","jan","iphone"]                                         #Needs query to get all the patient ID's
    patients = get_patients()
    if request.method == "POST":
        patient = ""
        zscoreP = str(request.form.getlist('zscorePos')).replace("[","").replace("]","").replace("'","")
        zscoreN = str(request.form.getlist('zscoreNeg')).replace("[","").replace("]","").replace("'","")

        selected_patient = request.form.get('patientC')
        answer_patient = request.form.get('answer')
        print(f"patient:{selected_patient}, z-scorep:{zscoreP}, z-scoren:{zscoreN}")
        if selected_patient == "":
            patient = answer_patient
        else:
            patient = selected_patient
        print(patient)
        print("tot hier werkt het wel")

        graph = sunburstplot.get_figure(patient,zscoreN,zscoreP)
        return render_template("Resultspatient.html",patients=patients,grah=graph)
    else:
        return render_template("Resultspatient.html", patients=patients,grah="")

@app.route('/ResultsGlobal',methods=["POST", "GET"])
def resultsGlobal():
    metabolieten = get_metabolieten()
    if request.method == "POST":
        metaboliet = request.form.get('Metabolites')
        if metaboliet=="":
            metaboliet = request.form.get('answer')
        print(metaboliet)
        output = info_meta_ophalen(metaboliet)
        headers = ["name", "origin_name", "hmbd_code", "fluids_name"]
        genen = genen_ophalen(metaboliet)
        print(genen)
        ziektes = ziekte_ophalen(metaboliet)
        print(ziektes)
        return render_template("ResultsGlobal.html",Metabolites=metabolieten, output=output, headers=headers,genes=genen,ziektes=ziektes)
    else:
        return render_template("ResultsGlobal.html",Metabolites=metabolieten)

@app.route('/Results',methods=["POST", "GET"])
def results():
    if request.method == "POST":
        order_desc_asc = request.form['order']

        z_score_neg = request.form['zscoreNeg']
        z_score_pos = request.form['zscorePos']
        # Name metabolite or patient iD
        search = request.form.get('answer')
        output = get_patient_info(z_score_neg, z_score_pos, order_desc_asc, search)
        return render_template("Results.html", output=output)
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
    return regels

def get_metabolieten():   #moet conn and cursor meekrijgen
    cursor = conn.cursor()
    postgre = ("""SELECT name FROM metabolieten;""")
    cursor.execute(postgre)
    result = cursor.fetchall()
    patients = []
    patients.append("")
    for i in result:
        meta = str(i)
        patients.append(meta[2:len(meta)-3])
    return patients

def get_patients():   #moet conn and cursor meekrijgen
    cursor = conn.cursor()
    postgre = ("""SELECT id_patient FROM patients;""")
    cursor.execute(postgre)
    result = cursor.fetchall()
    patients = []
    patients.append("")
    for i in result:
        patient = str(i)
        patients.append(patient[2:len(patient)-3])
    return patients

def info_meta_ophalen(search):  #name weghalen, overweeg discription weg te halen want dat ziet er niet goed, misschien iets ander toevoegen?
    cursor = conn.cursor()
    postgre = ("""SELECT name,origin_name,hmbd_code,fluids_name,description  FROM metabolieten
     JOIN origins_metabolieten ON metabolieten.id_metaboliet=origins_metabolieten.metabolieten_id_metaboliet
     JOIN origins ON origins_metabolieten.origins_id_orgins= origins.id_orgins
     JOIN relevance ON metabolieten.relevance_id_relevance=relevance.id_relevance
     JOIN z_scores ON metabolieten.id_metaboliet=z_scores.metabolieten_id_metaboliet
     join fluids f on metabolieten.id_fluids = f.id_fluids
     WHERE name like'{}%'
    limit 1;""").format(search)

    cursor.execute(postgre)
    result = cursor.fetchall()

    info_met = []
    for a in result: #"; \n    "
        row = []
        for item in a:
            if item == "; \n    " or item == ";":
                item = ""
            row.append(item)
        info_met.append(row)
    return info_met

def info_patient_ophalen(z_score_neg,z_score_pos,order_desc_asc,search):
    print(search)
    print(f"zscoreN:{z_score_neg}, zscoreP:{z_score_pos}, order:{order_desc_asc}, patient:{search}")
    cursor = conn.cursor()
    postgre = ("""SELECT name, z_score FROM metabolieten
         JOIN z_scores ON metabolieten.id_metaboliet=z_scores.metabolieten_id_metaboliet
         JOIN patients ON z_scores.patients_id_patient=patients.id_patient
         WHERE id_patient like'{}%' AND (z_score < {} OR z_score > {})
         ORDER BY z_score {} limit 5;""").format(search,z_score_neg,z_score_pos,order_desc_asc)        #heeft voor nu even een limit anders duurt het erg lang
    cursor.execute(postgre)
    result = cursor.fetchall()
    info_pat = []
    for i in result:  #Wat aangepast nu doet deze het ook
        info_pat.append(i)
    #z-score is nog steeds heel vreemd, denk bijna dat er echt iets niet moet kloppen!!!
    return info_pat

def genen_ophalen(search):  #name weghalen, overweeg discription weg te halen want dat ziet er niet goed, misschien iets ander toevoegen?
    cursor = conn.cursor()
    postgre = (f"""select genes,count
from metabolieten
join metabolieten_pubom mp on metabolieten.id_metaboliet = mp.metabolieten_id_metaboliet
join pubom p on mp.pubom_id_pum_om = p.id_pum_om
join pub_disease_pubom pdp on p.id_pum_om = pdp.pubom_id_pum_om
join pubom_pub_genes ppg on p.id_pum_om = ppg.pubom_id_pum_om
join pub_genes pg on ppg.pub_genes_id_artikel = pg.id_artikel
where name='{search }'
group by genes, count;""")

    cursor.execute(postgre)
    result = cursor.fetchall()

    info_met = []
    for a in result:
        info_met.append(a)
    return info_met

def ziekte_ophalen(search):  #name weghalen, overweeg discription weg te halen want dat ziet er niet goed, misschien iets ander toevoegen?
    cursor = conn.cursor()
    postgre = (f"""select disease,count,mesh_code
from metabolieten
join metabolieten_pubom mp on metabolieten.id_metaboliet = mp.metabolieten_id_metaboliet
join pubom p on mp.pubom_id_pum_om = p.id_pum_om
join pub_disease_pubom pdp on p.id_pum_om = pdp.pubom_id_pum_om
join pub_disease pd on pdp.pub_disease_id_article = pd.id_article
where name='{search}'
group by disease, count,mesh_code
order by count desc;""")

    cursor.execute(postgre)
    result = cursor.fetchall()

    info_met = []
    for a in result:
        info_met.append(a)
    return info_met

def get_patient_info(z_score_neg,z_score_pos,order_desc_asc,search):   #P1005.1_Zscore
    cursor = conn.cursor()
    postgre = ("""select name,z_score,disease,count,mesh_code
from patients
join z_scores zs on patients.id_patient = zs.patients_id_patient
join metabolieten m on m.id_metaboliet = zs.metabolieten_id_metaboliet
join metabolieten_pubom mp on m.id_metaboliet = mp.metabolieten_id_metaboliet
join pub_disease_pubom pdp on mp.pubom_id_pum_om = pdp.pubom_id_pum_om
join pub_disease pd on pd.id_article = pdp.pub_disease_id_article
         WHERE id_patient like'{}%' AND (z_score < {} OR z_score > {})
         ORDER BY z_score {};""").format(search,z_score_neg,z_score_pos,order_desc_asc)   # heeft voor nu even een limit anders duurt het erg lang
    cursor.execute(postgre)
    result = cursor.fetchall()
    info_pat = []
    print(list(result))
    d = []

    dict_test = {}
    for i in result:
        if i[0] in dict_test:
            listt = dict_test[i[0]][1]
            print(listt.append(i[2:5]))
            #dict_test[i[0]] = [float(i[1])]
        else:
            listt = [float(i[1]),[list(i[2:5])]]
            dict_test[str(i[0])] = listt
    return dict_test

def get_email(reciever):
    import smtplib

    host = "postgres.biocentre.nl"
    server = smtplib.SMTP(host)
    FROM = "Y.Hopmans@student.han.nl"
    TO = reciever
    MSG = "Subject: Test email python\n\nBody of your message!"
    server.sendmail(FROM, TO, MSG)

    server.quit()
    print("Email Send")

def opbouw_keuzes(keus):
    search = ""
    for item in keus:
        if item != "":
            search = search + str(item) + ","
    return search[0:len(search) - 1]

if __name__ == '__main__':
    app.run()
