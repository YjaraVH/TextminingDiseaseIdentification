import matplotlib.pyplot as plt
import numpy as np
import psycopg2
from mysql.connector import cursor
from fileReader import main


def visualisatie():
    value = -100
    value2 = 100
    global result
    patient_name = "P1002.1_Zscore"
    filter = "desc"
    postgre = ("""SELECT name, z_score FROM metabolieten
     JOIN z_scores ON metabolieten.id_metaboliet=z_scores.metabolieten_id_metaboliet
     JOIN patients ON z_scores.patients_id_patient=patients.id_patient
     WHERE id_patient='{}' AND (z_score < {} OR z_score > {})
     ORDER BY z_score {} LIMIT 10;""").format(patient_name,
        value, value2, filter)
    cursor.execute(postgre)
    result = cursor.fetchall()

    return result

def grafiek_maken():
    postgre = ("""SELECT disease, count FROM pub_disease;""")
    cursor.execute(postgre)
    result = cursor.fetchall()
    print(result)
    print(postgre.split())
    labels = postgre.split(",")
    sizes = [15, 30, 45, 10]
    explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis(
        'equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.show()


if __name__ == '__main__':
    # connect aan de database
    conn = psycopg2.connect(host="postgres.biocentre.nl",
                            user="BI2_PG1", password="blaat1234",
                            database="bio_jaar_2_pg_1")

    # open een cursor
    cursor = conn.cursor()
    person_ids = main()
    # result = visualisatie()
    grafiek_maken()
