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


########################

def insert_database(key, value, fluids, tissue, patient_id, relevance, paths,
                        origin, disease, name, desc, HMBD_code):
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
    update_fluids(fluids, getal, conn, cursor)
    update_link_fluids_metb(getal, conn, cursor)
    update_tissue(tissue, getal, conn, cursor)
    update_patiens(patient_id, getal, conn, cursor)
    update_link_patient_metb(getal, conn, cursor)
    update_diseases(disease, getal, conn, cursor)
    update_link_diseases_metb(getal, conn, cursor)
    update_origins(origin, getal, conn, cursor)
    update_link_origins_metb(getal, conn, cursor)
    update_pathways(paths, getal, conn, cursor)
    update_link_pathways_metb(getal, conn, cursor)
    update_Metabolieten(getal, name, desc, HMBD_code, cursor, conn)


def update_fluids(fluids, getal, conn, cursor):
    cursor.execute("insert into fluids(id_fluids, fluids_name)"
                   "values ('{}', '{}')").format(getal, fluids[getal])
    conn.commit()

def update_link_fluids_metb(getal, conn, cursor):
    cursor.execute("insert into Metabolieten_fluids(Metabolieten_id_metaboliet, fluids_id_fluids)"
                   "values ('{}', '{}')").format(getal, getal)
    conn.commit()

def update_tissue(tissue, getal, conn, cursor):
    cursor.execute("insert into tissue(id_tissue, tissue_name)"
                       "values ('{}', '{}')").format(getal, tissue[getal])
    conn.commit()

def update_link_tissue_metb(getal, conn, cursor):
    cursor.execute("insert into Metabolieten_tissue(Metabolieten_id_metaboliet, tissue_id_tissue)"
                       "values ('{}', '{}')").format(getal, getal)
    conn.commit()

def update_patiens(patient_id, getal, conn, cursor):
    cursor.execute("insert into Patients(id_patient, id_metaboliet, z_score)"
                   "values ('{}', '{}', '{}')").format(patient_id[getal], getal,
                                                       str(value))
    conn.commit()

def update_link_patient_metb(getal, conn, cursor):
    cursor.execute("insert into Patients_Metabolieten(Patients_id_patient, Metabolieten_id_metaboliet)"
                   "values ('{}', '{}')").format(getal, getal)
    ### moet dit patient_patient releatie gelijk zijn aan patient id?
    conn.commit()

def update_diseases(disease, getal, conn, cursor):
    cursor.execute("insert into diseases(id_disease, disease_name)"
                   "values ('{}', '{}')").format(getal, disease[getal])
    conn.commit()

def update_link_diseases_metb(getal, conn, cursor):
    cursor.execute("insert into Metabolieten_diseases(Metabolieten_id_metaboliet, diseases_id_disease)"
                   "values ('{}', '{}')").format(getal, getal)
    conn.commit()

def update_origins(origin, getal, conn, cursor):
    cursor.execute("insert into fluids(id_orgins, orgin_name)"
                   "values ('{}', '{}')").format(getal, origin[getal])
    conn.commit()

def update_link_origins_metb(getal, conn, cursor):
    cursor.execute("insert into origins_Metabolieten(orings_id_origins, Metabolieten_id_metaboliet)"
                   "values ('{}', '{}')").format(getal, getal)
    conn.commit()

def update_pathways(paths, getal, conn, cursor):
    cursor.execute("insert into pathways(id_path, path_name)"
                   "values ('{}', '{}')").format(getal, paths[getal])
    conn.commit()

def update_link_pathways_metb(getal, conn, cursor):
    cursor.execute("insert into pathways_Metabolieten(pathways_id_pathways, Metabolieten_id_metaboliet)"
                   "values ('{}', '{}')").format(getal, getal)
    conn.commit()

def update_Metabolieten(getal, name, desc, HMBD_code, cursor, conn):
    cursor.execute("insert into Metabolieten(id_relevance, id_metaboliet, id_origin, id_fluids, name,"
                   " description, HMBD_code, relevance_id_relevance)"
                   "values ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')").format(getal, getal, getal, getal,
                                                                                     name[getal], desc[getal],
                                                                                     HMBD_code[getal], getal)
    conn.commit()



if __name__ == '__main__':
    #File name
    file = "Dataset/Untargeted_metabolomics.xlsx"
    #file = 'Compounds_DIMS_HEXA.xlsx'

    data = readFile(file)
    metabolieten = getMetabolites(data)
    person_ids,start,stop = getPatientsId(data)

    dict = getDicMetbZscore(data,metabolieten,start,stop)

    #print best wel veel uit, maar dan kun je even kijken hoe het eruit ziet:)
    #printDictionary(dict)
    #print(person_ids)
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

    getal = 1
    for key, value, in dict.items():
        insert_database(key, value, fluids, tissue, person_inds, relevance, pathway,
                        origin, disease, metabolieten, description, hmdb_code)
        getal +=1

