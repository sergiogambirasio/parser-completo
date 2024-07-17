import csv_xml_generic

def main():

    csv_file = './files-input/01testcsv.csv' #codice temporaneo statico per il nome del file csv
    xml_file = './files-output/01_csv-xml-output.xml' #codice temporaneo statico per il nome del file xml

    nodeHeader = "persone" #parte statica temporanea per recuperare il nodo header
    nodeChild = "persona" #parte statica temporanea per recuperare il nodo figlio

    csv_xml_generic.csv_to_xml(csv_file, xml_file, nodeHeader, nodeChild)

if __name__ == "__main__":
    main()