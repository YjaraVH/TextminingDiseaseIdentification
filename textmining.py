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


pub_disease = 0   #disease id number
pub_Om = 0 #Omim ID
metab = 0 #metabolite key






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
        date = startdate
        handle = Entrez.esearch(db='pubmed', term=f"{get_synonyms(item)}[Title/Abstract]",
                                mindate=f'{date}/01/01')
        record = Entrez.read(handle)
        handle.close()
        idlist = record["IdList"]
        print(f">>>{item}<<<<<")

        global metab
        metab +=1
        get_title_diseases(idlist)

#Abstract gene, Geïndexeerd met Medical Subject Headings (MeSH)
def get_title_diseases(ids):
    # submit request
    Format = "pubtator"
    Type = "pmids"
    Bioconcepts = "disease"
    identities = ''.join([str(elem + ",") for elem in ids])

    r = requests.get(
        f"https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/{Format}?{Type}={identities[0:len(identities)-1]}&concepts={Bioconcepts}")

    #print(r)

    info_per_article(r.text.split("\n"))
    return r.text.split("\n")

def info_per_article(info):
    global pub_disease
    global pub_Om
    articles = {}
    diseases = []
    mushs = {}
    title = ""
    id_n = ""
    id = ""
    for item in info:
        id = item[0:8]
        if id == "" and title != "":
            if not diseases == []:
                pub_Om +=1
                metab_key = metab   #secondary key Metabolieten
                id_pum_om = pub_Om  #primary key PubOm
                PMID = id_n
                article_name = title

                #fill pubOM table (database)
                fill_PubOM(id_pum_om, PMID, article_name)

                # Obtain how frequent an diseases occurs in text
                diseases_freq_article(diseases, mushs)

                #adds key, article and diseases to dict
                articles[id_n] = [title,diseases]
                ##hier vullen we gelijk de table pubmed (database)
                diseases = []
        if item[9:11] == "t|":
            title = item.split("t|")[1]
        elif item.startswith(f"{id}\t"):
            items = item.split("\t")
            if items[5] == "":
                mesh = "NULL"
            else:
                pub_disease += 1
                mesh = items[5][5:]
            mushs[item.split("\t")[3].lower()] = mesh
            diseases.append(item.split("\t")[3].lower())
        id_n = item[0:8]

def diseases_freq_article(diseases,mushs):
    counts = {}
    for disease in diseases:
        counts[disease] = counts.get(disease,0)+1
    fill_pub_disease(counts,mushs)


def fill_pub_disease(diseases_counts,mushs):
    for key, value in diseases_counts.items(): #werkt dan niet met een primary key??!! of zo lijkt het
       print(f"pubO: {pub_Om}, disease:{key}, count:{value}, MESH_code: {mushs.get(key)}")

def fill_PubOM(id_pum_om,PMID,article_name):
    print(">>>PubOM<<<<")
    print(f"id={id_pum_om} PMID={PMID} Metab:{metab} article={article_name}")

if __name__ == '__main__':
    metabolieten = ["1,3-Diaminopropane","2-Ketobutyric acid","2-Hydroxybutyric acid"]
    #metabolieten = ["2-Ketobutyric acid"]
    get_ids_all_pubmed(metabolieten)