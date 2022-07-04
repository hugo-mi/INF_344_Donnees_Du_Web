import isodate
from SPARQLWrapper import SPARQLWrapper, JSON, N3, TURTLE
from rdflib import Graph, URIRef, Literal
import json
from urllib.parse import urlencode, quote_plus
import urllib.request
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
        self.step1()
        self.step2()
        self.step3()
        self.step4()
        self.step5()
        self.step6()
        
    def sparqlcall(self, sparqlquery):
        unsecurecontext = ssl._create_unverified_context()
        basedbpedia = "https://dbpedia.org/sparql?"
        payload = {'format': 'application/sparql-results+json', 'query': sparqlquery }
        params = urlencode(payload, quote_via=quote_plus)
        urldbpedia = basedbpedia+params
        with urllib.request.urlopen(urldbpedia, context=unsecurecontext) as response:
            return json.loads(response.read())

    def step1(self):
        stepfilename = self.basename+"1"
        result = { "typelist": []}
        # votre code ici
        
        query = """
        
        select distinct ?t

        where { ?h a ?t }
        
        limit 10
        
        """
        output_query = self.sparqlcall(query)
        list_result_query = list()
        
        for i in range(len(output_query["results"]["bindings"])):
            out = output_query["results"]["bindings"][i]["t"]["value"]
            list_result_query.append(out)
        
        result["typelist"] = list_result_query
        
        print("========== STEP 1 ==========")
        print(result)
        print("\n\n\n")
        
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            json.dump(result, resfile)

    def step2(self):
        stepfilename = self.basename+"2"
        result = {}
        # votre code ici
        
        result = {'prefix': '',
                  'personcount': '', 
                  'firstten': '',
                  'tenothers': ''}
        
        #### PREFIX ####
        result["prefix"] = "http://xmlns.com/foaf/0.1/"
        
        #### PERSONCOUNT ####
        query_person_count = """
            PREFIX foaf:<http://xmlns.com/foaf/0.1/>
            SELECT (count(?person) as ?c)
            WHERE { ?person rdf:type foaf:Person . }
        """
        
        result_query_person_count = int(self.sparqlcall(query_person_count)["results"]["bindings"][0]["c"]["value"])
        
        result["personcount"] = result_query_person_count
        
        #### FIRSTTEN ####
        query_first_ten = """
            PREFIX foaf:<http://xmlns.com/foaf/0.1/>
            SELECT ( ?person )
            WHERE { ?person rdf:type foaf:Person . }
            LIMIT 10
        """
        
        result_query_first_ten = self.sparqlcall(query_first_ten)
        
        first_ten_list = list()
        
        for i in range(len(result_query_first_ten["results"]["bindings"])):
            out = result_query_first_ten["results"]["bindings"][i]["person"]["value"]
            first_ten_list.append(out)
        
        result["firstten"] = first_ten_list
        
        #### TEN OTHER ###
        query_first_ten_other = """
            PREFIX foaf:<http://xmlns.com/foaf/0.1/>
            SELECT ( ?person )
            WHERE { ?person rdf:type foaf:Person . }
            LIMIT 10
            OFFSET 100
         """
        result_query_first_ten_other = self.sparqlcall(query_first_ten_other)
        
        first_ten_list_other = list()
        
        for i in range(len(result_query_first_ten_other["results"]["bindings"])):
            out = result_query_first_ten_other["results"]["bindings"][i]["person"]["value"]
            first_ten_list_other.append(out)
        
        result["tenothers"] = first_ten_list_other
        
        print("========== STEP 2 ==========")
        print(result)
        print("\n\n\n")
        
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            json.dump(result, resfile)

    def step3(self):
        stepfilename = self.basename+"3"
        result = {}
        # votre code ici
        
        result = {'predicatescount': '',
                  'predicates': '',
                  'rqpredicates': '',
                  'placecount': '',
                  'rqplacecount': '',
                 }

        #### COUNT PREDICATE ####
        query_predicate_count = """
            SELECT COUNT(DISTINCT ?pred) as ?c
            WHERE { { SELECT ?pers WHERE { ?pers a foaf:Person } LIMIT 1000 } ?pers ?pred ?obj }
        """      
        
        result_query_predicate_count = self.sparqlcall(query_predicate_count)["results"]["bindings"][0]["c"]["value"]
        
        result['predicatescount'] = int(result_query_predicate_count)
        
        #### 20th PREDICATES ####
        
        query_predicate = """
            SELECT DISTINCT ?pred
            WHERE { {SELECT ?pers WHERE { ?pers a foaf:Person } LIMIT 1000 } ?pers ?pred ?obj } 
            LIMIT 20
        """
        
        result_query_predicate = self.sparqlcall(query_predicate)
        
        list_predicates = list()

        for i in range(len(result_query_predicate["results"]["bindings"])):
            out = result_query_predicate["results"]["bindings"][i]["pred"]["value"]
            list_predicates.append(out)
        
        result['predicates'] = list_predicates
        
        result['rqpredicates'] = "PREFIX foaf:<http://xmlns.com/foaf/0.1/> SELECT DISTINCT ?pred WHERE { {SELECT ?pers WHERE { ?pers a foaf:Person} LIMIT 1000 } ?pers ?pred ?obj } LIMIT 20"
        
        ### COUNT DEATH PLACE ###
        
        query_count_death_place = """
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            SELECT COUNT(?pers) as ?c
            WHERE
            {
                {select ?pers where { ?pers a foaf:Person}} ?pers <http://dbpedia.org/ontology/deathPlace> ?o
            }"""
        
        result_query_count_death_place = self.sparqlcall(query_count_death_place)["results"]["bindings"][0]["c"]["value"]
        
        result["placecount"] = result_query_count_death_place
        
        result["rqplacecount"] = "PREFIX foaf: <http://xmlns.com/foaf/0.1/> SELECT COUNT(?pers) as ?c WHERE { {select ?pers where { ?pers a foaf:Person}} ?pers <http://dbpedia.org/ontology/deathPlace> ?o }"
        
        print("========== STEP 3 ==========")
        print(result)
        print("\n\n\n")
        
        # QUESTION : Pourquoi il est intéressant de rendre une URI "déréférençable" ?
        
        # Réponse : 
            #Une URI est plus intéressante quans elle est déférençable car cela signifie qu'il est
            # possible de récupérer la description de la ressource identifiée.
            # Autrement dit, lorsque les URI identifient des objets réels, il est important de ne pas cofondre
            # les objets eux-mêmes avec le document web qui les décrivent. 
            # Par conséquent, pour éviter ce genre de situation, il est important que l'URI qui décrit un
            # objet soit unique afin de lever toute ambiguïté. 
            # Par exemple, dans notre cas, pour l'entité "FamilyName" il est possible que plusieurs personnes
            # portent le même le nom et prénom. Ainsi si à chacune de ses personnes n'est pas attribué une 
            # URI déréférençable alors il peut avoir ambiguïté entre le document HTML qui décrit la personne et
            # l'URI qui définit réellement cette personne.
        
        
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            json.dump(result, resfile)

    def step4(self):
        stepfilename = self.basename+"4"
        result = {}
        # votre code ici
        
        result = {'julesverne' : '',
                  'jvpredicate' : '',
                  'jvdoc': ''
            }
        
        #### JULE VERNES ####
        
        query_jules_vernes = """
            SELECT ?s ?p WHERE {?s a foaf:Person. ?s ?p "Jules Verne"@fr}
        """
        
        result_query_jules_verne = self.sparqlcall(query_jules_vernes)
        
        uri_jules_verne = result_query_jules_verne["results"]["bindings"][0]['s']['value']
        
        predicate_jules_verne = result_query_jules_verne["results"]["bindings"][0]['p']['value']
    
        result['julesverne'] = uri_jules_verne
        
        result['jvpredicate'] = predicate_jules_verne
        
        #Trouvez les valeurs  liées à l'entité précédente par la propriété
        #<http://dbpedia.org/property/notableworks
        
        query_value_predicate_jules_verne = """
            SELECT ?s ?p ?o WHERE {?s a foaf:Person . ?s ?p "Jules Verne"@fr . ?s <http://dbpedia.org/property/notableworks> ?o}
        """
        
        result_query_value_predicate_jules_verne = self.sparqlcall(query_value_predicate_jules_verne)
        
        list_result_value_predicate_jules_verne = list()
        
        for i in range(len(result_query_value_predicate_jules_verne["results"]["bindings"])):
            out = result_query_value_predicate_jules_verne["results"]["bindings"][i]['o']['value']
            list_result_value_predicate_jules_verne.append(out)
        
        result["jvdoc"] = list_result_value_predicate_jules_verne
        
        print("========== STEP 4 ==========")
        print(result)
        print("\n\n\n")        
        
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            json.dump(result, resfile)

    def step5(self):
        stepfilename = self.basename+"5"
        result = {}
        # votre code ici
        
        result = {'jvpredicates' : '',
                  'triplecount'  : ''
                 }
        
        
        #### ALL PREDICATES CORRESPOND TO URI ####
        query_predicate_uri_jules_vernes = """
            PREFIX foaf: <http://xmlns.com/foaf/0.1/>
            SELECT DISTINCT(?p)
            WHERE
            {
                ?pers a foaf:Person .
                ?pers ?pred "Jules Verne"@fr .
                ?pers ?p ?o .
            }"""
        
        list_predicate_uri_jule_vernes = list()
        
        result_query_predicate_uri_jule_vernes = self.sparqlcall(query_predicate_uri_jules_vernes)
        
        for i in range(len(result_query_predicate_uri_jule_vernes["results"]["bindings"])):
            out = result_query_predicate_uri_jule_vernes["results"]["bindings"][i]['p']['value']
            list_predicate_uri_jule_vernes.append(out)
            
        result['jvpredicates'] = list_predicate_uri_jule_vernes

        ### COUNT ALL TRIPLES FROM URI ###
        
        list_triples = list()
        offset = 0
        
        # on initialise un liste de 100 éléments vides
        list_result_query_triples = list([''])*100
        
        while len(list_result_query_triples) == 100:
            query_triple_jule_vernes = """SELECT ?pers ?p ?o WHERE { ?pers a foaf:Person . ?pers ?pred "Jules Verne"@fr . ?pers ?p ?o . } LIMIT 100 OFFSET """ + str(offset) 
            list_result_query_triples = self.sparqlcall(query_triple_jule_vernes)['results']['bindings']
            list_triples.extend(list_result_query_triples)
            offset = offset + 100

        result['triplecount'] = len(list_triples)
        
        print("========== STEP 5 ==========")
        print(result)
        print("\n\n\n")          
        
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            json.dump(result, resfile)

    def step6(self):
        
        print("========== STEP 6 ==========")
        print("Création du graphe...")
        # On initialise le dictionnaire qui contient les triplets
        triple = {'uri' : [],
                  'predicates': [],
                  'values': []
            }
        
        # on initialise un liste de 100 éléments vides
        list_result_query_triples = list([''])*100
        
        list_uri = list()
        list_predicates = list()
        list_values = list()
        offset = 0
        
        while len(list_result_query_triples) == 100:
            query_triple_jule_vernes = """SELECT ?pers ?p ?o WHERE { ?pers a foaf:Person . ?pers ?pred "Jules Verne"@fr . ?pers ?p ?o . } LIMIT 100 OFFSET """ + str(offset) 
            list_result_query_triples = self.sparqlcall(query_triple_jule_vernes)['results']['bindings']
            for i in range(len(list_result_query_triples)):
                list_uri.append(list_result_query_triples[i]["pers"]["value"])
                list_predicates.append(list_result_query_triples[i]["p"]["value"])
                list_values.append(list_result_query_triples[i]["o"]["value"])
            offset = offset + 100
            
        triple['uri'] = list_uri
        triple['predicates'] = list_predicates
        triple['values'] = list_values
        
        
        # On converti le dictionnaire en Dataframe
        df_triple = pd.DataFrame(triple)

        # Création d'un Graph
        g = Graph()

        # --- On insert tous les triplets dans le graphe
        df_triple.apply(lambda x: g.add(
                (URIRef(x[0]), URIRef(x[1]), Literal(x[2]))
            ), axis=1)

        # --- On sauve le graphe au format n3
        g.serialize(destination='julesverne.n3', format='n3')
        
        print("Graphe crée et sauvé !")

if __name__ == "__main__":
    testeur = RdfDev()
    testeur.rdfdev()
