import pandas as pd
import psycopg2

def readFile(file):
    data = pd.read_excel(file)
    return data


def getPatientsId(data):
    columns = data.columns
    person_ids = []
    count = 0
    firstCount = 0
    for i in columns:
        if firstCount == 0:
            count = count + 1
        string_i = str(i)
        if string_i.startswith("P") and string_i.endswith("Zscore"):
            if firstCount == 0:
                firstCount = count - 1
            count = count + 1
            person_ids.append(string_i)
    return person_ids, firstCount, count


def getMetabolites(data):
    metabolites = data["name"]
    return list(metabolites)


def getDicMetbZscore(data, metabolites, start, stop):
    dict = {}
    for index in range(0, len(metabolites)):
        dict[metabolites[index]] = list(data.loc[index])[start:stop]
    return dict


def printDictionary(dict):
    for item in dict:
        print("key: {}, Value {}".format(item, dict[item]))


def getMetabolieten(data):
    metabolieten = []
    metabolites = data["name"]
    metabolieten.append(list(metabolites))
    return metabolieten


def getRelevance(data):
    relevance = []
    rele = data["relevance"]
    relevance.append(list(rele))
    return relevance


def getDescription(data):
    description = []
    desc = data["descr"]
    description.append(list(desc))
    return description


def getOrigin(data):
    origin = []
    ori = data["origin"]
    origin.append(list(ori))
    return origin


def getFluids(data):
    fluids = []
    fluid = data["fluids"]
    fluids.append(list(fluid))
    return fluids


def getTissue(data):
    tissue = []
    tiss = data["tissue"]
    tissue.append(list(tiss))
    return tissue


def getDisease(data):
    disease = []
    dis = data["disease"]
    disease.append(list(dis))
    return disease


def getPathway(data):
    pathway = []
    path = data["pathway"]
    pathway.append(list(path))
    return pathway


def getHMDBcode(data):
    hmdb_code = []
    code = data["HMDB_code"]
    hmdb_code.append(list(code))
    return hmdb_code
def getPatient1(data):
    patient1 = []
    zscores = data["P1002.1_Zscore"]
    patient1.append(list(zscores))
    patient1.insert(0,"P1002.1_Zscore")
    return patient1


def getPatient2(data):
    patient2 = []
    zscores = data["P1003.1_Zscore"]
    patient2.append(list(zscores))
    patient2.insert(0, "P1003.1_Zscore")
    return patient2


def getPatient3(data):
    patient3 = []
    zscores = data["P1005.1_Zscore"]
    patient3.append(list(zscores))
    patient3.insert(0, "P1005.1_Zscore")
    return patient3


def getPatient4(data):
    patient4 = []
    zscores = data["P1005.2_Zscore"]
    patient4.append(list(zscores))
    patient4.insert(0, "P1005.2_Zscore")
    return patient4


def getPatient5(data):
    patient5 = []
    zscores = data["P2021M01703.1_Zscore"]
    patient5.append(list(zscores))
    patient5.insert(0, "P2021M01703.1_Zscore")
    return patient5


def getPatient6(data):
    patient6 = []
    zscores = data["P2021M01743.1_Zscore"]
    patient6.append(list(zscores))
    patient6.insert(0, "P2021M01743.1_Zscore")
    return patient6


def getPatient7(data):
    patient7 = []
    zscores = data["P2021M01865.1_Zscore"]
    patient7.append(list(zscores))
    patient7.insert(0, "P2021M01865.1_Zscore")
    return patient7


def getPatient8(data):
    patient8 = []
    zscores = data["P2021M01871.1_Zscore"]
    patient8.append(list(zscores))
    patient8.insert(0, "P2021M01871.1_Zscore")
    return patient8


def getPatient9(data):
    patient9 = []
    zscores = data["P2021M01896.1_Zscore"]
    patient9.append(list(zscores))
    patient9.insert(0, "P2021M01896.1_Zscore")
    return patient9


def getPatient10(data):
    patient10 = []
    zscores = data["P2021M01902.1_Zscore"]
    patient10.append(list(zscores))
    patient10.insert(0, "P2021M01902.1_Zscore")
    return patient10


def getPatient11(data):
    patient11 = []
    zscores = data["P2021M01906.1_Zscore"]
    patient11.append(list(zscores))
    patient11.insert(0, "P2021M01906.1_Zscore")
    return patient11


def getPatient12(data):
    patient12 = []
    zscores = data["P2021M01908.1_Zscore"]
    patient12.append(list(zscores))
    patient12.insert(0, "P2021M01908.1_Zscore")
    return patient12


def getPatient13(data):
    patient13 = []
    zscores = data["P2021M01912.1_Zscore"]
    patient13.append(list(zscores))
    patient13.insert(0, "P2021M01912.1_Zscore")
    return patient13


def getPatient14(data):
    patient14 = []
    zscores = data["P2021M01918.1_Zscore"]
    patient14.append(list(zscores))
    patient14.insert(0, "P2021M01918.1_Zscore")
    return patient14


def getPatient15(data):
    patient15 = []
    zscores = data["P2021M01932.1_Zscore"]
    patient15.append(list(zscores))
    patient15.insert(0, "P2021M01932.1_Zscore")
    return patient15


def getPatient16(data):
    patient16 = []
    zscores = data["P2021M01951.1_Zscore"]
    patient16.append(list(zscores))
    patient16.insert(0, "P2021M01951.1_Zscore")
    return patient16


def getPatient17(data):
    patient17 = []
    zscores = data["P2021M01956.1_Zscore"]
    patient17.append(list(zscores))
    patient17.insert(0, "P2021M01956.1_Zscore")
    return patient17


def getPatient18(data):
    patient18 = []
    zscores = data["P2021M01958.1_Zscore"]
    patient18.append(list(zscores))
    patient18.insert(0, "P2021M01958.1_Zscore")
    return patient18


def getPatient19(data):
    patient19 = []
    zscores = data["P2021M01962.1_Zscore"]
    patient19.append(list(zscores))
    patient19.insert(0, "P2021M01962.1_Zscore")
    return patient19


def getPatient20(data):
    patient20 = []
    zscores = data["P2021M01971.1_Zscore"]
    patient20.append(list(zscores))
    patient20.insert(0, "P2021M01971.1_Zscore")
    return patient20


def getPatient21(data):
    patient21 = []
    zscores = data["P2021M01973.1_Zscore"]
    patient21.append(list(zscores))
    patient21.insert(0, "P2021M01973.1_Zscore")
    return patient21


def getPatient22(data):
    patient22 = []
    zscores = data["P2021M01981.1_Zscore"]
    patient22.append(list(zscores))
    patient22.insert(0, "P2021M01981.1_Zscore")
    return patient22


def getPatient23(data):
    patient23 = []
    zscores = data["P2021M01984.1_Zscore"]
    patient23.append(list(zscores))
    patient23.insert(0, "P2021M01984.1_Zscore")
    return patient23


def getPatient24(data):
    patient24 = []
    zscores = data["P2021M01990.1_Zscore"]
    patient24.append(list(zscores))
    patient24.insert(0, "P2021M01990.1_Zscore")
    return patient24


def getPatient25(data):
    patient25 = []
    zscores = data["P2021M02023.1_Zscore"]
    patient25.append(list(zscores))
    patient25.insert(0, "P2021M02023.1_Zscore")
    return patient25


def getPatient26(data):
    patient26 = []
    zscores = data["P2021M02031.1_Zscore"]
    patient26.append(list(zscores))
    patient26.insert(0, "P2021M02031.1_Zscore")
    return patient26


def getPatient27(data):
    patient27 = []
    zscores = data["P2021M02035.1_Zscore"]
    patient27.append(list(zscores))
    patient27.insert(0, "P2021M02035.1_Zscore")
    return patient27


def getPatient28(data):
    patient28 = []
    zscores = data["P2021M02040.1_Zscore"]
    patient28.append(list(zscores))
    patient28.insert(0, "P2021M02040.1_Zscore")
    return patient28


def getPatient29(data):
    patient29 = []
    zscores = data["P2021M02052.1_Zscore"]
    patient29.append(list(zscores))
    patient29.insert(0, "P2021M02052.1_Zscore")
    return patient29


def getPatient30(data):
    patient30 = []
    zscores = data["P2021M02098.1_Zscore"]
    patient30.append(list(zscores))
    patient30.insert(0, "P2021M02098.1_Zscore")
    return patient30


def getPatient31(data):
    patient31 = []
    zscores = data["P2021M02101.1_Zscore"]
    patient31.append(list(zscores))
    patient31.insert(0, "P2021M02101.1_Zscore")
    return patient31

########################

def insert_database(fluids, tissue, patient_id, relevance, paths,
                        origin, disease, name, desc, HMBD_code, list_patients):
    """
    Voegt de informatie die uit de resultaten van BLAST
    gehaald zijn toe aan de database.
    :return:
    """
    # connect aan de database
    conn = psycopg2.connect(host="postgres.biocentre.nl", user="BI2_PG1", password="blaat1234",
                            database="bio_jaar_2_pg_1")

    # open een cursor
    cursor = conn.cursor()
    update_fluids(fluids, conn, cursor)
    print("tabel fluids geupdate")
    update_tissue(tissue, conn, cursor)
    print("tabel tissue geupdate")
    update_patients(patient_id, conn, cursor)
    print("tabel patients geupdate")
    update_relevance(relevance, conn, cursor)
    print("tabel relevance geupdate")
    update_Metabolieten(name, desc, HMBD_code, cursor, conn)
    print("tabel metabolieten geupdate")
    update_zscore(conn, cursor, list_patients)
    print("tabel z-score geupdate")
    update_diseases(disease, conn, cursor)
    print("tabel diseases geupdate")
    update_origins(origin, conn, cursor)
    print("tabel origins geupdate")
    update_pathways(paths, conn, cursor)
    print("tabel pathways geupdate")
    update_link_fluids_metb(fluids, conn, cursor)
    print("tabel link fluids metabolieten geupdate")
    update_link_tissue_metb(tissue, conn, cursor)
    print("tabel link tissue metabolieten geupdate")
    #update_link_patient_metb(patient, getal, conn, cursor)
    print("tabel link patient metabolieten geupdate")
    update_link_diseases_metb(disease, conn, cursor)
    print("tabel link diseases metabolieten geupdate")
    update_link_origins_metb(origin, conn, cursor)
    print("tabel link origins metabolieten geupdate")
    update_link_pathways_metb(paths, conn, cursor)
    print("tabel link pathways metabolieten geupdate")

    conn.close()


def update_fluids(fluids, conn, cursor):
    print(fluids)
    getal = 1
    for fluid in fluids:
        cursor.execute("insert into fluids(id_fluids, fluids_name)"
                       "values ('{}', '{}')".format(getal, fluids[0][getal-1]))
        conn.commit()
        getal += 1

def update_link_fluids_metb(fluids, conn, cursor):
    getal = 1
    for link in fluids:
        cursor.execute("insert into Metabolieten_fluids(Metabolieten_id_metaboliet, fluids_id_fluids)"
                       "values ('{}', '{}')".format(getal, getal))
        conn.commit()
        getal += 1


def update_tissue(tissue, conn, cursor):
    getal = 1
    for tiss in tissue:
        cursor.execute("insert into tissue(id_tissue, tissue_name)"
                           "values ('{}', '{}')".format(getal, tissue[0][getal-1]))
        conn.commit()
        getal += 1


def update_link_tissue_metb(tissue, conn, cursor):
    getal = 1
    for link in tissue:
        cursor.execute("insert into Metabolieten_tissue(Metabolieten_id_metaboliet, tissue_id_tissue)"
                           "values ('{}', '{}')".format(getal, getal))
        conn.commit()
        getal += 1


def update_zscore(conn, cursor, list_patient):
    number = 1
    for score in list_patient[number-1][1]:
        cursor.execute("insert into Z_scores(z_id, z_score, patients_id_patient, metabolieten_id_metaboliet) "
                       "values ('{}', '{}', '{}', '{}')".format(number, score, list_patient[number-1][0], number))
        conn.commit()
        number += 1


def update_patients(patient_id, conn, cursor):
    getal = 1
    for patient in patient_id:
        cursor.execute("insert into Patients(id_patient)"
                       "values ('{}')".format(patient_id[0][getal-1]))
        conn.commit()
        getal += 1


# def update_link_patient_metb(getal, conn, cursor):
#     cursor.execute("insert into Patients_Z_scores(Patients_id_patient, Metabolieten_id_metaboliet)"
#                    "values ('{}', '{}')".format(getal, getal))
#     ### moet dit patient_patient releatie gelijk zijn aan patient id?
#     conn.commit()


def update_diseases(disease, conn, cursor):
    getal = 1
    for dis in disease:
        cursor.execute("insert into diseases(id_disease, disease_name)"
                       "values ('{}', '{}')".format(getal, disease[0][getal-1]))
        conn.commit()
        getal += 1


def update_link_diseases_metb(dissease, conn, cursor):
    getal = 1
    for link in dissease:
        cursor.execute("insert into Metabolieten_diseases(Metabolieten_id_metaboliet, diseases_id_disease)"
                       "values ('{}', '{}')".format(getal, getal))
        conn.commit()
        getal += 1


def update_origins(origin, conn, cursor):
    getal = 1
    for ori in origin:
        cursor.execute("insert into origins(id_orgins, orgin_name)"
                       "values ('{}', '{}')".format(getal, origin[0][getal-1]))
        conn.commit()
        getal += 1


def update_link_origins_metb(origin, conn, cursor):
    getal = 1
    for link in origin:
        cursor.execute("insert into origins_Metabolieten(orings_id_origins, Metabolieten_id_metaboliet)"
                       "values ('{}', '{}')".format(getal, getal))
        conn.commit()
        getal += 1


def update_pathways(paths, conn, cursor):
    getal = 1
    for pat in paths:
        cursor.execute("insert into pathways(id_path, path_name)"
                       "values ('{}', '{}')")
        conn.commit()
        getal += 1

def update_link_pathways_metb(paths, conn, cursor):
    getal = 1
    for link in paths:
        cursor.execute("insert into pathways_Metabolieten(pathways_id_pathways, Metabolieten_id_metaboliet)"
                       "values ('{}', '{}')".format(getal, getal))
        conn.commit()
        getal += 1


def update_Metabolieten(name, desc, HMBD_code, cursor, conn):
    getal = 1
    for na in name:
        cursor.execute("insert into Metabolieten(id_relevance, id_metaboliet, id_origin, id_fluids, name,"
                       " description, HMBD_code, relevance_id_relevance)"
                       "values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(getal, getal, getal, getal,
                                                                                         name[0][getal-1], desc[0][getal-1],
                                                                                         HMBD_code[0][getal-1], getal))
        conn.commit()
        getal += 1

def update_relevance(relevance, conn, cursor):
    getal = 1
    for rel in relevance:
        place = relevance[0][getal-1].split(",")
        if place[0] == "Endogenous" or place[0] == "endogenous":
            if place[1] == "relevant":
                cursor.execute("insert into relevance(id_relevance,endogenous, exogenous, relevant)"
                               "values ('{}', TRUE, FALSE, TRUE)".format(getal))
                conn.commit()
            else:
                cursor.execute("insert into relevance(id_relevance,endogenous, exogenous, relevant)"
                               "values ('{}', TRUE, FALSE, FALSE)".format(getal))
                conn.commit()
        elif place[0] == "Internal standard":
            cursor.execute("insert into relevance(id_relevance,endogenous, exogenous, relevant)"
                           "values ('{}', NULL, NULL, NULL)".format(getal))
            conn.commit()
        elif place[0] == "Onbekend":
            cursor.execute("insert into relevance(id_relevance,endogenous, exogenous, relevant)"
                           "values ('{}', NULL, NULL, NULL)".format(getal))
            conn.commit()
        getal += 1



if __name__ == '__main__':
    # File name
    file = "Untargeted_metabolomics.xlsx"
    # file = 'Compounds_DIMS_HEXA.xlsx'

    data = readFile(file)
    metabolieten = getMetabolites(data)
    person_ids, start, stop = getPatientsId(data)

    dict = getDicMetbZscore(data, metabolieten, start, stop)

    # print best wel veel uit, maar dan kun je even kijken hoe het eruit ziet:)
    # printDictionary(dict)
    # print(person_ids)
    person_inds = getPatientsId(data)
    metabolieten = getMetabolieten(data)
    # print(metabolieten)
    relevance = getRelevance(data)
    # print(relevance)
    description = getDescription(data)
    # print(description)
    origin = getOrigin(data)
    # print(origin)
    fluids = getFluids(data)
    # print(fluids)
    disease = getDisease(data)
    # print(disease)
    pathway = getPathway(data)
    # print(pathway)
    hmdb_code = getHMDBcode(data)
    # print(hmdb_code)
    tissue = getTissue(data)


    patient1 = getPatient1(data)
    # print(patient1)
    patient2 = getPatient2(data)
    # print(patient2)
    patient3 = getPatient3(data)
    # print(patient3)
    patient4 = getPatient4(data)
    # print(patient4)
    patient5 = getPatient5(data)
    # print(patient5)
    patient6 = getPatient6(data)
    # print(patient6)
    patient7 = getPatient7(data)
    # print(patient7)
    patient8 = getPatient8(data)
    # print(patient8)
    patient9 = getPatient9(data)
    # print(patient9)
    patient10 = getPatient10(data)
    # print(patient10)
    patient11 = getPatient11(data)
    # print(patient11)
    patient12 = getPatient12(data)
    # print(patient12)
    patient13 = getPatient13(data)
    # print(patient13)
    patient14 = getPatient14(data)
    # print(patient14)
    patient15 = getPatient15(data)
    # print(patient15)
    patient16 = getPatient16(data)
    # print(patient16)
    patient17 = getPatient17(data)
    # print(patient17)
    patient18 = getPatient18(data)
    # print(patient18)
    patient19 = getPatient19(data)
    # print(patient19)
    patient20 = getPatient20(data)
    # print(patient20)
    patient21 = getPatient21(data)
    # print(patient21)
    patient22 = getPatient22(data)
    # print(patient22)
    patient23 = getPatient23(data)
    # print(patient23)
    patient24 = getPatient24(data)
    # print(patient24)
    patient25 = getPatient25(data)
    # print(patient25)
    patient26 = getPatient26(data)
    # print(patient26)
    patient27 = getPatient27(data)
    # print(patient27)
    patient28 = getPatient28(data)
    # print(patient28)
    patient29 = getPatient29(data)
    # print(patient29)
    patient30 = getPatient30(data)
    # print(patient30)
    patient31 = getPatient31(data)
    # print(patient31)

    lijst_patienten_lijsten = [patient1, patient2, patient3, patient4,
                               patient5, patient6, patient7, patient8,
                               patient9, patient10, patient11, patient12,
                               patient13, patient14, patient15, patient16,
                               patient17, patient18, patient19, patient20,
                               patient21, patient22, patient23, patient24,
                               patient25, patient26, patient27, patient28,
                               patient29, patient30, patient31]


    insert_database(fluids, tissue, person_inds, relevance, pathway,
                    origin, disease, metabolieten, description, hmdb_code, lijst_patienten_lijsten)

