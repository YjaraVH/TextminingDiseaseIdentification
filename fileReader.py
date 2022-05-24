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


def getPatient2(data):
    patient2 = []
    zscores = data["P1003.1_Zscore"]
    patient2.append(list(zscores))
    return patient2


def getPatient3(data):
    patient3 = []
    zscores = data["P1005.1_Zscore"]
    patient3.append(list(zscores))
    return patient3


def getPatient4(data):
    patient4 = []
    zscores = data["P1005.2_Zscore"]
    patient4.append(list(zscores))
    return patient4


def getPatient5(data):
    patient5 = []
    zscores = data["P2021M01703.1_Zscore"]
    patient5.append(list(zscores))
    return patient5


def getPatient6(data):
    patient6 = []
    zscores = data["P2021M01743.1_Zscore"]
    patient6.append(list(zscores))
    return patient6


def getPatient7(data):
    patient7 = []
    zscores = data["P2021M01865.1_Zscore"]
    patient7.append(list(zscores))
    return patient7


def getPatient8(data):
    patient8 = []
    zscores = data["P2021M01871.1_Zscore"]
    patient8.append(list(zscores))
    return patient8


def getPatient9(data):
    patient9 = []
    zscores = data["P2021M01896.1_Zscore"]
    patient9.append(list(zscores))
    return patient9


def getPatient10(data):
    patient10 = []
    zscores = data["P2021M01902.1_Zscore"]
    patient10.append(list(zscores))
    return patient10


def getPatient11(data):
    patient11 = []
    zscores = data["P2021M01906.1_Zscore"]
    patient11.append(list(zscores))
    return patient11


def getPatient12(data):
    patient12 = []
    zscores = data["P2021M01908.1_Zscore"]
    patient12.append(list(zscores))
    return patient12


def getPatient13(data):
    patient13 = []
    zscores = data["P2021M01912.1_Zscore"]
    patient13.append(list(zscores))
    return patient13


def getPatient14(data):
    patient14 = []
    zscores = data["P2021M01918.1_Zscore"]
    patient14.append(list(zscores))
    return patient14


def getPatient15(data):
    patient15 = []
    zscores = data["P2021M01932.1_Zscore"]
    patient15.append(list(zscores))
    return patient15


def getPatient16(data):
    patient16 = []
    zscores = data["P2021M01951.1_Zscore"]
    patient16.append(list(zscores))
    return patient16


def getPatient17(data):
    patient17 = []
    zscores = data["P2021M01956.1_Zscore"]
    patient17.append(list(zscores))
    return patient17


def getPatient18(data):
    patient18 = []
    zscores = data["P2021M01958.1_Zscore"]
    patient18.append(list(zscores))
    return patient18


def getPatient19(data):
    patient19 = []
    zscores = data["P2021M01962.1_Zscore"]
    patient19.append(list(zscores))
    return patient19


def getPatient20(data):
    patient20 = []
    zscores = data["P2021M01971.1_Zscore"]
    patient20.append(list(zscores))
    return patient20


def getPatient21(data):
    patient21 = []
    zscores = data["P2021M01973.1_Zscore"]
    patient21.append(list(zscores))
    return patient21


def getPatient22(data):
    patient22 = []
    zscores = data["P2021M01981.1_Zscore"]
    patient22.append(list(zscores))
    return patient22


def getPatient23(data):
    patient23 = []
    zscores = data["P2021M01984.1_Zscore"]
    patient23.append(list(zscores))
    return patient23


def getPatient24(data):
    patient24 = []
    zscores = data["P2021M01990.1_Zscore"]
    patient24.append(list(zscores))
    return patient24


def getPatient25(data):
    patient25 = []
    zscores = data["P2021M02023.1_Zscore"]
    patient25.append(list(zscores))
    return patient25


def getPatient26(data):
    patient26 = []
    zscores = data["P2021M02031.1_Zscore"]
    patient26.append(list(zscores))
    return patient26


def getPatient27(data):
    patient27 = []
    zscores = data["P2021M02035.1_Zscore"]
    patient27.append(list(zscores))
    return patient27


def getPatient28(data):
    patient28 = []
    zscores = data["P2021M02040.1_Zscore"]
    patient28.append(list(zscores))
    return patient28


def getPatient29(data):
    patient29 = []
    zscores = data["P2021M02052.1_Zscore"]
    patient29.append(list(zscores))
    return patient29


def getPatient30(data):
    patient30 = []
    zscores = data["P2021M02098.1_Zscore"]
    patient30.append(list(zscores))
    return patient30


def getPatient31(data):
    patient31 = []
    zscores = data["P2021M02101.1_Zscore"]
    patient31.append(list(zscores))
    return patient31


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