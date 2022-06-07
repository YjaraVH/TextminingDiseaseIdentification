import psycopg2
'''
    Filename: visualisatie.py
    Authors: Nienke Gertsen
    Date created: 6/06/2022
'''


def info_patient_ophalen(cursor):
    """
    haalt informatie uit de database op die het verband weergeeft tussen de patienten,
    metabolieten, ziektes gevonden m.b.v. pubtator die gekoppeld kunnen worden aan bepaalde
    metabolieten en tot slot de z-score die zegt over de waarschijnlijkheid dat een bepaalde
    metaboliet verantwoordelijk is voor een bepaalde ziekte.
    :param cursor: cursor.
    """
    # default waarde om te testen
    value = -100
    value2 = 100
    patient_name = "P1002.1_Zscore"
    fil = "desc"
    # definieert de query voor het ophalen.
    postgre = ("""SELECT id_patient, name, disease, z_score FROM metabolieten
      JOIN z_scores ON metabolieten.id_metaboliet=z_scores.metabolieten_id_metaboliet
      JOIN patients ON z_scores.patients_id_patient=patients.id_patient
      JOIN metabolieten_pubom mp ON metabolieten.id_metaboliet = mp.metabolieten_id_metaboliet
      JOIN pubom ON mp.pubom_id_pum_om = pubom.id_pum_om
      JOIN pub_disease_pubom pdp ON pubom.id_pum_om = pdp.pubom_id_pum_om
      JOIN pub_disease ON pdp.pub_disease_id_article = pub_disease.id_article
      WHERE id_patient='{}' AND (z_score < {} OR z_score > {})
      ORDER BY z_score {}
      LIMIT 10;""").format(patient_name, value, value2, fil)
    # voert de query uit
    cursor.execute(postgre)
    # slaat alle resultaten op onder result
    result = cursor.fetchall()
    # definieert een lijst om alle informatie van alle patienten met significante metabolieten op te slaan.
    info_pat = []
    for i in result:
        # print(i)
        # definieert een lijst per patient.
        row = []
        name = i[1]
        dis = i[2]
        z_score = i[3]
        row.append(name)
        row.append(dis)
        row.append(z_score)
        info_pat.append(info_pat)


def info_meta_ophalen(cursor):
    """
    haalt informatie uit de database op die het verband weergeeft tussen de metaboliet naam, origin, relevantie en
    weergeeft hierbij ook de description en de hmdb-code.
    :param cursor: cursor
    """
    # default waarde om te testen
    value = -100
    value2 = 100
    filt = "desc"
    # definieert query voor ophalen
    postgre = ("""SELECT name, origin_name, description, hmbd_code, relevance FROM metabolieten
     JOIN origins_metabolieten ON metabolieten.id_metaboliet=origins_metabolieten.metabolieten_id_metaboliet
     JOIN origins ON origins_metabolieten.origins_id_orgins= origins.id_orgins
     JOIN relevance ON metabolieten.relevance_id_relevance=relevance.id_relevance
     JOIN z_scores ON metabolieten.id_metaboliet=z_scores.metabolieten_id_metaboliet
     WHERE (z_score < {} OR z_score > {})
     ORDER BY z_score {}
     LIMIT 10;""").format(value, value2, filt)
    # voert de query uit.
    cursor.execute(postgre)
    # slaat alle resultaten op onder result
    result = cursor.fetchall()

    # definieert een lijst om alle informatie van alle metabolieten op te slaan.
    info_met = []
    for a in result:
        # definieert een lijst per metaboliet.
        row = []
        name = a[0]
        origin = a[1]
        # checkt of origin bekend is.
        if origin == "; \n    ":
            origin = "ONBEKEND"
        else:
            origin = origin
        descr = a[2]
        code = a[3]
        rel = ""
        relevance = a[4].split(",")
        # checkt of de metaboliet niet relevant is.
        if relevance[3] == "f)":
            rel = "FALSE"
        # checkt of de metaboliet relevant is.
        elif relevance[3] == "t)":
            rel = "TRUE"
        # checkt of de metaboliet onbekend is.
        elif relevance[3] == ")":
            rel = "ONBEKEND"
        row.append(name)
        row.append(origin)
        row.append(descr)
        row.append(code)
        row.append(rel)
        info_met.append(row)


def get_patients(cursor):
    """
    Haalt alle patienten op uit de database.
    :param cursor: cursor
    """
    # definieert query voor ophalen
    postgre = """SELECT id_patient FROM patients;"""
    # voert query uit
    cursor.execute(postgre)
    # slaat alle resultaten op onder result
    result = cursor.fetchall()

    # loopt door result heen.
    for i in result:
        print(i)


if __name__ == '__main__':
    # connect aan de database
    connect = psycopg2.connect(host="postgres.biocentre.nl", user="BI2_PG1", password="blaat1234",
                               database="bio_jaar_2_pg_1", port="5900")

    # open een cursor
    curs = connect.cursor()
    info_patient_ophalen(curs)
    # info_meta_ophalen(cursor)
    # get_patients(cursor)
