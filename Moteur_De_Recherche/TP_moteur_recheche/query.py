import sqlite3
from shared import stem
from collections import defaultdict
import sys

conn = sqlite3.connect('data.db')
cursor = conn.cursor()


query = input("Saisissez votre requête : ")
if query == "":
    query = "comment multiplier des matrices"

queryWords = list()
for i in query.split():
    if stem(i) != "":
        queryWords.append(stem(i))

dict_invert_document_frequency = dict()
for row in cursor.execute("SELECT keyword, idf FROM invert_document_frequency"):
    keyword, idf = row[0], row[1]
    dict_invert_document_frequency[keyword] = idf


dict_rank_score = dict()
for row in cursor.execute("SELECT URL, rank_score FROM page_rank"):
    URL, rank_score = row[0], row[1]
    dict_rank_score[URL] = rank_score


# Quelles sont les dix premières pages pour “comment multiplier des matrices” en utilisant seulement la métrique tf-idf ?

point = dict()
for word in queryWords :

    result = (word, dict_invert_document_frequency[word])
    if result != None :

        idf_word = result[1]

        for row in cursor.execute("SELECT * FROM inverted_index WHERE keyword = ?", (word,)):
            URL,frequency = row[1], row[2]

            if URL in point.keys():
                point[URL] += frequency * idf_word
            else :
                point[URL] = frequency * idf_word

top = list()
for i in point:
    top+= [(point[i], i), ]

top.sort()
top.reverse()

print("Résultat avec tf-idf")

for i in range(1, 11): print("classement", i, " : " , top[i-1][1])




# Quelles sont les dix premières pages pour “comment multiplier des matrices” en combinant tf-idf et Page-Rank?

point = dict()  
for word in queryWords :

    result = (word, dict_invert_document_frequency[word])
    if result != None :

        idf_word = result[1]

        for row in cursor.execute("SELECT * FROM inverted_index WHERE keyword = ?", (word,)):
            URL,frequency = row[1], row[2]

            rank_score = dict_rank_score[URL] 

            if URL in point.keys():
                point[URL] += frequency * idf_word * rank_score
            else :
                point[URL] = frequency * idf_word * rank_score
                
top = list()
for i in point:
    top+= [(point[i], i), ]

top.sort()
top.reverse()

print("Résultat avec tf-idf * pagerank")

for i in range(1, 11): print("classement", i, " : " , top[i-1][1])
    
conn.close()