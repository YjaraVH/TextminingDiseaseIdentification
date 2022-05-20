from fileReader2.py import dict

def insert_database():
    """
    Voegt de informatie die uit de resultaten van BLAST
    gehaald zijn toe aan de database.
    :return:
    """

    print(dict)
    # import MYSQL connectie package
    import mysql.connector

    # connect aan de database
    conn = mysql.connector.connect(host="....",
                                   user="....", db="....")

    # open een cursor
    cursor = conn.cursor()
    getal = 0
    # voer een query uit voor tabel micro-organisms
    for i in info:
        getal += 1
        cursor.execute("insert into micro_organisms(name_organsim, "
                       "identitiy_percentage, accession_number, "
                       "E_value, species_id, header, function_id)"
                       "values ('{}', '{}', '{}', '{}', '{}', '{}',"
                       " '{}')").format(i[5], i[1], i[0],
                                        i[2], getal, i[4], getal)

    # voer een query uit voor tabel protein_functions
    for i in protein_data:
        getal += 1
        split = i.split(":")
        description = i[1]
        cursor.execute("insert into protein_functions (function_id, "
                       "function_description, biological_domain, "
                       "biological_process) values ('{}', '{}', '{}',"
                       " '{}')").format(getal, description, ..., ...)

    # voer een query uit voor tabel reads
    for i in info:
        cursor.execute("insert into reads(header, read, reliablity) "
                       "values ('{}', '{}', '{}')").format(i[4], i[3],
                                                           ...)
    for x in qscores:
        cursor.execute("insert into reads(header, read, reliablity) "
                       "values ('{}', '{}', '{}')").format(i[4], i[3],
                                                           x)

    # voer een query uit voor tabel species_info
    for i in taxonomy_data:
        getal += 1
        pieces = i.split(",")
        species = i[1]
        cursor.execute(
            "insert into species_info (species, genus_id, species_id) "
            "values ('{}', '{}', '{}')").format(species, getal, getal)

    # voer een query uit voor tabel genus_info
    for i in taxonomy_data:
        getal += 1
        pieces = i.split(",")
        genus = i[2]
        cursor.execute(
            "insert into genus_info (genus, family_id, genus_id) "
            "values ('{}', '{}', '{}')").format(genus, getal, getal)

    # voer een query uit voor tabel family_info
    for i in taxonomy_data:
        getal += 1
        pieces = i.split(",")
        family = i[3]
        cursor.execute(
            "insert into family_info (family, family_id) "
            "values ('{}', '{}')").format(family, getal)

    conn.commit()

    if __name__ == '__main__':
        insert_database()

