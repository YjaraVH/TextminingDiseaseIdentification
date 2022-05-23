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
        maxDate = 2022
        date = startdate
        handle = Entrez.esearch(db='pubmed', term=f"{get_synonyms(item)}[Title/Abstract]",
                                mindate=f'{date}/01/01',
                                maxdate=f'{maxDate}/12/31')
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

    #!!!
    print("print one of them")
    print(articles["32866201"])





if __name__ == '__main__':
   # metabolieten = ["1,3-Diaminopropane","2-Ketobutyric acid","2-Hydroxybutyric acid"]
    metabolieten = ["2-Ketobutyric acid"]
    get_ids_all_pubmed(metabolieten)

    #get_title_diseases()