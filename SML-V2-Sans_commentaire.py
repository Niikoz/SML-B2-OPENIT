import random
import os
import json

def choix_ponderé(dictionnaire):
    total = sum(dictionnaire.values())
    r = random.uniform(0, total)
    cumul = 0
    for cle, valeur in dictionnaire.items():
        cumul += valeur
        if r <= cumul:
            return cle

def createWord(tab, caracs, mot="#", max_length=15):
    if len(mot) >= max_length:
        return mot[1:-1]  # Retourne le mot sans les caractères de début et de fin
    elif caracs[len(caracs) - 1] == '_':
        return mot[1:-1]
    else:
        add = choix_ponderé(tab.get(caracs))
        mot += add
        return createWord(tab, mot[len(mot) - 2] + mot[len(mot) - 1], mot, max_length)

def load_words_from_file(filename):
    with open(filename, "r", encoding="utf8") as file:
        words = [line.strip() for line in file.readlines()]
    return words

def create_stats_dict(words):
    dico = {}
    for word in words:
        word = [c for c in word] 
        for i in range(2):
            word.insert(0, "#")
            word.insert(len(word), "_")
        for i in range(len(word) - 2):
            occu = word[i] + word[i + 1] + word[i + 2]
            if occu != "###" and occu != "___":
                if dico.get(occu):
                    dico[occu] += 1
                else:
                    dico[occu] = 1
    return dico

def create_stats_table(dico):
    tableauStat = {}
    for cle in dico.keys():
        lttrAvt = cle[:2]
        val = cle[2]
        if lttrAvt not in tableauStat:
            tableauStat[lttrAvt] = {}
        if val not in tableauStat[lttrAvt]:
            tableauStat[lttrAvt][val] = dico[cle]
        else:
            tableauStat[lttrAvt][val] += dico[cle]
    return tableauStat

def get_user_input():
    min_word_length = int(input("Entrez la taille minimale des mots à générer : "))
    num_words = int(input("Entrez le nombre de mots à générer : "))
    return min_word_length, num_words

def save_words_to_file(words, filename):
    with open(filename, "w", encoding="utf8") as file:
        file.write("\n".join(words))

def open_file(filename):
    os.system(f"start {filename}")

def load_data_from_json(filename):
    if os.path.isfile(filename):  # Vérifie si le fichier existe
        # Demande à l'utilisateur s'il souhaite supprimer le fichier existant
        reponse = input("Le fichier JSON existe déjà. Voulez-vous le supprimer ? (Oui/Non) : ")
        if reponse.lower() == "oui":
            os.remove(filename)  # Supprime le fichier existant
            # Supprime également le fichier Mot.txt
            if os.path.isfile("Mot.txt"):
                os.remove("Mot.txt")
            print("Fichiers supprimés.")
        else:
            # Charge les données existantes sans le supprimer
            with open(filename, "r", encoding="utf8") as json_file:
                data = json.load(json_file)
            return data
    
    # Génère les données si le fichier n'existe pas ou s'il a été supprimé
    words = load_words_from_file("Listmot.txt")
    dico = create_stats_dict(words)
    tableauStat = create_stats_table(dico)
    with open(filename, "w", encoding="utf8") as json_file:
        json.dump(tableauStat, json_file, indent=4)
    return tableauStat

# Charger les données à partir du fichier JSON ou le générer
filename_json = "tableauStat.json"
tableauStat_from_json = load_data_from_json(filename_json)

min_length, num_words = get_user_input()

generated_words = []
for _ in range(num_words):
    word = createWord(tableauStat_from_json, "##", max_length=20)
    while len(word) < min_length:
        word = createWord(tableauStat_from_json, "##", max_length=20)
    generated_words.append(word)

save_words_to_file(generated_words, "Mot.txt")
open_file("Mot.txt")
