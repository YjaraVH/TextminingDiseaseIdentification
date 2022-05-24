import pandas as pd

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
    return patient1


if __name__ == '__main__':
    #File name
    file = "Dataset/Untargeted_metabolomics.xlsx"
    data = readFile(file)
    metabolites = getMetabolites(data)
    person_ids, start, stop = getPatientsId(data)
    dict = getDicMetbZscore(data, metabolites, start, stop)
    #print best wel veel uit, maar dan kun je even kijken hoe het eruit ziet:)
    # printDictionary(dict)

    # print(person_ids)
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
    patient1 = getPatient1(data)
    print(patient1)
