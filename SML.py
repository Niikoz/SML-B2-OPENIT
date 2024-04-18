import random
import json
import os

#Fonction pour recup une valeur dans le dictionnaire
def choix_ponderé(dictionnaire):
    total = sum(dictionnaire.values())
    r = random.uniform(0, total)
    cumul = 0
    for cle, valeur in dictionnaire.items():
        cumul += valeur
        if r <= cumul:
            return cle
        
#fonction qui genere un mot par reccurence qui s'arrete si le mot est trop grand ou le carac qui l'arrete
def createWord(tab, caracs, mot="#", max_length=15):
    if len(mot) >= max_length:
        return mot[1:-1]  # Retourne le mot sans les caractères de début et de fin
    elif caracs[len(caracs) - 1] == '_':
        return mot[1:-1]
    else:
        add = choix_ponderé(tab.get(caracs))
        mot += add
        return createWord(tab, mot[len(mot) - 2] + mot[len(mot) - 1], mot, max_length)

#Qui permet de load le fichier de mots
def load_words_from_file(filename):
    with open(filename, "r", encoding="utf8") as file:
        words = [line.strip() for line in file.readlines()]
    return words

#creation du premier Dico d'occurence 
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
#creation du dico de statistique 
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
#recuperer des inputs de l'utilisateur
def get_user_input():
    min_word_length = int(input("Entrez la taille minimale des mots à générer : "))
    num_words = int(input("Entrez le nombre de mots à générer : "))
    return min_word_length, num_words

#permet de save les mots generer dans un txt
def save_words_to_file(words, filename):
    with open(filename, "w", encoding="utf8") as file:
        file.write("\n".join(words))

#permet d'exporter le tableau(dico) en JSON
def export_to_json(tableauStat):
    json_file = json.dumps(tableauStat, ensure_ascii=False, indent=4)
    with open('tableauStat.json', 'w', encoding='utf-8') as f:
        f.write(json_file)

filename = "Listmot.txt"
#permet de questionner et de supprimer le json si besoin
def questionJson(filename):
     if os.path.isfile(filename):  # Vérifie si le fichier existe
        # Demande à l'utilisateur s'il souhaite supprimer le fichier existant
        reponse = input("Le fichier JSON existe déjà. Voulez-vous le supprimer ? (Y/N) : ")
        if reponse.lower() == "y":
            os.remove(filename)
questionJson("tableauStat.json")

#verif si jsopn exist sinon lancer le programme pour le créer et faire le TableauStat
if os.path.exists("tableauStat.json"):
    with open('tableauStat.json', 'r', encoding='utf-8') as file: 
        tableauStat = json.load(file)
else:
    words = load_words_from_file(filename)
    dico = create_stats_dict(words)
    tableauStat = create_stats_table(dico)
    export_to_json(tableauStat)
min_length, num_words = get_user_input()

#boucle pour génerrer les mots
generated_words = []
for _ in range(num_words):
    word = createWord(tableauStat, "##", max_length=20)
    while len(word) < min_length:
        word = createWord(tableauStat, "##", max_length=20)
    generated_words.append(word)

save_words_to_file(generated_words, "Mots.txt")