import pandas as pd
import xml.etree.ElementTree as ET
from xml.dom import minidom
import html
from collections import defaultdict

def csv_to_xml(csv_file, xml_file, nodeHeader, nodeChild):
    # Leggi il CSV con il separatore ';'
    df = pd.read_csv(csv_file, sep=';')

    with open(xml_file, "w", encoding='utf-8') as f:

        f.write("<?xml version='1.0' encoding='UTF-8'?>" + '\n') #Intestazione
        f.write("<" + nodeHeader + ">" + '\n') #Nodo principale

        for i in range(len(df.values)):

            f.write('\t' + "<" + nodeChild + ">" + '\n') #Nodo per ogni record appartenente al nodo principale

            radici = defaultdict(list)

            for j in range(len(df.columns)):
                radice = df.columns[j].split('_')[0]
                radici[radice].append(df.columns[j])

            print(str(df.values[i]))

            countField = 0 #count per il prossimo campo da scrivere

            for radice, elementi in radici.items():

                if len(elementi) > 1:

                    f.write("\t" + "\t" + "<main_" + radice + ">" + "\n") #Sottonodo con ulteriori figli
                    radiciElementi = defaultdict(list)

                    for e in range(len(elementi)):
                        radiciElementi[elementi[e].split('_')[1]].append(elementi[e]) #raggruppo tutti i sottonodi simili (con la stessa radice)

                    countChild = 0 #count per il numero di sottonodi

                    multiRadici = defaultdict(list)

                    countMultiRadici = 0

                    for re in radiciElementi.values():

                        if len(re) > 1:

                            #future 1 --> gestire i sottonodi dei sottonodi precedenti (con la stessa radice)
                            #future 2 --> gestire questo passaggio in modo ricorsivo, visto che potrei avere nodi infiniti

                            multiRadiciInterni = defaultdict(list)

                            countSplit = 0

                            """for r in range(len(re)): #cerco quanti nodi delimitati da _ esistono, per sviluppare tutti i nodi
                                
                                if len(re[r].split('_')) > countSplit:
                                    countSplit = len(re[r].split('_'))

                            print("Massimo numero di nodi " + str(countSplit))

                            numeroIniziale = 1
                            for cs in range(countSplit):

                                multiRadiciInterni[re[cs].split('_')[numeroIniziale + 1] + re[cs].split('_')[numeroIniziale]].append(re[cs])

                            numeroIniziale += 1"""

                            """for r in range(len(re)):
                                #print(re[r])
                                multiRadiciInterni[re[r].split('_')[2] + re[r].split('_')[1]].append(re[r])"""

                            #print(multiRadiciInterni)

                            multiRadici[countMultiRadici] = multiRadiciInterni

                            countMultiRadici += 1

                            print(multiRadici)

                            print("---------")




                            f.write("\t" + "\t" + "\t" + "<" + elementi[countChild].split('_')[0] + elementi[countChild].split('_')[1] + ">\n")

                            #ogni volta viene controllato se il valore è nan (non presente), di conseguenza viene gestito nel momento in cui si inserisce nel xml file

                            for t in re:
                                if len(t.split('_')) >= 3: #sottonodi con almeno 3 parti di radice uguale

                                    if str(df.values[i][countField]) == "nan":
                                        f.write("\t" + "\t" + "\t" + "\t" + "<" + t.split('_')[2] + "></" + t.split('_')[2] + ">\n")
                                    else:
                                        f.write("\t" + "\t" + "\t" + "\t" + "<" + t.split('_')[2] + ">" + str(df.values[i][countField]) + "</" + t.split('_')[2] + ">\n")

                                else:

                                    if str(df.values[i][countField]) == "nan":
                                        f.write("\t" + "\t" + "\t" + "\t" + "<" + t.split('_')[1] + "></" + t.split('_')[1] + ">\n")
                                    else:
                                        f.write("\t" + "\t" + "\t" + "\t" + "<" + t.split('_')[1] + ">" + str(df.values[i][countField]) + "</" + t.split('_')[1] + ">\n")

                                countField += 1

                            f.write("\t" + "\t" + "\t" + "</" + elementi[(countChild)].split('_')[0] + elementi[(countChild)].split('_')[1] + ">\n")

                            countChild += 1

                        else:
                            for t in re:
                                if str(df.values[i][countField]) == "nan":                                
                                    f.write("\t" + "\t" + "\t" + "<" + t.split('_')[1] + "></" + t.split('_')[1] + ">\n")
                                else:
                                    f.write("\t" + "\t" + "\t" + "<" + t.split('_')[1] + ">" + str(df.values[i][countField]) + "</" + t.split('_')[1] + ">\n")

                            countField += 1

                        countChild += 1

                    f.write("\t" + "\t" + "</main_" + radice + ">" + "\n") #chiudo i sottonodi multipli

                else:
                    #entro qui quando devo inserire solo un record, ad esempio nome, cognome, ecc...
                    if str(df.values[i][countField]) == "nan":              
                        f.write("\t" + "\t" + "<" + radice + "></" + radice + ">" + '\n')
                    else:
                        f.write("\t" + "\t" + "<" + radice + ">" + str(df.values[i][countField]) + "</" + radice + ">" + '\n')

                    countField += 1

            f.write('\t' + "</" + nodeChild + ">" + '\n') #chiudo nodo principale figlio del nodo header

        f.write("</" + nodeHeader + ">" + '\n') #chiudo il nodo del file xml

# Esempio di utilizzo
csv_file = './files-input/01testcsv.csv' #codice temporaneo statico per il nome del file csv
xml_file = './files-output/csv-xml-output.xml' #codice temporaneo statico per il nome del file xml

nodeHeader = "persone" #parte statica temporanea per recuperare il nodo header
nodeChild = "persona" #parte statica temporanea per recuperare il nodo figlio

csv_to_xml(csv_file, xml_file, nodeHeader, nodeChild) #richiamo la funzione di scrittura