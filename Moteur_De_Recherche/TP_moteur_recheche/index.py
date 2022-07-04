#!/usr/bin/env python3

# Custom import
import operator

import sqlite3
import re
from math import log
from shared import extractListOfWords, stem
from collections import defaultdict
conn = sqlite3.connect('data.db')
cursor = conn.cursor()
cursor1 = conn.cursor()

# compute the inverted index and the idf and store them

conn.commit()
counter = 0


########### PREMIERE PHASE ###########
print("#### PREMIRE PHASE ####")

# QUESTION 1 : Combien il y a de pages indexées ?
cursor.execute("SELECT COUNT(*) FROM webpages")
query_1 = cursor.fetchone()
print("QUESTION 1")
print("Il y a " + str(query_1[0]) + " indexées\n")

# QUESTION 2 : Combien de pages ont la même URL requêtée et répondue ?
cursor.execute("SELECT COUNT(*) FROM responses WHERE responses.queryURL == responses.respURL")
query_2 = cursor.fetchone()
print("QUESTION 2")
print(str(query_2[0]) + " pages ont la même URL requêtée et répondue\n")

# QUESTION 3 : Certaines pages comme https://wiki.jachiet.com/wikipedia_fr_mathematics_ nopic_2020-04/A/Surface_de_Delaunay ne sont pas indexées, pourquoi ? Pouvez-vous en trouver d’autres ?
print("QUESTION 3")
page_requete = 'https://wiki.jachiet.com/wikipedia_fr_mathematics_nopic_2020-04/A/Surface_de_Delaunay'
cursor.execute("SELECT COUNT(respURL) FROM responses WHERE queryURL = ?", (page_requete,))
if cursor.fetchone()[0] == 0:
    print("La page 'https://wiki.jachiet.com/wikipedia_fr_mathematics_nopic_2020-04/A/Surface_de_Delaunay' n'est pas indexée\n")


# On répuère la liste des URL de la colonne "respURL"
list_reponses_url = list()
for url in cursor.execute('SELECT respURL FROM responses'):
        list_reponses_url.append(url[0])
        
#print(list_reponses_url)

# On récupère la liste des URL de la table webpages (url des pages indexées)
list_webpages_url = list()
for url in cursor.execute('SELECT URL FROM webpages'):
    list_webpages_url.append(url[0])

#print(list_webpages_url)
      

print("Nombre d'url répondue", len(list_reponses_url))
print("Nombre d'url indexée", len(list_webpages_url))

########### DEUXIEME PHASE ###########
print("#### DEUXIEME PHASE ####")


# 2.1 Sous-phrase 1: Calcul de l'index inversé

# ----------- Calcul de l'index inversé -----------
print("----------- Calcul de l'index inversé -----------")
# Etape 1

def countFreq(word_list):
    word_freq = [word_list.count(word) for word in word_list]
    dico_word_freq = dict(list(zip(word_list, word_freq)))
    
    # On ordonne le dictionnaire dans l'ordre décroissant (descending order) 
    sorted_freq_dico = dict(sorted(dico_word_freq.items(), key=operator.itemgetter(1), reverse=True))
    
    # On convertit le nouveau dictionnaire en ordonnée en liste de tuple
    # format du tuple (word, occurence)
    list_tuples_word_freq = [(k, v) for k, v in sorted_freq_dico.items()]
    return list_tuples_word_freq

# Etape 2

conn.execute("DROP TABLE IF EXISTS inverted_index")
conn.commit()
conn.execute("CREATE TABLE inverted_index (keyword TEXT, URL TEXT, frequency REAL)")
conn.commit()

counter_insert = 0
# On récupère la liste des URL de la table webpages (url des pages indexées)
for row in cursor.execute("SELECT * FROM webpages"):
    
    word_list_extracted = list(extractListOfWords(row[0]))
    #print(word_list_extracted)
    
    word_list_stemmed = list()
    
    # On stemmatize chaque mot extrait de l'url de la page
    for word in word_list_extracted:
        word_stemmed = stem(word)
        word_list_stemmed.append(word_stemmed)    
    #print(word_list_stemmed)
    
    # On crée la liste de tuple (word, frequence)
    tuple_word_freq = countFreq(word_list_stemmed)
    #print(tuple_word_freq)
    
    # On nourrit la table inverted_index avec la liste de tuple que l'on vient de créer
    for elm in tuple_word_freq:

        cursor1.execute('INSERT INTO inverted_index VALUES (?,?,?)', (elm[0], row[1], elm[1]/len(word_list_stemmed)))
    
    # Log pour le suivi de l'insertion des données en DB
    counter_insert = counter_insert +1
    print(counter_insert)
    
# On sauvegarde les insertions sinon la DB reste bloquée
conn.commit()

# On crée un index inverse pour la table inverted_index en se basant sur la colonne 'keyword'
conn.execute("DROP INDEX IF EXISTS inv_ind")
conn.commit()
conn.execute("CREATE INDEX inv_ind ON inverted_index(keyword)")
conn.commit()



# Question 4 : Dans quelle page apparaît le plus souvent (en fréquence) le terme “matrice” ?
cursor.execute("SELECT keyword, URL, MAX(frequency) FROM inverted_index WHERE keyword LIKE('matric')")
page_matrice = cursor.fetchone()
print("\n\nQUESTION 4")    
print("Le terme " + page_matrice[0] + " apparaît le plus souvent dans " + page_matrice[1] + " avec une fréquence de " + str(page_matrice[2]))


# 2.1 Sous-phrase 2: précalcul de l’inverse document frequency

# ----------- Calcul de IDF -----------
print("----------- Calcul de IDF -----------")

# Création de la table invert_document_frequency (keyword, idf)
conn.execute("DROP TABLE IF EXISTS invert_document_frequency")
conn.commit()
conn.execute("CREATE TABLE invert_document_frequency (keyword TEXT, idf REAL)")
conn.commit()

# On récupère le nombre d'url contenu dans la table webpages pour le calcul de IDF
cursor.execute("SELECT COUNT(*) FROM webpages")
nb_url = cursor.fetchone()[0]
print(nb_url)

# On insère en db le mot et sa valeur idf (idf = log(N/n_w))
    # N est le nombre de documents
    # n_w le nombre de document où w apparaît
counter_insert_bis = 0    
    

for row in cursor.execute("SELECT keyword, COUNT(URL) FROM inverted_index GROUP BY keyword"):
    
    cursor1.execute("INSERT INTO invert_document_frequency VALUES (?,?)", (row[0], log(nb_url / row[1])))
    counter_insert_bis = counter_insert_bis + 1
    print(counter_insert_bis)
    
# On sauvegarde les insertions en db
conn.commit()

# Création de l'index pour la table "invert_document_frequency"
conn.execute("DROP INDEX IF EXISTS inv_doc_freq_ind")
conn.commit()
conn.execute("CREATE INDEX inv_doc_freq_ind ON invert_document_frequency(keyword)")
conn.commit()

# Question 5 : Quel est l’IDF de “matrice”  ?
cursor.execute("SELECT * FROM invert_document_frequency WHERE keyword LIKE('matric')")
idf_matrice = cursor.fetchone()
print("\n\nQUESTION 5")    
print("IDF de " + idf_matrice[0] + " = " + str(idf_matrice[1]))
