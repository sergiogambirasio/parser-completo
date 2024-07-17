import csv_xml_generic

import sys
import tkinter as tk
from tkinter import filedialog
import shutil
import os

def esc(): #funzione di escape
    print("Chiusura del programma...")
    sys.exit()

def select_file_and_copy(destination_folder):
    root = tk.Tk() # Inizializza la finestra di Tkinter
    root.withdraw() # Nasconde la finestra principale
    
    file_path = filedialog.askopenfilename() # Apre una finestra di dialogo per selezionare il file
    
    if file_path: # Verifica se un file è stato selezionato
        try:
            file_name = os.path.basename(file_path) # Ottieni il nome del file selezionato
            destination_path = os.path.join(destination_folder, file_name) # Costruisce il percorso completo di destinazione

            if os.path.isfile(destination_path):
                copiare = input("Esiste già un file con questo nome nel percorso di destinazione, si intende sovrascriverlo? S/N ")
                if copiare == 'S':
                    shutil.copy(file_path, destination_path) # Copia il file nella cartella di destinazione
                    print(f"File copiato in: {destination_path}")
                    return os.path.basename(file_path) #return del nome da usare come parametro
                else:
                    esegui = input("Desideri comunque eseguire la conversione? S/N ")
                    if esegui == 'S':
                        return os.path.basename(file_path) #return del nome da usare come parametro
                    else:
                        return ""
            else:
                shutil.copy(file_path, destination_path) # Copia il file nella cartella di destinazione
                print(f"File copiato in: {destination_path}")
                return os.path.basename(file_path) #return del nome da usare come parametro

        except Exception as e:
            print(f"Errore durante la copia del file {e}")
            return ""
    else:
        print("Nessun file selezionato.")
        return ""

def csv_xml(): #da csv a xml
    # Specifica la cartella di destinazione
    destination_folder = 'files-input/'

    # Assicurati che la cartella di destinazione esista
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    csv_file = destination_folder

    nome_file = select_file_and_copy(destination_folder) # Chiama la funzione per selezionare il file e copiarlo

    if nome_file != "":
        csv_file = csv_file + nome_file

        file_senza_estensione, estensione_file = os.path.splitext(nome_file)

        if estensione_file == ".csv":
            xml_file = './files-output/' + file_senza_estensione + '.xml' #codice temporaneo statico per il nome del file xml

            nodeHeader = "persone" #parte statica temporanea per recuperare il nodo header
            nodeChild = "persona" #parte statica temporanea per recuperare il nodo figlio

            print("Preparazione del file in corso...")
            csv_xml_generic.csv_to_xml(csv_file, xml_file, nodeHeader, nodeChild) #esecuzione della trasformazione
            print("Operazione terminata")
        else:
            print("L'estensione del file non è valida, deve corrispondere a .csv")
    else:
        print("Non verrà eseguita alcuna conversione")

def default_case(): #funzione che ritorna il messaggio in caso non sia presente una funzione
    return "Funzione non disponibile"

#dizionario di funzioni per la scelta di quale conversione si desidera effettuare
switch = {
    "0": esc,
    "1": csv_xml,
}

def switch_case(case): #richiamo il dizionario di funzioni
    return switch.get(case, default_case)()

def main():

    eseguire = True
    continuare = 'S'

    while eseguire: #ciclo while che si interrompe quando non si vuole più proseguire

        print("\nEcco le conversioni possibili al momento:\n1) Da CSV a X.M.L\nDigita 0 per uscire")
        scelta = input("Scegli la conversione che desideri ")

        if not switch.__contains__(scelta): #se non è contenuto nel dizionario, richiamo la funzione e ritorno il messaggio
            print(default_case())

        switch_case(scelta)
    
        continuare = input("Continuare? S/N ")

        if continuare != 'S':
            eseguire = False
            print("Chiusura del programma...")

if __name__ == "__main__":
    main()