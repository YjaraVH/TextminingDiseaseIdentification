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
        # Selected file
        file = request.files['file']

        # For further upgrades (make a difference between excel files
        # with only new patients or new metabolites and new patients
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
        # Checks file
        if filename == '':
            error = "Filename is empty"
            return render_template("Homepage.html", error=error)
        if filename.endswith(".xlsx") == False:
            error = "This file is not allowed"
            return render_template("Homepage.html", error=error)
        else:
            file = request.form['org_pro']
            # To obtain all information in file
            data = fileReader.readFile(file)
            # To obtain metabolieten for textmining
            metabolieten = fileReader.getMetabolites(data)
            # Start textmining
            textmining2.start_textmining(metabolieten)
            return render_template("Homepage.html", error="")
    else:
        return render_template("Homepage.html")

@app.route('/About',methods=["POST", "GET"])
def info():
    return render_template("About.html")

@app.route('/Resultspatient',methods=["POST", "GET"])
def resultspatient():
    # To obtain all patients (names)
    patients = get_patients()

    if request.method == "POST":
        # Obtain positive and negative z-score threshold
        zscoreP = str(request.form.getlist('zscorePos')).replace("[","").replace("]","").replace("'","")
        zscoreN = str(request.form.getlist('zscoreNeg')).replace("[","").replace("]","").replace("'","")

        # Obtain patient ID: dropdown menu
        selected_patient = request.form.get('patientC')

        # Obtain patient ID: text
        answer_patient = request.form.get('answer')
        print(f"patient:{selected_patient}, z-scorep:{zscoreP}, z-scoren:{zscoreN}")
        if selected_patient == "":
            patient = answer_patient
        else:
            patient = selected_patient
        print(patient)

        # Obtain graph
        graph = sunburstplot.get_figure(patient,zscoreN,zscoreP)
        return render_template("Resultspatient.html",patients=patients)
    else:
        return render_template("Resultspatient.html", patients=patients)

@app.route('/ResultsGlobal',methods=["POST", "GET"])
def resultsGlobal():
    # Obtain all metabolites (names)
    metabolieten = get_metabolieten()
    if request.method == "POST":
        # Obtain chosen metabolite
        metaboliet = request.form.get('Metabolites')
        if metaboliet=="":
            metaboliet = request.form.get('answer')

        # Obtain name, origin_name, hmbd_code, fluids_name and description from
        # metabolite (metaboliet)
        output = info_meta_ophalen(metaboliet)

        # Headers for table in ResultsGlobal.html
        headers = ["name", "origin_name", "hmbd_code", "fluids_name"]

        # Gene(s) related to give metabolite (metaboliet)
        genen = genen_ophalen(metaboliet)

        # Disease(s) related to give metabolite (metaboliet)
        ziektes = ziekte_ophalen(metaboliet)

        return render_template("ResultsGlobal.html",Metabolites=metabolieten, output=output, headers=headers,genes=genen,ziektes=ziektes)
    else:
        return render_template("ResultsGlobal.html",Metabolites=metabolieten)

@app.route('/Results',methods=["POST", "GET"])
def results():
    if request.method == "POST":
        # Order descending or ascending (queri database)
        order_desc_asc = request.form['order']

        # Obtain positive and negative z-score threshold
        z_score_neg = request.form['zscoreNeg']
        z_score_pos = request.form['zscorePos']

        # Obtain patient iD
        search = request.form.get('answer')

        # Obtain metabolites, z-score and diseases related to metabolite
        # from patient
        output = get_patient_info(z_score_neg, z_score_pos, order_desc_asc, search)
        return render_template("Results.html", output=output)
    else:
        return render_template("Results.html")

@app.errorhandler(404)
def not_found(e):
    return render_template("errorPage.html")

def get_metabolieten():
    """ To obtain a list with all metabolites (names)

    :return: list- with metabolites
    """
    cursor = conn.cursor()
    postgre = ("""SELECT name FROM metabolieten;""")
    cursor.execute(postgre)
    result = cursor.fetchall()
    metabolieten = []
    metabolieten.append("")
    for i in result:
        meta = str(i)
        metabolieten.append(meta[2:len(meta)-3])
    return metabolieten

def get_patients():
    """ To obtain a list with all patients (ids)

    :return: list- with patients
    """
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

def info_meta_ophalen(search):
    """ To obtain name, origin_name, hmbd_code, fluids_name and description
    from metabolite (search)

    :param search: str- metabolite
    :return: list- with name, origin_name, hmbd_code, fluids_name and
                description from metabolite (metaboliet)
    """
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
    for a in result:
        row = []
        for item in a:
            # Make item "" if there are no results
            if item == "; \n    " or item == ";":
                item = ""
            row.append(item)
        info_met.append(row)
    return info_met

def genen_ophalen(search):
    """ Obtain gene(s) related to give metabolite (search)

    :param search: str- metabolite (name)
    :return: list- gene(s) (and count)
    """
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

def ziekte_ophalen(search):
    """ Obtain disease(s) related to give metabolite (search)

    :param search: str- metabolite (name)
    :return: list- disease(s) (and count)
    """
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

def get_patient_info(z_score_neg,z_score_pos,order_desc_asc,search):
    """To obtain metabolites, z-score and diseases related to metabolite
       from patient

    :param z_score_neg: str- negative z-score threshold
    :param z_score_pos: str- positive z-score threshold
    :param order_desc_asc: str- ascending or descending
    :param search: str- patient id
    :return: list- with metabolites, z-score and diseases related to metabolite
       from patient
    """
    cursor = conn.cursor()
    postgre = ("""select name,z_score,disease,count,mesh_code
from patients
join z_scores zs on patients.id_patient = zs.patients_id_patient
join metabolieten m on m.id_metaboliet = zs.metabolieten_id_metaboliet
join metabolieten_pubom mp on m.id_metaboliet = mp.metabolieten_id_metaboliet
join pub_disease_pubom pdp on mp.pubom_id_pum_om = pdp.pubom_id_pum_om
join pub_disease pd on pd.id_article = pdp.pub_disease_id_article
         WHERE id_patient like'{}%' AND (z_score < {} OR z_score > {})
         ORDER BY z_score {};""").format(search,z_score_neg,z_score_pos,order_desc_asc)
    cursor.execute(postgre)
    result = cursor.fetchall()

    dict_test = {}
    for i in result:
        if i[0] in dict_test:
            listt = dict_test[i[0]][1]
            print(listt)
        else:
            listt = [float(i[1]),[list(i[2:5])]]
            dict_test[str(i[0])] = listt
    return dict_test

def get_email(reciever):
    """ Unfinished function, if finished sends email to reciever/client/user
    to alert them that the results are ready (textmining is finished)

    :param reciever: str- email of client/user
    """
    import smtplib

    host = ""
    server = smtplib.SMTP(host)
    FROM = ""
    TO = reciever
    MSG = "Subject: textminingDiseaseIdentification\n\nResults are ready!"
    server.sendmail(FROM, TO, MSG)

    server.quit()
    print("Email Send")

if __name__ == '__main__':
    app.run()
