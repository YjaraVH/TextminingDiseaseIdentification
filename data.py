from fileReader import main
import psycopg2

def update_fluid(fluid):
    getal = 1
    for flu in fluid[0]:
        cursor.execute("insert into fluids(id_fluids, fluids_name)"
                       "values ('{}', '{}')".format(getal, flu))
        conn.commit()
        getal += 1
    print("tabel fluids geupdate")


def update_tissue(tissue):
    getal = 1
    for tis in tissue[0]:
        cursor.execute("insert into tissue(id_tissue, tissue_name)"
                       "values ('{}', '{}')".format(getal, tis))
        conn.commit()
        getal += 1
    print("tabel tissue geupdate")


def update_diseases(disease):
    getal = 1
    for dis in disease[0]:
        dis = str(dis).replace("'", "")
        cursor.execute("insert into diseases(id_disease, disease_name)"
                       "values ('{}', '{}')".format(getal, dis))
        conn.commit()
        getal += 1
    print("tabel diseases geupdate")

def update_origins(origin):
    getal = 1
    for org in origin[0]:
        cursor.execute("insert into origins(id_orgins, origin_name)"
                       "values ('{}', '{}')".format(getal, org))
        conn.commit()
        getal += 1
    print("tabel origins geupdate")


def update_paths(pathway):
    getal = 1
    for pat in pathway[0]:
        cursor.execute("insert into pathways(id_path, path_name)"
                       "values ('{}', '{}')".format(getal, pat))
        conn.commit()
        getal += 1
    print("tabel pathways geupdate")


def update_relevance(relevance):
    getal = 1
    for rel in relevance[0]:
        place = rel.split(",")
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
    print("tabel relevance is geupdate")


def update_Patients(person_ids):
    getal = 1
    for per in person_ids:
        cursor.execute("insert into Patients(id_patient)"
                       "values ('{}')".format(per))
        conn.commit()
        getal += 1
    print("tabel patients geupdate")


def update_Metabolieten(name, desc, HMBD_code):
    getal = 1
    for na in name[0]:
        cursor.execute("insert into Metabolieten(id_metaboliet, id_origin, id_fluids, name,"
                       " description, HMBD_code, relevance_id_relevance)"
                       "values ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(getal, getal, getal,
                                                                                        na.replace("'", ""), str(desc[0][getal-1]).replace("'", ""),
                                                                                        HMBD_code[0][getal - 1],
                                                                                        getal))
        conn.commit()
        getal += 1
    print("tabel Metabolieten geupdate")


def update_z_score(lijst_patienten_lijsten):
    number = 1
    for patient in lijst_patienten_lijsten:
        getal = 1
        for score in patient[1]:
            cursor.execute("insert into Z_scores(z_id, z_score, patients_id_patient, metabolieten_id_metaboliet) "
                           "values ('{}', '{}', '{}', '{}')".format(number, score, patient[0], getal))
            conn.commit()
            getal += 1
            number += 1
    print("tabel Z-scores geupdate")

def update_link_meta_tis(getal):
    cursor.execute("insert into Metabolieten_tissue(metabolieten_id_metaboliet, tissue_id_tissue) "
                   "values ('{}', '{}')".format(getal, getal))
    conn.commit()


def update_link_meta_flu(getal):
    cursor.execute("insert into Metabolieten_fluids(metabolieten_id_metaboliet, fluids_id_fluids) "
                   "values ('{}', '{}')".format(getal, getal))
    conn.commit()


def update_link_meta_dis(getal):
    cursor.execute("insert into Metabolieten_diseases(metabolieten_id_metaboliet, diseases_id_disease) "
                   "values ('{}', '{}')".format(getal, getal))
    conn.commit()


def update_link_meta_ori(getal):
    cursor.execute("insert into origins_Metabolieten(origins_id_orgins, metabolieten_id_metaboliet) "
                   "values ('{}', '{}')".format(getal, getal))
    conn.commit()


def update_link_meta_path(getal):
    cursor.execute("insert into pathways_Metabolieten(pathways_id_path, metabolieten_id_metaboliet) "
                   "values ('{}', '{}')".format(getal, getal))
    conn.commit()


def update_link_meta_pubom(getal):
    cursor.execute("insert into metabolieten_pubom(pathways_id_path, metabolieten_id_metaboliet) "
                   "values ('{}', '{}')".format(getal, getal))
    conn.commit()



if __name__ == '__main__':
    # connect aan de database
    conn = psycopg2.connect(host="postgres.biocentre.nl", user="BI2_PG1", password="blaat1234",
                            database="bio_jaar_2_pg_1")

    # open een cursor
    cursor = conn.cursor()
    fluids, tissue, person_ids, relevance, pathway, origin, disease, metabolieten, description, hmdb_code, lijst_patienten_lijsten  = main()
    #update_fluid(fluids)
    #update_tissue(tissue)
    #update_diseases(disease)
    #update_origins(origin)
    #update_paths(pathway)
    #update_relevance(relevance)
    #update_Patients(person_ids)
    #update_Metabolieten(metabolieten, description, hmdb_code)
    #update_z_score(lijst_patienten_lijsten)

    getal = 1
    for nam in metabolieten[0]:
        #update_link_meta_tis(getal)
        #update_link_meta_flu(getal)
        #update_link_meta_dis(getal)
        #update_link_meta_ori(getal)
        #update_link_meta_path(getal)
        getal += 1
    print("tabel link Metabolieten_tissue geupdate")
    print("tabel link Metabolieten_fluids geupdate")
    print("tabel link Metabolieten_diseases geupdate")
    print("tabel link origins_Metabolieten geupdate")
    print("tabel link pathways_Metabolieten geupdate")

    conn.close()
