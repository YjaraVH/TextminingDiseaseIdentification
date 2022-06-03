import psycopg2

# def connect():
#     # connect aan de database
#     conn = psycopg2.connect(host="postgres.biocentre.nl", user="BI2_PG1", password="blaat1234",
#                             database="bio_jaar_2_pg_1")
#
#     # open een cursor
#     cursor = conn.cursor()


def info_patient_ophalen(conn, cursor):
    value = -100
    value2 = 100
    patient_name = "P1002.1_Zscore"
    filter = "desc"
    postgre = ("""SELECT name, z_score FROM metabolieten
     JOIN z_scores ON metabolieten.id_metaboliet=z_scores.metabolieten_id_metaboliet
     JOIN patients ON z_scores.patients_id_patient=patients.id_patient
     WHERE id_patient='{}' AND (z_score < {} OR z_score > {})
     ORDER BY z_score {};""").format(patient_name,
        value, value2, filter)
    cursor.execute(postgre)
    result = cursor.fetchall()

    for i in result:
        print(i)


def info_meta_ophalen(conn, cursor):
    value = -100
    value2 = 100
    filter = "desc"
    postgre = ("""SELECT name, origin_name, description, hmbd_code, relevance FROM metabolieten
     JOIN origins_metabolieten ON metabolieten.id_metaboliet=origins_metabolieten.metabolieten_id_metaboliet
     JOIN origins ON origins_metabolieten.origins_id_orgins= origins.id_orgins
     JOIN relevance ON metabolieten.relevance_id_relevance=relevance.id_relevance
     JOIN z_scores ON metabolieten.id_metaboliet=z_scores.metabolieten_id_metaboliet
     WHERE (z_score < {} OR z_score > {})
     ORDER BY z_score {};""").format(value, value2, filter)
    cursor.execute(postgre)
    result = cursor.fetchall()

    for a in result:
        row = []
        name = a[0]
        origin = a[1]
        if origin == "; \n    ":
            origin = "ONBEKEND"
        else:
            origin = origin
        descr = a[2]
        code = a[3]
        rel = ""
        relevance = a[4].split(",")
        if relevance[3] == "f)":
            rel = "FALSE"
        elif relevance[3] == "t)":
            rel = "TRUE"
        elif relevance[3] == ")":
            rel = "ONBEKEND"
        row.append(name)
        row.append(origin)
        row.append(descr)
        row.append(code)
        row.append(rel)
    print(row)




if __name__ == '__main__':
    # connect aan de database
    conn = psycopg2.connect(host="postgres.biocentre.nl", user="BI2_PG1", password="blaat1234",
                            database="bio_jaar_2_pg_1")

    # open een cursor
    cursor = conn.cursor()
    #info_patient_ophalen(conn, cursor)
    info_meta_ophalen(conn, cursor)