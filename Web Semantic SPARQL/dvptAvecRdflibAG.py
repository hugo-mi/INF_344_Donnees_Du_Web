from time import sleep, time
import isodate
from SPARQLWrapper import SPARQLWrapper, JSON, N3, TURTLE
from rdflib import Graph, URIRef, Literal
import json
import urllib
import ssl
import pandas as pd

class RdfDev:
    def __init__(self):
        """__init__
        Initialise la session de collecte
        :return: Object of class Collecte
        """
        # NE PAS MODIFIER
        self.basename = "rdfsparql.step"

    def rdfdev(self):
        """collectes
        Plusieurs étapes de collectes. VOTRE CODE VA VENIR CI-DESSOUS
        COMPLETER les méthodes stepX.
        """
        #self.step1()
        #self.step2()
        #self.step3()
        #self.step4()
        self.step5()


    def sparqlcall(self, sparqlquery): 
        from urllib.parse import urlencode, quote_plus 
        
        unsecurecontext = ssl._create_unverified_context() 
        basedbpedia = "https://dbpedia.org/sparql?" 
        payload = {'format': 'application/sparql-results+json', 'query': sparqlquery } 
        params = urlencode(payload, quote_via=quote_plus) 
        urldbpedia = basedbpedia+params 
        
        with urllib.request.urlopen(urldbpedia, context=unsecurecontext) as response: 
                return json.loads(response.read())
            

    def result_query(self, sparqlquery, key):
        """
        
        """
        # --- Délai d’au moins 1 seconde entre 2 appels
        sleep(1)

        # --- Exécution de la requête
        query_dict = self.sparqlcall(sparqlquery)

        # --- Séléction des données contenant le résultat de la requête
        bindings_list = query_dict['results']['bindings']

        # --- Liste des résultats
        result_list = [bindings_list[i][key]['value'] for i in range(len(bindings_list))]

        if len(result_list) == 1:
            result_list = result_list[0]

        return result_list


    def step1(self):
        print('-'*80)
        print('--- Step 1')
        stepfilename = self.basename+"1"

        # --- Requête à éxécuter en SPARQL
        sparqlquery = """
            SELECT DISTINCT ?t 
            WHERE
            {
                ?h a ?t .
            }
            LIMIT 10"""

        # --- Ecriture des résultats de la requête dans le dictionnaire result
        result = { "typelist": self.result_query(sparqlquery, key='t')}

        # --- Ecriture du fichier de sortie
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            json.dump(result, resfile)
        
        print("Done\n")


    def step2(self):
        print('-'*80)
        print('--- Step 2')
        stepfilename = self.basename+"2"
        result = {}
        
        # --- Récupération du préfix de foaf
        result['prefix'] = 'http://xmlns.com/foaf/0.1/' 

        # ---------------------------------------------------------------------
        # ---               Comptage du nombre de Person

        # --- Requête à éxécuter en SPARQL
        sparqlquery = "PREFIX foaf: <{}>".format(result['prefix']) + """
            SELECT COUNT(?person) as ?nb_person
            WHERE 
            {
                ?person ?p foaf:Person .
            }
        """

        # --- Ecriture des résultats de la requête dans le dictionnaire result
        result["personcount"] = self.result_query(sparqlquery, key='nb_person')

        # ---------------------------------------------------------------------
        # ---               Top 10 uris de personnes décrites

        # --- Requête à éxécuter en SPARQL
        sparqlquery = "PREFIX foaf: <{}>".format(result['prefix']) + """
            SELECT ?person
            WHERE 
            {
                ?person ?p foaf:Person .
            }
            LIMIT 10"""

        # --- Ecriture des résultats de la requête dans le dictionnaire result
        result["firstten"] = self.result_query(sparqlquery, key='person')

        # ---------------------------------------------------------------------
        # ---       Top 10 uris de personnes décrites avec Offset de 100

        # --- Requête à éxécuter en SPARQL
        sparqlquery = "PREFIX foaf: <{}>".format(result['prefix']) + """
            SELECT ?person
            WHERE 
            {
                ?person ?p foaf:Person .
            }
            OFFSET 100
            LIMIT 10"""

        # --- Ecriture des résultats de la requête dans le dictionnaire result
        result["tenothers"] = self.result_query(sparqlquery, key='person')

        # --- Ecriture du fichier de sortie
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            json.dump(result, resfile)
        
        print('Done\n')

    def step3(self):
        print('-'*80)
        print('--- Step 3')
        stepfilename = self.basename+"3"
        result = {}
        # ---------------------------------------------------------------------
        # ---               Calcul du nombre de predicates

        # --- Requête à éxécuter en SPARQL
        sparqlquery = """
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            SELECT COUNT(DISTINCT(?p)) as ?nb_predicates
            WHERE 
            {
                {SELECT ?pers WHERE { ?pers a foaf:Person} LIMIT 1000} ?pers ?p ?v .
            }"""

        # --- Ecriture des résultats de la requête dans le dictionnaire result
        result["predicatescount"] = self.result_query(sparqlquery, key='nb_predicates')

        # ---------------------------------------------------------------------
        # ---                   Les 20 premiers predicates

        # --- Requête à éxécuter en SPARQL
        sparqlquery = """
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            SELECT DISTINCT(?p)
            WHERE 
            {
                {SELECT ?pers WHERE { ?pers a foaf:Person} LIMIT 1000} ?pers ?p ?v .
            }
            LIMIT 20"""

        # --- Ecriture des résultats de la requête dans le dictionnaire result
        result['predicates'] = self.result_query(sparqlquery, key='p')
        result['rqpredicates'] = sparqlquery
        
        # ---------------------------------------------------------------------
        # ---        Comptage <http://dbpedia.org/ontology/deathPlace>

        # --- Requête à éxécuter en SPARQL
        sparqlquery = """
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            SELECT COUNT(?pers) as ?nb_ent
            WHERE
            {
                {select ?pers where { ?pers a foaf:Person}} ?pers <http://dbpedia.org/ontology/deathPlace> ?o
            }"""
        
        # --- Ecriture des résultats de la requête dans le dictionnaire result
        result['placecount'] = self.result_query(sparqlquery, key='nb_ent')
        result['rqplacecount'] = sparqlquery

        # --- Ecriture du fichier de sortie
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            json.dump(result, resfile)
        
        print(result)
        
        print('Done\n')

    def step4(self):
        print('-'*80)
        print('--- Step 4')
        stepfilename = self.basename+"4"
        result = {}

        # ---------------------------------------------------------------------
        # ---                       Jules Verne

        # --- Requête à éxécuter en SPARQL
        sparqlquery = """
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            SELECT ?uri ?p
            WHERE
            {
                ?uri a foaf:Person .
                ?uri ?p "Jules Verne"@fr .
            }"""
        
        # --- Ecriture des résultats de la requête dans le dictionnaire result
        result['julesverne'] = self.result_query(sparqlquery, key='uri')
        result['jvpredicate'] = self.result_query(sparqlquery, key='p')

        # ---------------------------------------------------------------------
        # ---  Valeurs liées par <http://dbpedia.org/property/notableworks>

        # --- Requête à éxécuter en SPARQL
        sparqlquery = """
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            SELECT ?v
            WHERE
            {
                ?uri a foaf:Person .
                ?uri ?p "Jules Verne"@fr .
                ?uri <http://dbpedia.org/property/notableworks> ?v .
            }"""
        
        # --- Ecriture des résultats de la requête dans le dictionnaire result
        result['jvdoc'] = self.result_query(sparqlquery, key='v')

        # --- Ecriture du fichier de sortie
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            json.dump(result, resfile)
        
        print('Done\n')

    def step5(self):
        print('-'*80)
        print('--- Step 5')
        stepfilename = self.basename+"5"
        result = {}
        "?uri ?p ?o"

        # ---------------------------------------------------------------------
        # ---  Prédicats assosciés à http://dbpedia.org/resource/Jules_Verne

        # --- Requête à éxécuter en SPARQL
        sparqlquery = """
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            SELECT DISTINCT(?p)
            WHERE
            {
                ?pers a foaf:Person .
                ?pers ?pred "Jules Verne"@fr .
                ?pers ?p ?o .
            }"""
        
        # --- Ecriture des résultats de la requête dans le dictionnaire result
        result['jvpredicates'] = self.result_query(sparqlquery, key='p')

        # ---------------------------------------------------------------------
        # ---           Récupération des triplets de cette uri

        # --- Requête à éxécuter en SPARQL
        sparqlquery = """
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            SELECT ?pers ?p ?o
            WHERE
            {
                ?pers a foaf:Person .
                ?pers ?pred "Jules Verne"@fr .
                ?pers ?p ?o .
            }
            LIMIT 100
            OFFSET """
        
        # --- Boucle sur les offsets 
        offset = 0
        ad_offset = True
        triplets = {
            'uris': [],
            'predicates': [],
            'values': []
        }

        while ad_offset:
            # --- Calcul du nombre de triplets par offset
            nb_triplets = len(self.result_query(sparqlquery+str(offset), key='o'))

            # --- Ajout des triplets dans un dictionnaire pour l'étape 6
            triplets['uris'] += self.result_query(sparqlquery+str(offset), key='pers')
            triplets['predicates'] += self.result_query(sparqlquery+str(offset), key='p')
            triplets['values'] += self.result_query(sparqlquery+str(offset), key='o')
            
            # --- Si le nombre de triplets est de 100, on augmente l'OFFSET de 100
            if nb_triplets == 100:
                offset += 100
            
            # --- Sinon, on a trouvé le nombre final de triplet
            else:
                ad_offset = False
                
        # --- Ecriture des résultats de la requête dans le dictionnaire result
        result['triplecount'] = str(offset + nb_triplets)
        
        print(len(result["jvpredicates"]))
        
        # --- Ecriture du fichier de sortie
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            json.dump(result, resfile)


        
        print("\n\n")
        print('Done\n')
"""
        # ---------------------------------------------------------------------
        # ---           Etape 6: Créer et sauver un graphe local
        
        print('-'*80)
        print('--- Step 6')

        # --- Transnformation du dictionnaire en Dataframe pour plus de facilité
        df_triple = pd.DataFrame(triplets)

        # Création d'un Graph
        g = Graph()

        # --- Insertion de tous les triplets dans le graphe
        df_triple.apply(lambda x: g.add(
                (URIRef(x[0]), URIRef(x[1]), Literal(x[2]))
            ), axis=1)

        # --- Sauvegarde du graphe au format adéquat
        g.serialize(destination='julesverne.n3', format='n3')
        print('Done\n')
"""

if __name__ == "__main__":
    print('*'*80)
    print("\t\t\tLaunching Lab 8 - Semantic Web\n")
    t_init = time()

    testeur = RdfDev()
    testeur.rdfdev()

    t_final = time() - t_init

    print('_'*80)
    if t_final < 60:
        print("\nTotal execution time: {:.2f}s".format(t_final))
    else:
        print("\nTotal execution time: {:.0f}min {:.0f}s".format(t_final//60, t_final%60))
    print('*'*80)