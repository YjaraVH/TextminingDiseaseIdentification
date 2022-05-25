import threading
import time
from datetime import datetime
import re
import nltk
from nltk.corpus import wordnet
#nltk.download('wordnet')
#nltk.download('omw-1.4')
from Bio import Entrez
import urllib

import requests
import io
import json
import sys


import fileReader
def obtain_info_single_article():
    # submit request
    Format = "pubtator"
    Type = "pmids"
    Identifiers = ['35432460', '35049836', '34948323']
    Bioconcepts = "disease"
    trest = ''.join([str(elem + ",") for elem in Identifiers]) #trest[0:len(trest)-1]
    ident = "35432460"


    test = f"https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/{Format}?{Type}={ident}&concepts={Bioconcepts}"
    print(test)
    r = requests.get(
        f"https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/{Format}?{Type}={ident}&concepts={Bioconcepts}")
    print(r)
    print(">>>>>>>>>>")
    print(r.text.split(ident))
    diseases = []
    for item in r.text.split(ident):
        if item.startswith("|t|"):
            title = item[3:len(item)-1]
        elif item.startswith("\t"):
            diseases.append(item.split("\t")[3])
    print(title)
    print(diseases)


#Abstract gene, Geïndexeerd met Medical Subject Headings (MeSH)
def get_title_diseases(ids):
    # submit request
    Format = "pubtator"
    Type = "pmids"
    Identifiers = ['35432460', '35049836', '34948323']
    Bioconcepts = "disease"
    #trest = ''.join([str(elem + ",") for elem in Identifiers]) #trest[0:len(trest)-1]
    ident = "35432460"
    identities = ''.join([str(elem + ",") for elem in ids])


    test = f"https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/{Format}?{Type}={identities[0:len(identities)-1]}&concepts={Bioconcepts}"
    print(test)
    r = requests.get(
        f"https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/{Format}?{Type}={identities[0:len(identities)-1]}&concepts={Bioconcepts}")
    print(r)
   # print(">>>>>>>>>>")
    #print(r.text)
    info_per_article(r.text.split("\n"))
    return r.text.split("\n")



def get_synonyms(word):
    synonyms = []

    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms.append(l.name())
    stringSyn = str(set(synonyms)).replace("', '", " OR ").replace("{'",
                                                                   "").replace(
        "'}", "")
    if stringSyn == 'set()':
        stringSyn = word
    return stringSyn

def get_ids(combie):
    startdate = 2000
    maxDate = 2022
    date = startdate
    handle = Entrez.esearch(db='pubmed', term=f"{combie}[Title/Abstract]",
                            mindate=f'{date}/01/01',
                            maxdate=f'{maxDate}/12/31')
    record = Entrez.read(handle)
    handle.close()
    idlist = record["IdList"]
    return idlist

def get_ids_all_pubmed(metabolites):
    Entrez.email = 'A.C.Other@example.com'
    for item in metabolites:
        startdate = 2000
        #maxDate = 2022
        date = startdate
        handle = Entrez.esearch(db='pubmed', term=f"{get_synonyms(item)}[Title/Abstract]",
                                mindate=f'{date}/01/01') #maxdate=f'{maxDate}/12/31'
        record = Entrez.read(handle)
        handle.close()
        idlist = record["IdList"]
        print(f">>>{item}<<<<<")
        get_title_diseases(idlist)
       # return idlist

def info_per_article(info):
    articles = {}
    diseases = []
    title = ""
    id_n = ""
    id = ""
    print("########################")
    for item in info:
        id = item[0:8]
        if id == "" and title != "":
            articles[id_n] = [title,diseases]
            diseases = []
        if item[9:11] == "t|":
            title = item.split("t|")[1]
        elif item.startswith(f"{id}\t"):
            diseases.append(item.split("\t")[3])
        id_n = item[0:8]

    for key, value in articles.items():
        print(key, ':', value)
    #!!!
   # print("print one of them")
   # print(articles["32866201"])


def ophalen():
    data = fileReader.readFile("Untargeted_metabolomics.xlsx")
    # print(person_ids)
    metabolieten = fileReader.getMetabolieten(data)
    # print(metabolieten)
    relevance = fileReader.getRelevance(data)
    # print(relevance)
    description = fileReader.getDescription(data)
    # print(description)
    origin = fileReader.getOrigin(data)
    # print(origin)
    fluids = fileReader.getFluids(data)
    # print(fluids)
    disease = fileReader.getDisease(data)
    # print(disease)
    pathway = fileReader.getPathway(data)
    # print(pathway)
    hmdb_code = fileReader.getHMDBcode(data)
    # print(hmdb_code)
    patient1 = fileReader.getPatient1(data)
    # print(patfileReader.ent1)
    patient2 = fileReader.getPatient2(data)
    # print(patfileReader.gent2)
    patient3 = fileReader.getPatient3(data)
    # print(patfileReader.gent3)
    patient4 = fileReader.getPatient4(data)
    # print(patfileReader.gent4)
    patient5 = fileReader.getPatient5(data)
    # print(patfileReader.gent5)
    patient6 = fileReader.getPatient6(data)
    # print(patfileReader.gent6)
    patient7 = fileReader.getPatient7(data)
    # print(patfileReader.gent7)
    patient8 = fileReader.getPatient8(data)
    # print(patfileReader.gent8)
    patient9 = fileReader.getPatient9(data)
    # print(patfileReader.ent9)
    patient10 =fileReader.getPatient10(data)
    # print(patfileReader.ent10)
    patient11 =fileReader.getPatient11(data)
    # print(patfileReader.ent11)
    patient12 =fileReader.getPatient12(data)
    # print(patfileReader.ent12)
    patient13 =fileReader.getPatient13(data)
    # print(patfileReader.ent13)
    patient14 =fileReader.getPatient14(data)
    # print(patfileReader.ent14)
    patient15 =fileReader.getPatient15(data)
    # print(patfileReader.ent15)
    patient16 =fileReader.getPatient16(data)
    # print(patfileReader.ent16)
    patient17 =fileReader.getPatient17(data)
    # print(patfileReader.ent17)
    patient18 =fileReader.getPatient18(data)
    # print(patfileReader.ent18)
    patient19 =fileReader.getPatient19(data)
    # print(patfileReader.ent19)
    patient20 =fileReader.getPatient20(data)
    # print(patfileReader.ent20)
    patient21 =fileReader.getPatient21(data)
    # print(patfileReader.ent21)
    patient22 =fileReader.getPatient22(data)
    # print(patfileReader.ent22)
    patient23 =fileReader.getPatient23(data)
    # print(patfileReader.ent23)
    patient24 =fileReader.getPatient24(data)
    # print(patfileReader.ent24)
    patient25 =fileReader.getPatient25(data)
    # print(patfileReader.ent25)
    patient26 =fileReader.getPatient26(data)
    # print(patfileReader.ent26)
    patient27 =fileReader.getPatient27(data)
    # print(patfileReader.ent27)
    patient28 =fileReader.getPatient28(data)
    # print(patfileReader.ent28)
    patient29 =fileReader.getPatient29(data)
    # print(patfileReader.ent29)
    patient30 =fileReader.getPatient30(data)
    # print(patfileReader.ent30)
    patient31 =fileReader.getPatient31(data)
    # print(patient31)

    lijst_patienten_lijsten = [patient1, patient2, patient3, patient4,
                               patient5, patient6, patient7, patient8,
                               patient9, patient10, patient11, patient12,
                               patient13, patient14, patient15, patient16,
                               patient17, patient18, patient19, patient20,
                               patient21, patient22, patient23, patient24,
                               patient25, patient26, patient27, patient28,
                               patient29, patient30, patient31]


if __name__ == '__main__':





    metabolieten = ["1,3-Diaminopropane","2-Ketobutyric acid","2-Hydroxybutyric acid"]
    #metabolieten = ["2-Ketobutyric acid"]
    get_ids_all_pubmed(metabolieten)

    #get_title_diseases()