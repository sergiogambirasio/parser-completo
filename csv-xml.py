import pandas as pd
import xml.etree.ElementTree as ET
from xml.dom import minidom

def csv_to_xml(csv_file, xml_file, nodeHeader, nodeChild):
    def add_element(parent, tag, text=None):
        element = ET.SubElement(parent, tag)
        if text:
            element.text = str(text)
        return element

    # Leggi il CSV con il separatore ';'
    df = pd.read_csv(csv_file, sep=';')

    root = ET.Element(nodeHeader)

    for _, row in df.iterrows():
        persona = add_element(root, nodeChild)
        
        grouped_data = {}
        
        # Raggruppa i dati in base al prefisso
        for col in df.columns:
            if '_' in col:
                prefix, subfield = col.split('_', 1)
                if prefix not in grouped_data:
                    grouped_data[prefix] = {}
                grouped_data[prefix][subfield] = row[col]
            else:
                add_element(persona, col, row[col])

        group_node = ET.SubElement(persona, col.split('_', 1) + "s")  # Aggiungi 's' per fare al plurale

        # Aggiungi nodi raggruppati dinamicamente
        for group, attributes in grouped_data.items():
            # Aggiungi il nodo del gruppo sotto la persona
            
            subnode = ET.SubElement(group_node, group)  # Aggiungi il sottonodo principale
            
            for attr, value in attributes.items():
                add_element(subnode, attr, value)

    # Crea l'albero XML
    tree = ET.ElementTree(root)

    # Formatta e scrivi l'XML in modo leggibile
    xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")
    with open(xml_file, "w", encoding='utf-8') as f:
        f.write(xml_str)

# Esempio di utilizzo
csv_file = './files-input/01testcsv.csv'
xml_file = './files-output/csv-xml-output.xml'

nodeHeader = "persone"
nodeChild = "persona"

csv_to_xml(csv_file, xml_file, nodeHeader, nodeChild)