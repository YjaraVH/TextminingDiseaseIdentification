import plotly.express as px
import psycopg2
'''
    Filename: sunburstplot.py
    Authors: Nienke Gertsen
    Date created: 6/06/2022
'''

char = []
par = []
values = []
metabolits = []


def get_meta_top(connect, cursor, patient, val, val2):
    """
    Verzamelt de data die nodig is voor het maken van de sunburstplot.
    :param patient: string - patient
    :param val: int - z-score filter 1
    :param val2: int - z-score filter 2
    :param connect: connection
    :param cursor: cursor
    """
    global char
    global par
    global values
    global metabolits

    # query om informatie op te halen uit de database
    postgre = ("""SELECT id_patient, name, disease, count FROM metabolieten
      JOIN z_scores ON metabolieten.id_metaboliet=z_scores.metabolieten_id_metaboliet
      JOIN patients ON z_scores.patients_id_patient=patients.id_patient
      JOIN metabolieten_pubom mp ON metabolieten.id_metaboliet = mp.metabolieten_id_metaboliet
      JOIN pubom ON mp.pubom_id_pum_om = pubom.id_pum_om
      JOIN pub_disease_pubom pdp ON pubom.id_pum_om = pdp.pubom_id_pum_om
      JOIN pub_disease ON pdp.pub_disease_id_article = pub_disease.id_article
      WHERE id_patient='{}' AND (z_score < {} OR z_score > {})
      ORDER BY z_score desc;""").format(patient, val, val2)
    # voert de query uit
    cursor.execute(postgre)
    # opgehaalde informatie wordt weggeschreven onder results
    result = cursor.fetchall()
    # Maakt een lege lijst metabolieten aan die alle metabolieten op slaat.
    metabolen = []
    for x in result:
        # print(x)
        pat = x[0]
        meta = x[1]
        metabolen.append(meta)

        # checkt of de metaboliet al eens voorgekomen is en maakt zo een lijst waar alle
        # metaboliet namen die siginifcant zijn voor de patient een keer op geslagen wordt.
        if meta in metabolits:
            pass
        else:
            metabolits.append(meta)

    for met in metabolits:
        # telt per metaboliet het voorkomen hiervan.
        nmb = metabolen.count(str(met))
        char.append(met)
        par.append(pat)
        values.append(nmb)

    for a in result:
        meta = a[1]
        dis = a[2]
        cnt = a[3]
        char.append(dis)
        par.append(meta)
        values.append(cnt)

    connect.close()


def make_figure():
    """
    Maakt de sunburstplot.
    """
    global char
    global par
    global values
    # schrijft alle lijsten die nodig zijn voor het maken van de plot weg in data.
    data = dict(
        character=char, parent=par, value=values)
    # maken van de sunburstplot.
    fig = px.sunburst(
        data,
        names='character',
        parents='parent',
        values='value', width=800, height=800)
    # zorgt voor visualisatie van de plot.
    return fig.show()


def get_figure(pat, neg, pos):
    # connect aan de database
    conn = psycopg2.connect(host="postgres.biocentre.nl", user="BI2_PG1",
                            password="blaat1234",
                            database="bio_jaar_2_pg_1", port="5900")

    # open een cursor
    cur = conn.cursor()
    # default waarde
    get_meta_top(conn, cur, pat, neg, pos)
    make_figure()


if __name__ == '__main__':
    get_figure("P1002.1_Zscore", -100, 100)
