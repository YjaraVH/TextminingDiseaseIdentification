import plotly.express as px
import psycopg2

char = []
par = []
values = []

def get_meta_top(conn, cursor):
    global char
    global par
    global values
    patient = "P1002.1_Zscore"
    val = -100
    val2 = 100
    postgre = ("""SELECT id_patient, name FROM metabolieten
      JOIN z_scores ON metabolieten.id_metaboliet=z_scores.metabolieten_id_metaboliet
      JOIN patients ON z_scores.patients_id_patient=patients.id_patient
      WHERE id_patient='{}' AND (z_score < {} OR z_score > {})
      ORDER BY z_score desc
      LIMIT 10;""").format(patient,
        val, val2)
    cursor.execute(postgre)
    result = cursor.fetchall()

    for x in result:
        # print(x)
        pat = x[0]
        meta = x[1]
        char.append(str(meta))

    i = 0
    while i <= len(result):
        par.append(str(pat))
        i += 1


def get_meta_bottom(conn, cursor):
    global char
    global par
    global values
    patient = "P1002.1_Zscore"
    val = -100
    val2 = 100
    postgre = ("""SELECT id_patient, name FROM metabolieten
      JOIN z_scores ON metabolieten.id_metaboliet=z_scores.metabolieten_id_metaboliet
      JOIN patients ON z_scores.patients_id_patient=patients.id_patient
      WHERE id_patient='{}' AND (z_score < {} OR z_score > {})
      ORDER BY z_score asc
      LIMIT 10;""").format(patient,
        val, val2)
    cursor.execute(postgre)
    result = cursor.fetchall()

    for x in result:
        # print(x)
        pat = x[0]
        meta = x[1]
        char.append(str(meta))

    i = 1
    while i < len(result):
        par.append(str(pat))
        i += 1


def get_disease_top(cursor):
    global char
    global par
    global values
    patient = "P1002.1_Zscore"
    val = -100
    val2 = 100
    postgre = ("""SELECT name, disease, count FROM metabolieten
      JOIN z_scores ON metabolieten.id_metaboliet=z_scores.metabolieten_id_metaboliet
      JOIN patients ON z_scores.patients_id_patient=patients.id_patient
      JOIN metabolieten_pubom mp ON metabolieten.id_metaboliet = mp.metabolieten_id_metaboliet
      JOIN pubom ON mp.pubom_id_pum_om = pubom.id_pum_om
      JOIN pub_disease_pubom pdp ON pubom.id_pum_om = pdp.pubom_id_pum_om
      JOIN pub_disease ON pdp.pub_disease_id_article = pub_disease.id_article
      WHERE id_patient='{}' AND (z_score < {} OR z_score > {})
      ORDER BY z_score desc;""").format(patient, val, val2)
    cursor.execute(postgre)
    result = cursor.fetchall()

    for x in result:
        # print(x)
        met = x[0]
        dis = x[1]
        cnt = x[2]
        char.append(str(dis))
        par.append(met)
        values.append(cnt)


def get_disease_bottom(cursor):
    global char
    global par
    global values
    patient = "P1002.1_Zscore"
    val = -100
    val2 = 100
    postgre = ("""SELECT name, disease, count FROM metabolieten
      JOIN z_scores ON metabolieten.id_metaboliet=z_scores.metabolieten_id_metaboliet
      JOIN patients ON z_scores.patients_id_patient=patients.id_patient
      JOIN metabolieten_pubom mp ON metabolieten.id_metaboliet = mp.metabolieten_id_metaboliet
      JOIN pubom ON mp.pubom_id_pum_om = pubom.id_pum_om
      JOIN pub_disease_pubom pdp ON pubom.id_pum_om = pdp.pubom_id_pum_om
      JOIN pub_disease ON pdp.pub_disease_id_article = pub_disease.id_article
      WHERE id_patient='{}' AND (z_score < {} OR z_score > {})
      ORDER BY z_score asc;""").format(patient, val, val2)
    cursor.execute(postgre)
    result = cursor.fetchall()

    for x in result:
        # print(x)
        met = x[0]
        dis = x[1]
        cnt = x[2]
        char.append(str(dis))
        par.append(met)
        values.append(cnt)


def make_figure():
    global char
    global par
    global values

    # print(len(char))
    # print(len(par))
    # print(len(values))
    #
    # print(char)
    # print(par)
    # print(values)

    data = dict(
        character=char, parent=par, value=values)

    fig = px.sunburst(
        data,
        names='character',
        parents='parent',
        values='value',
    )
    fig.show()





if __name__ == '__main__':
    # connect aan de database
    conn = psycopg2.connect(host="postgres.biocentre.nl", user="BI2_PG1", password="blaat1234",
                            database="bio_jaar_2_pg_1", port="5900")

    # open een cursor
    cursor = conn.cursor()
    get_meta_top(conn, cursor)
    get_meta_bottom(conn, cursor)

    for z in char:
        values.append(char.count(str(z)))

    get_disease_top(cursor)
    get_disease_bottom(cursor)
    make_figure()