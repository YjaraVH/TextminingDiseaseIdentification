from nltk.corpus import wordnet
# nltk.download('wordnet')
# nltk.download('omw-1.4')
from Bio import Entrez
import requests
import fileReader

pub_disease = 0  # disease id number
pub_Om = 0  # Omim ID
pub_gene = 0 # gene id
metab = 0  # metabolite key


def get_synonyms(word):
    """ Obtains synonyms from a word and makes one string of them in the
    following format: word1 OR word2 OR word3

    :param word: string, the word we want the synonyms from
    :return: string of the synonyms seperated by " OR "
    """
    synonyms = []
    for syn in wordnet.synsets(word):
        for l in syn.lemmas():
            synonyms.append(l.name())
    stringSyn = str(set(synonyms)).replace("', '", " OR ").replace("{'",
                                                                   "").replace(
        "'}", "")
    if stringSyn == 'set()':
        stringSyn = word
    print(stringSyn)
    return stringSyn


def get_ids_all_pubmed(metabolites,firstround):
    """Puts pubmed id's from artikels containing metabolite in list (idlist).
    Calls function get_title_diseases with as parameter idlist.
    (This is done for all metabolites)

    :param metabolites: list with all metabolites
    """
    global metab
    Entrez.email = 'A.C.Other@example.com'
    for item in metabolites:
        startdate = 2000
        if firstround:
            # This is done to keep count of the metabolites
            metab += 1
            search_w = get_synonyms(item)
        else:
            search_w = item
        handle = Entrez.esearch(db='pubmed',
                                term=f"{search_w}[Title/Abstract]",
                                mindate=f'{startdate}/01/01')
        record = Entrez.read(handle)
        handle.close()
        idlist = record["IdList"]
        print(f">>>{item}<<<<<")
        # To obtain information from the articles
        get_title_diseases(idlist,firstround)


def get_title_diseases(ids,firstround):
    """ Uses Pubtator to obtain data from pubmed articles.
    Calls info_per_article with as parameter the raw data

    :param ids: list with PMIDs
    """
    # pubtator parameters
    global pub_gene
    Format = "pubtator"
    Type = "pmids"
    if firstround:
        Bioconcepts = "disease,gene"
    else:
        Bioconcepts = "disease"
    identities = ''.join([str(elem + ",") for elem in ids])

    # web queri
    r = requests.get(
        f"https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/{Format}?{Type}={identities[0:len(identities) - 1]}&concepts={Bioconcepts}")

    print(
        f"https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/{Format}?{Type}={identities[0:len(identities) - 1]}&concepts={Bioconcepts}")

    if str(r) == "<Response [200]>":
        # to get the wanted information out the data of the pubmed articles
        if firstround == True:
            info_per_article_plus_gene(r.text.split("\n"),firstround)
        else:
            #pub_gene += 1
            info_per_article(r.text.split("\n"),firstround)
    else:
        print("Request was unsuccesfull")


def info_per_article_plus_gene(info,firstround):  ##########optioneel
    """ Obtains the wanted information out the data from Pubtator,
    and calls the functions to places this data correctly in the database

    :param info: list, with the data output from Pubtator
    """
    # to keep count of the articles
    global pub_Om
    # to keep count of the diseases
    global pub_disease

    # dictionary with as key PUMID, and values title (string)
    # and diseases (list)
    articles = {}
    diseases = []
    genes = []
    # Medical Subject Headings (MeSH)
    mushs = {}
    title = ""
    id_n = ""
    for item in info:
        # PMID
        id = item[0:8]
        if id == "" and title != "":
            if not diseases == [] or not genes == []:  # and genes is empty!!!
                pub_Om += 1

                # primary key PubOm
                id_pum_om = pub_Om
                PMID = id_n
                article_name = title
                # fill pubOM table (database)
                fill_PubOM(id_pum_om, PMID, article_name)

                # Obtain how frequent a diseases occurs in text
                if not diseases == []:
                    # fills pub_disease
                    diseases_freq_article(diseases, mushs,firstround)
                    if not genes == []:
                        genes_freq_article(genes)
                else:
                    genes_freq_article(genes)
                articles[id_n] = [title, diseases]
                diseases = []
                genes = []
        if item[9:11] == "t|":
            # obtain article title
            title = item.split("t|")[1]
        elif item.startswith(f"{id}\t"):
            # obtain diseases and MeSH
            items = item.split("\t")
            if items[4] == "Gene":
                genes.append(items[3])
            else:
                if items[5] == "":
                    mesh = "NULL"
                else:
                    mesh = items[5][5:]
                mushs[item.split("\t")[3].lower()] = mesh
                diseases.append(item.split("\t")[3].lower())
        id_n = item[0:8]


def info_per_article(info,firstround):
    """ Obtains the wanted information out the data from Pubtator,
    and calls the functions to places this data correctly in the database

    :param info: list, with the data output from Pubtator
    """
    # to keep count of the articles
    global pub_Om
    # to keep count of the diseases
    global pub_disease
    # to keep count of the genes
    global pub_gene

    # dictionary with as key PUMID, and values title (string)
    # and diseases (list)
    articles = {}
    diseases = []
    # Medical Subject Headings (MeSH)
    mushs = {}
    title = ""
    id_n = ""
    for item in info:
        # PMID
        id = item[0:8]
        if id == "" and title != "":
            if not diseases == []:
                pub_Om += 1

                # primary key PubOm
                id_pum_om = pub_Om
                PMID = id_n
                article_name = title
                # fill pubOM table (database)
                if firstround:
                    fill_PubOM(id_pum_om, PMID, article_name)
                else:
                    fill_PubOM_Gene(id_pum_om, PMID, article_name)

                # Obtain how frequent a diseases occurs in text
                # fills pub_disease
                diseases_freq_article(diseases, mushs,firstround)

                articles[id_n] = [title, diseases]
                diseases = []
        if item[9:11] == "t|":
            # obtain article title
            title = item.split("t|")[1]
        elif item.startswith(f"{id}\t"):
            # obtain diseases and MeSH
            items = item.split("\t")
            if items[5] == "":
                mesh = "NULL"
            else:
                mesh = items[5][5:]
            mushs[item.split("\t")[3].lower()] = mesh
            diseas = item.split("\t")[3].lower()

            # Om rekening te houden met meervoud en eenvoud
            if diseas.endswith("s"):
                diseases.append(diseas[0:len(diseas)-1])
            else:
                diseases.append(diseas)
        id_n = item[0:8]



def genes_freq_article(genes):
    """ Makes an dictionary with as key the disease and value the number of
    times that diseases was found in the article. And calls the function
    fill_pub_disease with as parameters counts (dict) and mushs (dict)

    :param diseases: list with diseases in article
    :param mushs: disctionary with diseases + MuSH
    """
    counts = {}
    for gene in genes:
        counts[gene] = counts.get(gene, 0) + 1
    # fills pub_disease
    fill_pub_gene(counts)

def diseases_freq_article(diseases, mushs,firstround):
    """ Makes an dictionary with as key the disease and value the number of
    times that diseases was found in the article. And calls the function
    fill_pub_disease with as parameters counts (dict) and mushs (dict)

    :param diseases: list with diseases in article
    :param mushs: disctionary with diseases + MuSH
    """
    counts = {}
    for disease in diseases:
        counts[disease] = counts.get(disease, 0) + 1
    # fills pub_disease
    fill_pub_disease(counts, mushs,firstround)


def fill_pub_disease(diseases_counts, mushs,firstround):
    global pub_disease
    global pub_gene
    for key, value in diseases_counts.items():  # werkt dan niet met een primary key??!! of zo lijkt het
        pub_disease += 1
        if firstround:
             print(
                 f"pubOm: {pub_Om}, disease:{key}, count:{value}, MESH_code: {mushs.get(key)},Gene_id:NULL, pub_disea:{pub_disease}")
        else:
            print(
                f"pubOm: {pub_Om}, disease:{key}, count:{value}, MESH_code: {mushs.get(key)},Gene_id:{pub_gene}, pub_disea:{pub_disease}")


def fill_pub_gene(gene_count):
    global pub_gene
    keys_del = []
    for key, value in gene_count.items():  # werkt dan niet met een primary key??!! of zo lijkt het
        if value < 3:
            keys_del.append(key)
        else:
            pub_gene += 1
            print(f"{key}")
            print(
                f"pubOm: {pub_Om}, gene:{key}, count:{value}, gene:{pub_gene}")
    for item in keys_del:
        del gene_count[item]
    if gene_count:
        get_ids_all_pubmed(list(gene_count.keys()), False)


def fill_pub_gene_V(gene_count):
    global pub_gene
    for key, value in gene_count.items():  # werkt dan niet met een primary key??!! of zo lijkt het
        print(f"{key}")
        print(
            f"pubOm: {pub_Om}, gene:{key}, count:{value}, gene:{pub_gene + 1}")
    get_ids_all_pubmed(list(gene_count.keys()), False)

def fill_PubOM(id_pum_om, PMID, article_name):
    print(f"Voor de metabolieten met artikel")
    print(f"id={id_pum_om} PMID={PMID} Metab:{metab} article={article_name}")

def fill_PubOM_Gene(id_pum_om, PMID, article_name):
    print(f"Voor de genen met artikel")
    print(f"id={id_pum_om} PMID={PMID} Metab:{metab} article={article_name}")

def start_textmining(metabolieten):
    get_ids_all_pubmed(metabolieten, True)
    print("klaar")


if __name__ == '__main__':
    from time import gmtime, strftime




    file = "Dataset/Untargeted_metabolomics.xlsx"
    data = fileReader.readFile(file)
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))

    metabolieten = fileReader.getMetabolites(data)
    # metabolieten = ["1,3-Diaminopropane","2-Ketobutyric acid","2-Hydroxybutyric acid"]
    # metabolieten = [ "Palmitoyl Serinol","Ethyl 2-hydroxyisovalerate", "8-oxo-dGDP"]
    #metabolieten = ["2-Ketobutyric acid"]

    get_ids_all_pubmed(metabolieten,True)
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))

