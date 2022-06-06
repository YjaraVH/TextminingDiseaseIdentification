from fileReader import main
import psycopg2


def update_fluid(fluid):
    """
    vult de tabel fluids in de database.
    :param fluid: list - met alle fluids per metaboliet
    """
    # getal telt op om de PK en FK te definieren.
    getal = 1
    for flu in fluid[0]:
        # voegt data toe aan de database
        cursor.execute("insert into fluids(id_fluids, fluids_name)"
                       "values ('{}', '{}')".format(getal, flu))
        conn.commit()
        getal += 1
    print("tabel fluids geupdate")


def update_tissue(tissue):
    """
    vult de tabel tissue in de database.
    :param tissue: list - met alle tissues per metaboliet.
    """
    # getal telt op om de PK en FK te definieren.
    getal = 1
    for tis in tissue[0]:
        # voegt data toe aan de database
        cursor.execute("insert into tissue(id_tissue, tissue_name)"
                       "values ('{}', '{}')".format(getal, tis))
        conn.commit()
        getal += 1
    print("tabel tissue geupdate")


def update_diseases(disease):
    """
    vult de tabel disease in de database.
    :param disease: list - met mogelijke diseases per metaboliet.
    """
    # getal telt op om de PK en FK te definieren.
    getal = 1
    for dis in disease[0]:
        # voegt data toe aan de database
        dis = str(dis).replace("'", "")
        cursor.execute("insert into diseases(id_disease, disease_name)"
                       "values ('{}', '{}')".format(getal, dis))
        conn.commit()
        getal += 1
    print("tabel diseases geupdate")


def update_origins(origin):
    """
    vult tabel origin in de database.
    :param origin: list - met origin van elke metaboliet.
    """
    # getal telt op om de PK en FK te definieren.
    getal = 1
    for org in origin[0]:
        # voegt data toe aan de database
        cursor.execute("insert into origins(id_orgins, origin_name)"
                       "values ('{}', '{}')".format(getal, org))
        conn.commit()
        getal += 1
    print("tabel origins geupdate")


def update_paths(pathway):
    """
    vult de tabel pathways in de database.
    :param pathway: list - met alle mogelijke pathways waarin de metaboliet een rol speelt.
    """
    # getal telt op om de PK en FK te definieren.
    getal = 1
    for pat in pathway[0]:
        # voegt data toe aan de database.
        cursor.execute("insert into pathways(id_path, path_name)"
                       "values ('{}', '{}')".format(getal, pat))
        conn.commit()
        getal += 1
    print("tabel pathways geupdate")


def update_relevance(relevance):
    """
    vult de tabel relevance in de database.
    :param relevance: list - met informatie over de relevantie van een bepaalde metaboliet.
    """
    # getal telt op om de PK en FK te definieren.
    getal = 1
    for rel in relevance[0]:
        place = rel.split(",")
        # checkt of de metaboliet endogenous is.
        if place[0] == "Endogenous" or place[0] == "endogenous":
            # checkt de relevantie van de metaboliet.
            if place[1] == "relevant":
                # voegt vastgestelde informatie toe aan de database.
                cursor.execute("insert into relevance(id_relevance,endogenous, exogenous, relevant)"
                               "values ('{}', TRUE, FALSE, TRUE)".format(getal))
                conn.commit()
            else:
                # voegt vastgestelde informatie toe aan de database.
                cursor.execute("insert into relevance(id_relevance,endogenous, exogenous, relevant)"
                               "values ('{}', TRUE, FALSE, FALSE)".format(getal))
                conn.commit()
        # checkt of de metaboliet een internal standaard is.
        elif place[0] == "Internal standard":
            # voegt vastgestelde informatie toe aan de database.
            cursor.execute("insert into relevance(id_relevance,endogenous, exogenous, relevant)"
                           "values ('{}', NULL, NULL, NULL)".format(getal))
            conn.commit()
        # checkt of de relevantie van de metaboliet nog onbekend is.
        elif place[0] == "Onbekend":
            # voegt vastgestelde informatie toe aan de database.
            cursor.execute("insert into relevance(id_relevance,endogenous, exogenous, relevant)"
                           "values ('{}', NULL, NULL, NULL)".format(getal))
            conn.commit()
        getal += 1
    print("tabel relevance is geupdate")


def update_patients(person_ids):
    """
    vult de tabel met patienten.
    :param person_ids: list - met alle patienten uit het excel bestand.
    """
    # getal telt op om de PK en FK te definieren.
    getal = 1
    for per in person_ids:
        # voegt data toe aan de database
        cursor.execute("insert into Patients(id_patient)"
                       "values ('{}')".format(per))
        conn.commit()
        getal += 1
    print("tabel patients geupdate")


def update_metabolieten(name, desc, hmbd_code):
    """
    vult de tabel metabolieten.
    :param name: list - met alle metabolieten
    :param desc: list - met descriptie van alle metabolieten
    :param hmbd_code: list - met HMDB-codes van alle metabolieten.
    """
    # getal telt op om de PK en FK te definieren.
    getal = 1
    for na in name[0]:
        # voegt data toe aan de database
        cursor.execute("insert into Metabolieten(id_metaboliet, id_origin, id_fluids, name,"
                       " description, HMBD_code, relevance_id_relevance)"
                       "values ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(getal, getal, getal,
                                                                                  na.replace("'", ""),
                                                                                  str(desc[0][getal-1])
                                                                                  .replace("'", ""),
                                                                                  hmbd_code[0][getal - 1], getal))
        conn.commit()
        getal += 1
    print("tabel Metabolieten geupdate")


def update_z_score(lijst_patienten_lijsten):
    """
    vult de tabel met z-scores.
    :param lijst_patienten_lijsten: geneste list - met list van z-scores per patient.
    """
    # number telt op om de de FK van metablieten te definieren.
    number = 1
    for patient in lijst_patienten_lijsten:
        # getal telt op om de PK van z-score te definieren.
        getal = 1
        for score in patient[1]:
            # voegt data toe aan de database
            cursor.execute("insert into Z_scores(z_id, z_score, patients_id_patient, metabolieten_id_metaboliet) "
                           "values ('{}', '{}', '{}', '{}')".format(number, score, patient[0], getal))
            conn.commit()
            getal += 1
            number += 1
    print("tabel Z-scores geupdate")


def update_link_meta_tis(getal):
    """
    vult de tussentabel tussen metabolieten en tissue.
    :param getal: int
    """
    # voegt data toe aan de database
    cursor.execute("insert into Metabolieten_tissue(metabolieten_id_metaboliet, tissue_id_tissue) "
                   "values ('{}', '{}')".format(getal, getal))
    conn.commit()


def update_link_meta_flu(getal):
    """
    vult de tussentabel tussen metabolieten en fluids.
    :param getal: int.
    """
    # voegt data toe aan de database
    cursor.execute("insert into Metabolieten_fluids(metabolieten_id_metaboliet, fluids_id_fluids) "
                   "values ('{}', '{}')".format(getal, getal))
    conn.commit()


def update_link_meta_dis(getal):
    """
    vult de tussentabel tussen metabolieten en diseases
    :param getal: int
    """
    # voegt data toe aan de database
    cursor.execute("insert into Metabolieten_diseases(metabolieten_id_metaboliet, diseases_id_disease) "
                   "values ('{}', '{}')".format(getal, getal))
    conn.commit()


def update_link_meta_ori(getal):
    """
    vult de tussentabel tussen metabolieten en origins.
    :param getal: int
    """
    # voegt data toe aan de database
    cursor.execute("insert into origins_Metabolieten(origins_id_orgins, metabolieten_id_metaboliet) "
                   "values ('{}', '{}')".format(getal, getal))
    conn.commit()


def update_link_meta_path(getal):
    """
    vult de tussentabel tussen metabolieten en pathways.
    :param getal: int
    """
    # voegt data toe aan de database
    cursor.execute("insert into pathways_Metabolieten(pathways_id_path, metabolieten_id_metaboliet) "
                   "values ('{}', '{}')".format(getal, getal))
    conn.commit()


if __name__ == '__main__':
    # connect aan de database
    conn = psycopg2.connect(host="postgres.biocentre.nl", user="BI2_PG1", password="blaat1234",
                            database="bio_jaar_2_pg_1")

    # open een cursor
    cursor = conn.cursor()
    # haalt data op uit script fileReader.py
    flui, tiss, persons, relev, pathw, orig, dise, metabol, descrip, hmdb, lijst_patienten = main()
    # update_fluid(flui)
    # update_tissue(tiss)
    # update_diseases(dise)
    # update_origins(orig)
    # update_paths(pathw)
    # update_relevance(relev)
    # update_Patients(persons)
    # update_Metabolieten(metabol, descrip, hmdb)
    # update_z_score(lijst_patienten)

    # getal telt op om de PK en FK te definieren.
    g = 1
    for nam in metabol[0]:
        # update_link_meta_tis(getal)
        # update_link_meta_flu(getal)
        # update_link_meta_dis(getal)
        # update_link_meta_ori(getal)
        # update_link_meta_path(getal)
        g += 1
    print("tabel link Metabolieten_tissue geupdate")
    print("tabel link Metabolieten_fluids geupdate")
    print("tabel link Metabolieten_diseases geupdate")
    print("tabel link origins_Metabolieten geupdate")
    print("tabel link pathways_Metabolieten geupdate")

    # sluit cursor af.
    conn.close()
