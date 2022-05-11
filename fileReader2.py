import pandas as pd

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
    return person_ids,firstCount,count

def readFile(file):
    data = pd.read_excel(file)
    return data

def getMetabolites(data):
    metabolites = data["name"]
    return list(metabolites)

def getDicMetbZscore(data,metabolieten,start,stop):
    dict = {}
    for index in range(0,len(metabolieten)):
        dict[metabolieten[index]] = list(data.loc[index])[start:stop]
    return dict

def printDictionary(dict):
    for item in dict:
        print("key: {}, Value {}".format(item,dict[item]))

if __name__ == '__main__':
    #File name
    file = "metabolomics.xlsx"
    #file = 'Compounds_DIMS_HEXA.xlsx'

    data = readFile(file)
    metabolieten = getMetabolites(data)
    person_ids,start,stop = getPatientsId(data)

    dict = getDicMetbZscore(data,metabolieten,start,stop)

    #print best wel veel uit, maar dan kun je even kijken hoe het eruit ziet:)
    printDictionary(dict)
