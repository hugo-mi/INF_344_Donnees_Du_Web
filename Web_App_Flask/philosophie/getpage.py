#!/usr/bin/python3
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from json import loads
from urllib.request import urlopen
from urllib.parse import urlencode, unquote
import ssl

# On crée le cache
cache = {}

# Question 1 (Partie 2)
def getJSON(page):
    """
    DESCRIPTION
        Réalise une requête sur API Wikipedia 
    RETOURNE
        Retourne au format JSON le contenu HTML de la page
    """
    params = urlencode({
      'format': 'json',  # TODO: compléter ceci
      'action': 'parse',  # TODO: compléter ceci
      'prop': 'text',  # TODO: compléter ceci
      'redirects': True,
      'page': page})
    API = "https://fr.wikipedia.org/w/api.php"  # TODO: changer ceci
    # désactivation de la vérification SSL pour contourner un problème sur le
    # serveur d'évaluation -- ne pas modifier
    gcontext = ssl.SSLContext()
    response = urlopen(API + "?" + params, context=gcontext)
    return response.read().decode('utf-8')

# Question 3 (Partie 2)
def getRawPage(page):
    """
    DESCRIPTION
        Parse le contenu le contenu JSON retourné par l API Wikipedia
    RETOURNE
        Retourne le contenu HTML de la page ainsi que son titre
    """
    parsed = loads(getJSON(page))
    try:
        title = parsed["parse"]["title"] # TODO: remplacer ceci
        content = parsed["parse"]["text"]["*"] # TODO: remplacer ceci
        return title, content
    except KeyError:
        # La page demandée n'existe pas
        return None, None

# Question 3 (Partie 2)
"""
def getPage(page):
    title, content_html = getRawPage(page)
    try:
        soup = BeautifulSoup(content_html)
        link_list = list()
        for a_href in soup.find_all("a", href=True):
            link_list.append(a_href["href"])
        return title, link_list
    except:
        return (None, [])
"""

# Question 4 (Partie 2)
"""
def getPage(page):
    title, content_html = getRawPage(page)
    try:
        soup = BeautifulSoup(content_html)
        link_list = list()
        soup2 = soup.find('div')
        
        soup3 = soup2.findAll('p', recursive=False)
        #print(soup3)
        
        for a_href in soup3:
            link = a_href.findAll('a')
            for a_href in link:
                link_list.append(a_href.get('href'))
        print(len(link_list))
        return title, link_list
    except:
        return (None, [])
"""

# Question 5 (Partie 2)
"""
def getPage(page):
    title, content_html = getRawPage(page)
    try:
        soup = BeautifulSoup(content_html)
        link_list = list()
        soup2 = soup.find('div')
        
        soup3 = soup2.findAll('p', recursive=False)
        #print(soup3)
        
        for a_href in soup3:
            link = a_href.findAll('a')
            for a_href in link:
                link_list.append(a_href.get('href'))
        print("Nombre de liens trouvés :", len(link_list))
        
        valid_link = list()
        for elm in link_list:
            if elm.startswith("/wiki") and "redlink=1" not in elm:
                valid_link.append(elm)
        print("Nombre de liens valides trouvés :", len(valid_link))
        return title, valid_link
    except:
        return (None, [])
"""

# Question 6 et Question 7 (Partie 2) + Queston 1, Question 2, Question 3, Question 4, Question 5, Question 6 (Partie 4)

def getPage(page):
    
    # Si la page est en cache, alors on va chercher la page dans stockée dans le cache au lieu de requêter l'API wikipedia
    if page in cache:
        return page, cache[page]
    else:
        # On récupère le contenu brute html de la page
        title, content_html = getRawPage(page)
        # On parse le contenu html de la page en récupérant le titre et les liens internes valides contenu dans la page
        try:
            soup = BeautifulSoup(content_html)
            link_list = list()
            soup2 = soup.find('div')
            
            soup3 = soup2.findAll('p', recursive=False)
            
            for a_href in soup3:
                link = a_href.findAll('a')
                for a_href in link:
                    link_list.append(a_href.get('href'))
            print("Nombre de liens trouvés :", len(link_list))
            
            # Parmi tous les liens trouvés, on ne garde que les liens internes (commence par /wiki) et valides (qui ne comportent pas la mention redlink=1)
            valid_intern_link = list()
            for elm in link_list:
                if elm.startswith("/wiki") and "redlink=1" not in elm:
                    
                    #### Debut nettoyage des liens ####
                    
                    # 1/ On supprime l'attribut /wiki/ au début de chaque lien interne valide
                    valid_link_formated = elm.replace("/wiki/", "")
                        
                    # 2/ On décode les caractères non-ASCII pour qu'ils soient compréhensible pour un humain
                    valid_link_formated = unquote(valid_link_formated)
                    
                    # 3/ On supprime le fragments des ancres d'une page
                    valid_link_formated = valid_link_formated.split("#")[0]
                    
                    # 4/ On remplace les underscores par des espaces
                    valid_link_formated = valid_link_formated.replace("_", " ")
                    
                    # 5/ On ne garde pas les liens qui comporte des ":" (Aide:référence nécessaire)
                    if (":" in valid_link_formated) or (not valid_link_formated):
                        pass
                    else:
                        # On ajoute le lien reformatés et nettoyés à la liste de liens internes qui doit être retournée
                        valid_intern_link.append(valid_link_formated)
                    
                    #### Fin nettoyage des liens ####
                    
            print("Nombre de liens internes valides trouvés :", len(valid_intern_link))
            print("\n\n")

            # Suppression des liens en doublon tout en gardant l'ordre d'apparition des liens
            # Ref: (https://www.developpez.net/forums/d1248736/autres-langages/python/general-python/suppression-doublons-liste/)

            valid_intern_link_no_duplicate = [ e for (i,e) in enumerate(valid_intern_link) if e not in valid_intern_link[:i] ]            
            
            # On ne garde uniquement que les 10 premiers liens
            ten_valid_intern_link_formated = valid_intern_link_no_duplicate[:10]
            
            # Mise à jour du cache
            cache[title] = ten_valid_intern_link_formated
            
            return title, ten_valid_intern_link_formated
        
        except:
            return (None, [])
    


if __name__ == '__main__':
    # Ce code est exécuté lorsque l'on exécute le fichier
    #print("Ça fonctionne !")
    
    # Voici des idées pour tester vos fonctions :
    # print("######################################## GET JSON ########################################")
    # print("\n\n")
    # print(getJSON("Utilisateur:A3nm/INF344"))
    
    # print("\n\n\n\n")
    
    # print("######################################## GET RAW PAGE ########################################")
    # print("\n\n")
    # print(getRawPage("Utilisateur:A3nm/INF344"))
    
    # print("\n\n\n\n")
    
    # print("######################################## GET RAW PAGE ########################################")
    # print("\n\n")
    # print(getRawPage("Histoire"))
    
    # print("\n\n\n\n")
    
    print("######################################## GET PAGE ########################################")
    print("\n\n")
    print(getPage("Utilisateur:A3nm/INF344"))
    print("\n\n")

