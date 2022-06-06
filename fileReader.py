import pandas as pd


def readFile(file):
    """ Opent het aangeleverde bestand en zet alle inhoud in
    een variabele

    :param
    file - xlsx file - Excel file met patient gegevens
    :return:
    data - String - String met alle informatie uit het ingelezen bestand
    """
    # Inlezen van de file
    data = pd.read_excel(file)
    return data


def getPatientsId(data):
    """ Inlezen van alle patient namen naar een lijst

    :param:
    data - String - String met alle informatie uit het ingelezen bestand
    :return:
    patient_ids - List - lijst met alle patient namen
    first_count - Int - ?
    count - Int - ?
    """
    columns = data.columns
    person_ids = []
    count = 0
    first_count = 0
    for i in columns:
        if first_count == 0:
            count = count + 1
        string_i = str(i)
        # Controleren van de informatie in de eerste rij van de file
        if string_i.startswith("P") and string_i.endswith("Zscore"):
            if first_count == 0:
                first_count = count - 1
            count = count + 1
            # Wanneer het element begint met P (patient) en eindigende
            # op Zscore dan wordt het toegevoegd aan de lijst
            person_ids.append(string_i)
    return person_ids, first_count, count


def getMetabolites(data):
    """ Inlezen van alle namen van metabolieten

    :param:
    data - String - String met alle informatie uit het ingelezen bestand
    :return:
    metabolites - List - Lijst met met alle metaboliet namen
    """
    # Zoeken naar de kolom met als "header" name
    metabolites = data["name"]
    return list(metabolites)


def getDicMetbZscore(data, metabolites, start, stop):
    """ Inlezen van alle z-scores van alle metabolieten voor alle
    patienten

    :param:
    data - String - String met alle informatie uit het ingelezen bestand
    metabolites - List - Lijst met alle metaboliet namen
    start - Int - ?
    stop - Int - ?
    :return:
    dict - Dictonary - Dictionary met alle metaboliet namen en z-scores
    """
    met_dict = {}
    # Zoeken naar de z-scores behorend bij de metabolieten
    for index in range(0, len(metabolites)):
        met_dict[metabolites[index]] = list(data.loc[index])[start:stop]
    return met_dict


def getRelevance(data):
    """ Inlezen van alle gegevens uit de kolom "relevance"

    :param:
    data - String - String met alle informatie uit het ingelezen bestand
    :return:
    relevance - List - Lijst alle waarden uit de kolom "relevance"
    """
    relevance = []
    # Zoeken naar de kolom met als "header" relevance
    rele = data["relevance"]
    relevance.append(list(rele))
    return relevance


def getDescription(data):
    """ Inlezen van alle gegevens uit de kolom "descr" (description)

    :param:
    data - String - String met alle informatie uit het ingelezen bestand
    :return:
    description - List - Lijst met alle gegevens uit de kolom "descr"
    """
    description = []
    # Zoeken naar de kolom met als "header" descr
    desc = data["descr"]
    description.append(list(desc))
    return description


def getOrigin(data):
    """ Inlezen van alle gegevens uit de kolom "origin"

    :param:
    data - String - String met alle informatie uit het ingelezen bestand
    :return:
    origin - List - Lijst met alle gegevens uit de kolom "origin"
    """
    origin = []
    # Zoeken naar de kolom met als "header" origin
    ori = data["origin"]
    origin.append(list(ori))
    return origin


def getFluids(data):
    """ Inlezen van alle gegevens uit de kolom "fluids"

    :param:
    data - String - String met alle informatie uit het ingelezen bestand
    :return:
    fluids - List - Lijst met alle gegevens uit de kolom "fluids"
    """
    fluids = []
    # Zoeken naar de kolom met als "header" fluids
    fluid = data["fluids"]
    fluids.append(list(fluid))
    return fluids


def getTissue(data):
    """ Inlezen van alle gegevens uit de kolom "tissue"

    :param:
    data - String - String met alle informatie uit het ingelezen bestand
    :return:
    tissue - List - Lijst met alle gegevens uit de kolom "tissue"
    """
    tissue = []
    # Zoeken naar de kolom met als "header" tissue
    tiss = data["tissue"]
    tissue.append(list(tiss))
    return tissue


def getDisease(data):
    """ Inlezen van alle gegevens uit de kolom "disease"

    :param:
    data - String - String met alle informatie uit het ingelezen bestand
    :return:
    disease - List - Lijst met alle gegevens uit de kolom "disease"
    """
    disease = []
    # Zoeken naar de kolom met als "header" disease
    dis = data["disease"]
    disease.append(list(dis))
    return disease


def getPathway(data):
    """ Inlezen van alle gegevens uit de kolom "pathway"

    :param:
    data - String - String met alle informatie uit het ingelezen bestand
    :return:
    pathway - List - Lijst met alle gegevens uit de kolom "pathway"
    """
    pathway = []
    # Zoeken naar de kolom met als "header" pathway
    path = data["pathway"]
    pathway.append(list(path))
    return pathway


def getHMDBcode(data):
    """ Inlezen van alle gegevens uit de kolom "HMDB_code"

    :param:
    data - String - String met alle informatie uit het ingelezen bestand
    :return:
    hmdb_code - List - Lijst met alle gegevens uit de kolom "HMDB_code"
    """
    hmdb_code = []
    # Zoeken naar de kolom met als "header" HMDB_code
    code = data["HMDB_code"]
    hmdb_code.append(list(code))
    return hmdb_code


def get_Patient_Z_score(person_ids, data):
    """ Inlezen van alle z-scores per patient

    :param:
    data - String - String met alle informatie uit het ingelezen bestand
    person_ids - List - Lijst met patient namen
    :return:
    dict_patient_zscore - Dictionary - Dictionary met patient namen
     en zscores
    """
    dict_patient_zscore = {}
    # Zoeken naar de patient naam in de data en de bijbehorende
    # z-scores worden toegevoegd aan de dictionary
    for item in person_ids:
        dict_patient_zscore[item] = list(data[item])
    for i in dict_patient_zscore:
        print(f"patient: {i}, {dict_patient_zscore[i]}")
    return dict_patient_zscore


def main():
    # File name
    file = "Dataset/metabolomics.xlsx"
    # Aanroepen van de functie om de file in te lezen
    data = readFile(file)
    # print(data)
    # Aanroepen van de functie, met het meegeven van de ingelezen data
    metabolites = getMetabolites(data)
    # print(metabolites)

    # Aanroepen van de functie, met het meegeven van de ingelezen data
    person_ids, start, stop = getPatientsId(data)
    met_dict = getDicMetbZscore(data, metabolites, start, stop)

    # dictionary met als key patient id en als value lijst met z-scores
    dict_p = get_Patient_Z_score(person_ids, data)
    # print(person_ids)
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
    dict_patient_zscore = get_Patient_Z_score(person_ids, data)

    # Returnen van alle lijsten en dictionary's voor gebruik in
    # andere scripts
    return fluids, tissue, person_ids, relevance, pathway,\
        origin, disease, description, hmdb_code,\
        dict_patient_zscore, met_dict, dict_p
