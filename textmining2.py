import nltk
import psycopg2
from nltk.corpus import wordnet
#nltk.download('wordnet')
#nltk.download('omw-1.4')
from Bio import Entrez
import requests
import fileReader

# Connect aan de database
conn = psycopg2.connect(host="postgres.biocentre.nl", user="BI2_PG1",
                        password="blaat1234",
                        database="bio_jaar_2_pg_1", port="5900")
# Open een cursor
cursor = conn.cursor()

pub_disease = 0  # disease id number
pub_Om = 0  # Omim ID
pub_gene = 0 # gene id
metab = 0  # metabolite key

# For the database (Foreign keys)
FK_metaboliet = []
FK_pub_gene = []
FK_pub_disease = []
FK_pub_disease2 = []


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
            print(f"metaboliet: {metab}")
            search_w = get_synonyms(item)
        else:
            search_w = item
        handle = Entrez.esearch(db='pubmed',
                                term=f"{search_w}[Title/Abstract]",
                                mindate=f'{startdate}/01/01')
        record = Entrez.read(handle)
        handle.close()
        idlist = record["IdList"]
        get_title_diseases(idlist, firstround)


def get_title_diseases(ids,firstround):
    """ Uses Pubtator to obtain data from pubmed articles.
    Calls info_per_article with as parameter the raw data

    :param ids: list with PMIDs
    """
    # Pubtator parameters
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
            info_per_article(r.text.split("\n"),firstround)
    else:
        print("Request was unsuccesfull")


def info_per_article_plus_gene(info,firstround):
    """ Obtains the wanted information out the data from Pubtator,
    and calls the functions to places this data correctly in the database

    :param info: list, with the data output from Pubtator
    """
    # to keep count of the articles
    global pub_Om
    # to keep count of the diseases
    global pub_disease

    # Dictionary with as key PUMID, and values title (string)
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

                # Fill pubOM table (database)
                fill_PubOM(id_pum_om, PMID, article_name)

                # Obtain how frequent a diseases occurs in text
                if not diseases == []:
                    # Fills pub_disease
                    diseases_freq_article(diseases, mushs,firstround)
                    if not genes == []:
                        genes_freq_article(genes)
                else:
                    genes_freq_article(genes)
                articles[id_n] = [title, diseases]
                diseases = []
                genes = []
        if item[9:11] == "t|":
            # Obtain article title
            title = item.split("t|")[1]
        elif item.startswith(f"{id}\t"):
            # Obtain diseases and MeSH
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


def info_per_article(info, firstround):
    """ Obtains the wanted information out the data from Pubtator,
    and calls the functions to places this data correctly in the database

    :param info: list, with the data output from Pubtator
    """
    # To keep count of the articles
    global pub_Om
    # To keep count of the diseases
    global pub_disease
    # To keep count of the genes
    global pub_gene

    # Dictionary with as key PUMID, and values title (string)
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

                # Primary key PubOm
                id_pum_om = pub_Om
                PMID = id_n
                article_name = title

                # Fill pubOM table (database)
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
            # Obtain article title
            title = item.split("t|")[1]
        elif item.startswith(f"{id}\t"):
            # Obtain diseases and MeSH
            items = item.split("\t")
            if items[5] == "":
                mesh = "NULL"
            else:
                mesh = items[5][5:]
            mushs[item.split("\t")[3].lower()] = mesh
            diseas = item.split("\t")[3].lower()

            # To take into account singular and plural words
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
    # Fills pub_disease
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
    # Fills pub_disease
    fill_pub_disease(counts, mushs,firstround)


def fill_pub_disease(diseases_counts, mushs,firstround):
    """ Fills the table pub_disease (database)

    :param diseases_counts: dict- with as key disease and value count
    :param mushs: dict- with as key disease and value MesH code
    :param firstround: bool- true if firstround else false
    """
    global pub_disease
    global pub_gene
    global FK_pub_disease
    global FK_pub_disease2
    for key, value in diseases_counts.items():
        pub_disease += 1
        # Difference first and second round
        # because there are different foreign keys to take into account
        if firstround:
             cursor.execute("insert into pub_disease(id_article, disease, count, MESH_code) "
                            "values ('{}', '{}', '{}', '{}')".format(pub_disease, key.replace("'", ""), value, mushs.get(key)))
             conn.commit()
             # Keys pub_Om and pub_disease
             FK_pub_disease.append([pub_Om, pub_disease])
        else:
            cursor.execute("insert into pub_disease(id_article, disease, count, MESH_code) "
                           "values ('{}', '{}', '{}', '{}')".format(pub_disease, key.replace("'",""), value, mushs.get(key)))
            conn.commit()
            # Keys pub_gene and pub_disease
            FK_pub_disease2.append([pub_gene, pub_disease])

def fill_pub_gene(gene_count):
    """ Fills the table pub_genes (database)

    :param gene_count: dict- with as key gene and value count
    """
    global pub_gene
    keys_del = []
    global FK_pub_gene
    for key, value in gene_count.items():
        # Genes which are found less than 5 times in the title or abstract
        # of article are deleted
        if value < 5:
            # keys (genes) to deleted/remove
            keys_del.append(key)
        else:
            pub_gene += 1
            cursor.execute("insert into pub_genes(id_artikel, genes, count) "
                           "values ('{}', '{}', '{}')".format(pub_gene, key.replace("'", ""), value))
            conn.commit()
            # Keys pub_Om and pub_disease
            FK_pub_gene.append([pub_Om, pub_gene])
    for item in keys_del:
        del gene_count[item]
    if gene_count:
        # Second round get_ids_all_pubmed
        get_ids_all_pubmed(list(gene_count.keys()), False)



def fill_PubOM(id_pum_om, PMID, article_name):
    """Fills the table pubOm (database)
    (fistround) article obtained with as pubmed input a metabolite

    :param id_pum_om: int- primary key
    :param PMID: str- PMID
    :param article_name: str- name article
    """
    global FK_metaboliet

    cursor.execute("insert into PubOm(id_pum_om, PMID, article_name) "
                   "values ('{}', '{}', '{}')".format(id_pum_om, PMID, article_name.replace("'", "")))
    conn.commit()
    # Keys metab and id_pum_om
    FK_metaboliet.append([metab, id_pum_om])


def fill_PubOM_Gene(id_pum_om, PMID, article_name):
    """Fills the table pubOm (database)
    (secondround) article obtained with as pubmed input a gene

        :param id_pum_om: int- primary key
        :param PMID: str- PMID
        :param article_name: str- name article
        """
    cursor.execute("insert into pubom(id_pum_om, pmid, article_name) "
                   "values ('{}', '{}', '{}')".format(id_pum_om, PMID, article_name.replace("'", "")))
    conn.commit()
    print("tabel pubOM2 is gevuld")

def fill_pubOM_pub_genes():
    """
    Fills connecting table (keys) pubom_pub_genes
    """
    global FK_pub_gene
    for pub in FK_pub_gene:
        cursor.execute("insert into Pubom_pub_genes(pubom_id_pum_om, pub_genes_id_artikel) "
                       "values ('{}', '{}')".format(pub[0], pub[1]))
        conn.commit()
    print("tussen tabel pubom pub genes gevuld")


def fill_pub_disease_pubom():
    """
    Fills connecting table (keys) pub_disease_pubom
    """
    global FK_pub_disease
    for pub in FK_pub_disease:
        cursor.execute("insert into pub_disease_pubom(pub_disease_id_article, pubom_id_pum_om) "
                       "values ('{}', '{}')".format(pub[1], pub[0]))
        conn.commit()
    print("tussen tabel pubom pub disease gevuld")


def fill_pub_disease_pub_genes():
    """
    Fills connecting table (keys) pub_disease_pub_genes
    """
    global FK_pub_disease2
    for pub in FK_pub_disease2:
        cursor.execute("insert into pub_disease_pub_genes(pub_disease_id_article, pub_genes_id_artikel) "
                       "values ('{}', '{}')".format(pub[1], pub[0]))
        conn.commit()
    print("tussen tabel pub genes pub disease gevuld")


def fill_pubom_metabolieten():
    """
    Fills connecting table (keys) metabolieten_pubom
    """
    global FK_metaboliet
    for pub in FK_metaboliet:
        cursor.execute("insert into metabolieten_pubom(metabolieten_id_metaboliet, pubom_id_pum_om) "
                       "values ('{}', '{}')".format(pub[0], pub[1]))
        conn.commit()
    print("tussen tabel metabolieten pubom gevuld")


def fill_tussentabellen():
    """
    Calls function to fill connecting tables (keys)
    """
    fill_pubOM_pub_genes()
    fill_pub_disease_pubom()
    fill_pub_disease_pub_genes()
    fill_pubom_metabolieten()
    print("Klaar met textminen!!!")
    conn.close()

def start_textmining(metabolieten):
    """ Starts textmining and filling of the database

    :param metabolieten: list- metabolites
    """
    # First round
    get_ids_all_pubmed(metabolieten, True)
    # Fill connecting tables
    fill_tussentabellen()

def start_textmining_test():
    """
    Has functioned as a test
    """
    # File name
    file = "Dataset/Untargeted_metabolomics.xlsx"
    # Data from file
    data = fileReader.readFile(file)
    # Metabolites
    metabolieten = fileReader.getMetabolites(data)
    # First round
    get_ids_all_pubmed(metabolieten, True)
    # Fill connecting tables
    fill_tussentabellen()

if __name__ == '__main__':
    # Textmining and filling of the database happens at the same time
    start_textmining_test()





