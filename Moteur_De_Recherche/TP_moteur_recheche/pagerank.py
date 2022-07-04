import sqlite3
import re
from math import log
from shared import extractText, neighbors
from collections import defaultdict
import pandas as pd


NB_ITERATIONS = 50
ALPHA = 0.15

conn = sqlite3.connect('data.db')
cursor = conn.cursor()

    
#compute and store pagerank

# 1. calculer un dictionnaire realURL qui retourne la respURL associée à une queryURL
realURL = {}
for row in cursor.execute("SELECT queryURL, respURL FROM responses"):
    queryURL, respURL = row[0], row[1]
    realURL[queryURL] = respURL

# respURL = 'https://wiki.jachiet.com/wikipedia_fr_mathematics_nopic_2020-04/A/Galil%C3%A9e_(savant)'
# queryURL = https://wiki.jachiet.com/wikipedia_fr_mathematics_nopic_2020-04/A/Galilée_(savant)

# 2. calculer un dictionnaire pointsTo qui stocke la liste neighbors(content) pour chaque respURL
pointsTo = {}
for row in cursor.execute("SELECT URL, content FROM webpages"):
    URL, content = row[0], row[1]
    pointsTo[URL] = neighbors(content, URL)




# 3. Modifier pointsTo pour que les queryURL soient remplacés par des respURL.
d = pointsTo.copy()
df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in d.items() ]))

list_realURL_key = [i for i in realURL.keys()]

for i in range(df.shape[1]):
    for j in range(df.shape[0]):
        if pd.isnull(df.iloc[j,i]) != True and df.iloc[j,i] in list_realURL_key:
            df.iloc[j,i] = realURL[df.iloc[j,i]]
            
list_pointsTo_key = [i for i in pointsTo.keys()]

for i in list_pointsTo_key:
    pointsTo[i] = df.loc[pd.isnull(df[i])!=True,i].tolist()


score,nouveau_score, nombre_de_page = dict(),dict(), len(pointsTo.keys())

for r in pointsTo:
    score[r] = 1/nombre_de_page

for i in range(NB_ITERATIONS):
    
    for r in pointsTo:
        nouveau_score[r] = 0
       
    proba_teleportation = 0
    
    for r in pointsTo:
        if len(pointsTo[r]) > 0 :
            proba_teleportation += ALPHA * score[r]
            for u in pointsTo[r]:
                nouveau_score[u] += score[r] * (1 - ALPHA) / len(pointsTo[r])           
        else:
            proba_teleportation += score[r]
              
    for r in pointsTo:
        nouveau_score[r] += proba_teleportation / nombre_de_page
    
    for r in nouveau_score:
        score[r] = nouveau_score[r]


conn.execute("DROP TABLE IF EXISTS page_rank")
conn.commit()
conn.execute("CREATE TABLE page_rank (URL TEXT, rank_score REAL)")
conn.commit()

for key, value in score.items():
    conn.execute('INSERT INTO page_rank VALUES (?,?)', (key, value))
    
conn.commit()
conn.close()


top = list()
for i in score:
    top+= [(score[i], i), ]

top.sort()
top.reverse()

for i in range(20):
    print(top[i])