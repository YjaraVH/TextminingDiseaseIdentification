# Name = 62
# Z-score = 127 t/m 153
import pandas as pd


# def fileLezen(file):
#     with open(file) as file:
#         metabolen_zscores = {}
#         count = 0
#         for line in file:
#             count += 1
#             if line != "":
#                 line = line.strip().replace(",", "").replace(";", "")
#                 print(line)
#                 metabolen_zscores.setdefault(line[62], []).append(line[127:153])
#
#     print(metabolen_zscores)

def fileLezen(file):
    with open(file) as file:
        metabolen_zscores = {}
        count = 0
        for line in file:
            count += 1
            if line != "":
                line = line.split(";")
                print(len(line))
                key = line[62]
                value = line[127:153]
                metabolen_zscores[key] = value
    print(metabolen_zscores)


def lezen():
    df = pd.read_excel("Untargeted_metabolomics.xlsx", sheet_name="Blad1")
    df.head()
    print(df)

def bestand_lezen():
    data = pd.read_excel("Dataset/Untargeted_metabolomics.xlsx")
    columns = data.columns
    person_ids = []
    for i in columns:
        print(i)
        string_i = str(i)
        if string_i.startswith("P") and string_i.endswith(".1"):
            person_ids.append(string_i)
    print(person_ids)


if __name__ == '__main__':
    #lezen()
    #bestand_lezen()
    file = "Dataset/Metabolics.csv"
    fileLezen(file)
