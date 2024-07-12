from collections import defaultdict

lista_elementi = ['nome_1', 'nome_2', 'cognome_1', 'cognome_2', 'eta_1', 'eta_2']
radici = defaultdict(list)

for elemento in lista_elementi:
    radice = elemento.split('_')[0]  # Assumiamo che la radice sia la parte prima dell'underscore
    radici[radice].append(elemento)

    print(elemento)

for radice, elementi in radici.items():
    print(f"Radice: {radice}, Elementi: {elementi}")