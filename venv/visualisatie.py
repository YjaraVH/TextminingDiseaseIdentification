import psycopg2

# def connect():
#     # connect aan de database
#     conn = psycopg2.connect(host="postgres.biocentre.nl", user="BI2_PG1", password="blaat1234",
#                             database="bio_jaar_2_pg_1")
#
#     # open een cursor
#     cursor = conn.cursor()


def info_ophalen(conn, cursor):
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





if __name__ == '__main__':
    # connect aan de database
    conn = psycopg2.connect(host="postgres.biocentre.nl", user="BI2_PG1", password="blaat1234",
                            database="bio_jaar_2_pg_1")

    # open een cursor
    cursor = conn.cursor()
    info_ophalen(conn, cursor)