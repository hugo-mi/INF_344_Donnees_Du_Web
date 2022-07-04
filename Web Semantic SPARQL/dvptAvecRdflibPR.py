import isodate
from SPARQLWrapper import SPARQLWrapper, JSON, N3, TURTLE
from rdflib import Graph, URIRef, Literal
import json
from urllib.parse import urlencode, quote_plus
from urllib.request import urlopen
from requests import get
import ssl

def sparqlcall(sparqlquery):
    unsecurecontext = ssl._create_unverified_context()
    basedbpedia = "https://dbpedia.org/sparql?"
    payload = {'format': 'application/sparql-results+json', 'query': sparqlquery}
    params = urlencode(payload, quote_via=quote_plus)
    urldbpedia = basedbpedia+params
    
    with urlopen(urldbpedia, context=unsecurecontext) as response:
            return json.loads(response.read())
    
    return ""

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
        # self.step3()
        # self.step4()
        # self.step5()
        # self.step6()

    def step1(self):
        stepfilename = self.basename+"1"
        result = { "typelist": []}

        # votre code ici
        # FROM <http://dbpedia.org>
        sparql_return = sparqlcall("""
        SELECT DISTINCT ?t
        WHERE { ?h a ?t }
        LIMIT 10""")
        typelist = [el['t']['value']  for el in sparql_return['results']['bindings']]
        result = { "typelist": typelist}

        with open(stepfilename, "w", encoding="utf-8") as resfile:
            json.dump(result, resfile)


    def step2(self):
        stepfilename = self.basename+"2"
        result = {}
        # votre code ici
        # définition des prefix
        result['prefix'] = """PREFIX foaf:<http://xmlns.com/foaf/0.1/>
        PREFIX a:<rdf:type>
        PREFIX dbpedia:<http://dbpedia.org> """
        # requette 1 pour le compte des personnes
        # FROM dbpedia:
        query1 = "SELECT (COUNT(?p) AS ?c) WHERE {?e a foaf:Person}"
        #result['query'] = query1

        sparql_return = sparqlcall(result['prefix']+query1)
        result['personcount'] = int(sparql_return['results']['bindings'][0]['c']['value'])

        # requette 2 pour la récupération des 10 premières personnes
        query2 = "SELECT DISTINCT ?p WHERE {?p a foaf:Person} LIMIT 10"
        sparql_return = sparqlcall(result['prefix']+query2)
        result['firstten'] = [el['p']['value']  for el in sparql_return['results']['bindings']]

        # requette 3 pour la récupération des 10 premières personnes à partir de la centième
        query3 = "SELECT DISTINCT ?p WHERE {?p a foaf:Person} OFFSET 100 LIMIT 10"
        sparql_return = sparqlcall(result['prefix']+query3)
        result['tenothers'] = [el['p']['value']  for el in sparql_return['results']['bindings']]

        # récupération de l’url apparaissant dans la barre de navigation du navigateur 
        result["urlhtml"] = [get(uri).url for uri in result["firstten"]]

        with open(stepfilename, "w", encoding="utf-8") as resfile:
            json.dump(result, resfile)

    def step3(self):
        stepfilename = self.basename+"3"
        result = {}
        # votre code ici
        # définition des prefix
        prefix = """PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX a: <rdf:type>
        PREFIX dbpedia: <http://dbpedia.org> """
        # requette 1 pour le compte du nombre de prédicats utilisés
        query1 = "SELECT COUNT(?pred) as ?c WHERE { {SELECT ?pers WHERE { ?pers a foaf:Person} limit 1000 } ?pers ?pred ?obj}"

        sparql_return = sparqlcall(prefix+query1)
        result['predicatescount'] = int(sparql_return['results']['bindings'][0]['c']['value'])

        # requette 2 pour l'extraction de 20 premiers predicats
        query2 = "SELECT DISTINCT ?pred WHERE { {SELECT ?pers WHERE { ?pers a foaf:Person} LIMIT 1000 } ?pers ?pred ?obj} LIMIT 20"
        result['rqpredicates'] = query2

        sparql_return = sparqlcall(prefix+query2)
        result['predicates'] = [el['pred']['value']  for el in sparql_return['results']['bindings']]
        
        # requette 3 pour le comptage des utilisations de la propriété <http://dbpedia.org/ontology/deathPlace> par les objets de type foaf:Person
        query3 = "SELECT (COUNT(?s) as ?c) WHERE { ?s <http://dbpedia.org/ontology/deathPlace> ?o. ?o a foaf:Person} "
        result['rqplacecount'] = query3

        sparql_return = sparqlcall(prefix+query3)
        result['placecount'] =  int(sparql_return['results']['bindings'][0]['c']['value'])

        print(result['predicatescount'])
        
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            json.dump(result, resfile)

    def step4(self):
        stepfilename = self.basename+"4"
        result = {}
        # votre code ici
        # définition des prefix
        prefix = """PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX a: <rdf:type>
        PREFIX dbpedia: <http://dbpedia.org> """
        # requette 1 pour l'uri de l'entité de type foaf:Person et ayant un prédicat dont la valeur est "Jules Verne"@fr.
        query1 = "SELECT ?s ?p WHERE {?s a foaf:Person. ?s ?p \"Jules Verne\"@fr}"

        sparql_return = sparqlcall(prefix+query1)
        # on enregistre l'uri
        result['julesverne'] = sparql_return['results']['bindings'][0]['s']['value']
        self.julesverne = result['julesverne']
        # on enregistre le predicat
        result['jvpredicate'] = sparql_return['results']['bindings'][0]['p']['value']

        # requette 2 pour trouver les valeurs liées à l'entité précédente par la propriété <http://dbpedia.org/property/notableworks>
        query2 = "SELECT ?o WHERE { <"+result['julesverne']+"> <http://dbpedia.org/property/notableworks> ?o}"
        sparql_return = sparqlcall(prefix+query2)

        # on enregistre le résultat
        result['jvdoc'] =  [el['o']['value']  for el in sparql_return['results']['bindings']]

        with open(stepfilename, "w", encoding="utf-8") as resfile:
            json.dump(result, resfile)

    def step5(self):
        stepfilename = self.basename+"5"
        result = {}
        # votre code ici
        # définition des prefix
        prefix = """PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX a: <rdf:type>
        PREFIX dbpedia: <http://dbpedia.org> """
        # requette 1 pour les prédicats sont associés à julesverne
        query1 = "SELECT DISTINCT ?p WHERE {<"+self.julesverne+"> ?p ?o}"

        sparql_return = sparqlcall(prefix+query1)
        # on enregistre les prédicats
        result['jvpredicates'] =  [el['p']['value']  for el in sparql_return['results']['bindings']]

        all_triplets = []
        offset = 0
        # on s'arrange pour avoir une liste de 100 éléments pour lancer la boucle
        sparql_return['results']['bindings'] = ['']*100
        while len(sparql_return['results']['bindings']) == 100:

            # on boucle pour  récupérer des triplets  descriptifs de julesverne
            query2 = "SELECT ?p ?o WHERE {<"+self.julesverne+"> ?p ?o} OFFSET "+str(offset)+" LIMIT 100"
            sparql_return = sparqlcall(prefix+query2)
            all_triplets.extend(sparql_return['results']['bindings'])
            offset += 100

        result['triplecount'] = len(all_triplets)
        self.tripletsjv = all_triplets

        with open(stepfilename, "w", encoding="utf-8") as resfile:
            json.dump(result, resfile)

    def step6(self):
        stepfilename = "julesverne.n3"
        result = {}
        # votre code ici
        graph = Graph()

        julesverns = URIRef(self.julesverne)
        
        for triplet in self.tripletsjv:
            p, o = triplet['p']['value'], triplet['o']['value']
            pred = URIRef(p)
            obj = Literal(o)

            graph.add((julesverns, pred, obj))

        result = graph.serialize()
        
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            json.dump(result, resfile)

if __name__ == "__main__":
    testeur = RdfDev()
    testeur.rdfdev()
