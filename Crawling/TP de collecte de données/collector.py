# -*- coding: utf-8 -*-
# écrit par Jean-Claude Moissinac, structure du code par Julien Romero

from sys import argv
import sys
if (sys.version_info > (3, 0)):
    from urllib.request import urlopen
    from urllib.parse import urlencode
else:
    from urllib2 import urlopen
    from urllib import urlencode
    
# Custom import
from bs4 import BeautifulSoup
import time
import ssl
import re

class Collecte:
    """pour pratiquer plusieurs méthodes de collecte de données"""

    def __init__(self):
        """__init__
        Initialise la session de collecte
        :return: Object of class Collecte
        """
        # DO NOT MODIFY
        self.basename = "collecte.step"

    def collectes(self):
        """collectes
        Plusieurs étapes de collectes. VOTRE CODE VA VENIR CI-DESSOUS
        COMPLETER les méthodes stepX.
        """
        self.step0()
        self.step1()
        self.step2()
        self.step3()
        self.step4()
        self.step5()
        self.step6()

    def step0(self):
        # cette étape ne sert qu'à valider que tout est en ordre; rien à coder
        stepfilename = self.basename+"0"
        self.name = "hmichel-20"
        print("Comment :=>> Validation de la configuration")
        self.unsecurecontext = ssl._create_unverified_context() # ne pas modifier
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            resfile.write(self.name)
    
            
    def step1(self):
        stepfilename = self.basename+"1"
        result = ""
        
        # votre code ici
        print("--------- STEP 1 ---------")
        url = "http://www.freepatentsonline.com/result.html?sort=relevance&srch=top&query_txt=video&submit=&patents=on"
        with urlopen(url, context = self.unsecurecontext) as response:
            html = response.read()
            #print(html)
            result = str(html)
        
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            resfile.write(result)
            
    
    def step2(self):
        stepfilename = self.basename+"2"
        result = ""
        
        # votre code ici
        print("--------- STEP 2 ---------")
        url = urlopen("http://www.freepatentsonline.com/result.html?sort=relevance&srch=top&query_txt=video&submit=&patents=on", context = self.unsecurecontext)
        my_bytes = url.read()
        my_str = my_bytes.decode("utf-8")
        
        # On crée l'objet bs4
        soup = BeautifulSoup(my_str)
        
        list_link = list()
        for a in soup.find_all('a', href=True):
            list_link.append(a['href'])
    
        #print(list_link)
        
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            for link in list_link:
                resfile.write(link + "\n")
        
    def linksfilter(self, links):
        flinks = links
        
        # votre code ici
        
        # 1/ Suppression des liens en doublons 
        flinks_temp = list(dict.fromkeys(flinks))
        
        # 2/ Suppression des liens spécifiques
        list_link_to_remove = ["/", "/services.html", "/contact.html",
                               "/privacy.html", "/register.html", "/tools-resources.html", 
                               "https://twitter.com/FPOCommunity", 
                               "http://www.linkedin.com/groups/FPO-Community-4524797", 
                               "http://www.sumobrainsolutions.com/"]
        flinks = list()
        for link in flinks_temp:
            if link in list_link_to_remove or link.startswith("result.html") or link.startswith("http://research") or link.startswith("/search.html"):
                pass     
            else:
                flinks.append(link)       
        
        #print(flinks)
        
        return flinks
        
    def step3(self):
        stepfilename = self.basename+"3"
        result = ""
        
        # votre code ici
        print("--------- STEP 3 ---------")
        # On récupère la liste des liens obtenu à l'étape 3
        link = open(self.basename+"2", 'r').read().splitlines()
        
        link_filtered = self.linksfilter(link)
        print("nombre url restant arpès filtrage", len(link_filtered))
        #print(link_filtered)
        
        link_filtered_sorted = sorted(link_filtered)
        #print(link_filtered_sorted)
        
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            for link in link_filtered_sorted:
                resfile.write(link + "\n")
        
    def step4(self):
        stepfilename = self.basename+"4"
        result = ""
        
        # votre code ici
        print("--------- STEP 4 ---------")
        # On sélectionne les 10 premiers éléments de la liste d'url obtenu à l'étape 3
        link10 = open(self.basename+"3", 'r').read().splitlines()[:10]
        
        href_link = list()
        
        for url in link10:
            print("---- Scrapping " + "http://www.freepatentsonline.com/" + url + "... ----")
            url = urlopen("http://www.freepatentsonline.com/" + url, context = self.unsecurecontext)
            my_bytes = url.read()
            my_str = my_bytes.decode("utf-8")
        
            # On crée l'objet bs4
            soup = BeautifulSoup(my_str)

            for a in soup.find_all('a', href=True):
                href_link.append(a['href'])
            
            # On attend 2 secondes entre chaque requête
            time.sleep(2)
        
        #print(href_link)
        
        # Suppression des doublons 
        href_link_cleaned = list(dict.fromkeys(href_link))
        
        # Tri par ordre alphabétique
        href_link_cleaned_sorted = sorted(href_link_cleaned)
        
        #print(href_link_cleaned_sorted)
        
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            for link in href_link_cleaned_sorted:
                resfile.write(link + "\n")
        
    def contentfilter(self, response):
        soup = BeautifulSoup(response, 'html.parser')
        for div in soup.findAll('div'):
            inventors = soup.find_all(text=re.compile('Inventors:'))
            title = soup.find_all(text=re.compile('Title:'))
            application_num = soup.find_all(text=re.compile('Application Number:'))        
        
        # On vérifie si la page contient les mots 'inventors', 'Title:' et 'Application Number:' 
        if inventors is not None or title is not None or application_num is not None:
            return True
        else:
            return False
        
        

    def step5(self):
        stepfilename = self.basename+"5"
        result = ""
        
        # votre code ici
        print("--------- STEP 5 ---------")
        link_step_4 = open(self.basename+"4", 'r').read().splitlines()
        
        list_link = list()
        
        for link in link_step_4:
            if len(list_link) == 10:
                break
            if link.endswith('html'):
                url = urlopen("http://www.freepatentsonline.com/" + link, context = self.unsecurecontext)
                my_bytes = url.read()
                my_str = my_bytes.decode("utf-8")
        
                if self.contentfilter(my_str) == True:
                    list_link.append(link)
                    
        #print(list_link)
        list_link_sorted = sorted(list_link)
        #print(list_link_sorted)
        
        
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            for link in list_link_sorted:
                resfile.write(link + "\n")
        
    def step6(self):
        stepfilename = self.basename+"6"
        result = ""
        
        # votre code ici
        print("--------- STEP 6 ---------")
        link_step_5 = open(self.basename+"5", 'r', encoding='utf-8').read().splitlines()[:5]
        
        list_inventors = list()
        
        for link in link_step_5:
            url = urlopen("http://www.freepatentsonline.com/" + link, context = self.unsecurecontext)
            my_bytes = url.read()
            my_str = my_bytes.decode("utf-8")
            
            # on crée l'objet soup
            soup = BeautifulSoup(my_str, 'html.parser')
            
            inventors = soup.find_all(text=re.compile('Inventors:'))
            
            divs = [inventor.parent.parent for inventor in inventors]
            for d in divs[0].descendants:
                if d.name == 'div' and d.get('class', '') == ['disp_elm_text']:
                    list_inventors.append(d.text)
            
        #print(list_inventors)
        
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            for elm in list_inventors:
                resfile.write(elm + "\n")
        
if __name__ == "__main__":
    collecte = Collecte()
    collecte.collectes()
