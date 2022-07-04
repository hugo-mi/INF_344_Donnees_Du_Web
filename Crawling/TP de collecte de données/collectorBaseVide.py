# -*- coding: utf-8 -*-
# écrit par Jean-Claude Moissinac, structure du code par Julien Romero

from sys import argv
import time
import sys
import bs4 as bs
import ssl
from urllib.request import urlopen
from urllib.parse import urlencode


class Collecte:
    """pour pratiquer plusieurs méthodes de collecte de données"""

    def __init__(self):
        """__init__
        Initialise la session de collecte
        :return: Object of class Collecte
        """
        self.basename = "collecte.step" # ne pas changer

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
        stepfilename = self.basename + "0"
        print("Comment :=>> Validation de la configuration")
        self.unsecurecontext = ssl._create_unverified_context() # ne pas modifier
        self.name = "YOUR NAME HERE"
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            resfile.write(self.name)

    def step1(self):
        stepfilename = self.basename + "1"
        result = ""
        # votre code ici
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            resfile.write(result)

    def step2(self):
        stepfilename = self.basename + "2"
        result = ""
        # votre code ici
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            resfile.write(result)

    def linksfilter(self, links):
        flinks = links
        # votre code ici
        return flinks

    def step3(self):
        stepfilename = self.basename + "3"
        result = ""
        # votre code ici
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            resfile.write(result)

    def step4(self):
        stepfilename = self.basename + "4"
        result = ""
        # votre code ici
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            resfile.write(result)

    def contentfilter(self, link):
        return False

    def step5(self):
        stepfilename = self.basename + "5"
        result = ""
        # votre code ici
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            resfile.write(result)

    def step6(self):
        stepfilename = self.basename + "6"
        result = ""
        # votre code ici
        with open(stepfilename, "w", encoding="utf-8") as resfile:
            resfile.write(result)


if __name__ == "__main__":
    collecte = Collecte()
    collecte.collectes()